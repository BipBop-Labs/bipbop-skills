# APOSD Patterns — techniques and refactorings

## Deep module
**When to use**: designing any class, method, service, or API.
**How**: hide a lot of functionality behind a small interface. Test by asking whether the interface is *much* simpler than the implementation. Design so the **common case is simplest**; make rare features reachable but invisible.
**Trade-offs**: the implementation absorbs complexity. Exemplars: Unix file I/O (5 calls over hundreds of thousands of lines, stable for decades); a garbage collector (zero interface — adding it *shrinks* the system's total interface).
→ Ch 4

## Information hiding
**When to use**: every new module.
**How**: identify design decisions the module can encapsulate — data structures, algorithms, page sizes, assumptions like "most files are small" — and keep them out of the interface.
**Trade-offs**: `private` alone doesn't achieve it if getters/setters expose the same information. Partial hiding (reachable only via separate methods, invisible in common use) still cuts dependencies substantially.
→ Ch 5

## Somewhat general-purpose interface
**When to use**: deciding a new module's API.
**How**: let *functionality* reflect today's needs, but make the *interface* general. Three checks: What's the simplest interface covering all current needs? In how many situations will this method be used (one = too special)? Is it still easy to use for today's job (no = over-generalized)?
**Trade-offs**: call sites get slightly longer but more obvious; total code shrinks; the callee stops carrying the caller's abstractions.
→ Ch 6

## Pull complexity downward
**When to use**: you've found unavoidable complexity related to the module's functionality.
**How**: absorb it in the implementation rather than exposing it. Compute values instead of exposing knobs (measure successful response times → derive the retry interval).
**Trade-offs**: only valid when the complexity is closely related to the class's existing function, simplifies many callers, *and* simplifies the interface. Otherwise it becomes information leakage.
→ Ch 8

## Define errors out of existence
**When to use**: you're about to throw for a condition the caller can't usefully act on.
**How**: redefine the operation's semantics so the case becomes normal. *"delete a variable"* → *"ensure a variable no longer exists."* Clamp out-of-range slice indices rather than throwing. Mark an in-use file for deletion and return success.
**Trade-offs**: simplifies the API *and* adds functionality, so the method gets deeper. The "but errors catch bugs" objection fails because error-ful APIs force extra caller code (more bug surface) or get forgotten (runtime surprises). Limit: if callers genuinely need the information, expose it.
→ Ch 10

## Exception masking
**When to use**: a low-level, widely-called library method encounters a condition it can resolve.
**How**: detect and handle it internally so higher levels never learn of it. TCP resending lost packets. NFS hanging and retrying rather than reporting failures upward.
**Trade-offs**: deepens the class (smaller interface, more functionality); it's pulling complexity downward. Place it **deep** — a shared method, where propagating would multiply handlers. Don't mask information callers need to be robust.
→ Ch 10

## Exception aggregation
**When to use**: many call sites throw conditions that all get handled the same way.
**How**: let exceptions propagate several levels and catch them in one place. For request-processing systems, define an exception that aborts the current request, cleans up state, and continues with the next — caught near the top of the request loop, with subclasses for different conditions. Generate the human-readable message where the exception is thrown; the top-level handler extracts and wraps it.
**Trade-offs**: opposite placement to masking (**shallow/top** vs. deep) but the same principle — put the handler where it catches the most. Keep request-fatal exceptions clearly distinct from system-fatal ones. Extends for free: new throwers inheriting the same superclass plug in with no other changes.
→ Ch 10

## Error promotion
**When to use**: you'd otherwise build a second recovery mechanism for a rare, smaller error.
**How**: promote it into an existing larger recovery path. RAMCloud crashes the whole server on a single corrupted object rather than restoring one object.
**Trade-offs**: fewer mechanisms, less code, and the surviving path runs more often so its bugs get found ("code that hasn't been executed doesn't work"). Recovery cost per incident rises sharply — **only viable for rare errors.** Never for frequent ones (you can't crash a server per lost packet).
→ Ch 10

## Design special cases out of existence
**When to use**: code is accumulating `if` statements for an absent/empty/edge state.
**How**: make the normal case handle the special one with no extra code. Instead of a "does a selection exist?" boolean, let the selection **always exist**, empty when invisible (start == end). Copying inserts 0 bytes; deleting concatenates the before- and after-portions, regenerating the original line.
**Trade-offs**: a user-facing concept ("no selection") needn't be represented internally — that's "different layer, different abstraction."
→ Ch 10, 17 (invariants)

## Just crash
**When to use**: errors that are rare *and* difficult or impossible to handle meaningfully.
**How**: print diagnostics and abort. Wrap the raw call so no caller must remember: `ckalloc` calls `malloc`, checks, aborts on exhaustion; the application never calls `malloc` directly.
**Trade-offs**: appropriate for out-of-memory, I/O errors on open files, unopenable sockets, and internal inconsistencies (which indicate bugs). **Not** for a replicated storage system hitting an I/O error — recovering data is part of its value.
→ Ch 10

## Context object
**When to use**: a variable is threaded through methods that don't use it (pass-through variable).
**How**: one object per system instance holding all global state — configuration, shared subsystems, performance counters. Store a context reference as an instance variable in major objects and pass it from creator to constructor, so **it appears as an explicit argument only in constructors.**
**Trade-offs**: adding a global touches only the context's constructor/destructor; global state becomes identifiable in one place; multiple instances coexist in one process; tests reconfigure by setting fields. But context variables carry most of the disadvantages of globals — unclear why present or where used — and without discipline it becomes "a huge grab-bag of data that creates nonobvious dependencies." **Make context variables immutable** to avoid thread-safety problems. Ousterhout: "far from an ideal solution," but he knows of nothing better. Prefer it over globals, which break multi-instance testing.
→ Ch 7

## Extract the general-purpose core
**When to use**: a general mechanism is entangled with code specialized for one of its uses (Special-General Mixture).
**How**: put the general mechanism in its own class, knowing nothing about specific uses; implement the special cases outside it. `History` manages a list of `History.Action` objects with `undo()`/`redo()`, and knows nothing about what they store. Text and UI modules supply `UndoableInsert`, `UndoableDelete`, `UndoableSelection`, `UndoableCursor`. Grouping uses **fences** placed by high-level code via `addFence`; undo walks back to the next fence.
**Trade-offs**: yields three independently implementable layers — general mechanism / specific actions / grouping policy. "The key design decision was… once that was done, the rest of the design fell out naturally." Scoping caveat: this applies *within one mechanism* — special-purpose undo code for text belongs in the text class, next to the general-purpose text mechanism.
**Direction**: lower layers general, upper layers special-purpose — so separate by pulling the special-purpose code **up**.
→ Ch 9

## Refactoring pass-through methods
**When to use**: a class's methods mostly forward to another class with the same signatures.
**How**, three options: **expose** the lower class directly to callers; **redistribute** functionality to eliminate the calls between them; or **merge** them if they can't be disentangled. Pick by answering "exactly which features and abstractions is each class responsible for?"
**Trade-offs**: same signatures are legitimate for **dispatchers** (which choose among methods — real functionality) and **multiple implementations of one interface** (disk drivers — which *reduce* cognitive load). The rule: **the interface to a piece of functionality belongs in the class that implements it.**
→ Ch 7

## Alternatives to a decorator
**When to use**: you're about to wrap a class to add a feature.
**How**, in order: add the functionality **directly to the underlying class** (if it's general-purpose, logically related, or wanted by most users — buffering belongs in `FileInputStream`); **merge it with the specific use case**; **merge it into an existing decorator** (one deeper decorator beats several shallow ones); or implement it as a **stand-alone class that doesn't wrap** (scrollbars separate from the window).
**Trade-offs**: decorators "introduce a large amount of boilerplate for a small amount of new functionality" and accumulate pass-through methods. "Sometimes decorators make sense, but there is usually a better alternative."
→ Ch 7

## Eliminating duplication
**When to use**: the Repetition red flag.
**How**, two ways: **factor the snippet into a method** — most effective when the snippet is long and the new signature is simple; weak for one-to-two-line snippets or code touching many locals (which forces a complex signature, e.g. many by-reference arguments). Or **restructure so the snippet executes once** — move shared cleanup to the end of a method and `goto` it from each error-return point.
**Trade-offs**: on `goto` — "generally considered a bad idea, and they can result in indecipherable code if used indiscriminately, but they are useful in situations like this where they are used to escape from nested code."
→ Ch 9

## Design it twice
**When to use**: every major design decision — interface, then implementation, separately.
**How**: sketch **two or more radically different** alternatives, a few key method signatures deep. Do it even when you're sure. List pros and cons, weighted: ease of use for callers first, then interface simplicity, generality, and implementation efficiency. Outcomes: pick one, **combine features into a better fourth option**, or (if none appeals) use the identified problems to drive new schemes.
**Trade-offs**: ~1–2 hours per class against days or weeks of implementation. Goals differ by level: interfaces are judged on ease of use, implementations on simplicity and performance. **When alternatives share a weakness, that shared weakness points to the better design.**
→ Ch 11

## Comments-first design
**When to use**: starting any new class.
**How**: class interface comment → interface comments + signatures for the main public methods with **empty bodies** → iterate until the structure feels right → declarations and comments for the main instance variables → fill in bodies. New methods discovered along the way get their interface comment before their body.
**Trade-offs**: no comment backlog ever; abstractions stabilize before coding, which may make it **net faster** (fewer code revisions). Doubles as a complexity meter — see `cheatsheet.md`.
→ Ch 15

## Cross-module documentation
**When to use**: a design decision spans modules with no single owner.
**How**: if there's a place every implementer must visit, put a checklist there (RAMCloud's `Status` enum carries a 7-step list of every other file to update — placed at the *end*, where new values get appended). If there isn't, use a central **`designNotes`** file with labeled topic sections, plus one-line pointers at each site: `// See "Zombies" in designNotes.`
**Trade-offs**: single copy and findable, but far from the code it describes, so harder to keep current — a knowing tension with "keep comments near the code."
**Why pointers beat copies**: a broken pointer is self-evident (the comment isn't where indicated; revision history explains why), whereas a stale duplicate gives no signal at all.
→ Ch 13, 16

## Automated convention enforcement
**When to use**: a convention keeps getting violated, especially by newcomers.
**How**: write a checker that runs before commit and **aborts the commit** on violation; ideally make it also repair the problem. RAMCloud's script rejected carriage returns in modified files and could rewrite CR/NL to NL.
**Trade-offs**: "This instantly eliminated the problems, and it also helped train new developers." Documentation alone failed for years because every developer's tools had to cooperate. Works best for low-level syntactic conventions.
→ Ch 17

## Design around the critical path
**When to use**: last resort, after measurement identifies a hotspot and no fundamental fix (cache, better algorithm) exists.
**How**: (1) Define **the ideal** — the minimum code for the common case, ignoring existing structure, special cases, method boundaries, and current data structures; assume whatever representation is most convenient, possibly **combining multiple variables into one value**. (2) Find the cleanest design that stays close to it (an extra call to a general-purpose hash table is fine). (3) **Remove special cases from the path.** (4) **Collapse detection into one `if` at the top**; branch off-path to handle special cases, structured for simplicity rather than speed.
**Trade-offs**: RAMCloud's `Buffer` got **2x faster, 20% smaller, and more readable** at once — a single `extraAppendBytes` variable subsumed three conditions (no space / last chunk not internal / no chunks at all), replacing six checks across three shallow layers. Sometimes you deliberately pay a little on one path to keep another fast (maintaining `totalLength` incrementally rather than recomputing it).
→ Ch 20
