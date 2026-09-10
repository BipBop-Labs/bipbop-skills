# Chapter 6: General-Purpose Modules are Deeper

## Core Idea
Make modules "somewhat general-purpose": the functionality should reflect your current needs, but the interface should not. The surprising payoff is that this yields *simpler* interfaces even if you never reuse the module.

## Frameworks Introduced
- **"Somewhat general-purpose" — the sweet spot.**
  - The rule: **functionality reflects today's needs; the interface is general enough to support multiple uses.** Easy to use for today's needs without being tied specifically to them.
  - "Somewhat" is load-bearing: don't build something so general it's hard to use for the current job.
  - When to use: every time you're deciding a new module's API — one of the most common design decisions you'll face.
  - Why it works: the primary benefit isn't future reuse (which is speculative), it's that general-purpose APIs come out **simpler and deeper right now**. Reuse is a bonus.
- **The three questions to ask yourself (§6.5)** — the chapter's most directly usable tool, since recognizing a clean general-purpose design is easier than creating one:
  1. **"What is the simplest interface that will cover all my current needs?"** If you reduce the *number* of methods without reducing capability, you're probably generalizing correctly. Caveat: only valid while each individual method's API stays simple — if you need lots of extra arguments to collapse methods, you aren't simplifying.
  2. **"In how many situations will this method be used?"** A method designed for one particular use is **a red flag** that it's too special-purpose. Look to replace several special-purpose methods with one general one.
  3. **"Is this API easy to use for my current needs?"** This catches over-generalization. If you must write a lot of extra code to use the class for its current purpose, the interface is wrong.
- **Generality leads to better information hiding.** A general interface cleanly separates layers; a special-purpose interface leaks the caller's abstractions downward.

## Key Concepts
- **General-purpose interface**: defined in terms of the module's own basic concepts, not the caller's higher-level operations.
- **Special-purpose interface**: one method per caller-visible feature.
- **False abstraction** (recurring from Ch 4): an interface that purports to hide information the caller actually needs.

## Anti-patterns
- **One method per UI feature / per caller operation**: produces many shallow methods, most invoked in exactly one place, and forces callers to learn a large API.
- **Leaking the caller's abstractions into the callee** (a `Cursor` or `Selection` type inside a text-storage class): now the lower module carries the higher module's concepts, and each new caller feature requires a new method in the lower class — so the two classes can no longer be developed independently.
- **Over-generalizing to single-element operations**: technically simple and general, but forces loops into every caller and performs badly on bulk operations.

## Code Examples

**Special-purpose (worse)** — a text-editor storage class with one method per keystroke:
```java
void backspace(Cursor cursor);
void delete(Cursor cursor);
void deleteSelection(Selection selection);
```
Three deletion methods. Each is shallow. `delete` is invoked in exactly one place. `Cursor` and `Selection` are user-interface abstractions now embedded in the text class.

**General-purpose (better)** — defined only in terms of basic text features:
```java
void insert(Position position, String newText);
void delete(Position start, Position end);
Position changePosition(Position position, int numChars);
```
`insert` puts an arbitrary string at an arbitrary position. `delete` removes characters at positions `>= start` and `< end`. `Position` replaces the UI-flavored `Cursor`. `changePosition` returns a position a given number of characters away — positive moves later in the file, negative earlier — automatically skipping to the next or previous line as needed.

The two keystrokes now live in the UI, where they belong:
```java
// delete key
text.delete(cursor, text.changePosition(cursor, 1));

// backspace key
text.delete(text.changePosition(cursor, -1), cursor);
```

Adding a search-and-replace tool needs only:
```java
Position findNext(Position start, String string);
```
The specialized `backspace`/`delete` methods would have been worthless for that application; the general-purpose class already had nearly everything.

## Worked Example — why the general version wins on every axis
Students building GUI text editors (multiple views of one file, multi-level undo/redo) each wrote a text class. Most made it special-purpose because they knew it would only be used by their editor.

Comparing the two designs:

| | Special-purpose | General-purpose |
|---|---|---|
| Deletion methods | 3 (`backspace`, `delete`, `deleteSelection`) | 1 (`delete`) |
| UI code length | Shorter per call site | Slightly longer per call site |
| Total code | More | **Less** — a few general methods replace many special ones |
| Is deletion behavior obvious? | No — must read the text class's docs/code | **Yes** — visible at the call site |
| Cognitive load on UI developer | Large API to learn | A few reusable methods |
| Adding a UI feature | Requires a new method in the text class | No change to the text class |
| Reusable for search-and-replace? | No | Yes, plus `findNext` |

The counterintuitive point is that the general version's call sites are *longer yet more obvious*. A UI developer cares which characters backspace deletes. In the general version, `text.delete(text.changePosition(cursor, -1), cursor)` says so. In the special version they must go read `backspace`'s implementation to confirm.

That makes the original `backspace` method a **false abstraction**: it claimed to hide which characters get deleted, but the UI module needs to know. Hiding it behind an interface only made the information harder to get.

The chapter's general lesson: **"One of the most important elements of software design is determining who needs to know what, and when. When the details are important, it is better to make them explicit and as obvious as possible."** Hiding important information creates obscurity, not abstraction.

## Key Takeaways
1. Let functionality follow today's needs; let the interface stay general.
2. Fewer, more general methods usually beat many special-purpose ones — as long as each method's own API stays simple.
3. A method with exactly one caller is a red flag for over-specialization.
4. Test for over-generalization by asking whether today's use is still easy.
5. Generality gives you information hiding for free by keeping the caller's abstractions out of the callee.
6. Don't hide information the caller genuinely needs — that's a false abstraction. Make it explicit at the call site.
7. Prefer range/bulk operations over single-element ones when callers work in ranges.

## Connects To
- **Ch 4**: general-purpose interfaces are how you get depth; false abstraction defined here.
- **Ch 5**: generality improves information hiding and removes leakage between layers.
- **Ch 7**: interface should differ from implementation (character-oriented API over line-oriented storage).
- **Ch 9**: "Separate general-purpose and special-purpose code" (design principle #8).
