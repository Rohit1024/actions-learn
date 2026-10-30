"""Stage only Module 5 lab recipes in a disposable repository for actionlint.

No active workflow files are created in the real repository. This is workflow
static analysis only; no Markdown, link, Mermaid, or documentation build checks.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--negative", choices=["missing-label", "missing-secret", "wrong-boolean", "wrong-number"])
args = parser.parse_args()
recipes = [
    "0025/consumer.yml", "0026/consumer.yml", "0027/consumer.yml",
    "0028/smoke.yml", "0028/broken-smoke.yml",
    "0029/module5-caller.yml", "0029/module5-reusable.yml",
    "0030/module5-orchestrator.yml", "0030/module5-worker.yml",
]
with TemporaryDirectory(prefix="module5 static ") as directory:
    project = Path(directory)
    workflows = project / ".github/workflows"
    workflows.mkdir(parents=True)
    (project / ".git").mkdir()
    (project / "labs").mkdir()
    for number in range(25, 31):
        (project / "labs" / f"{number:04}").symlink_to(root / "labs" / f"{number:04}", target_is_directory=True)
    selected = recipes if not args.negative else ["0029/module5-reusable.yml", f"0029/negative/{args.negative}.yml"]
    files = []
    for recipe in selected:
        # Unique names for the three early consumer recipes; local callees keep
        # their exact basenames so actionlint resolves their actual interfaces.
        name = recipe.replace("/", "-") if recipe.endswith("/consumer.yml") else Path(recipe).name
        destination = workflows / name
        shutil.copyfile(root / "labs" / recipe, destination)
        files.append(str(destination))
    result = subprocess.run([str(root / ".tools/bin/actionlint"), "-no-color", *files], cwd=project, capture_output=True, text=True, timeout=30)
    diagnostics = result.stdout + result.stderr
    if args.negative:
        if args.negative == "wrong-boolean":
            if result.returncode != 0:
                raise SystemExit(f"Installed linter behavior changed; review this fixture:\n{diagnostics}")
            print("STATIC GAP: actionlint 1.7.12 accepted nonboolean text for strict")
            print("No workflow executed; worker.test.cjs separately rejects invalid boolean transport")
            raise SystemExit(0)
        needle = {"missing-label": "label", "missing-secret": "fixture_token", "wrong-boolean": "boolean", "wrong-number": "number"}[args.negative]
        if result.returncode == 0 or needle not in diagnostics.lower():
            raise SystemExit(f"Expected interface failure absent: {result.returncode}\n{diagnostics}")
        print(diagnostics, end="")
        print(f"EXPECTED interface rejection: {args.negative}; actionlint exit={result.returncode}")
    else:
        if result.returncode:
            raise SystemExit(diagnostics)
        print("PASS: 9 explicit Module 5 workflow recipes, including real local call interfaces")
        print("broken-smoke.yml is syntax-valid; its caller assertion is expected to fail at runtime")
