# Discovery probe — manuscript-study (pre-registered 2026-11-19)

**Question (RAT):** is there anyone outside Pavol's family who holds a handwritten manuscript and
will run this (or ask for it), and do listeners look at the doubts rather than only listen?

**Threshold, read on 2026-11-28 (the discovery kill date):**
- PASS: ≥1 person outside the family tries the skill on their own manuscript or asks for a study
  of one (issue, comment, email), **or** ≥3 substantive comments describing a manuscript they hold.
- KILL per the record: nobody outside the family by 2026-11-28.
- Side signals, recorded not gated: GitHub stars, clones, renyi.pages.dev feedback-form reports
  (a report of a wrong note = someone checked a doubt).

**Channels (Pavol sends; nothing goes out without him):** Show HN, then r/ClaudeAI a day later; r/Archivists, r/musicology, r/Genealogy (drafts at the end).

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


## Reddit: music and archive communities (added 2026-11-19)
Rules could not be read from here (Reddit blocks it). **Before each post: open the sidebar and rules, and search the sub for "AI" in mod posts.** r/opensource bans AI-assisted projects: do not post there. Order: r/Archivists, then r/musicology, then r/Genealogy (read its wiki; it has had AI-bot trouble). Fallbacks: r/Sheetmusic, the r/composer monthly free-for-all thread.
**Check the family wording.** The drafts say "our family"; adjust if the relationship to Dr. Rényi is different (the Show HN draft says "a relative").

### r/Archivists

Title: `How do you flag doubtful readings when transcribing a handwritten music manuscript?`

> I am digitising a 6-page handwritten notebook of piano pieces (waltzes and two hymns, mid-20th century, Slovak/Hungarian). The handwriting is clear in most places, but ledger lines are often missing, so many low notes could be read two ways.
>
> What I ended up doing: every unsure reading gets a note (page, line, bar, what was read and why), 97 in total. The published page puts each original bar directly above the transcribed bar, marks the doubtful bars in yellow with the reason underneath, and plays it so a listener can hear the alternatives.
>
> The first reading was done by an AI model (Claude), which is exactly why every guess is shown rather than hidden.
>
> Questions for people who do this professionally:
> - Is there a convention you use for doubtful readings in music (MEI's <unclear>/<supplied>, bracketed editorial additions, something else)?
> - Would you keep the facsimile and transcription side by side like this, or is that only useful for non-specialists?
>
> Example (Slovak interface): https://renyi.pages.dev, open "Porovnať s rukopisom" on any piece. The tool is free and open source: https://github.com/Chartres/manuscript-study

Prefilled submit link: https://www.reddit.com/r/Archivists/submit?selftext=true&title=How%20do%20you%20flag%20doubtful%20readings%20when%20transcribing%20a%20handwritten%20music%20manuscript%3F&text=I%20am%20digitising%20a%206-page%20handwritten%20notebook%20of%20piano%20pieces%20%28waltzes%20and%20two%20hymns%2C%20mid-20th%20century%2C%20Slovak/Hungarian%29.%20The%20handwriting%20is%20clear%20in%20most%20places%2C%20but%20ledger%20lines%20are%20often%20missing%2C%20so%20many%20low%20notes%20could%20be%20read%20two%20ways.%0A%0AWhat%20I%20ended%20up%20doing%3A%20every%20unsure%20reading%20gets%20a%20note%20%28page%2C%20line%2C%20bar%2C%20what%20was%20read%20and%20why%29%2C%2097%20in%20total.%20The%20published%20page%20puts%20each%20original%20bar%20directly%20above%20the%20transcribed%20bar%2C%20marks%20the%20doubtful%20bars%20in%20yellow%20with%20the%20reason%20underneath%2C%20and%20plays%20it%20so%20a%20listener%20can%20hear%20the%20alternatives.%0A%0AThe%20first%20reading%20was%20done%20by%20an%20AI%20model%20%28Claude%29%2C%20which%20is%20exactly%20why%20every%20guess%20is%20shown%20rather%20than%20hidden.%0A%0AQuestions%20for%20people%20who%20do%20this%20professionally%3A%0A-%20Is%20there%20a%20convention%20you%20use%20for%20doubtful%20readings%20in%20music%20%28MEI%27s%20%3Cunclear%3E/%3Csupplied%3E%2C%20bracketed%20editorial%20additions%2C%20something%20else%29%3F%0A-%20Would%20you%20keep%20the%20facsimile%20and%20transcription%20side%20by%20side%20like%20this%2C%20or%20is%20that%20only%20useful%20for%20non-specialists%3F%0A%0AExample%20%28Slovak%20interface%29%3A%20https%3A//renyi.pages.dev%2C%20open%20%22Porovna%C5%A5%20s%20rukopisom%22%20on%20any%20piece.%20The%20tool%20is%20free%20and%20open%20source%3A%20https%3A//github.com/Chartres/manuscript-study

### r/Genealogy

Title: `Made my family's handwritten piano music playable, with the original shown bar by bar`

> Our family has a notebook of handwritten piano pieces by Dr. Zoltán Rényi: waltzes and two hymns. Nobody in the family reads music well enough to play them, and archives generally do not take this kind of material.
>
> I turned it into a page where you can listen to each piece, and while it plays the original handwriting and a clean transcription move along together, bar by bar. Places where the handwriting was unclear are marked, with the reason, so relatives can check them and report a wrong note.
>
> Disclosure: the first transcription was made with an AI model, and every spot where it was unsure is shown on the page instead of being smoothed over. The recording is a sampled piano, not a person.
>
> Page (in Slovak): https://renyi.pages.dev. If you have a similar notebook in a drawer, the tool is free and open source: https://github.com/Chartres/manuscript-study. I would like to hear how others have handled music in family papers.

Prefilled submit link: https://www.reddit.com/r/Genealogy/submit?selftext=true&title=Made%20my%20family%27s%20handwritten%20piano%20music%20playable%2C%20with%20the%20original%20shown%20bar%20by%20bar&text=Our%20family%20has%20a%20notebook%20of%20handwritten%20piano%20pieces%20by%20Dr.%20Zolt%C3%A1n%20R%C3%A9nyi%3A%20waltzes%20and%20two%20hymns.%20Nobody%20in%20the%20family%20reads%20music%20well%20enough%20to%20play%20them%2C%20and%20archives%20generally%20do%20not%20take%20this%20kind%20of%20material.%0A%0AI%20turned%20it%20into%20a%20page%20where%20you%20can%20listen%20to%20each%20piece%2C%20and%20while%20it%20plays%20the%20original%20handwriting%20and%20a%20clean%20transcription%20move%20along%20together%2C%20bar%20by%20bar.%20Places%20where%20the%20handwriting%20was%20unclear%20are%20marked%2C%20with%20the%20reason%2C%20so%20relatives%20can%20check%20them%20and%20report%20a%20wrong%20note.%0A%0ADisclosure%3A%20the%20first%20transcription%20was%20made%20with%20an%20AI%20model%2C%20and%20every%20spot%20where%20it%20was%20unsure%20is%20shown%20on%20the%20page%20instead%20of%20being%20smoothed%20over.%20The%20recording%20is%20a%20sampled%20piano%2C%20not%20a%20person.%0A%0APage%20%28in%20Slovak%29%3A%20https%3A//renyi.pages.dev.%20If%20you%20have%20a%20similar%20notebook%20in%20a%20drawer%2C%20the%20tool%20is%20free%20and%20open%20source%3A%20https%3A//github.com/Chartres/manuscript-study.%20I%20would%20like%20to%20hear%20how%20others%20have%20handled%20music%20in%20family%20papers.

### r/musicology

Title: `Marking uncertain readings in a transcription of an amateur music manuscript: what conventions would you use?`

> I transcribed a small handwritten manuscript of piano pieces (an amateur composer, mid-20th century) and had to decide how to present 97 uncertain readings to a non-specialist audience: mostly missing ledger lines and accidentals that may or may not carry over.
>
> My current solution: each original bar is shown directly above its transcribed bar, uncertain bars are highlighted with a short explanation (Bartók's inline "or possibly" in his folk-song sources was the model), and the music plays with a cursor across both. Disclosure: the first reading was AI-assisted, which is the reason the doubts are exposed rather than resolved silently.
>
> Is there established practice for this outside critical editions (MEI <unclear>/<supplied> with @cert, editorial brackets)? And is anything lost by stretching the facsimile bars to line up with the engraving?
>
> Example: https://renyi.pages.dev (Slovak). Code, free: https://github.com/Chartres/manuscript-study

Prefilled submit link: https://www.reddit.com/r/musicology/submit?selftext=true&title=Marking%20uncertain%20readings%20in%20a%20transcription%20of%20an%20amateur%20music%20manuscript%3A%20what%20conventions%20would%20you%20use%3F&text=I%20transcribed%20a%20small%20handwritten%20manuscript%20of%20piano%20pieces%20%28an%20amateur%20composer%2C%20mid-20th%20century%29%20and%20had%20to%20decide%20how%20to%20present%2097%20uncertain%20readings%20to%20a%20non-specialist%20audience%3A%20mostly%20missing%20ledger%20lines%20and%20accidentals%20that%20may%20or%20may%20not%20carry%20over.%0A%0AMy%20current%20solution%3A%20each%20original%20bar%20is%20shown%20directly%20above%20its%20transcribed%20bar%2C%20uncertain%20bars%20are%20highlighted%20with%20a%20short%20explanation%20%28Bart%C3%B3k%27s%20inline%20%22or%20possibly%22%20in%20his%20folk-song%20sources%20was%20the%20model%29%2C%20and%20the%20music%20plays%20with%20a%20cursor%20across%20both.%20Disclosure%3A%20the%20first%20reading%20was%20AI-assisted%2C%20which%20is%20the%20reason%20the%20doubts%20are%20exposed%20rather%20than%20resolved%20silently.%0A%0AIs%20there%20established%20practice%20for%20this%20outside%20critical%20editions%20%28MEI%20%3Cunclear%3E/%3Csupplied%3E%20with%20%40cert%2C%20editorial%20brackets%29%3F%20And%20is%20anything%20lost%20by%20stretching%20the%20facsimile%20bars%20to%20line%20up%20with%20the%20engraving%3F%0A%0AExample%3A%20https%3A//renyi.pages.dev%20%28Slovak%29.%20Code%2C%20free%3A%20https%3A//github.com/Chartres/manuscript-study
