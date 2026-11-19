# Manuscript study

Turn a scan of handwritten or old sheet music into a study you can listen to and check:
a transcription with every doubtful reading marked and explained, a piano recording, and a page
where each bar of the original sits over the same bar of the transcription while a cursor follows
the music.

**Example:** [renyi.pages.dev](https://renyi.pages.dev) — five piano pieces from a family manuscript
(Slovak). Open "Porovnať s rukopisom" on any piece.

## Why

Optical music recognition is built for printed scores, and the tools that read handwriting do not
show where they guessed. For a relative's handwritten waltz the guesses are the point: you need to
see the original next to every reading and know which bars are uncertain. Critical editions have
done this for a long time (Bartók flagged doubtful readings inline; MEI has `<unclear>`); this repo
does it for a family drawer.

## How it works

1. **Reading:** Claude (in your Claude Code session, as a skill) transcribes each page into ABC
   notation, one line per manuscript system, logging every unsure reading as a `% ?` note.
2. **Sound:** `abc2midi` + `fluidsynth` with a sampled grand piano → loudness-normalised MP3 and FLAC.
3. **Bars on the scan:** a small image-processing step finds staves and barlines on the pages and
   checks each system's bar count against the transcription; mismatches stop the build. Wrong
   systems get a hand override (debug overlays show where).
4. **Page:** [abcjs](https://github.com/paulrosen/abcjs) renders and times the transcription; each
   manuscript bar is cut out and stretched over its transcribed bar; one box per bar carries the
   cursor, the doubt mark and click-to-seek. Static files, host anywhere.

No server, no API key, no account: the reading happens in your own Claude session.

## Use

```sh
git clone https://github.com/Chartres/manuscript-study && cd manuscript-study
./install.sh              # links the skill into ~/.claude/skills
```

Then in Claude Code, in a directory with your scan: "make a manuscript study of this PDF". The
skill (`skill/manuscript-study/SKILL.md`) walks through setup, transcription, the build, the bar
check and publishing.

Rebuild the example: `MS_SOUNDFONT=/path/to/piano.sf2 python3 -I tools/build.py examples/renyi`.
Tests: `python3 -I tests/structure_test.py`; browser check: `tests/e2e_check.py`.

## Limits

- Two-staff piano music. Other layouts need the conventions and the staff pairing extended.
- The transcription is only as good as the reading; that is why the doubts are on the page.
  Listeners can report errors through the study's feedback link.
- The recording is synthetic: a sampled piano playing the notes, not an interpretation.

## Licence

MIT for this repo's code. abcjs is MIT (`site/lib`). The example manuscript and its transcription
are published by Pavol Dravecký; ask before reusing them.
