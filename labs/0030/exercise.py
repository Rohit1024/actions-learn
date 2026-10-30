"""Run actual project commands and join policy, sequentially on this host."""
import argparse
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

parser = argparse.ArgumentParser()
parser.add_argument("--case", choices=["pass", "fail-test", "missing-test", "skipped-test", "stale-test"], default="pass")
args = parser.parse_args()
source = Path(__file__).resolve().parent
with TemporaryDirectory(prefix="module5 pipeline ") as directory:
    root = Path(directory)
    env = dict(os.environ, CANDIDATE="preview-1", WORK_DIR=str(root / "build workspace"))
    results = {}
    for kind in ["build", "test"]:
        if kind == "test" and args.case == "skipped-test":
            results[kind] = "skipped"
            continue
        command = ["node", str(source / "build.cjs")] if kind == "build" else ["node", "--test", str(source / "domain.test.cjs")]
        work = subprocess.run(command, env=env, capture_output=True, text=True, timeout=10)
        assert work.returncode == 0, work.stderr
        output = root / f"{kind} output"
        output.touch()
        worker_env = dict(env, KIND=kind, FAIL_KIND="test" if args.case == "fail-test" else "none", EVIDENCE_DIR=str(root / "evidence" / kind), GITHUB_OUTPUT=str(output))
        emit = subprocess.run(["node", str(source / "emit.cjs")], env=worker_env, capture_output=True, text=True, timeout=5)
        results[kind] = "success" if emit.returncode == 0 else "failure"
        if results[kind] == "failure":
            assert output.read_text() == ""
            print(emit.stderr.strip())
        else:
            assert output.read_text() == f"artifact=evidence-{kind}\n"
    assert (root / "build workspace/bundle.txt").read_text() == "candidate=preview-1\n"
    test_file = root / "evidence/test/test.json"
    if args.case == "missing-test":
        test_file.unlink()
    if args.case == "stale-test":
        test_file.write_text(test_file.read_text().replace("preview-1", "preview-2"))
    gate_output = root / "gate output"
    gate_output.touch()
    gate_env = dict(env, BUILD_RESULT=results["build"], TEST_RESULT=results["test"], EVIDENCE_DIR=str(root / "evidence"), GITHUB_OUTPUT=str(gate_output))
    gate = subprocess.run(["node", str(source / "gate.cjs")], env=gate_env, capture_output=True, text=True, timeout=5)
    print(f"host results: build={results['build']}, test={results['test']}")
    print((gate.stdout or gate.stderr).strip())
    if args.case == "pass":
        assert gate.returncode == 0 and gate_output.read_text() == "ready=true\n"
        print("PLAN ONLY: no release or deployment occurs")
    else:
        assert gate.returncode == 1 and gate_output.read_text() == ""
    raise SystemExit(gate.returncode)
