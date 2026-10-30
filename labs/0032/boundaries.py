"""Bounded fixtures: generated shell text and data-only ZIP consumption."""
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import zipfile

EXPECTED = {"repository": "example/lesson", "workflow_id": 32, "run_id": 320,
            "head_sha": "a" * 40, "event": "push", "conclusion": "success"}


def injection_demo():
    bash = shutil.which("bash")
    if not bash:
        raise RuntimeError("installed bash is required")
    with tempfile.TemporaryDirectory(prefix="lesson-0032-") as folder:
        marker = Path(folder) / "marker"
        # Fixed lab payload can only create this temporary marker.
        text = '"; : > marker; #'
        unsafe = 'printf "%s\\n" "' + text + '"\n'
        subprocess.run([bash, "--noprofile", "--norc", "-c", unsafe], cwd=folder,
                       env={"PATH": os.defpath}, capture_output=True, check=True)
        assert marker.exists(), "unsafe interpolation should create marker"
        marker.unlink()
        safe = subprocess.run([bash, "--noprofile", "--norc", "-c", 'printf "%s\\n" "$TITLE"'],
                              cwd=folder, env={"PATH": os.defpath, "TITLE": text},
                              capture_output=True, text=True, check=True)
        assert safe.stdout == text + "\n" and not marker.exists()
    return ["unsafe: marker created", "safe: exact text preserved; marker absent",
            "temporary directory removed; no inherited credentials or network calls"]


def archive(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as result:
        for name, data in entries:
            result.writestr(name, data)
    return output.getvalue()


def consume(data, observed_producer):
    # In a real integration observed_producer must come from trusted service evidence,
    # never from JSON supplied inside the artifact. Here both are synthetic fixtures.
    if observed_producer != EXPECTED:
        raise ValueError("producer context mismatch")
    if len(data) > 16384:
        raise ValueError("archive too large")
    with zipfile.ZipFile(io.BytesIO(data)) as result:
        files = result.infolist()
        if len(files) != 1 or files[0].filename != "report.json":
            raise ValueError("expected exactly report.json")
        item = files[0]
        if stat.S_ISLNK(item.external_attr >> 16) or item.file_size > 1024:
            raise ValueError("symlink or oversized report")
        report = json.loads(result.read(item))
    if (not isinstance(report, dict) or set(report) != {"schema", "passed", "total"}
            or type(report["schema"]) is not int or report["schema"] != 1
            or type(report["passed"]) is not int or type(report["total"]) is not int
            or not 0 <= report["passed"] <= report["total"] <= 100):
        raise ValueError("invalid report schema")
    return f"report: {report['passed']}/{report['total']} checks passed (data only)"


if __name__ == "__main__":
    for line in injection_demo():
        print(line)
    print(consume(archive([("report.json", '{"schema":1,"passed":3,"total":3}')]), EXPECTED))
