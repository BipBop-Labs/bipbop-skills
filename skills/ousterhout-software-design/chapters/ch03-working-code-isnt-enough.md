# Chapter 3: Working Code Isn't Enough (Strategic vs. Tactical Programming)

## Core Idea
Working code is the floor, not the goal: your primary goal must be a great design that also happens to work, funded by a continuous 10–20% investment of development time.

## Frameworks Introduced
- **Tactical programming** — the default, and the thing to avoid.
  - Shape: focus is getting a feature or fix working as fast as possible. Planning for the future isn't a priority. Small kludges seem like reasonable trades. Complexity compounds; refactoring keeps losing to the next feature; eventually cleanup would take months and never happens.
  - Failure mode: it is self-reinforcing. "Once you start down the tactical path, it's difficult to change."
- **Strategic programming** — the alternative.
  - Definition: your primary goal is to produce a great design, which also happens to work.
  - Rationale: most code in any system is written by extending existing code, so your most important job is facilitating future extensions.
  - How: an **investment mindset**, in two forms:
    - **Proactive** — take extra time to find a simple design for each new class; try a couple of alternatives and pick the cleanest; imagine future changes and check your design accommodates them; write good documentation.
    - **Reactive** — when you discover a design mistake (and you will), fix it rather than ignoring or patching around it.
- **How much to invest: 10–20% of total development time.**
  - Small enough not to wreck schedules, large enough to compound.
  - The payback curve: initial projects take 10–20% longer; benefits appear within a few months; before long you're moving 10–20% *faster*, at which point the investments are free — past investments fund future ones.
  - The tactical mirror image: 10–20% faster at first, then progressively slower as complexity accrues. Anyone who has worked in a badly degraded code base will tell you poor quality costs at least 20%.

## Key Concepts
- **Investment mindset**: deliberately spending time now to improve design, accepting short-term slowdown for long-term speed.
- **Tactical tornado**: the prolific programmer who ships features faster than anyone while working entirely tactically. Sometimes treated as a hero by management; leaves a wake of destruction. The engineers cleaning up after them are the real heroes, and they look slower.
- **Zero tolerance**: refusing to let small complexities in, because complexity is incremental (Ch 2).

## Mental Models
- **"Working code isn't enough."** Introducing unnecessary complexity to finish faster is not an acceptable trade.
- **Think of investment as something to do today, not tomorrow.** When you hit a crunch it's tempting to defer cleanup until after — but there is always another crunch. Deferral becomes permanent, and the culture slides tactical.
- **Design debt grows scarier as it grows.** The longer you wait, the bigger the problem and the more intimidating the fix, which makes deferring it even easier. Small and continuous beats large and heroic.

## Worked Example — startups, and the two paths
The strongest force against strategic programming is early-stage startup pressure, where even 10–20% seems unaffordable. The rationalization: if we succeed, we'll hire engineers to clean it up later. Ousterhout's rebuttal, three parts:

1. **Spaghetti is nearly unfixable.** Once a code base turns, you pay high development costs for the life of the product.
2. **The payoff is fast enough that tactical may not even win the first release.**
3. **It poisons hiring** — the best engineers care deeply about good design. Word gets out about a wrecked code base, you end up with mediocre engineers, and the structure degrades further.

**Facebook** — motto "Move fast and break things." New grads pushed to production in week one. Genuinely empowering, and the company was spectacularly successful. But the code base suffered: unstable, hard to understand, few comments or tests, painful to work with. The culture proved unsustainable and the motto became "Move fast with solid infrastructure." (Ousterhout notes Facebook's code probably wasn't worse than the startup average — just more visible.)

**Google and VMware** — same era, strategic approach, heavy emphasis on code quality and design. Both built sophisticated, reliable systems, and their technical cultures became well known enough that few competitors could win the top talent.

Conclusion: a company can succeed either way — but it's far better to work somewhere with a clean code base.

## Key Takeaways
1. Make a great design your primary goal; working code is a constraint, not the objective.
2. Budget 10–20% of development time for design investment, continuously.
3. Invest proactively (try alternative designs, document) and reactively (fix design mistakes when found).
4. Never defer cleanup to "after the crunch" — the deferral becomes permanent.
5. Don't reward tactical tornadoes; the cleanup cost is real but invisible in feature velocity.
6. Big up-front design is not the alternative to tactical work — that's waterfall. Many small continuous investments are.
7. The most effective approach requires *every* engineer investing continuously, not a designated cleanup crew.

## Connects To
- **Ch 2**: complexity is incremental — the reason zero tolerance and continuous investment are the right response.
- **Ch 11**: "Design it Twice" — the highest-leverage proactive investment.
- **Ch 16**: "Modifying Existing Code" — staying strategic while changing code you didn't write.
- **Ch 19**: how agile can drift tactical when increments are features rather than abstractions.
