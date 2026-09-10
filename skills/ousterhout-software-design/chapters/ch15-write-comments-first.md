# Chapter 15: Write The Comments First (Use Comments As Part Of The Design Process)

## Core Idea
Write comments at the very beginning, before the code — not to document better (though it does), but because **comments are the only way to fully capture abstractions, so writing them early lets you review and tune your design before implementing it.**

## Frameworks Introduced
- **The comments-first workflow (§15.2)**, in order:
  1. For a new class, **write the class interface comment first.**
  2. Write **interface comments and signatures for the most important public methods** — leaving the **method bodies empty.**
  3. **Iterate over these comments until the basic structure feels about right.**
  4. Write **declarations and comments for the most important instance variables.**
  5. **Fill in the method bodies**, adding implementation comments as needed.
  6. While writing bodies you'll discover the need for more methods and variables. **For each new method, write the interface comment before the body**; for each variable, write the comment at the same time as the declaration.
  - The payoff: **"When the code is done, the comments are also done. There is never a backlog of unwritten comments."**
- **Comments as a design tool (§15.3)** — the most important benefit.
  - Why it works: comments are the only way to fully capture abstractions, and good abstractions are fundamental to good design. Writing them first lets you **review and tune the abstractions before writing implementation code.**
  - "To write a good comment, you must identify the essence of a variable or piece of code: what are the most important aspects of this thing? **It's important to do this early in the design process; otherwise you are just hacking code.**"
- **Comments as a complexity meter** — "a canary in the coal mine of complexity." Three concrete diagnostics:
  - **Interface complexity:** "The best way to judge the complexity of an interface is from the comments that describe it." Short, simple, *and* complete → simple interface. No way to describe it completely without a long complicated comment → complex interface.
  - **Depth:** **compare the interface comment against the implementation.** "If the interface comment must describe all the major features of the implementation, then the method is shallow."
  - **Variable decomposition:** "if it takes a long comment to fully describe a variable, it's a red flag that suggests you may not have chosen the right variable decomposition."
  - The caveat that keeps the meter honest: comments only indicate complexity **if they are complete and clear.** An interface comment that omits information needed to invoke the method, or is cryptic, "doesn't provide a good measure of the method's depth."
- **Write the interface comment before each method body** specifically "so you can focus on the method's abstraction and interface without being distracted by its implementation."

## Key Concepts
- **Comments-first**: writing interface documentation as the design step, before implementation.
- **Canary in the coal mine**: a long or awkward comment as an early warning of a bad abstraction.

## Anti-patterns
- **Red Flag — Hard to Describe**: "The comment that describes a method or variable should be simple and yet complete. If you find it difficult to write such a comment, that's an indicator that there may be a problem with the design of the thing you are describing."
- **Delaying documentation until after coding and unit testing** — "one of the surest ways to produce poor quality documentation." The failure chain (§15.1):
  - **The stated reason** ("the code is still changing, I'd have to rewrite the comments") plus the **suspected real reason**: developers view documentation as drudge work, so they defer it as long as possible.
  - **Delay compounds into never.** "Once you start delaying, it's easy to delay a bit more; after all, the code will be even more stable in a few more weeks." By the time it's inarguably stable there's a lot of it, so the task is huge and even less attractive. There's never a convenient time to stop for a few days, and it's easy to rationalize moving on to bugs or features — creating still more undocumented code.
  - **Even with the discipline to go back** ("and don't fool yourself: you probably don't"), the comments are bad, for four specific reasons:
    1. **You've checked out mentally** — the code is done in your mind and you want to move on. You want to get through it as fast as possible, adding "just enough comments to look respectable."
    2. **Your memory of the design has gone fuzzy.**
    3. **You look at the code while commenting, so the comments repeat the code.**
    4. **The things you don't remember are missing** — "thus, the comments are missing some of the most important things they should describe."

## Worked Example — the cost argument, settled with arithmetic (§15.5)
The case for delaying is avoiding rework as the code evolves. Ousterhout's back-of-the-envelope:

- Total development time spent **typing code and comments together**, including revisions: **unlikely to be more than ~10%.**
- Even if **half your lines are comments**, writing comments is **no more than ~5% of total development time.**
- Delaying saves only **a fraction of that 5%** — "which isn't very much."

Then the argument reverses. Writing comments first means **the abstractions are more stable before you start coding**, which probably *saves* time during coding. Write the code first and the abstractions evolve as you go, requiring **more code revisions** than the comments-first approach. "When you consider all of these factors, **it's possible that it might be faster overall to write the comments first.**"

## Worked Example — why early comments are fun (§15.4)
This is the chapter's third benefit and it's more than a pleasantry — it describes what design work actually feels like when done this way.

"One of the most enjoyable parts of programming is the early design phase for a new class, where I'm fleshing out the abstractions and structure for the class. Most of my comments are written during this phase, and **the comments are how I record and test the quality of my design decisions.**"

The concrete aesthetic goal: **"I'm looking for the design that can be expressed completely and clearly in the fewest words. The simpler the comments, the better I feel about my design, so finding simple comments is a source of pride."**

And the link back to Ch 3: **"If you are programming strategically, where your main goal is a great design rather than just writing code that works, then writing comments should be fun, since that's how you identify the best designs."** Under tactical programming, comments are overhead on already-finished work; under strategic programming, they *are* the design work.

## Key Takeaways
1. Write the class interface comment first, then method interface comments and signatures with empty bodies, and iterate before implementing.
2. Never let a backlog of unwritten comments accumulate — finish comments with the code.
3. Use the interface comment to judge interface complexity: short, simple, and complete means a simple interface.
4. Compare interface comment to implementation to measure depth; if the comment must describe the implementation's major features, the method is shallow.
5. A long comment for a variable means the wrong variable decomposition.
6. Difficulty writing a simple-yet-complete comment is a design problem, not a writing problem.
7. Deferred comments are worse comments — written from the code, from fading memory, by someone who has mentally moved on.
8. Comments cost ~5% of development time; writing them first may actually be net faster because it stabilizes abstractions before coding.
9. "If you haven't ever tried writing the comments first, give it a try. Stick with it long enough to get used to it."

## Connects To
- **Ch 3**: strategic programming — comments-first is what design-as-you-go looks like in practice.
- **Ch 4**: depth; the interface-vs-implementation comment comparison operationalizes it.
- **Ch 11**: design it twice — iterating over interface comments *is* a cheap way to compare alternatives.
- **Ch 12–13**: why comments matter and how to write them; this chapter is *when*.
- **Ch 14**: the Hard to Pick Name red flag is the naming counterpart to Hard to Describe.
- **Ch 16**: keeping the comments current once the code starts changing.
