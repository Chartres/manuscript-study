# Transcription conventions (all sections)

Source: the study's pages at `<study>/build/pages/p-N.png` (220 dpi unless study.json says otherwise).
Scratch files (crops, renders) go under `<study>/build/tmp/`, not `/tmp`: reads outside the working directories stop agents on a permission prompt.
Goal: a faithful ABC transcription that `abc2midi` turns into a piano performance.

- ABC 2.1. Header: `X:1`, `T:<title> (section)`, `M:3/4` (or what the page says), `L:1/8`, `Q:1/4=<tempo>`, `K:<key>`.
- Two voices: `%%score {RH LH}`, `V:RH clef=treble`, `V:LH clef=bass`.
- Write music system by system, matching the page: for each system a `% pN sM` comment, then `[V:RH]` line, then `[V:LH]` line. Every system: RH and LH have the same number of bars and each bar adds up to the time signature (use `z` rests; chords as `[FAc]`; ties `-`; dotted `A3`).
- Keep repeats and voltas as written (`|:`, `:|`, `[1`, `[2`). Do not expand them; abc2midi expands them.
- Key and metre: read them from each system's signatures; inline `K:`/`M:` changes where they change. Write accidentals exactly as handwritten; remember bar-line resets.
- Handwriting is unclear in places. Resolve by harmonic sense (e.g. in a waltz the LH has a bass note on beat 1 and a chord on 2 and 3; voice-leading and the harmony of the bar). Log every guess as `% ? pN sM bK: <what and why>` directly after the bar's system.
- Dynamics (`!p!`, `!f!`, `!mf!`) and `!fermata!` where written; skip slurs (no audible effect).
- Self-check before finishing:
  1. `abc2midi <file> -o /tmp/<name>.mid` prints no bar-length or voice warnings.
  2. `abcm2ps -g <file> -O /tmp/<name>.svg` then `rsvg-convert -b white -z 2 /tmp/<name>001.svg -o /tmp/<name>.png` — render the result and compare it bar by bar with the scan (crop the page with Python + Pillow if you need to zoom). Fix mismatches.
