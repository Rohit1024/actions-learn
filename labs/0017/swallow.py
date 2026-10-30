"""Deliberately broken adapter: loses the worker's nonzero status."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "action"))
import worker

worker.main()  # BUG: no raise SystemExit(...), so normal interpreter exit is zero.
