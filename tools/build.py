"""Build a study: manuscript pages, joined ABC, piano audio (FLAC + MP3), score PDFs, comparison data.
Run: python -I tools/build.py <study-dir>
Needs on PATH: pdftoppm, abc2midi, abcm2ps, rsvg-convert, fluidsynth, ffmpeg, ffprobe.
Soundfont: study.json "soundfont", or $MS_SOUNDFONT (e.g. Salamander Grand Piano SF2)."""
import os, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from study import load

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent


def run(*cmd, **kw):
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def main():
    cfg = load(); root = cfg["_root"]
    build, site = root / "build", root / "site"
    for d in (build / "pages", site / "audio", site / "noty"): d.mkdir(parents=True, exist_ok=True)

    # 1. pages as PNG at the study's dpi (named p-1.png … regardless of pdftoppm's zero padding)
    scan = root / cfg["scan"]
    if not list((build / "pages").glob("p-*.png")):
        run("pdftoppm", "-r", cfg.get("dpi", 220), "-png", scan, build / "pages/raw")
        for f in (build / "pages").glob("raw-*.png"):
            f.rename(build / "pages" / f"p-{int(f.stem.split('-')[1])}.png")
    shutil.copy(scan, site / "noty/manuscript.pdf")
    missing = [f for p in cfg["pieces"] for f in p["abc"] if not (root / f).exists()]
    if not cfg["pieces"] or missing:
        print(f"pages ready in {build / 'pages'}; transcribe next (missing: {missing or 'no pieces in study.json'})")
        return

    # 2. one ABC per piece: sections transcribed separately are joined under the first header
    for p in cfg["pieces"]:
        parts = [(root / f).read_text() for f in p["abc"]]
        body = [parts[0]] + ["\n".join(l for l in t.splitlines() if not re.match(r"^([XTCMLQKV]:|%%score)", l)) for t in parts[1:]]
        (build / f"{p['slug']}.abc").write_text("\n".join(body) + "\n")

    sf2 = cfg.get("soundfont") or os.environ.get("MS_SOUNDFONT")
    for p in cfg["pieces"]:
        slug, abc = p["slug"], build / f"{p['slug']}.abc"
        # 3. audio: abc2midi defaults to acoustic grand with a beat-1 accent
        if sf2:
            run("abc2midi", abc, "-o", build / f"{slug}.mid", "-quiet", stdout=subprocess.DEVNULL)
            run("fluidsynth", "-ni", "-q", "-g", "0.35", "-r", "48000", "-R", "1", "-C", "0",
                "-F", build / f"{slug}.wav", Path(sf2).expanduser(), build / f"{slug}.mid", stderr=subprocess.DEVNULL)
            # trim trailing silence past 2 s, normalise to -16 LUFS
            run("ffmpeg", "-loglevel", "error", "-y", "-i", build / f"{slug}.wav", "-af",
                "areverse,silenceremove=start_periods=1:start_silence=2:start_threshold=-60dB,areverse,"
                "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", site / f"audio/{slug}.flac")
            run("ffmpeg", "-loglevel", "error", "-y", "-i", site / f"audio/{slug}.flac", "-codec:a", "libmp3lame",
                "-b:a", "320k", site / f"audio/{slug}.mp3")
        else:
            print(f"{slug}: no soundfont (study.json 'soundfont' or $MS_SOUNDFONT); audio skipped")
        # 4. score PDF with every bar numbered
        for f in build.glob(f"{slug}-*.svg"): f.unlink()
        run("abcm2ps", "-q", "-v", "-j1", "-D", REPO, "-F", "score.fmt", abc, "-O", build / f"{slug}-",
            stdout=subprocess.DEVNULL)
        run("rsvg-convert", "-f", "pdf", "-b", "white", "-o", site / f"noty/{slug}.pdf", *sorted(build.glob(f"{slug}-*.svg")))
        print(f"{slug}: built")

    # 5. comparison data: systems, barlines, scan strips, doubts
    run(sys.executable, "-I", TOOLS / "bars.py", root)
    # 6. the page template
    for f in (REPO / "site").rglob("*"):
        if f.is_file():
            dest = site / f.relative_to(REPO / "site"); dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, dest)


if __name__ == "__main__":
    main()
