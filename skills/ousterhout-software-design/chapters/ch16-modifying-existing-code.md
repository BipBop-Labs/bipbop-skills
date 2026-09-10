# Chapter 16: Modifying Existing Code

## Core Idea
A mature system's design is determined more by the changes made during its evolution than by any initial conception — so every modification must leave the system with **the structure it would have had if you had designed it from the start with that change in mind.**

## Frameworks Introduced
- **Stay strategic while modifying (§16.1).**
  - **The goal, stated precisely:** "Ideally, when you have finished with each change, the system will have the structure it would have had if you had designed it from the start with that change in mind."
  - **How:** resist the quick fix. Ask whether the current design is still the best one *in light of the desired change*. If not, refactor so you end up with the best possible design. "With this approach, **the system design improves with every modification.**"
  - **Even when no refactoring is required**, stay on the lookout for design imperfections you can fix while you're in the code. **"Whenever you modify any code, try to find a way to improve the system design at least a little bit in the process. If you're not making the design better, you are probably making it worse."**
- **The commercial-reality escape hatch, and how to use it honestly.** Ousterhout concedes the constraints: if the right refactoring takes three months and a quick fix takes two hours, you may have to take the quick fix under a tight deadline; if refactoring would create incompatibilities affecting many other people and teams, it may not be practical.
  - But: **"you should resist these compromises as much as possible."** The question to ask is *"Is this the best I can possibly do to create a clean system design, given my current constraints?"*
  - Two concrete moves: look for **an alternative that's almost as clean as the 3-month refactoring but takes a couple of days**; or if you can't do it now, **get your boss to allocate time to come back to it after the deadline.**
  - Organizational version: "Every development organization should plan to spend a small fraction of its total effort on cleanup and refactoring; this work will pay for itself over the long run."
- **Keep comments near the code (§16.2).** "The best way to ensure that comments get updated is to position them close to the code they describe, so developers will see them when they change the code. **The farther a comment is from its associated code, the less likely it is that it will be updated properly.**"
  - **The concrete recommendation, which is contrarian:** for C/C++, put a method's interface comment **next to the method body in the code file, not next to the declaration in the `.h` file.** The header is a long way from the code — developers won't see those comments when modifying the body, and it takes extra work to open another file and find them.
  - **The rebuttal to "but users need to read the header":** *"users should not need to read either code or header files; they should get their information from documentation compiled by tools such as Doxygen or Javadoc."* Many IDEs also extract and display documentation as you type a method name. **"Given tools such as these, the documentation should be located in the place that is most convenient for developers working on the code."**
  - **For implementation comments:** don't stack them all at the top of the method. **"Spread them out, pushing each comment down to the narrowest scope that includes all of the code referred to by the comment."** A three-phase method gets a comment just above the first line of each phase — not one big comment describing all three in detail.
  - **But a strategy comment at the top can still help:**
    ```
    // We proceed in three phases:
    // Phase 1: Find feasible candidates
    // Phase 2: Assign each candidate a score
    // Phase 3: Choose the best, and remove it
    ```
    with details documented above each phase's code.
  - **The governing rule:** *"In general, the farther a comment is from the code it describes, the more abstract it should be"* — which reduces the chance code changes invalidate it.
- **Comments belong in the code, not the commit log (§16.3).** A common mistake is putting detailed information about a change in the commit message and not in the code. Commit messages *can* be browsed, "but a developer who needs the information is unlikely to think of scanning the repository log. Even if they do scan the log, it will be tedious to find the right log message."
  - **The test:** "When writing a commit message, ask yourself whether developers will need to use that information in the future. If so, then document this information in the code."
  - **The concrete danger:** a commit message describing a subtle problem that motivated a change. If it isn't in the code, "a developer might come along later and **undo the change without realizing that they have re-created a bug.**"
  - Duplicating it in the commit message too is fine; getting it in the code is the important part. The principle: **put documentation where developers are most likely to see it, and "the commit log is rarely that place."**
- **Avoid duplication (§16.4).** "Try to document each design decision exactly once." If several places are affected by one decision, don't repeat the documentation at each — **find the most obvious single place.** For tricky behavior tied to a variable, the comment next to the variable's declaration is the natural spot developers will check.
  - **When there's no obvious place:** create a `designNotes` file (Ch 13.7), or pick the best available place and add **short pointers** elsewhere: `"See the comment in xyz for an explanation of the code below."`
  - **Why pointers beat copies** — the failure modes are asymmetric. If the master comment moves or is deleted, **the broken reference is self-evident**: developers won't find the comment where indicated, and can use revision history to see what happened and fix the reference. "In contrast, if the documentation is duplicated and some of the copies don't get updated, **there will be no indication to developers that they are using stale information.**"
  - **Don't re-document another module's decisions.** Specifically: **don't put comments before a method call explaining what happens inside the called method.** Readers should look at that method's interface comments — and good tools display them on selection or hover. "Try to make it easy for developers to find appropriate documentation, but don't do it by repeating the documentation."
  - **Don't duplicate documentation that already exists outside your program — reference it.** Implementing HTTP? Don't describe the protocol in your code; add a comment with a URL. Implementing documented commands? `// Implements the Foo command; see the user manual for details.`
  - The summarizing line: **"It's important that readers can easily find all the documentation needed to understand your code, but that doesn't mean you have to write all of that documentation."**
- **Check the diffs (§16.5).** "Take a few minutes before committing a change to your revision control system to scan over all the changes for that commit; make sure that each change is properly reflected in the documentation." Bonus catches: **debugging code accidentally left in the system, and unfixed TODO items.**
- **Higher-level comments are easier to maintain (§16.6).** Abstract comments don't reflect code details, so minor code changes don't invalidate them — only changes in overall behavior do. Some comments do need to be detailed and precise (Ch 13), but note the happy coincidence: **"the comments that are most useful (they don't simply repeat the code) are also easiest to maintain."**

## Key Concepts
- **Strategic modification**: changing code so the resulting design looks intentional in hindsight.
- **Pre-commit diff scan**: reviewing your own diff for doc drift, leftover debug code, and TODOs.
- **Pointer comment**: a short reference to a single canonical explanation elsewhere.

## Anti-patterns
- **"What is the smallest possible change I can make that does what I need?"** — the typical mindset, and the source of tactical drift in mature systems. Sometimes justified by discomfort with unfamiliar code and fear that larger changes risk new bugs. But **"each one of these minimal changes introduces a few special cases, dependencies, or other forms of complexity. As a result, the system design gets just a bit worse, and the problems accumulate with each step in the system's evolution."**
- **Letting inaccurate comments accumulate.** "Inaccurate comments are frustrating to readers, and if there are very many of them, **readers begin to distrust all of the comments.**"
- **Interface comments in header files** (in C/C++), where the developer changing the body will never see them.
- **All implementation comments stacked at the top of a method.**
- **Design rationale living only in the commit log.**
- **Duplicated documentation** — hard to find all copies, and stale copies give no signal that they're stale.
- **Explaining a called method at the call site.**
- **Restating external specs** (HTTP, user manuals) inside your code.

## Worked Example — the whole documentation-maintenance system
The chapter's five techniques form one coherent strategy against comment rot. Read together:

| Technique | Mechanism | Failure it prevents |
|---|---|---|
| **Keep comments near the code** (§16.2) | The developer editing the code physically sees the comment | Comments silently going stale in a distant file |
| **Push comments to the narrowest scope** | Each comment sits directly above the code it describes | A top-of-method comment block describing code that has since changed |
| **Farther = more abstract** | Distance and detail scale inversely | Detailed remote comments invalidated by minor edits |
| **Comments in code, not the commit log** (§16.3) | Rationale lives where a future developer will encounter it | Someone reverting a fix and re-creating the bug |
| **Document each decision once** (§16.4) | One canonical location, short pointers elsewhere | Multiple copies drifting apart with no signal |
| **Reference, don't restate** (§16.4) | Link external specs and manuals | Maintaining a second copy of someone else's documentation |
| **Check the diffs** (§16.5) | A pre-commit scan of your own changes | Doc drift, leftover debug code, forgotten TODOs |
| **Prefer higher-level comments** (§16.6) | Abstract comments survive detail changes | Comments coupled to lines that churn |

Note the one genuine tension in the book: **§16.2 says keep documentation near the code it describes; §13.7's `designNotes` file deliberately does the opposite** for cross-module decisions that have no natural single home. Ousterhout names that tradeoff himself — centralizing makes it findable and single-copy, at the cost of being far from the code and therefore harder to keep current.

## Key Takeaways
1. Judge each change by whether the resulting design looks like it was intended from the start.
2. Improve the design at least slightly on every visit; not improving it usually means degrading it.
3. When constraints force a quick fix, look for the cheap-but-clean alternative, and schedule the real cleanup explicitly.
4. Put comments where the developer changing the code will see them — for C/C++, next to the body, not in the header.
5. Users shouldn't read your headers; generated docs and IDEs serve them, so optimize comment placement for maintainers.
6. Spread implementation comments to the narrowest enclosing scope, with an optional high-level strategy comment at the top.
7. Put design rationale in the code, not only the commit message — otherwise a future developer may undo it.
8. Document each decision exactly once and point to it; a broken pointer is visible, a stale copy is not.
9. Reference external documentation instead of reproducing it.
10. Scan your own diff before every commit for doc drift, debug code, and TODOs.
11. Prefer higher-level comments — the most useful ones are also the most durable.

## Connects To
- **Ch 1**: design is continuous because development is incremental; this chapter is that claim operationalized.
- **Ch 2**: complexity is incremental — minimal changes are exactly how it accumulates.
- **Ch 3**: the investment mindset, applied to code you didn't write.
- **Ch 13**: what to write; §13.7's `designNotes` and its tension with §16.2.
- **Ch 15**: comments-first keeps the backlog at zero; this chapter keeps it there as code changes.
- **Ch 17**: code reviews as the enforcement mechanism for both consistency and comment freshness.
