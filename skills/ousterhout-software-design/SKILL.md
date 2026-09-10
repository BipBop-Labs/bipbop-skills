---
name: ousterhout-software-design
description: "Knowledge base from \"A Philosophy of Software Design\" by John Ousterhout. Use when designing or reviewing code for complexity, module depth, information hiding, interface design, error handling, comments, naming, or performance — or when a design decision needs a rationale beyond taste."
---

<!-- argument-hint: [topic, framework name, red flag, or chapter number] -->

# A Philosophy of Software Design
**Author**: John Ousterhout | **Pages**: ~188 | **Chapters**: 21 | **Generated**: 2026-08-10

## How to Use This Skill

- **While writing code** — apply the red flags below as stop-and-redesign signals; consult [cheatsheet.md](cheatsheet.md) for the decision rules.
- **While reviewing code** — the red flag table is the review checklist. Ousterhout designed the book for exactly this use.
- **With a topic** — ask about `deep modules`, `information hiding`, `exceptions`, `naming`, `comments`, `performance`; I read the relevant chapter first.
- **With a chapter** — ask for `ch10`; I load that file.

Every chapter file carries the book's actual code examples and worked cases, so recommendations can cite a concrete precedent rather than a slogan.

---

## The Central Claim

Complexity is the fundamental limit on software — "anything related to the structure of a software system that makes it hard to understand and modify the system." It is **caused** by two things and **shows up** as three:

| Causes | Symptoms |
|---|---|
| **Dependencies** — code that can't be understood or changed in isolation | **Change amplification** — a simple change touches many places |
| **Obscurity** — important information isn't obvious | **Cognitive load** — how much you must know to make a change |
| | **Unknown unknowns** — you can't tell *what* you need to know ← **the worst** |

Only two tools exist: **eliminate** complexity (simpler, more obvious code) or **encapsulate** it (modular design).

Complexity is **incremental** — never one catastrophe, always hundreds of small dependencies and obscurities. So sweat the small stuff, and adopt zero tolerance.

---

## Core Frameworks

**Deep modules** (Ch 4) — The single most important idea. Picture a module as a rectangle: area = functionality, top edge = interface complexity. **Deep** = a lot of functionality behind a small interface. Ask of every class and method: *is the interface much simpler than the implementation?* Unix file I/O is five calls over hundreds of thousands of lines, unchanged for decades. A garbage collector has *no* interface — adding it shrinks the system's total interface. Conversely, "interfaces are good, but more, or larger, interfaces are not necessarily better," and **"any method longer than N lines should be split" is wrong** — it manufactures shallow methods.

**Information hiding** (Ch 5) — How modules become deep: each encapsulates design decisions that never appear in its interface. Note that `private` is *not* information hiding if getters and setters expose the same knowledge. **Decompose by the knowledge needed for each task, not by the order operations occur** — the latter is temporal decomposition and it leaks.

**Somewhat general-purpose** (Ch 6) — Functionality reflects today's needs; the *interface* does not. The payoff isn't speculative reuse, it's a simpler interface right now. A method with exactly one caller is a red flag for over-specialization.

**Different layer, different abstraction** (Ch 7) — Follow an operation through layers; the abstraction should change at each call. And the general test behind it: **for every element you add — class, method, argument, interface — name the complexity it eliminates. If you can't, omit it.**

**Pull complexity downward** (Ch 8) — **"It is more important for a module to have a simple interface than a simple implementation."** Most modules have more users than developers, so developer suffering is the cheaper suffering. The two ways people push complexity *up*: throwing an exception when unsure, and adding a configuration parameter when undecided.

**Define errors out of existence** (Ch 10) — Redefine semantics so the error case becomes normal. Not *"delete a variable"* but *"ensure a variable no longer exists."* Exceptions are part of your interface and the most expensive part, since they propagate through callers you don't control. **Never throw because you don't know what to do — the caller won't know either.** Four techniques, in order: define away → mask (place **deep**) → aggregate (place **high**) → crash.

**Design it twice** (Ch 11) — Sketch two or more *radically different* alternatives before committing, even when you're certain. Costs 1–2 hours per class. "No-one is good enough to get it right with their first try."

**Comments as a design tool** (Ch 15) — Write them first: class comment, then method comments and signatures with empty bodies, iterate, then variables, then bodies. Comments are a **complexity meter**: if the interface comment must describe the implementation's major features, the method is shallow; if a variable needs a long comment, the decomposition is wrong.

**Strategic vs. tactical** (Ch 3) — Working code is the floor, not the goal. Invest **10–20%** of development time continuously; a degraded code base costs **≥20%**. "Whenever you modify any code, try to find a way to improve the system design at least a little bit in the process. **If you're not making the design better, you are probably making it worse.**" (Ch 16)

**Obviousness** (Ch 18) — Code is obvious when a reader's *first guess* is correct. Attack nonobviousness in order: (1) reduce the information needed — abstraction, eliminate special cases; (2) use information readers already have — conventions; (3) present it — names, comments. **Comments are the third resort.** And: "if a reader thinks it's not obvious, then it's not obvious."

**Performance** (Ch 20) — Clean design and speed are compatible; the `Buffer` rewrite got **2x faster, 20% smaller, and more readable** at once. Never optimize on intuition. Simple code is fast for concrete reasons: no special-case checks, deeper classes doing more per call, fewer layer crossings.

---

## The 14 Red Flags — the working checklist

| Red flag | Trigger | Ch |
|---|---|---|
| **Shallow Module** | Interface isn't much simpler than implementation | 4 |
| **Information Leakage** | One design decision reflected in multiple modules | 5 |
| **Temporal Decomposition** | Structure follows execution order, not information hiding | 5 |
| **Overexposure** | Common features force learning rare ones | 5 |
| **Pass-Through Method** | Does nothing but forward its arguments | 7 |
| **Repetition** | Nontrivial code repeated | 9 |
| **Special-General Mixture** | General mechanism carries code specialized to one use | 9 |
| **Conjoined Methods** | Can't understand one without the other | 9 |
| **Comment Repeats Code** | Comment derivable from adjacent code | 13 |
| **Implementation Doc Contaminates Interface** | Interface comment describes internals | 13 |
| **Vague Name** | Broad enough to mean many things | 14 |
| **Hard to Pick Name** | Can't name it precisely → **bad design** | 14 |
| **Hard to Describe** | Needs a long comment to document → **bad design** | 15 |
| **Nonobvious Code** | Can't be understood on a quick read | 18 |

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction-complexity.md) | Introduction (It's All About Complexity) | eliminate vs. encapsulate, red-flag-driven design |
| [ch02](chapters/ch02-nature-of-complexity.md) | The Nature of Complexity | complexity defined, 3 symptoms, 2 causes, weighted complexity |
| [ch03](chapters/ch03-working-code-isnt-enough.md) | Working Code Isn't Enough | tactical vs. strategic, 10–20% investment, tactical tornado |
| [ch04](chapters/ch04-modules-should-be-deep.md) | Modules Should Be Deep | deep/shallow, abstraction, false abstraction, classitis |
| [ch05](chapters/ch05-information-hiding.md) | Information Hiding (and Leakage) | information hiding, leakage, temporal decomposition, defaults |
| [ch06](chapters/ch06-general-purpose-modules.md) | General-Purpose Modules are Deeper | somewhat general-purpose, the three questions |
| [ch07](chapters/ch07-different-layer-different-abstraction.md) | Different Layer, Different Abstraction | layer rule, net-gain test, decorator alternatives, context object |
| [ch08](chapters/ch08-pull-complexity-downwards.md) | Pull Complexity Downwards | simple interface > simple implementation, config-parameter test |
| [ch09](chapters/ch09-better-together-or-apart.md) | Better Together Or Better Apart? | 4 costs of subdivision, 4 signs of relatedness, method splitting |
| [ch10](chapters/ch10-define-errors-out-of-existence.md) | Define Errors Out Of Existence | define away, mask, aggregate, crash, error promotion |
| [ch11](chapters/ch11-design-it-twice.md) | Design it Twice | radically different alternatives, comparison criteria |
| [ch12](chapters/ch12-why-write-comments.md) | Why Write Comments? The Four Excuses | comments enable abstraction, the 10% argument |
| [ch13](chapters/ch13-comments-describe-nonobvious.md) | Comments Should Describe Things that Aren't Obvious | 4 categories, precision vs. intuition, designNotes |
| [ch14](chapters/ch14-choosing-names.md) | Choosing Names | create an image, precision + consistency, the `block` bug |
| [ch15](chapters/ch15-write-comments-first.md) | Write The Comments First | comments-first workflow, comments as complexity meter |
| [ch16](chapters/ch16-modifying-existing-code.md) | Modifying Existing Code | stay strategic, comment placement, avoid duplication, check diffs |
| [ch17](chapters/ch17-consistency.md) | Consistency | cognitive leverage, invariants, automated enforcement, When in Rome |
| [ch18](chapters/ch18-code-should-be-obvious.md) | Code Should be Obvious | 3 ways to make code obvious, white space, generic containers |
| [ch19](chapters/ch19-software-trends.md) | Software Trends | inheritance, agile, unit tests, TDD, patterns, getters/setters |
| [ch20](chapters/ch20-designing-for-performance.md) | Designing for Performance | cost awareness, measure first, critical path, Buffer rewrite |
| [ch21](chapters/ch21-conclusion.md) | Conclusion | the book's own summary; costs and payoff |

## Topic Index

- **Abstraction** → ch04, ch06, ch12, ch13, ch18
- **Agile / incremental development** → ch01, ch19
- **Comments** → ch12, ch13, ch15, ch16, ch18
- **Configuration parameters** → ch08
- **Consistency** → ch14, ch17, ch18
- **Context objects / globals** → ch07
- **Decorators** → ch07, ch19
- **Deep modules** → ch04, ch05, ch06, ch08, ch20
- **Dependencies** → ch02, ch04, ch07, ch19
- **Design patterns** → ch17, ch19
- **Duplication** → ch09, ch16
- **Errors / exceptions** → ch08, ch10, ch13
- **General- vs. special-purpose** → ch06, ch09, ch10
- **Inheritance** → ch19
- **Interface vs. implementation** → ch04, ch07, ch13, ch15
- **Invariants** → ch13, ch17
- **Layering** → ch07, ch09, ch20
- **Method length / splitting** → ch04, ch09, ch12
- **Naming** → ch13, ch14, ch17, ch18
- **Obscurity / obviousness** → ch02, ch13, ch18
- **Performance** → ch19, ch20
- **Red flags** → ch01, and one or more in ch04, 05, 07, 09, 13, 14, 15, 18
- **Refactoring** → ch16, ch19, ch20
- **Special cases** → ch10, ch17, ch20
- **Strategic vs. tactical** → ch03, ch16, ch19
- **Testing** → ch19
- **Whitespace / formatting** → ch17, ch18

## Supporting Files

- [cheatsheet.md](cheatsheet.md) — **start here while coding**: all 14 red flags, the 15 design principles, and the decision rules (split or join? throw or not? expose a parameter? optimize now?) plus every threshold and number in the book
- [patterns.md](patterns.md) — the 20 named techniques and refactorings, each with when-to-use / how / trade-offs
- [glossary.md](glossary.md) — every term with a one-line definition and chapter reference

---

## Scope & Limits

Book content only. Examples are Java and C++ and the discussion is class-oriented, but Ousterhout notes the ideas apply to functions in non-OO languages and to subsystems and services alike.

Two things to carry carefully:
- **Apply everything with moderation.** "Every rule has its exceptions, and every principle has its limits. If you take any design idea to its extreme, you will probably end up in a bad place." Most chapters have an explicit *Taking it too far* section; those are preserved in the chapter files and worth reading before pushing a principle hard.
- **Some positions are deliberately contrarian** — against splitting methods by line count, against TDD, against getters and setters, against agile's defer-generality advice, against short Go-style names. The book argues each from complexity; the arguments are in the chapter files, so cite the reasoning rather than the verdict.

Absolute performance numbers in ch20 are from 2018; the ratios are the durable part.
