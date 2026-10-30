"""Assemble an action snapshot locally; never tag, push, dispatch, or publish."""

from pathlib import Path
import shutil

here = Path(__file__).resolve().parent
candidate = here / "package"
candidate.mkdir(exist_ok=True)
source = here.parent / "0052/action"
for name in ("action.yml",):
    shutil.copy2(source / name, candidate / name)
for name in ("src", "dist"):
    shutil.copytree(source / name, candidate / name, dirs_exist_ok=True)
for template, name in (("candidate-readme.md", "README.md"),
                       ("candidate-license.txt", "LICENSE"),
                       ("release-notes.md", "CHANGELOG.md")):
    shutil.copy2(here / template, candidate / name)
print("Prepared labs/0054/package with root metadata, source, distribution, and release documents")
print("Local candidate only: no repository, tag, release, or Marketplace listing created")
