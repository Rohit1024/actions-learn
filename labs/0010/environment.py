"""Read-only map of the host/client/engine boundaries; never starts a VM."""

import os
import platform
import shutil
import subprocess


def inspect(command):
    print("$ " + " ".join(command))
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=15)
        print((result.stdout + result.stderr).strip())
        print("exit=" + str(result.returncode))
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired) as error:
        print("unavailable: " + str(error))
        return False


print("host=" + platform.system() + "/" + platform.machine())
print("DOCKER_HOST=" + (os.environ.get("DOCKER_HOST") or "unset (client default)"))
for tool in ("docker", "podman", "act"):
    print(tool + "=" + (shutil.which(tool) or "unavailable"))
if shutil.which("podman"):
    inspect(["podman", "machine", "list", "--format", "json"])
ready = inspect(["docker", "info"])
print("engine=" + ("reachable; image and architecture checks still needed" if ready
                   else "deferred; no reachable engine, no container evidence"))
