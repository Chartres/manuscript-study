"""Read the transcriptions: for each piece, its systems in order (page, system, bar count, RH text)
and the doubt notes mapped to (system index, bar indices within the system).
ABC is written one line per manuscript system (a `% pN sM` comment, then [V:RH] and [V:LH]),
so system index == abcjs line index."""
import re
from pathlib import Path

BAR = re.compile(r"\|\]|\|\||:\|\|?:?|\|:|\|")


def count_bars(line):
    """Bars in one voice line: barline tokens after the first note (a leading |: opens, it does not close)."""
    s = re.sub(r'"[^"]*"|![^!]*!|\[[12]|\[[A-Za-z]:[^\]]*\]', " ", line)
    toks = [m.start() for m in BAR.finditer(s)]
    first_note = re.search(r"[A-Ga-gz]", s)
    return sum(1 for pos in toks if first_note and pos > first_note.start())


def systems(files):
    """files: ABC paths of one piece, in order."""
    out, cur = [], None
    for f in files:
        for raw in Path(f).read_text().splitlines():
            m = re.match(r"%\s*p(\d+)\s*s(\d+)\b", raw.strip())
            if m and not (cur and (cur["page"], cur["system"]) == (int(m[1]), int(m[2]))):
                cur = {"page": int(m[1]), "system": int(m[2]), "rh": None, "bars": 0, "doubts": []}
                out.append(cur)
            elif raw.startswith("[V:RH]") and cur is not None and cur["rh"] is None:
                cur["rh"] = raw[6:]
                cur["bars"] = count_bars(raw[6:])
            elif raw.startswith("% ?") and cur is not None:
                cur["doubts"].append(raw[3:].strip())
    return out


def doubt_bars(sys_list):
    """Map each doubt note to {line, bars, text}. Notes name pN sM and bK, bK-L, bK-bL or bK, bL;
    absolute bar numbers are recognised when K exceeds the system's bar count."""
    starts, n = [], 0
    for s in sys_list:
        starts.append(n); n += s["bars"]
    res = []
    for i, s in enumerate(sys_list):
        for note in s["doubts"]:
            m = re.match(r"p(\d+)\s*s(\d+)\s*(.*)", note)
            si, rest = i, note
            if m:
                tgt = [j for j, t in enumerate(sys_list) if t["page"] == int(m[1]) and t["system"] == int(m[2])]
                si, rest = (tgt[0] if tgt else i), m[3]
            nums = []
            for a, b in re.findall(r"b(\d+)(?:\s*[-–]\s*b?(\d+))?", rest.split(":")[0]):
                a = int(a); b = int(b) if b else a
                nums += list(range(a, b + 1))
            sysb = sys_list[si]["bars"]
            if nums and max(nums) > sysb:
                nums = [k - starts[si] for k in nums]
            bars = sorted({k - 1 for k in nums if 1 <= k <= sysb})
            text = note.split(":", 1)[1].strip() if ":" in note else note
            res.append({"line": si, "bars": bars, "text": text, "raw": note})
    return res
