# Discovery probe — manuscript-study (pre-registered 2026-11-19)

**Question (RAT):** is there anyone outside Pavol's family who holds a handwritten manuscript and
will run this (or ask for it), and do listeners look at the doubts rather than only listen?

**Threshold, read on 2026-11-28 (the discovery kill date):**
- PASS: ≥1 person outside the family tries the skill on their own manuscript or asks for a study
  of one (issue, comment, email), **or** ≥3 substantive comments describing a manuscript they hold.
- KILL per the record: nobody outside the family by 2026-11-28.
- Side signals, recorded not gated: GitHub stars, clones, renyi.pages.dev feedback-form reports
  (a report of a wrong note = someone checked a doubt).

**Channels (Pavol sends; nothing goes out without him):** Show HN, then r/ClaudeAI a day later.

---

## Show HN

Title: `Show HN: Turn a handwritten score into a page where the original plays bar by bar`

URL: https://github.com/Chartres/manuscript-study

First comment:

> A relative left a notebook of handwritten piano pieces: waltzes, two hymns. Nobody in the family
> reads music well enough to play them. OMR tools are built for print, and the ones that accept
> handwriting do not tell you where they guessed.
>
> So I had Claude Code read the pages into ABC notation, one line per manuscript system, logging
> every unsure note with a reason (97 of them for 6 pages). A small script finds the barlines on the
> scan and checks each line's bar count against the transcription, which catches dropped bars. The
> page then stretches each original bar over the matching transcribed bar, plays a sampled piano,
> and moves a box across both. Doubtful bars are yellow with the reason underneath, and listeners can
> report a wrong note.
>
> Demo (in Slovak): https://renyi.pages.dev — open "Porovnať s rukopisom" on any piece.
>
> It is a Claude Code skill plus a build script; no server or API key. The barline detector needed
> hand overrides on about 15 of 42 systems, mostly where both hands' chords line up and look like a
> barline. Two-staff piano only for now. I would like to hear from anyone with a drawer of family or
> parish manuscripts.

Prefilled submit link (opens HN with title and URL filled; Pavol adds the comment after posting):
https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2FChartres%2Fmanuscript-study&t=Show%20HN%3A%20Turn%20a%20handwritten%20score%20into%20a%20page%20where%20the%20original%20plays%20bar%20by%20bar

## r/ClaudeAI (a day later)

Title: `I used Claude Code to read a handwritten family manuscript and make a page where the original plays bar by bar`

Body: the HN comment above, plus one paragraph:

> What worked: one agent per page with strict conventions (one ABC line per system, every guess
> logged with page/system/bar). What did not: letting agents write scratch files to /tmp (permission
> prompts), and trusting a barline count without checking it against the image.

Prefilled submit link: https://www.reddit.com/r/ClaudeAI/submit?title=I%20used%20Claude%20Code%20to%20read%20a%20handwritten%20family%20manuscript%20and%20make%20a%20page%20where%20the%20original%20plays%20bar%20by%20bar&url=https%3A%2F%2Fgithub.com%2FChartres%2Fmanuscript-study
