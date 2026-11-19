"""Find every system and barline on the manuscript pages and write the comparison data:
site/data/<slug>.json (systems, bar edges, doubts), site/data/<slug>.abc, site/scan/<slug>-<n>.webp.

The transcription is the check: each system must yield exactly as many bars as its ABC line, or the
script stops and names the system. Overlays for checking by eye go to build/bars/p-N.png (green =
barline found, red = count mismatch). Fix a wrong system with a hand override in study.json
("bars.override": {"page:system": [x, ...]} in page pixels at the study's dpi).

Run: python -I tools/bars.py <study-dir>"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from structure import systems, doubt_bars
from study import load

INK = 140  # grey level below which a pixel counts as ink


def staves(mask, k, skip):
    """Staves as (top, bottom) rows. Hand-ruled lines slant, so single rows miss them; smooth the row
    ink profile over one staff height and take peaks a staff-gap apart. k scales pixels from 220 dpi."""
    H, W = mask.shape
    prof = mask[:, int(W * .15):int(W * .85)].mean(1)
    sm = np.convolve(prof, np.ones(int(72 * k)) / int(72 * k), "same")
    peaks = []
    for y in np.argsort(-sm):
        if sm[y] < .045: break
        if all(abs(y - p) > 120 * k for p in peaks): peaks.append(int(y))
    half = int(38 * k)
    st = sorted((p - half, p + half) for p in peaks if 60 * k < p < H - 60 * k)
    keep = []
    for t, b in st:  # drop empty staves: nothing vertical between the lines
        band = mask[max(0, t - int(25 * k)):b + int(25 * k), int(W * .1):int(W * .95)]
        if (band.mean(0) > .25).mean() > .03: keep.append((t, b))
    return [s for s in keep if not any(abs(s[0] - y) < 40 * k for y in skip)]


def barlines(mask, treble, bass, n, k):
    """n+1 x positions: the system's left edge plus n barlines. A barline is a thin stroke through the
    full height of both staves with nothing beside it but staff lines; a stem has noteheads next to it."""
    W = mask.shape[1]

    def feats(t, b):
        band = mask[t - 4:b + 5]
        pad = np.pad(band, ((0, 0), (2, 2)))
        thick = np.max(np.stack([pad[:, i:i + W] for i in range(5)]), axis=0)  # tolerate slant
        dens = band.mean(0)
        w = np.ones(int(9 * k)); z = np.zeros(int(7 * k))
        side = (np.convolve(dens, np.r_[w, z, np.zeros(len(w))], "same") +
                np.convolve(dens, np.r_[np.zeros(len(w)), z, w], "same")) / (2 * len(w))
        return thick.mean(0), side
    ct, st = feats(*treble)
    cb, sb = feats(*bass)
    full = np.minimum(ct, cb)
    score = full - 1.5 * np.maximum(st - .2, 0) - 1.5 * np.maximum(sb - .2, 0)
    left = int(np.argmax(full[:int(W * .2)] > .6))
    zone = np.where(full[int(W * .75):int(W * .975)] > .6)[0]  # stop short of the paper edge
    right = int(W * .75) + int(zone[-1]) if len(zone) else W - 1
    picked = [left, right]
    for x in np.argsort(-score):
        if score[x] < .45 or len(picked) == n + 1: break
        if left + 60 * k < x < right - 40 * k and all(abs(x - p) > 45 * k for p in picked): picked.append(int(x))
    return sorted(picked)


def main():
    cfg = load(); root = cfg["_root"]
    dpi = cfg.get("dpi", 220); k = dpi / 220
    bcfg = cfg.get("bars", {})
    skip = {int(p): ys for p, ys in bcfg.get("skip_staves", {}).items()}
    override = {tuple(map(int, key.split(":"))): xs for key, xs in bcfg.get("override", {}).items()}
    pages_dir = root / "build/pages"
    out_dir = root / "site/data"; scan_dir = root / "site/scan"; dbg = root / "build/bars"
    for d in (out_dir, scan_dir, dbg): d.mkdir(parents=True, exist_ok=True)

    piece_sys = {p["slug"]: systems([root / f for f in p["abc"]]) for p in cfg["pieces"]}
    by_page = {}
    for slug, ss in piece_sys.items():
        for s in ss: by_page.setdefault(s["page"], []).append((slug, s))
    problems, result = [], {slug: [] for slug in piece_sys}
    for page, items in sorted(by_page.items()):
        img = Image.open(pages_dir / f"p-{page}.png").convert("RGB")
        mask = np.asarray(ImageOps.grayscale(img), dtype=np.int16) < INK
        st = staves(mask, k, skip.get(page, []))
        if len(st) != 2 * len(items):
            problems.append(f"p{page}: {len(st)} staves found, {2 * len(items)} expected "
                            f"(add blank-staff tops to bars.skip_staves; staff tops: {[t for t, _ in st]})")
            continue
        d = ImageDraw.Draw(img)
        for i, (slug, s) in enumerate(sorted(items, key=lambda t: t[1]["system"])):
            tr, bs = st[2 * i], st[2 * i + 1]
            xs = override.get((page, s["system"])) or barlines(mask, tr, bs, s["bars"], k)
            ok = len(xs) == s["bars"] + 1
            if not ok: problems.append(f"p{page} s{s['system']}: {len(xs) - 1} bars found, {s['bars']} in ABC")
            for x in xs: d.line([(x, tr[0] - 10), (x, bs[1] + 10)], fill=(0, 160, 0) if ok else (220, 0, 0), width=5)
            d.text((10, tr[0]), f"s{s['system']}", fill=(220, 0, 0))
            result[slug].append({"page": page, "system": s["system"], "y0": max(0, tr[0] - int(70 * k)),
                                 "y1": min(img.height, bs[1] + int(70 * k)), "bars": list(xs)})
        img.thumbnail((1100, 1600)); img.save(dbg / f"p-{page}.png")
    if problems:
        print("\n".join(problems)); print(f"overlays: {dbg}"); sys.exit(1)

    lang = cfg.get("lang", "en")
    tr_path = root / f"abc/doubts-{lang}.json"
    translated = json.loads(tr_path.read_text()) if tr_path.exists() else {}
    pages = {}
    for p in cfg["pieces"]:
        slug = p["slug"]
        for i, s in enumerate(result[slug]):
            im = pages.setdefault(s["page"], Image.open(pages_dir / f"p-{s['page']}.png").convert("RGB"))
            x0 = max(0, s["bars"][0] - int(50 * k)); x1 = min(im.width, s["bars"][-1] + int(50 * k)); W = x1 - x0
            strip = im.crop((x0, s["y0"], x1, s["y1"]))
            strip = strip.resize((1400, round(strip.height * 1400 / W)), Image.LANCZOS)
            name = f"{slug}-{i + 1}.webp"
            strip.save(scan_dir / name, quality=72)
            s.update(img=f"scan/{name}", aspect=round(strip.width / strip.height, 4),
                     bars=[round((x - x0) / W, 4) for x in s["bars"]])
            del s["y0"], s["y1"]
        doubts = doubt_bars(piece_sys[slug])
        for i, dd in enumerate(doubts):
            dd["note"] = translated.get(f"{slug}#{i}", dd["text"])
        (out_dir / f"{slug}.abc").write_text((root / f"build/{slug}.abc").read_text())
        (out_dir / f"{slug}.json").write_text(json.dumps({"systems": result[slug], "doubts": doubts}, ensure_ascii=False))
    meta = {k_: cfg.get(k_) for k_ in ("title", "subtitle", "composer", "lang", "feedback_url", "footer")}
    meta["pieces"] = [{x: p.get(x) for x in ("slug", "title", "meta")} | {"pages": sorted({s["page"] for s in result[p["slug"]]})}
                      for p in cfg["pieces"]]
    (out_dir / "study.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print("ok", {slug: len(v) for slug, v in result.items()})


if __name__ == "__main__":
    main()
