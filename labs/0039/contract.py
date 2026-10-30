"""Exercise real local module resolution, file integrity, and recipe naming.

The temporary download marker and copy operation are synthetic fixtures, not
an implementation of npm ci, cache restore, or upload/download-artifact.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent


def cache_key(os_name, arch, node_major, lock_bytes):
    return f"npm-{os_name}-{arch}-node{node_major}-" + hashlib.sha256(lock_bytes).hexdigest()


def check_names(recipe):
    producer = next(s for s in recipe["jobs"]["build"]["steps"] if s.get("id") == "upload")
    consumer = next(s for s in recipe["jobs"]["consume"]["steps"] if s.get("id") == "download")
    if producer["with"]["name"] != consumer["with"]["name"]:
        raise ValueError("artifact name mismatch")


def run(skip_install=False, tamper=False, wrong_name=False):
    recipe = yaml.load((HERE / "exchange.yml").read_text(), Loader=yaml.BaseLoader)
    if wrong_name:
        next(s for s in recipe["jobs"]["consume"]["steps"] if s.get("id") == "download")["with"]["name"] = "other-bundle"
    check_names(recipe)
    with tempfile.TemporaryDirectory(prefix="module7-data-") as temporary:
        workspace = Path(temporary)
        downloads = workspace / "npm-cache"
        downloads.mkdir()
        (downloads / "download.txt").write_text("synthetic cached package bytes\n")
        assert not (workspace / "node_modules").exists()
        if not skip_install:
            installed = workspace / "node_modules/fixture-dependency"
            installed.mkdir(parents=True)
            shutil.copyfile(HERE / "fixture-dependency.cjs", installed / "index.cjs")
        result = workspace / "result.json"
        process = subprocess.run(["node", str(HERE / "build.cjs"), str(result)], cwd=workspace, text=True, capture_output=True, timeout=10)
        if process.returncode:
            raise ValueError(process.stderr.strip() + "; download bytes did not install the module")
        expected = hashlib.sha256(result.read_bytes()).hexdigest()
        destination = workspace / "consumer"
        destination.mkdir()
        shutil.copyfile(result, destination / "result.json")
        if tamper:
            (destination / "result.json").write_text('{"message":"changed"}\n')
        if hashlib.sha256((destination / "result.json").read_bytes()).hexdigest() != expected:
            raise ValueError("consumer digest mismatch")
        assert json.loads((destination / "result.json").read_text())["message"] == "bounded fixture result"
        print("PASS: synthetic dependency materialized; real Node build and local file consumer verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-install", action="store_true")
    parser.add_argument("--tamper", action="store_true")
    parser.add_argument("--wrong-name", action="store_true")
    args = parser.parse_args()
    try:
        run(args.skip_install, args.tamper, args.wrong_name)
    except ValueError as error:
        print(f"BLOCKED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
