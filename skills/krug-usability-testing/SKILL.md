---
name: krug-usability-testing
description: "Knowledge base from \"Rocket Surgery Made Easy\" by Steve Krug: do-it-yourself usability testing to find and fix usability problems. Use when planning or running user tests, validating a concept or sketch early in discovery, recruiting participants, writing test tasks and scenarios, facilitating think-aloud sessions, involving stakeholders as observers, debriefing and prioritizing findings, choosing minimal fixes, or reviewing a test plan, script, or scenario for bias and clue-giving."
---

<!-- argument-hint: [topic, maxim, artifact to review, or chapter number] -->

# Rocket Surgery Made Easy
**Author**: Steve Krug | **Chapters**: 16 | **Generated**: 2026-09-21

## How to Use This Skill

- **Planning a round**: start from the six maxims below and the defaults in [cheatsheet.md](cheatsheet.md). Produce a concrete plan covering the date, what to test, three participants and how to find them, 5–10 tasks narrowed to about 35 minutes, observers, and a debrief slot.
- **Early discovery or concept validation**: use the napkin test, competitor testing, and wireframe tests from [ch04](chapters/ch04-what-and-when-to-test.md). Push to test *earlier* than the user plans to.
- **Writing artifacts**: scenarios, invitations, scripts, observer handouts, the debrief agenda, and the summary email all have templates in [test-kit.md](test-kit.md). Adapt them to the product and language, and invent examples rather than using real user data.
- **Reviewing a test plan, script, or scenarios**: report only concrete defects, each with the location, the rule it breaks, and a rewrite. Typical defects: on-screen words in a scenario, opinion questions ("Do you like…?"), leading or clue-giving phrasing, too many participants per round, testing scheduled only at the end, no observers, a debrief with no fix commitment, or redesign-sized fixes. At most 5 findings. If there are none, say so in one line.
- **Interpreting findings or choosing fixes**: rank by severity (how many people × how bad), keep the top ten, and for each ask "What's the smallest change that stops the *observed* problem?" Tweak and take away before you redesign or add.
- **With a topic or chapter**: ask about `recruiting`, `facilitation`, `debrief`, `remote`, `Home page`, or `ch08`, and I read that chapter file first.

---

## What DIY Testing Is (and Isn't)

**Usability testing = watching people try to use what you're building.** Actual use, not opinions, which is what separates it from surveys, interviews, and focus groups. Krug's kind is **qualitative**: the goal is insight to *improve*, not statistics to *prove*. That permits three users, an unscientific process, and changing tasks mid-round. It **always works** because every product has problems, the serious ones are obvious to outsiders, and watching makes the team better designers. Analytics tell you *what*; testing tells you *why*.

When someone asks for statistical validity, the answer is: you're right, three users prove nothing; the point is to find and fix obvious problems, which need no proof.

---

## The Six Maxims (the whole method)

1. **A morning a month, that's all we ask.** A fixed recurring date with three users in the morning and a debrief over lunch, done by early afternoon. The routine removes the decision about *when*. Monthly is the floor. In Agile, run a round per sprint, perhaps with two users and some remote rounds, testing last sprint's code and a paper prototype of the next. (ch03)
2. **Start earlier than you think makes sense.** The worse shape it's in, the less you want to show it, and the more you gain by showing it. Test your current product, competitors' products (free prototypes), napkin sketches ("What do you think this is supposed to be?", never "Do you like it?"), wireframes (navigation and naming), and comps (does each page read?). You're in it for the surprises. (ch04)
3. **Recruit loosely and grade on a curve.** Most serious problems don't depend on domain knowledge. Roughly match your audience, add one outsider "ringer" per round, and discount failures caused only by missing jargon. **Three per round**: more rounds beat more users. First Law: *one user is 100% better than none.* (ch05)
4. **Make it a spectator sport.** Get everyone, executives included, to watch live from a separate room. Seeing is believing: skeptics convert, and everyone learns that users aren't like them. Each observer writes their **top three problems per session**. (ch09)
5. **Focus ruthlessly on a small number of the most important problems.** You'll always have more problems than resources, and easy minor ones crowd out the worst. The same-day debrief (attendees only) distills a ranked **top ten**, works down it without skipping, and stops at this month's capacity. (ch10)
6. **When fixing problems, always do the least you can do.** Make the smallest, simplest change likely to prevent **the problem you observed**, not its inflated version ("redesign the menu system"). **Tweak, don't redesign. Take something away** before adding. Don't wait for the big redesign. (ch11)

---

## Core Techniques

**Tasks → scenarios** (ch06). Pick from 5–10 key *user goals* by criticality, worry, and support or analytics signals. Write each as a short "You are… you need to…" card with the data they need, **without the interface's own words** ("Choose the kind of music you want to listen to", not "Customize your LAUNCHcast station"). Ban search unless you're testing it. Pilot, then print one per sheet, unnumbered.

**The session** (ch08), 50 minutes: welcome read verbatim (we test the site, not you; think aloud) · a few warm-up questions · **Home page tour** ("tell me what you make of it", no clicking) · **tasks, ~35 min**, each scenario read aloud · probing (observers' questions first) · wrap-up · a 10-minute reset.

**Facilitator as therapist.** Keep them talking: **if you're not sure what they're thinking, ask** "What are you thinking?" Stay neutral: no clues, answer questions with questions ("What would you do if you were at home?"), no opinions, poker face. Save the whys for the probe. Move on when the task is done, they're miserable ("it's not a crash test"), time is short, or learning stops, after a little overtime. Participants leave in no worse shape than they came, with privacy protected.

**Severity** (ch10) = how many people × how bad. The hard calls are corner cases (rare but severe) and ubiquitous nuisances (common but minor). Keep the debate on evidence: "Did anybody in the tests have that problem?"

**Tweak loop** (ch11): simplest change → did it work? If not, the same tweak *louder*, then a different tweak, then check nothing else broke. Verify by looking at it, a hallway test, an unmoderated remote test, or an A/B test.

**Usual suspects** (ch12): **getting off on the wrong foot**, where wrong first-seconds assumptions snowball (fix Home page orientation and tour it every session), and **failure to shout**, where important things are too subtle (make them stand out more than feels right).

**Making fixes stick** (ch13): reports don't cause change. Keep commitments small, give observers a voice, and convert management by demonstration rather than ROI decks.

**Remote** (ch14): moderated remote gives ~80% of the benefit for ~70% of the effort, with easier recruiting and less control. Do about three in-person rounds first. Unmoderated services suit quick questions and fix retests but can't probe.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-what-diy-testing-is.md) | You don't see any elephants around here, do you? | testing definition, qualitative vs. quantitative, why it always works, analytics vs. testing |
| [ch02](chapters/ch02-what-a-test-looks-like.md) | I will now saw my [lovely] assistant in half | watching a demo test, top-three habit |
| [ch03](chapters/ch03-a-morning-a-month.md) | A morning a month, that's all we ask | monthly cadence, Big Honkin' Test comparison, Agile, budget |
| [ch04](chapters/ch04-what-and-when-to-test.md) | What do you test, and when do you test it? | start early, napkin test, competitor testing, wireframes, comps |
| [ch05](chapters/ch05-recruiting.md) | Recruit loosely and grade on a curve | domain knowledge, three users, where to find them, screening, incentives, standby |
| [ch06](chapters/ch06-tasks-and-scenarios.md) | Find some things for them to do | task selection, scenario writing, no clues, pilot test |
| [ch07](chapters/ch07-checklists.md) | Some boring checklists | three-week countdown, test-day setup, the recorder |
| [ch08](chapters/ch08-facilitating.md) | Mind reading made easy | tour guide/therapist, session timeline, think-aloud, neutrality phrases, ethics, tough customers |
| [ch09](chapters/ch09-observers.md) | Make it a spectator sport | seeing is believing, observer role, observation room, Hall Monitor |
| [ch10](chapters/ch10-debriefing.md) | Debriefing 101 | worst first, severity, top-ten process, short report |
| [ch11](chapters/ch11-least-you-can-do.md) | The least you can do™ | tweak don't redesign, take something away, tweak loop, verification |
| [ch12](chapters/ch12-usual-suspects.md) | The usual suspects | wrong foot, Big Bang Theory, kitchen sink, failure to shout |
| [ch13](chapters/ch13-making-life-improve.md) | Making sure life actually improves | why fixes stall, demonstration over ROI |
| [ch14](chapters/ch14-remote-testing.md) | Teleportation made easy | moderated remote, unmoderated remote, 80/70 |
| [ch15–16](chapters/ch15-16-reading-and-maxims.md) | Overachievers only / Happy trails to you | the six maxims, further reading |

## Topic Index

- **Agile / sprint cadence** → ch03, ch14
- **Analytics vs. testing** → ch01, ch06
- **Budget / cost** → ch03, ch05
- **Concept validation / discovery** → ch04, ch12
- **Competitor testing** → ch04, ch09
- **Debrief** → ch10, ch13
- **Domain knowledge** → ch05, ch08
- **Ethics / privacy / consent** → ch08, test-kit
- **Facilitation / think-aloud** → ch08
- **Fixing problems / tweaks** → ch11, ch12
- **Home page** → ch08, ch12
- **Management buy-in** → ch09, ch13
- **Observers** → ch09, ch10
- **Prioritization / severity** → ch10
- **Probing** → ch08
- **Quantitative vs. qualitative** → ch01, ch03, ch15-16
- **Recruiting / number of users** → ch05, ch14
- **Redesign** → ch10, ch11, ch13
- **Remote / unmoderated testing** → ch14, ch11
- **Scenarios / tasks** → ch06
- **Scheduling / logistics** → ch03, ch07
- **Test script** → ch08, test-kit
- **Wireframes / comps / prototypes** → ch04

## Supporting Files

- [cheatsheet.md](cheatsheet.md): **start here while planning or reviewing**. Defaults and thresholds, if-then decision rules, tells and smells.
- [test-kit.md](test-kit.md): adaptable invitation, screener, scenario template, facilitator script, neutral phrases, consent form, observer sheet, debrief agenda, summary email.
- [patterns.md](patterns.md): 18 named techniques, each with when, how, and trade-offs.
- [glossary.md](glossary.md): every term with a one-line definition and chapter.

---

## Scope & Limits

This skill covers the book's method only: **evaluative, qualitative, small-sample usability testing**. For discovery it covers testing concepts early (napkin tests, competitor tests, wireframes). It does **not** cover generative research such as user interviews, contextual inquiry, surveys, or jobs-to-be-done. Krug explicitly contrasts testing with opinion-gathering methods. Say so when a question needs those methods, and don't stretch the book to cover them.

Not for proving things (benchmarks, statistical comparisons) or for safety-critical systems. Both need rigorous quantitative studies.

The book is from 2009 and web-focused. Tool names (Camtasia, GoToMeeting, Google Website Optimizer) and dollar figures are dated; the method and ratios still hold. Krug says it applies to anything people use (apps, forms, devices, documents). Substitute "first screen" for "Home page" where needed. Screenshots and cartoons in the source (about 100 images) were not read, except the maxims, comparison tables, neutrality chart, and tweak flowchart, which were transcribed.
