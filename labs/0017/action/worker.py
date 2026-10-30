"""A bounded teaching worker, with one staging file per isolated workspace."""
import os
from pathlib import Path
import signal
import sys
import time


class Interrupted(Exception):
    def __init__(self, signum: int):
        self.signum = signum


def on_signal(signum, _frame):
    raise Interrupted(signum)


def main() -> int:
    partial = None
    try:
        mode = sys.argv[1] if len(sys.argv) > 1 else "success"
        if mode not in ("success", "fail", "wait"):
            raise ValueError("mode must be success, fail, or wait")
        if not os.environ.get("GITHUB_WORKSPACE") or not os.environ.get("GITHUB_OUTPUT"):
            raise ValueError("GITHUB_WORKSPACE and GITHUB_OUTPUT must be set")
        signal.signal(signal.SIGINT, on_signal)
        signal.signal(signal.SIGTERM, on_signal)
        workspace = Path(os.environ["GITHUB_WORKSPACE"])
        partial = workspace / ".lesson17.partial"
        partial.write_text("completed local report\n", encoding="utf-8")
        print("READY: staging file exists", flush=True)
        if mode == "wait":
            while True:
                time.sleep(0.05)
        if mode == "fail":
            raise ValueError("deliberate failure before publication")
        partial.replace(workspace / "result.txt")
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
            output.write("result=result.txt\n")
        print("DONE: result published", flush=True)
        return 0
    except Interrupted as error:
        print(f"interrupted: {signal.Signals(error.signum).name}", file=sys.stderr)
        return 128 + error.signum
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    finally:
        if partial is not None:
            partial.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
