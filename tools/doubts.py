"""Export the doubt notes for translation: writes build/doubts-en.json ({"<slug>#<n>": text}).
Translate into abc/doubts-<lang>.json with the same keys; the build uses it for study.json "lang".
Run: python -I tools/doubts.py <study-dir>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from structure import systems, doubt_bars
from study import load

cfg = load(); root = cfg["_root"]
out = {f"{p['slug']}#{i}": d["text"] for p in cfg["pieces"]
       for i, d in enumerate(doubt_bars(systems([root / f for f in p["abc"]])))}
(root / "build").mkdir(exist_ok=True)
(root / "build/doubts-en.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"{len(out)} notes → {root / 'build/doubts-en.json'}")
