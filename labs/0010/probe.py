"""This same process can run on the host or inside a compatible Linux image."""

import json
import os
from pathlib import Path
import platform

value = {"system": platform.system(), "machine": platform.machine()}
print(json.dumps(value, sort_keys=True))
output = os.environ.get("GITHUB_OUTPUT")
if output:
    with Path(output).open("a", encoding="utf-8") as handle:
        handle.write("platform=" + value["system"] + "/" + value["machine"] + "\n")
    print("output record appended")
