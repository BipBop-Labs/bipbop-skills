# Chapter 3: A morning a month, that's all we ask

## Core Idea
Most people skip testing because they picture a Big Honkin' Test. The replacement is a fixed routine: **one morning a month, three users, then debrief over lunch.** By early afternoon you know what you'll fix before next month.

## Frameworks Introduced
- **Maxim: "A morning a month, that's all we ask."**
  - **Morning**: capping testing at half a day means three users. That makes recruiting simple and lets more people come and watch.
  - **Month**: about as often as most teams can afford, and it finds enough problems to keep them busy fixing until the next round.
- **Make it a fixed date** (e.g., "the third Thursday of each month"). A routine removes the *decision* about when to test. You test whatever is ready that day. "If you have to think about when you're going to test, you're not going to end up testing as often."
- **Big Honkin' Test vs. DIY testing**:

| | Big Honkin' Test | Do-it-yourself |
|---|---|---|
| Time per round | 1–2 days of tests, a week to prepare a briefing, then a process to decide what to fix | One morning: testing, debrief, and deciding what to fix |
| When | When the site is nearly complete | Continually, throughout development |
| Rounds | 1–2 per project (time, expense) | One every month |
| Participants per round | 5–8, sometimes 10 to convince a skeptical manager | Three |
| Who | Recruited carefully to match the target audience | Recruited loosely; frequency matters more than "actual" users |
| Where | Off-site rented facility, one-way mirror | On-site, observers in any conference room via screen sharing |
| Who watches | Few people, because it's 2–3 days off-site | Many people, because it's half a day on-site |
| Reporting | Someone spends ≥1 week on a briefing | A 1–2 page email of the decisions made in the debrief |
| Who identifies problems | The person running the tests | The whole team and stakeholders, over lunch, same day |
| Primary purpose | A long list (sometimes hundreds) of problems, categorized by severity | A short list of the most serious problems plus a commitment to fix them before next round |
| Record participant's face | Yes (to show frustration) | No. Screen plus clear audio is enough |
| Out-of-pocket cost | $5,000–$15,000 per round if outsourced | A few hundred dollars per round |

- **Budget (the book's 2009 figures; the proportions are what matter)**: roughly $4,000–$6,000 a year for a standard program (microphone, speakers, screen recorder, screen-sharing subscription, snacks and lunch around $100 a month, incentives of $50–$100 × 36 participants). A no-frills version with free tools, mugs or T-shirts instead of cash, and ~$25 gift cards comes to ~$1,250–$2,150 a year. **Incentives and food dominate the cost.**

## Key Concepts
- **Round**: one testing morning of three sessions plus the debrief.
- **Prep time**: the organizer needs 2–3 full days for the first round and 1–2 days for later ones (tasks, scenarios, recruiting, rounding up observers). For everyone else the cost really is a morning.

## Mental Models
- **A morning a month is the minimum, not the target.** Test more often if you can, but *never less*. Once the fixed date slips, you're back to deciding, and the odds of testing "drop dramatically."
- **Agile: "a morning a sprint."** Keep rounds leaner (two users instead of three), use remote testing for some rounds (ch14), and expect to test **last sprint's working code and a paper prototype of next sprint's work** in the same round, because you have to lay track ahead of the developers.
- **Evening variant**: if participants can't come during work hours, run sessions at 6, 7, and 8 pm with dinner for observers and debrief the next morning. The rule is **all sessions in one half-day, and debrief while it's fresh.**

## Anti-patterns
- **The Big Honkin' Test as the default.** It's expensive, late, rare, and watched by few people.
- **Testing "when we're ready".** That turns into never, or once at the end.
- **Arguing statistics.** The scripted answer to "three users can't be statistically valid" is: "You're absolutely right… But the point of this kind of testing isn't to prove anything; the point is to identify major problems and make the thing better by fixing them. It just works, because most of the kinds of problems that need to be fixed are so obvious that there's no need for 'proof.'" Say it "with a lot of conviction and a friendly smile."

## Key Takeaways
1. Put a recurring testing day on the calendar and announce it.
2. Three users in the morning, debrief at lunch, done by early afternoon.
3. Test whatever exists on testing day. The routine drives readiness.
4. Monthly is the floor. In Agile, do a round per sprint with fewer users.
5. The out-of-pocket cost is small, mostly incentives and food.
6. Don't defend the sample size with statistics. Defend it with the purpose.

## Connects To
- **Ch 5**: why three users is enough.
- **Ch 7**: the week-by-week checklist behind the "morning".
- **Ch 10**: the lunch debrief.
- **Ch 14**: remote rounds for Agile cadence.
