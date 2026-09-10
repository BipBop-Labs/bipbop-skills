# APOSD Cheatsheet — decision rules for writing code

## The 14 red flags (verbatim from the book's appendix)

Stop and look for an alternate design when you see one of these.

| Red flag | Definition | Ch |
|---|---|---|
| **Shallow Module** | The interface for a class or method isn't much simpler than its implementation | 4 |
| **Information Leakage** | A design decision is reflected in multiple modules | 5 |
| **Temporal Decomposition** | The code structure is based on the order in which operations are executed, not on information hiding | 5 |
| **Overexposure** | An API forces callers to be aware of rarely used features in order to use commonly used features | 5 |
| **Pass-Through Method** | A method does almost nothing except pass its arguments to another method with a similar signature | 7 |
| **Repetition** | A nontrivial piece of code is repeated over and over | 9 |
| **Special-General Mixture** | Special-purpose code is not cleanly separated from general-purpose code | 9 |
| **Conjoined Methods** | Two methods have so many dependencies that it's hard to understand the implementation of one without understanding the implementation of the other | 9 |
| **Comment Repeats Code** | All of the information in a comment is immediately obvious from the code next to the comment | 13 |
| **Implementation Documentation Contaminates Interface** | An interface comment describes implementation details not needed by users of the thing being documented | 13 |
| **Vague Name** | The name of a variable or method is so imprecise that it doesn't convey much useful information | 14 |
| **Hard to Pick Name** | It is difficult to come up with a precise and intuitive name for an entity | 14 |
| **Hard to Describe** | In order to be complete, the documentation for a variable or method must be long | 15 |
| **Nonobvious Code** | The behavior or meaning of a piece of code cannot be understood easily | 18 |

**Nonobvious Code** is also listed in the book as a red flag from Ch 18; **Hard to Describe** and **Hard to Pick Name** are the two that indict the *design*, not the documentation — treat them as the strongest signals.

## The 15 design principles (verbatim from the book's appendix)

1. Complexity is incremental: you have to sweat the small stuff.
2. Working code isn't enough.
3. Make continual small investments to improve system design.
4. Modules should be deep.
5. Interfaces should be designed to make the most common usage as simple as possible.
6. It's more important for a module to have a simple interface than a simple implementation.
7. General-purpose modules are deeper.
8. Separate general-purpose and special-purpose code.
9. Different layers should have different abstractions.
10. Pull complexity downward.
11. Define errors (and special cases) out of existence.
12. Design it twice.
13. Comments should describe things that are not obvious from the code.
14. Software should be designed for ease of reading, not ease of writing.
15. The increments of software development should be abstractions, not features.

## Decision rules

### Adding any new element (class, method, argument, interface, definition)
**Name the complexity it eliminates.** If you can't, don't add it. Every element costs — developers must learn it. (Ch 7)

### Should this be one module or two?
| Combine when | Separate when |
|---|---|
| They share information (both know a format) | The relationship is one-directional (block cache needs a hash table; hash tables don't need block caches) |
| They're used together **bidirectionally** | One is general-purpose and the other specializes it — pull the special-purpose part *up* |
| They overlap conceptually under one category | They're truly independent |
| You can't understand one without the other | Combining forces a discriminator field/boolean to answer basic questions |
| Combining simplifies the interface or lets you do something automatically | |

Decide by: **best information hiding, fewest dependencies, deepest interfaces.** (Ch 9)

### Should I split this method?
- **Length alone: no.** "Each method should do one thing and do it completely." Long deep methods are fine.
- **Extract a subtask** — the best split. Valid only if a reader of the child needs nothing from the parent *and* a reader of the parent needs nothing from the child's implementation.
- **Split into two caller-visible methods** — rarely right. Each new interface must be simpler than the original, and most callers should need only one. If callers must call both and pass state between them, don't.
- **After splitting, if you flip back and forth between the halves → Conjoined Methods → undo it.** (Ch 9)

### I found unavoidable complexity — where does it go?
**Down, into the implementation.** More users than developers; better that developers suffer. But only when all three hold: (a) it's closely related to the class's existing functionality, (b) it simplifies many things elsewhere, (c) it simplifies the class's interface. Otherwise you're just creating information leakage. (Ch 8)

### Should I expose a configuration parameter?
Ask: **"will users be able to determine a better value than we can determine here?"**
- No → compute it internally. Prefer *measuring* over a static value (measure successful response times → derive the retry interval).
- Yes → still compute a default so users only intervene in exceptional cases.

Each module should solve its problem **completely**. (Ch 8)

### Should this throw?
Try these in order (Ch 10):
1. **Define the error out of existence** — redefine the operation's semantics so the case is normal. *"delete a variable"* → *"ensure a variable no longer exists."* Clamp out-of-range indices instead of throwing.
2. **Mask it** — handle low, in shared library code, so no caller learns of it. Best placed **deep**.
3. **Aggregate it** — one handler high up, best placed **shallow/top**. For request-processing systems: one exception that aborts the request, cleans up, and continues, caught near the top of the loop — kept distinct from system-fatal exceptions.
4. **Crash** — rare + unhandleable. Wrap the raw call (`ckalloc`) so no caller must remember to check.

**Never throw just because you don't know what to do — the caller won't either.** Exceptions are part of your interface, and the most expensive part, since they propagate through callers you don't control.

**Limit:** if a caller genuinely needs the information (network failures, lost messages), expose it despite the interface cost.

### Naming
- Test: **could someone seeing this name in isolation guess what it refers to?**
- Two properties: **precise** + **consistent**. Consistency = always use the name for that purpose, never for anything else, and keep the purpose narrow enough that behavior is uniform.
- Booleans must be **predicates** (`cursorVisible`, not `blinkStatus`).
- **Longer distance between declaration and use → longer name.** `i`/`j` fine in short loops; `i` outermost, `j` nested, always.
- Two of the same kind → common name + prefix: `srcFileBlock`, `dstFileBlock`.
- Can also be **too specific** — don't bake a caller's context into a general parameter (`selection` → `range`).
- **Hard to name → probably badly factored.** Consider splitting the entity. (Ch 14)

### Comments
- **Write them first** — class interface comment, then method interface comments + signatures with empty bodies, iterate, then variables, then bodies. Zero backlog, ever. (Ch 15)
- **Never at the code's level of detail.** Go lower (precision) or higher (intuition).
- **The test:** could someone write this comment from the adjacent code alone? Then delete it.
- **Use different words than the entity's name.**
- **Declarations must specify:** units · inclusive/exclusive bounds · what null means · who frees/closes · invariants.
- **Variables: nouns, not verbs** — what it represents, not how it's mutated.
- **Method interface comments must cover:** behavior as callers see it · every argument and return, with constraints and inter-argument dependencies · side effects · exceptions · preconditions.
- **Keep implementation out of interface comments** — needing them means the module is shallow.
- **Inside methods:** what and why, per major block, not how per line.
- **Placement:** near the code (in C/C++, next to the body, *not* the header) · narrowest enclosing scope · farther away → more abstract · in the code, not the commit log · document each decision **once** and point to it elsewhere.

### Comments as a design meter (Ch 15)
| Symptom | Diagnosis |
|---|---|
| Interface comment is short, simple, **and** complete | Simple interface ✓ |
| Can't describe it completely without a long complicated comment | Complex interface |
| Interface comment must describe the implementation's major features | **Shallow module** |
| Variable needs a long comment to describe fully | Wrong variable decomposition |

### Making code obvious (Ch 18) — in this order
1. **Reduce the information needed** — abstraction, eliminate special cases.
2. **Use information readers already have** — follow conventions and expectations.
3. **Present it** — good names, strategic comments.

Comments are the *third* resort, not the first.

### Performance (Ch 20)
1. **Take free speed always.** Hash table over ordered map unless you need ordering (5–10x). Structures inline in an array, not pointers to them.
2. **Small hidden complexity, no interface change** → usually worth it. **Large or interface-visible** → stay simple, optimize later. **Clear evidence it matters** → do it now.
3. **Never optimize on intuition.** Measure deep enough to name specific hotspots; keep a baseline; **back out anything that didn't measurably help** unless it also simplified the code.
4. **Prefer a fundamental fix** (cache, better algorithm) over redesigning code for speed.
5. **Critical path method:** define the ideal (minimum common-case code, ignoring all existing structure), then find the cleanest design close to it. **Collapse all special-case detection into one `if` at the top**; branch off-path to handle them, structured for simplicity not speed.

### Cost awareness — orders of magnitude
| Operation | Instruction times |
|---|---|
| Cache miss (DRAM → cache) | few hundred |
| Fast NVM I/O (~1 µs) | ~2,000 |
| Datacenter network round-trip (10–50 µs) | tens of thousands |
| Disk I/O (5–10 ms) | millions |

### Trend verdicts (Ch 19)
| Practice | Verdict |
|---|---|
| Interface inheritance | ✓ deepens the interface |
| Implementation inheritance | ⚠ try composition + helper classes first; if unavoidable, hide parent state from subclasses |
| Incremental development | ✓ but increment by **abstractions, not features** |
| "Start special-purpose, generalize later" | ✗ tactical programming |
| Unit tests | ✓ essential — they're what makes refactoring safe |
| TDD | ✗ for design; ✓ for bug fixes (write the failing test first, or you can't prove the fix) |
| Design patterns | ✓ when they fit; never force a problem into one |
| Getters/setters | ✗ shallow methods around an exposed-state mistake |

### Thresholds and numbers
| Quantity | Value |
|---|---|
| Time to invest in design | **10–20%** of total development time |
| Cost of a degraded code base | **≥20%** slower development |
| Design-it-twice cost for one class | **1–2 hours** |
| Comment writing as share of dev time | **~5%** (typing code+comments ≈10%) |
| Cost of ignoring performance entirely | **5–10x** slower than necessary |
| Alternatives to sketch per major decision | **≥2**, deliberately radically different |

### Review stance
- **"If a reader thinks it's not obvious, then it's not obvious."** Don't argue — find what confused them and fix the comment *or* the code. (Ch 13, 18)
- **Be nit-picky as a reviewer** — fastest way to propagate conventions. (Ch 17)
- **Scan your own diff before committing** — doc drift, leftover debug code, unfixed TODOs. (Ch 16)
- **Every modification should leave the design as if you'd planned for that change from the start.** Not improving it usually means degrading it. (Ch 16)
