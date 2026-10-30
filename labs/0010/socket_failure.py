"""Deliberately connect to an absent disposable Unix socket, then stop."""

from pathlib import Path
import socket
import sys
import tempfile

with tempfile.TemporaryDirectory(prefix="module2 absent socket ") as directory:
    path = Path(directory) / "engine.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        try:
            client.connect(str(path))
        except OSError as error:
            print("EXPECTED CONNECTION FAILURE: " + str(error), file=sys.stderr)
            print("No engine API request, image pull, or action process ran.", file=sys.stderr)
            sys.exit(1)
raise AssertionError("an absent socket unexpectedly accepted a connection")
