---
name: manuscript-study
description: Turn a scan of handwritten or old sheet music (piano, two staves) into a study - a transcription with every doubtful reading marked and explained, a piano recording, and a static web page where each bar of the original sits over the same bar of the transcription and a cursor follows the audio. Use when someone has a PDF or photos of a manuscript and wants to hear it, check it, or share it.
---

# Manuscript study

Scan in; out comes a folder of static files: `index.html` (pieces, players, downloads),
`study.html?k=<piece>` (original over transcription, live cursor, doubts), score PDFs, MP3/FLAC.
You (Claude, in the user's session) do the reading. No API calls, no server, no account.

The honesty rule: a machine transcription of someone's handwriting is a set of guesses. Every
guess you are not sure of gets a `% ?` note, and the page shows it. Do not drop notes to make
the result look cleaner, and say in the footer that the recording is machine-made.

## 0. Setup (once)

Tools on PATH: `pdftoppm` (poppler), `abc2midi` (abcmidi), `abcm2ps`, `rsvg-convert` (librsvg),
`fluidsynth`, `ffmpeg`. macOS: `brew install poppler abcmidi abcm2ps librsvg fluid-synth ffmpeg`.
Python 3 with `pillow numpy` (and `playwright` for the browser check). A piano soundfont, e.g.
Salamander Grand Piano SF2 (CC-BY, freepats.zenvoid.org) → `export MS_SOUNDFONT=/path/to.sf2`.
`TOOLS` below means this repo's `tools/` directory.

## 1. Start the study

Make a directory with the scan (`src/manuscript.pdf`; photos → one PDF with Pillow) and a
`study.json` (see `examples/renyi/study.json`):

```json
{ "title": "…", "subtitle": "…", "composer": "…", "lang": "en", "scan": "src/manuscript.pdf",
  "dpi": 220, "pieces": [], "feedback_url": "mailto:…", "footer": "Transcribed from the manuscript;
  the recording is machine-made." }
```

Run `python -I TOOLS/build.py <study>`: with no pieces it stops after writing the pages to
`build/pages/p-N.png`. Look at every page. Name the pieces, their pages and systems, and fill
`pieces` (`slug`, `title`, `meta`, `abc`: the ABC files in page order). A piece that spans pages is
transcribed in sections, one file per page, joined by the build.

## 2. Transcribe (the expensive, careful part)

One agent per page or page section, in parallel, top-tier model: this is judgment, not bulk work.
Each brief: the page path, which systems, title/key/metre/tempo as far as you can see them, the
output file, and `references/transcription.md` (conventions; follow exactly). Ask each for its bar
count per system and its list of `% ?` notes. Lessons from the first study:
- Handwriters often draw one ledger line where two belong and put low notes a step off; agents
  should decide those from the harmony and log them.
- `fine` at the end of a section usually just means "end"; a repeat start that is not marked must
  be decided (log it) or the MIDI repeats from the top.
- Say where scratch files go (`build/tmp/`): reads outside the working directory stop agents on
  permission prompts.

## 3. Build and check

`python -I TOOLS/build.py <study>` renders audio, score PDFs and the comparison data. It stops when a
system's barlines on the scan do not match its bar count in the ABC, and names it. Then:
- Open `build/bars/p-N.png` (green = barline found). Stems where both hands' chords line up and
  repeat signs fool the detector. For a wrong system add `"bars": {"override": {"<page>:<system>":
  [x0, x1, …]}}` (page pixels at the study's dpi: left edge, every barline, right edge) and rebuild.
  A blank staff next to a title can count as a staff: add its top row to `bars.skip_staves`.
- `abc2midi` warnings mean a bar does not add up: fix the ABC, not the warning.

## 4. Doubts in the reader's language

If `lang` is not `en`: `python -I TOOLS/doubts.py <study>` writes `build/doubts-en.json`; translate
it (keep every pitch; plain words; in Slovak, Czech, German and Hungarian a natural B is H and B-flat
is B) to `abc/doubts-<lang>.json` with the same keys, and rebuild. UI strings exist for `en` and `sk`;
add a language to the `T` tables in `site/index.html` and `site/study.html`.

## 5. Look, then publish

`cd <study>/site && python3 -m http.server`, open `study.html?k=<slug>`, play, click a bar.
`python -I tests/e2e_check.py http://localhost:8000 <slug> <seconds-per-bar>` checks alignment,
cursor, seeking and phone width. Show the user before publishing. Any static host works; Cloudflare
Pages: `npx wrangler pages deploy <study>/site --project-name <name>`. The players load each MP3
whole, because some hosts ignore Range requests and a streamed MP3 cannot seek there.

Publishing someone's manuscript is their call, not yours: ask before deploying.
