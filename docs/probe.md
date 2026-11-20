# Probe — manuscript-study (pre-registered 2026-11-19, revised 2026-11-20)

**Question (RAT):** do people outside the family send a handwritten manuscript when the offer is
"send photos, get a study back", and do their families check the marked notes rather than only listen?

**Instrument:** the concierge page https://manuscript-study.dravec.org — photos + email, Pavol and
Claude make a study like renyi within a week, free for the first ten. Persona, job and journey:
me.dravec.org/manuscript-persona.html. Demand evidence: me.dravec.org/manuscript-demand.html.

**Thresholds (read 14 days after the first post):**
- BUILD the phone app: ≥5 requests from outside the family.
- ITERATE (different channel or offer): 1–4 requests.
- KILL per the flywheel record: nobody outside the family tries it or asks by 2026-11-28.
- Recorded, not gated: doubts answered per delivered study (journey step 6, the riskiest step),
  days to delivery, plays per study, stars on the repo.

**Channels (Pavol sends; nothing goes out without him).** Order: Show HN → r/Genealogy →
r/Archivists → r/musicology → r/ClaudeAI (technical, for the repo). Before each Reddit post: open
the sidebar and rules, search the sub for "AI" in mod posts. r/opensource bans AI-assisted projects:
do not post there.

---

## Show HN

Title: `Show HN: My grandfather's handwritten waltzes, played bar by bar against the original`

URL: https://manuscript-study.dravec.org

First comment:

> My grandfather, Dr. Zoltán Rényi, left a squared school notebook of piano pieces: two waltzes,
> two hymns, one untitled waltz. Nobody in the family reads music well enough to play them, and the
> sheet-music scanning apps could not read his handwriting.
>
> I had Claude read the pages into ABC notation, one line per manuscript system, logging every
> unsure note with a reason (97 for six pages). A second, closer pass cleared most of those and
> fixed seven bars; thirteen remain for someone who reads music. A small script finds the barlines on
> the scan and checks each line's bar count against the transcription, which catches dropped bars.
> The page stretches each original bar over the matching transcribed bar, plays a sampled piano, and
> moves a box across both. Family members can tap a marked bar on their phone and answer "correct",
> "wrong" (with a note editor) or "not sure"; every answer is kept with who and when.
>
> His notebook: https://renyi.dravec.org (Slovak; open "Porovnať s rukopisom").
> Code (MIT): https://github.com/Chartres/manuscript-study
>
> The link above is an offer: send photos of a handwritten manuscript and I will make the same for the
> first ten, free, within a week. I want to learn whether other families have these notebooks and
> whether they check the marked notes or only listen.

Prefilled submit link: https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fmanuscript-study.dravec.org&t=Show%20HN%3A%20My%20grandfather%27s%20handwritten%20waltzes%2C%20played%20bar%20by%20bar%20against%20the%20original

## r/Genealogy

Title: `My grandfather's handwritten piano music, made playable with the original shown bar by bar`

> My grandfather, Dr. Zoltán Rényi, left a notebook of handwritten piano pieces: waltzes and two
> hymns. Nobody in the family reads music well enough to play them, and archives generally do not
> take this kind of material.
>
> I turned it into a page where you listen to each piece while the original handwriting and a clean
> transcription move along together, bar by bar. Places where the handwriting was unclear are marked
> with the reason, and relatives can confirm or correct them from their phones.
>
> Disclosure: the first reading was made with an AI model and then checked; every spot where it was
> unsure is shown rather than smoothed over. The recording is a sampled piano, not a person.
>
> His notebook (Slovak): https://renyi.dravec.org. If you have a similar notebook in a drawer, I will
> make the same for the first ten people, free: https://manuscript-study.dravec.org. I would also like
> to hear how others have handled music in family papers.

Prefilled submit link (paste the body; Reddit's prefill does not carry long text reliably): https://www.reddit.com/r/Genealogy/submit?selftext=true&title=My%20grandfather%27s%20handwritten%20piano%20music%2C%20made%20playable%20with%20the%20original%20shown%20bar%20by%20bar

## r/Archivists

Title: `How do you flag doubtful readings when transcribing a handwritten music manuscript?`

> I transcribed my grandfather's 6-page handwritten notebook of piano pieces (mid-20th century,
> Slovak/Hungarian). The handwriting is clear in most places, but ledger lines are often missing, so
> many low notes could be read two ways.
>
> What I did: every unsure reading gets a note (page, line, bar, what was read and why). The page
> puts each original bar directly above the transcribed bar, marks doubtful bars in yellow with the
> reason, plays the music, and lets a reader confirm or correct a bar with a record of who and when.
> The first reading was AI-made, which is why every guess is exposed rather than resolved silently.
>
> Questions for people who do this professionally:
> - Is there a convention you use for doubtful readings in music (MEI's <unclear>/<supplied>,
>   editorial brackets, something else)?
> - Is the who-checked-what record useful to you, or only to families?
>
> Example (Slovak interface): https://renyi.dravec.org. Code, free: https://github.com/Chartres/manuscript-study

Prefilled submit link (paste the body): https://www.reddit.com/r/Archivists/submit?selftext=true&title=How%20do%20you%20flag%20doubtful%20readings%20when%20transcribing%20a%20handwritten%20music%20manuscript%3F

## r/musicology

Title: `Marking uncertain readings in a transcription of an amateur music manuscript: what conventions would you use?`

> I transcribed my grandfather's handwritten piano pieces (an amateur composer, mid-20th century) and
> had to present uncertain readings to a non-specialist family: mostly missing ledger lines and
> accidentals that may or may not carry over. Each original bar is shown above its transcribed bar,
> uncertain bars carry a short explanation (Bartók's inline "or possibly" in his folk-song sources was
> the model), and the music plays with a cursor across both. Disclosure: the first reading was
> AI-assisted, which is the reason the doubts are exposed.
>
> Is there established practice for this outside critical editions (MEI <unclear>/<supplied> with
> @cert, editorial brackets)? Is anything lost by stretching the facsimile bars to line up with the
> engraving?
>
> Example: https://renyi.dravec.org (Slovak). Code: https://github.com/Chartres/manuscript-study

Prefilled submit link (paste the body): https://www.reddit.com/r/musicology/submit?selftext=true&title=Marking%20uncertain%20readings%20in%20a%20transcription%20of%20an%20amateur%20music%20manuscript%3A%20what%20conventions%20would%20you%20use%3F

## r/ClaudeAI

Title: `I used Claude Code to read my grandfather's handwritten music and make a page where the original plays bar by bar`

Body: the Show HN comment, plus:

> What worked: one agent per page with strict conventions (one ABC line per system, every guess
> logged with page/system/bar), then a second pass of agents that looked at each doubtful bar at full
> resolution and answered clear / keep / fix (78 of 97 were false alarms, 7 bars were wrong). What did
> not: letting agents write scratch files to /tmp (permission prompts), and trusting a barline count
> without checking it against the image.

Prefilled submit link: https://www.reddit.com/r/ClaudeAI/submit?title=I%20used%20Claude%20Code%20to%20read%20my%20grandfather%27s%20handwritten%20music%20and%20make%20a%20page%20where%20the%20original%20plays%20bar%20by%20bar&url=https%3A%2F%2Fgithub.com%2FChartres%2Fmanuscript-study
