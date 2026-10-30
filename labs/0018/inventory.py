"""Inventory our small source tree; this is not an image SBOM or a scan."""
import ast
from pathlib import Path

action = Path(__file__).parent / "action"
print(next(line for line in (action / "Dockerfile").read_text().splitlines() if line.startswith("FROM ")))
tree = ast.parse((action / "entrypoint.py").read_text())
modules = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        modules.update(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom):
        modules.add(node.module)
print("program imports=" + ", ".join(sorted(modules)))
print("explicit extra package installs=none")
print("base OS and interpreter packages=not inventoried without image/SBOM")
print("base digest, vulnerability scan, image timings=not collected")
