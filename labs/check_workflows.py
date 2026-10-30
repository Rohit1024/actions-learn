"""Lint inactive Module 1 recipes, including their real local call interfaces."""

from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory


root = Path(__file__).resolve().parents[1]
recipes = sorted((root / "labs").glob("000[1-6]/module1-*.yml"))
linter = root / ".tools/bin/actionlint"
if not linter.is_file():
    raise SystemExit("Run task tools:lint first; see the local testing guide")
with TemporaryDirectory(prefix="actions-module1-lint-") as directory:
    project = Path(directory)
    workflows = project / ".github/workflows"
    workflows.mkdir(parents=True)
    (project / ".git").mkdir()
    (project / "examples").symlink_to(root / "examples", target_is_directory=True)
    for recipe in recipes:
        shutil.copy2(recipe, workflows / recipe.name)
    subprocess.run([str(linter), "-color"], cwd=project, check=True)
print(f"Checked {len(recipes)} inactive Module 1 workflows and local action/call metadata")
