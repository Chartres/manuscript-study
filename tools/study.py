"""Load study.json from the study directory (argv[1] or the current directory)."""
import json, sys
from pathlib import Path


def load(argv=None):
    argv = sys.argv if argv is None else argv
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    cfg = json.loads((root / "study.json").read_text())
    cfg["_root"] = root
    return cfg
