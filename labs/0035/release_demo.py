"""Local ref map and stale-distribution experiment; never invokes git or an API."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
NODE = shutil.which("node")


def run_node(args, *, env=None, cwd=None):
    return subprocess.run([NODE, *map(str, args)], text=True, capture_output=True,
                          env=env if env is not None else {"PATH": os.defpath}, cwd=cwd, timeout=30)


def consume(root, name="Ada"):
    with tempfile.TemporaryDirectory(prefix="consumer-0035-") as folder:
        output = Path(folder) / "output"
        result = run_node([root / "dist/index.cjs"], env={"PATH": os.defpath,
                          "INPUT_NAME": name, "GITHUB_OUTPUT": str(output)}, cwd=folder)
        return result, output.read_text() if output.exists() else ""


def demo():
    assert NODE, "installed Node required"
    refs = {"v1.0.0": "a" * 40, "v1": "a" * 40}
    pinned = refs["v1"]
    refs["v1"] = "b" * 40
    assert pinned != refs["v1"] and refs["v1.0.0"] == pinned
    print("synthetic refs: v1 moved; full commit and v1.0.0 snapshot unchanged")
    with tempfile.TemporaryDirectory(prefix="lesson-0035-") as folder:
        candidate = Path(folder) / "candidate"
        shutil.copytree(ROOT / "src", candidate / "src")
        shutil.copytree(ROOT / "dist", candidate / "dist")
        shutil.copy2(ROOT / "action.yml", candidate / "action.yml")
        shutil.copy2(ROOT / "tsconfig.json", candidate / "tsconfig.json")
        source = candidate / "src/index.ts"
        source.write_text(source.read_text().replace("Hello,", "Welcome,"))
        before = (candidate / "dist/index.cjs").read_bytes()
        check = run_node([ROOT / "build.cjs", "--root", candidate, "--check"])
        assert check.returncode == 1 and "distribution differs" in check.stderr
        assert (candidate / "dist/index.cjs").read_bytes() == before
        result, output = consume(candidate)
        assert result.returncode == 0 and output == "greeting=Hello, Ada!\n"
        print("stale candidate: source changed; check exit=1; consumer still says Hello, Ada!")
        build = run_node([ROOT / "build.cjs", "--root", candidate])
        assert build.returncode == 0, build.stderr
        assert run_node([ROOT / "build.cjs", "--root", candidate, "--check"]).returncode == 0
        result, output = consume(candidate)
        assert result.returncode == 0 and output == "greeting=Welcome, Ada!\n"
        digest = hashlib.sha256((candidate / "dist/index.cjs").read_bytes()).hexdigest()
        record = {"candidate_commit": "b" * 40, "distribution_sha256": digest,
                  "hosted_consumer": "not-run", "attestation": "not-generated", "publication": "none"}
        (candidate / "review.json").write_text(json.dumps(record, indent=2))
        print("repaired candidate: check exit=0; consumer says Welcome, Ada!")
        print("review record: digest collected; hosted consumer and attestation remain unverified")
    print("temporary candidate removed; no git refs or releases changed")


if __name__ == "__main__":
    demo()
