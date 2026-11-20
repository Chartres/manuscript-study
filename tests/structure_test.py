"""Bar counting and doubt placement, checked on the renyi example (counts read off the manuscript).
Run: python -I tests/structure_test.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from structure import systems, doubt_bars, count_bars

assert count_bars(" [FA]6 | [FA]2 z2 z2 |: !f! [CG]4 B2 | E4 [EG]2 |") == 4
assert count_bars(" [2 [A,CF]6 || C2 F2- [FA]2 | [Ac]6 |") == 3
assert count_bars(' "^Tempo di valse"!p! A,4 DF | F6 & x4 de |') == 2
ex = ROOT / "examples/renyi/abc"
expected = {
    ("olga-1", "olga-2", "olga-3"): [6, 5, 6, 5, 5, 5, 5, 6, 5, 6, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 5, 7],
    ("hymna",): [4, 4], ("hymnisches-lied",): [6, 5, 5],
    ("maria",): [6, 6, 6, 6, 6, 6, 7, 5], ("valcik",): [4, 4, 3, 4, 4, 3, 2],
}
unplaced = 0
for names, counts in expected.items():
    ss = systems([ex / f"{n}.abc" for n in names])
    assert [s["bars"] for s in ss] == counts, (names, [s["bars"] for s in ss])
    for d in doubt_bars(ss):
        assert all(0 <= k < ss[d["line"]]["bars"] for k in d["bars"]), d
        unplaced += not d["bars"]
assert unplaced <= 1, unplaced  # only a page-wide note may lack a bar
# Maria's notes use absolute bar numbers: "b7-8" is the first two bars of line 2
print("structure: ok")
