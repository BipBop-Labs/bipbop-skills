# Krug Usability Testing Cheatsheet: decision rules

## The six maxims
| Maxim | Decides | Ch |
|---|---|---|
| A morning a month, that's all we ask | Cadence: a fixed recurring date, never less than monthly | 3 |
| Start earlier than you think makes sense | Timing: test sketches, competitors, the current site | 4 |
| Recruit loosely and grade on a curve | Who: roughly your audience, then discount jargon-only failures | 5 |
| Make it a spectator sport | Who watches: everyone, live | 9 |
| Focus ruthlessly on a small number of the most important problems | What to fix: the top ten, worst first | 10 |
| When fixing problems, always do the least you can do | How to fix: the smallest change that prevents the observed problem | 11 |

First Law: **one user is 100% better than none.**

## Defaults and thresholds
| Thing | Default |
|---|---|
| Participants per round | **3** (2 per round in Agile, with more frequent rounds) |
| Cadence | Monthly minimum; one per sprint in Agile |
| Session | 50 min, then a 10–15 min break (not longer, or observers drift away) |
| Session split | Welcome 4 · Questions 2 · Home page tour 3 · **Tasks 35** · Probe 5 · Wrap-up 5 |
| Task list | 5–10 key user goals, with this round's subset fitting ~35 min plus fillers |
| Pilot test | ~15 min, 1–2 days before |
| Napkin test | < 5 min per person |
| Top problems per observer | 3 per session |
| Debrief | Same day, ~1 hour, over lunch; distill a **top ten** |
| Report | ≤ 2 min to read, ≤ 30 min to write |
| Prep effort | 2–3 days for the first round, 1–2 days after that |
| Remote | ~80% of the benefit for ~70% of the effort; only after ~3 in-person rounds |
| Incentive | Slightly above market (about $50 general, hundreds for specialists, 2009 figures) |

## Decision rules
- **Someone wants proof or statistics** → DIY testing can't provide it and isn't trying to. Point to quantitative methods (*Measuring the User Experience*). Don't defend n=3 with math.
- **Nothing is "ready" yet** → test the current product, a competitor, or a napkin sketch. Waiting is the worst option.
- **Asking about a concept or sketch** → ask "What do you think this is?", **never** "Do you like it?" or "What do you think of it?"
- **Recruiting a specialist is hard** → is domain knowledge actually needed for these tasks? If not, recruit loosely. If so, recruit remotely or outsource.
- **Participant fails on jargon** → grade on a curve: would *our* users know this term? If yes, discount it. If unsure, it's a finding.
- **Should I prompt a quiet participant?** → only if you're **not sure** what they're thinking.
- **Participant asks you a question** → answer with a question. Offer to answer at the end.
- **Move to the next task?** → done, miserable, out of time, or no longer learning (give it a little overtime first).
- **First participant fails a task for an obvious reason** → change or skip the task for the others. That's allowed in qualitative testing.
- **Observer wants to sit in the test room** → no. Observers go in a separate, non-adjacent room.
- **On-site person wants to watch from their desk** → no. Remote viewing is only for people who can't be there.
- **Arguing about a problem in the debrief** → "Did anybody in the tests have that problem?" If not, it's off the table.
- **Severity** → how many people × how bad. Hardest calls: corner cases (rare but severe) and ubiquitous nuisances (common but minor).
- **"The redesign will fix it"** → ask for the smallest change that smooths it over *now*.
- **Choosing a fix** → tweak (size, position, appearance, wording) before redesigning, and try **removing** something before adding.
- **Tweak didn't work** → still believe in it? Make it louder. If not, try a different tweak. Then check for side effects.
- **Unsure a fix worked** → look at it, then run a hallway test, an unmoderated remote test, or an A/B test. Re-include major changes in next month's tasks.
- **Management won't back fixes** → get them into the observation room. Demonstration beats ROI decks.

## Tells and smells
| If you see… | You're probably… |
|---|---|
| Testing scheduled "when it's done" | Heading for the Big Honkin' Test or no test at all |
| A scenario that contains the link label | Testing word-matching, not usability |
| Facilitator saying "feedback" or "opinion" | Improvising, and inviting critique instead of use |
| Observers checking email and snacking after user 3 | Past the useful number of sessions for the day |
| Home page described as "a lot of stuff" | Suffering kitchen-sink syndrome |
| Users confidently going the wrong way | Seeing a wrong-foot problem that orientation fixes |
| "They didn't notice X" | Seeing a failure to shout, so make X louder |
| A fix that starts "add instructions…" | Missing the chance to take something away |
| A 40-page findings report | Producing a report that nobody will act on |
| Top-ten items silently dropped | Letting the worst problems survive another month |
