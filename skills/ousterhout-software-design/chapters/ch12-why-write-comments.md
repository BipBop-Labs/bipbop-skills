# Chapter 12: Why Write Comments? The Four Excuses

## Core Idea
Comments capture information that was in the designer's mind but couldn't be represented in the code — and without them you cannot have abstraction at all, because a reader forced into your implementation sees all of its complexity.

## Frameworks Introduced
- **The purpose of comments, stated precisely**: *"to capture information that was in the mind of the designer but couldn't be represented in the code."* This spans low-level details (a hardware quirk motivating a tricky piece of code) up to high-level concepts (the rationale for a class).
- **The three roles of documentation** (the chapter's opening claims):
  1. Helping developers understand a system and work efficiently.
  2. **Enabling abstraction** — "without comments, you can't hide complexity."
  3. **Improving the design itself** — the process of writing comments, done correctly, improves the system's design (developed in Ch 15).
  - Converse: "a good software design loses much of its value if it is poorly documented."
- **The four excuses, and their answers** — the body of the chapter:

| Excuse | Answer |
|---|---|
| "Good code is self-documenting" | A "delicious myth, like a rumor that ice cream is good for your health." Only a small part of an interface (signatures) can be specified in code. The informal aspects can't be. |
| "I don't have time to write comments" | The investment mindset (Ch 3), plus arithmetic: ~10% of development time at most. |
| "Comments get out of date and become misleading" | True but manageable; large doc changes only follow large code changes, which cost more anyway. |
| "All the comments I have seen are worthless" | "Probably the one with the most merit" — and solvable, which is what Ch 13–16 are for. |

- **The 10% argument (§12.2), in full.** Ask what fraction of your development time you spend *typing code* — as opposed to designing, compiling, testing. "I doubt that the answer is more than 10%." Now assume you spend **as much time typing comments as typing code** — a safe upper bound. So good comments add **at most about 10%** to development time, which the maintainability benefit offsets quickly.
  - And the most important comments — top-level documentation for classes and methods — should be written **as part of the design process** (Ch 15), where they serve as a design tool. **"These comments pay for themselves immediately."**
- **Why comments are fundamental to abstraction (§12.1)** — the chapter's strongest argument:
  - An abstraction preserves essential information and omits details that can safely be ignored. **"If users must read the code of a method in order to use it, then there is no abstraction: all of the complexity of the method is exposed."**
  - Without comments, a method's only abstraction is its **declaration** — name, argument names and types, result type — and that is missing too much to be useful. Concretely: for a substring method with `start` and `end`, the declaration cannot tell you **whether the character at `end` is included, or what happens if `start > end`.**
  - Comments being in a **human language** is a feature: less precise than code, but with more expressive power, so you can write simple intuitive descriptions.
- **How documentation attacks complexity** (mapping back to Ch 2). Good documentation helps with **two of the three symptoms**:
  - **Cognitive load** — it supplies the information needed to make a change and lets developers **ignore what's irrelevant**; without it they must read large amounts of code to reconstruct the designer's mind.
  - **Unknown unknowns** — it clarifies the system's structure so it's clear what code and information matter for a given change.
  - (It does not directly help with change amplification.) On causes: documentation **clarifies dependencies** and **fills gaps to eliminate obscurity.**

## Key Concepts
- **Self-documenting code** (the myth): the belief that well-written code needs no comments.
- **Informal interface aspects**: high-level behavior, meaning of results, calling constraints, design rationale — expressible only in comments.

## Anti-patterns
- **"Just read the code of the method."** Three problems: (1) deducing the abstract interface from an implementation is possible but "time-consuming and painful"; (2) if you *write* code expecting readers to read implementations, you'll make every method as short as possible and break up anything nontrivial — **producing a large number of shallow methods** (Ch 4); and (3) it doesn't even work — to understand the top-level method, readers must understand the nested ones. For large systems it isn't practical.
- **De-prioritizing comments against features.** "Software projects are almost always under time pressure, and there will always be things that seem higher priority than writing comments. Thus, if you allow documentation to be de-prioritized, you'll end up with no documentation."
- **Treating comments as drudge work.** Even on teams that encourage documentation, this plus not knowing how to write them yields mediocre docs, which "creates a huge and unnecessary drag on software development."

## Key Takeaways
1. Write comments to record what was in your head and couldn't go in the code — rationale, informal behavior, calling constraints.
2. There is no abstraction without comments; a declaration alone under-specifies the contract.
3. Good variable names reduce the need for comments but cannot replace them.
4. "Read the code" isn't an alternative — and designing *for* it pushes you toward shallow methods.
5. Budget roughly 10% of development time; interface comments written during design pay back immediately.
6. Comments do go stale, but proportionally to code churn — and code review catches it.
7. Documentation reduces cognitive load and unknown unknowns, clarifies dependencies, and removes obscurity.
8. Comments are valuable even when you're the only maintainer: "if it has been more than a few weeks since you last worked in a piece of code, you will have forgotten many of the details of the original design."

## Connects To
- **Ch 2**: the symptoms and causes documentation addresses.
- **Ch 3**: the investment mindset answering "no time."
- **Ch 4**: the informal parts of an interface are the larger part, and are comments.
- **Ch 13**: how to write comments that aren't worthless.
- **Ch 14**: choosing names — the legitimate part of "self-documenting."
- **Ch 15**: writing comments first, as a design tool.
- **Ch 16**: organizing documentation so it stays current (avoid duplication, keep it near the code).
