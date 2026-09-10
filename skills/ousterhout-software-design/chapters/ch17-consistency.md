# Chapter 17: Consistency

## Core Idea
Consistency means **similar things are done in similar ways and dissimilar things are done in different ways** — it creates cognitive leverage, letting a reader apply what they learned in one place everywhere else.

## Frameworks Introduced
- **The two benefits of consistency:**
  1. **Cognitive leverage** — "once you have learned how something is done in one place, you can use that knowledge to immediately understand other places that use the same approach." Without it, developers must learn each situation separately.
  2. **Fewer mistakes** — in an inconsistent system, "two situations may appear the same when in fact they are different," so a developer sees a familiar-looking pattern and makes incorrect assumptions. In a consistent system, **assumptions made from familiar-looking situations are safe.**
- **The five levels consistency applies at (§17.1):**
  1. **Names** (Ch 14).
  2. **Coding style** — style guides restricting program structure beyond what compilers enforce: indentation, curly-brace placement, order of declarations, naming, commenting, and restrictions on language features considered dangerous. They "make code easier to read and can reduce some kinds of errors."
  3. **Interfaces** — an interface with multiple implementations. "Once you understand one implementation of the interface, any other implementation becomes easier to understand because you already know the features it will have to provide."
  4. **Design patterns** — generally-accepted solutions to common problems, e.g. model-view-controller for UI. Using an existing pattern means the implementation proceeds more quickly, is more likely to work, and is more obvious to readers. (Tempered in Ch 19.5.)
  5. **Invariants** — "a property of a variable or structure that is always true," e.g. a text data structure enforcing that every line ends with a newline. **"Invariants reduce the number of special cases that must be considered in code and make it easier to reason about the code's behavior."**
- **The four techniques for ensuring consistency (§17.2).** The problem is real: "People in one group may not know about conventions established in another group. Newcomers don't know the rules, so they unintentionally violate the conventions and create new conventions that conflict with existing ones."
  1. **Document.** A document listing the most important overall conventions, **placed somewhere developers will actually see it** — a conspicuous place on the project wiki. Have new people read it and existing people review it occasionally; consider starting from a published style guide. For localized conventions like invariants, **find an appropriate spot in the code.** "If you don't write the conventions down, it's unlikely that other people will follow them."
  2. **Enforce.** "Even with good documentation, it's hard for developers to remember all of the conventions. **The best way to enforce conventions is to write a tool that checks for violations, and make sure that code cannot be committed to the repository unless it passes the checker.**" Automated checkers work particularly well for low-level syntactic conventions.
  3. **Code reviews** — "another opportunity for enforcing conventions and for educating new developers." Note the deliberately counterintuitive advice: **"The more nit-picky that code reviewers are, the more quickly everyone on the team will learn the conventions, and the cleaner the code will be."**
  4. **"When in Rome, do as the Romans do"** — "the most important convention of all." When working in a new file, look around at how the existing code is structured: Are public variables and methods declared before private ones? Are methods in alphabetical order? Is it `firstServerName` (camel case) or `first_server_name` (snake case)? **"When you see anything that looks like it might possibly be a convention, follow it."** And when making a design decision, ask whether a similar decision was likely made elsewhere in the project; if so, find the existing example and use the same approach.
- **Don't change existing conventions.** "Resist the urge to 'improve' on existing conventions. Having a 'better idea' is not a sufficient excuse to introduce inconsistencies. **Your new idea may indeed be better, but the value of consistency over inconsistency is almost always greater than the value of one approach over another.**"
  - **The two-question gate** before introducing inconsistent behavior:
    1. **Do you have significant new information** justifying your approach that wasn't available when the old convention was established?
    2. **Is the new approach so much better that it's worth taking the time to update all of the old uses?**
  - If **your organization** agrees both answers are yes, make the upgrade — and **"when you are done, there should be no sign of the old convention."** Even then you risk other developers not knowing about the new convention and reintroducing the old approach later.
  - The blunt summary: **"reconsidering established conventions is rarely a good use of developer time."**

## Key Concepts
- **Cognitive leverage**: knowledge acquired once applying safely in many places.
- **Invariant**: a property of a variable or structure that is always true.
- **Automated checker**: a pre-commit tool that makes a convention unbreakable rather than merely documented.

## Anti-patterns
- **"I have a better idea"** as grounds for a new convention — see the two-question gate.
- **Overzealous consistency** — see "Taking it too far."
- **Undocumented conventions**, which newcomers can neither follow nor discover.
- **Documented-but-unenforced conventions**, which decay as the team grows.

## Worked Example — the line-terminator problem, and why documenting wasn't enough
This is the chapter's best illustration of why *enforce* beats *document*.

**The problem.** Some developers worked on Unix (lines end with a newline), others on Windows (carriage return + newline). "If a developer on one system made a small edit to a file previously edited on the other system, the editor would sometimes replace all of the line terminators with ones appropriate for that system." The consequence: **every line of the file appeared modified, which made it hard to track the meaningful changes.**

**Step 1 — a convention.** They established that files should contain newlines only. It didn't work: **"it was hard to ensure that every tool used by every developer followed the convention."** And it kept recurring — **"every time a new developer joined the project, we would experience a rash of line termination problems while that developer adjusted to the convention."**

**Step 2 — a checker.** They wrote a short script run automatically before commits. It checks all modified files and **aborts the commit if any contain carriage returns.** It can also be run manually to *repair* damaged files by replacing CR/NL sequences with newlines.

**The result:** "This **instantly eliminated the problems**, and it also **helped train new developers.**"

Two lessons worth extracting. First, the enforcement point matters — a pre-commit hook makes the convention structurally unbreakable, rather than depending on every developer's tool configuration. Second, **the checker doubled as documentation and onboarding**: it teaches the convention at exactly the moment a newcomer violates it, which no wiki page can do.

## Key Takeaways
1. Consistency lets a reader reuse knowledge; inconsistency forces relearning and invites false assumptions.
2. Apply it to names, style, interfaces, patterns, and invariants.
3. Invariants are a consistency tool that directly removes special cases.
4. Write conventions down where developers will see them, and put localized ones (invariants) in the code.
5. Automate enforcement — a pre-commit checker beats documentation, and trains newcomers as a side effect.
6. Be nit-picky in code review; it's the fastest way to propagate conventions.
7. Follow whatever looks like a convention in an unfamiliar file, and look for existing precedent before making a design decision.
8. Don't replace a convention on the strength of a better idea alone; require new information *and* the willingness to migrate every old use.
9. **Taking it too far (§17.3)**: consistency means dissimilar things should be done *differently*. "If you become overzealous about consistency and try to force dissimilar things into the same approach, such as by using the same variable name for things that are really different or using an existing design pattern for a task that doesn't fit the pattern, you'll create complexity and confusion." **"Consistency only provides benefits when developers have confidence that 'if it looks like an x, it really is an x.'"**
10. This is the investment mindset again: work to decide conventions, build checkers, find situations to mimic, and educate in review — repaid by code that is more obvious and faster to work in with fewer bugs.

## Connects To
- **Ch 2**: inconsistency is a major contributor to obscurity, and obscurity causes unknown unknowns.
- **Ch 3**: consistency as continuous investment.
- **Ch 10**: invariants remove special cases — the same goal as defining errors out of existence.
- **Ch 14**: consistent naming, including the `block` bug that came from violating it.
- **Ch 16**: code reviews as the shared enforcement mechanism.
- **Ch 18**: consistency is one of the two most important techniques for making code obvious.
- **Ch 19.5**: the more skeptical treatment of design patterns.
