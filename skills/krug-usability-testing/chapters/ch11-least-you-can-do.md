# Chapter 11: The least you can do™

## Core Idea
When fixing a problem, **do the least you can do**: the smallest, simplest change likely to keep people from having **the problem you observed**. Tweak, don't redesign. Often the best tweak is to take something away.

## Frameworks Introduced
- **Maxim: "When fixing problems, always do the least you can do™."**
- **The governing question**: "What's the smallest, simplest change we can make that's likely to keep people from having the problem we observed?"
  - Note the wording: *the problem we observed*, not *the problem*. Observed problems get inflated: "He had trouble with that menu" becomes "We need to redesign our menu system."
- **Five objections to doing little, and the answers**:
  - *"If we fix it, let's do it right."* The perfect is the enemy of the good. The goal is "make it better for our users right now," not "eliminate the problem." You can keep working on the perfect fix afterwards.
  - *"It's a core problem, so there's no easy fix."* You may not reach the root cause soon, but you can almost always **mitigate the impact**, even if it's lipstick on the pig.
  - *"It'll change soon anyway."* **Don't wait for a redesign to fix serious problems.** The duplicated effort is small because the fix is small. (Krug's kitchen: he lived with ugly countertops for ten years waiting to renovate "soon", when $1,000 of stopgap would have bought a decade of better life.)
  - *"It'll feel like a kludge."* Duct tape over a hole in your pants beats a hole.
  - *"We don't have time."* For the worst problems you always have time to do *something*.
- **Principle 1: Tweak, don't redesign.** Nine reasons tweaks win: they cost less; need less work; don't "ruin lives, break up families, and wreck careers"; ship sooner; are more likely to actually ship; are less likely to break things that work; users dislike change; redesigns bundle many risky changes at once; and redesigns mean many people in many meetings.
  - **What a tweak is**: a slight adjustment, often needing a few rounds of trial and error. On the web that usually means changing **size, position, appearance, or wording**, or moving things around.
- **The tweak loop**:
  1. Pick the simplest change you think might fix it for most people, and make it.
  2. Did it fix the problem? If yes, **make sure you haven't broken anything else**, and you're done.
  3. If not, and you still believe in this tweak, **try the same tweak "louder"** (a bit bigger, bolder, higher). Repeat until it feels done or clearly won't work.
  4. If you no longer believe in it, **try a different tweak** before considering a redesign.
- **Principle 2: Take something away.** The instinct is to *add*: more instructions, more text, more color. But the real problem is often **too much already there**, the noise that hides what users need. Question every impulse to add. (Saint-Exupéry: perfection is reached "when there is nothing left to take away.")

## Verifying tweaks
Retesting is less necessary than Krug once thought ("Tweak, but verify"). Usually one look shows whether the tweak solves it. If you're unsure:
- **Hallway test**: grab almost anyone, give them the affected scenario (or a narrowed version), and have them think aloud.
- **Unmoderated remote test** (ch14): submit the tweaked URL and the task, and pay for one or two users.
- **A/B test** of the original vs. the tweaked version, measuring who reaches the target.
- After a major change or many small ones, **include the task again in next month's round**.

## Key Concepts
- **Tweak**: a small adjustment to size, position, appearance, or wording, iterated.
- **Louder**: a stronger version of the same tweak.
- **Unintended consequences**: "if it ain't broke, don't break it."

## Mental Models
- **Fix the observed problem, not its inflated abstraction.**
- **Subtraction before addition.**
- **Continuous, phased redesign beats wholesale redesign.** Jared Spool claims he's never seen a major redesign that worked. Redesign isn't forbidden, but all-at-once rebuilds are a "maybe" at best.

## Anti-patterns
- Turning one observed stumble into a redesign project.
- Adding explanatory text to fix confusion caused by clutter.
- Waiting for the next big release.
- Declaring a problem "core" and therefore untouchable.
- Tweaking without checking for side effects.

## Worked Example: a missed left-hand navigation
Observed: two of three participants never noticed the section navigation on the left.
- Tempting response: "Redesign the navigation system."
- Least you can do: increase the nav's contrast and give it a clear heading, **and remove** the promotional box above it that competed for attention.
- Check: does it now look noticeable? If unsure, hallway-test the same scenario with one or two people. If it's still missed, make it *louder* (a larger heading, a background tint). If that still fails, try a different tweak, such as moving it. Then confirm nothing else on the page broke.

## Key Takeaways
1. Ask for the smallest, simplest change that prevents *the observed* problem.
2. Don't let perfect, "core", "redesign soon", "kludge", or "no time" block a mitigation.
3. Tweak (size, position, look, wording) and iterate louder before trying something different.
4. Try taking something away before adding anything.
5. Always check for collateral damage.
6. Verify cheaply with a look, a hallway test, a remote test, or A/B.

## Connects To
- **Ch 10**: each top-ten item gets a "least you can do" fix.
- **Ch 12**: "failure to shout" is the classic case where *louder* is the fix.
- **Ch 14**: unmoderated remote tests as quick retests.
