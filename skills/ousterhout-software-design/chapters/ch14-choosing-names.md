# Chapter 14: Choosing Names

## Core Idea
Names are a form of abstraction and one of the most underrated aspects of design: good ones must be **precise** and **consistent**, and a single vague name can cost months.

## Frameworks Introduced
- **The goal: create an image.** "When choosing a name, the goal is to create an image in the mind of the reader about the nature of the thing being named. A good name conveys a lot of information about what the underlying entity is, and, **just as important, what it is not.**"
  - **The test to apply:** *"If someone sees this name in isolation, without seeing its declaration, its documentation, or any code that uses the name, how closely will they be able to guess what the name refers to? Is there some other name that will paint a clearer picture?"*
  - The constraint: names become unwieldy past two or three words, so **the challenge is finding a few words that capture the most important aspects.**
  - Names are abstraction: "the best names are those that focus attention on what is most important about the underlying entity while omitting details that are less important."
- **The two properties of good names: precision and consistency.**
- **Precision (§14.3).** "The most common problem with names is that they are too generic or vague." The reader may then assume the name means something other than reality.
  - Sub-rule: **"names of boolean variables should always be predicates."**
- **Consistency (§14.4).** For each repeated concept, pick one name and use it everywhere. This "reduces cognitive load in much the same way as reusing a common class: once the reader has seen the name in one context, they can reuse their knowledge and instantly make assumptions when they see the name in a different context."
  - **Three requirements:**
    1. **Always use** the common name for that purpose.
    2. **Never use** the common name for anything else.
    3. **Make the purpose narrow enough that all variables with the name have the same behavior.** ← This is the one the `block` bug violated.
  - When you need two of the same kind of thing, keep the common name and add a distinguishing prefix: `srcFileBlock`, `dstFileBlock`.
  - **Loops**: if you use `i` and `j`, **always use `i` for outermost and `j` for nested** — readers can then make instant, safe assumptions.
- **The exceptions to precision:**
  - **Generic loop variables are fine** when the loop spans only a few lines: "If you can see the entire range of usage of a variable, then the meaning of the variable will probably be obvious from the code so you don't need a long name." If the loop grows past one screen, or the variable's meaning is harder to derive, use a descriptive name.
  - **A name can be too specific.** In `void delete(Range selection)`, the argument name `selection` wrongly implies the text is always selected in the UI, when the method works on any range. It should be `range`.
- **The point of agreement with the Go style guide:** *"The greater the distance between a name's declaration and its uses, the longer the name should be."* (Gerrand) — the `i`/`j` rule is an instance.

## Key Concepts
- **Precision**: the name narrows to one thing.
- **Consistency**: one name per concept, one concept per name, narrow enough that behavior is uniform.
- **Predicate name**: a boolean name from which the meaning of `true` is guessable (`cursorVisible`, not `blinkStatus`).

## Anti-patterns
- **Red Flag — Vague Name**: a name broad enough to refer to many different things conveys little and makes the entity **more likely to be misused.**
- **Red Flag — Hard to Pick Name**: "If it's hard to find a simple name for a variable or method that creates a clear image of the underlying object, that's a hint that the underlying object may not have a clean design."
  - **What to do about it:** consider alternative factorings. "Perhaps you are trying to use a single variable to represent several things; if so, separating the representation into multiple variables may result in a simpler definition for each variable." **The process of choosing good names can improve your design by identifying weaknesses.**
- **Settling for "reasonably close."** "Most developers don't spend much time thinking about names. They tend to use the first name that comes to mind, as long as it's reasonably close to matching the thing it names."
- **`result` in a method with no return value** — doubly wrong: it falsely implies it will be returned, *and* it says nothing about what it holds. (In a method that *does* return, `result` is reasonable — still generic, but readers can check the method documentation, and it's helpful to know the value becomes the return.)

## Code Examples — imprecise → precise

| Bad | Why | Better |
|---|---|---|
| `int IndexletManager::getCount()` | "Count" of *what*? A reader seeing an invocation can't tell without reading the docs | `getActiveIndexlets` or `numIndexlets` |
| `x`, `y` for a character's position in a file | Far too generic — they could just as easily be pixel coordinates on screen | `charIndex`, `lineIndex` — reflecting the abstractions the code actually implements |
| `blinkStatus` | "Status" is too vague for a boolean — no clue what `true` means. "Blink" doesn't say *what* blinks | `cursorVisible` |
| `VOTED_FOR_SENTINEL_VALUE` | Says the value is special but not what the special meaning is | `NOT_YET_VOTED` |
| `result` in a void method | Implies a return value; says nothing about content | `mergedLine`, `totalChars` |
| `void delete(Range selection)` | Too *specific* — implies always-selected text | `void delete(Range range)` |

The blink example in full:
```java
// Blink state: true when cursor visible.
private boolean blinkStatus = true;
```
```java
// Controls cursor blinking: true means the cursor is visible,
// false means the cursor is not displayed.
private boolean cursorVisible = true;
```
Note the deliberate trade: "blink" leaves the name, so a reader wanting to know *why* the cursor isn't always visible must consult the documentation — **and that information is less important** than what `true` means.

Acceptable generic name, because the whole range of use is visible:
```java
for (i = 0; i < numLines; i++) {
    ...
}
```

## Worked Example — the `block` bug: six months for one name
In the late 1980s–early 90s, Ousterhout and his graduate students built the **Sprite** distributed operating system. They noticed files occasionally losing data: **a data block would suddenly become all zeroes, even though no user had modified the file.** It happened rarely, so it was exceptionally hard to track down. Several graduate students tried and gave up. ("I consider any unsolved bug to be an intolerable personal insult.")

**It took six months.** The cause: the file system used the variable name **`block` for two different purposes** — sometimes a *physical* block number on disk, sometimes a *logical* block number within a file. At one point a `block` holding a logical number was used where a physical number was needed, so **an unrelated block on disk got overwritten with zeroes.**

The part that matters most is why it stayed hidden: **several people, including Ousterhout, read the faulty code and never saw it.**

> "When we saw the variable `block` used as a physical block number, we reflexively assumed that it really held a physical block number. It took a long process of instrumentation, which eventually showed that the corruption must be happening in a particular statement, before I was able to get past the mental block created by the name and check to see exactly where its value came from."

**A name creates an assumption that a reader will not re-examine.** With `fileBlock` and `diskBlock`, "it's unlikely that the error would have happened; the programmer would have known that `fileBlock` couldn't be used in that situation."

And note that `block` is not a *bad* name — "it's a pretty close match for both a physical block on disk and a logical block within a file; it's certainly not a horrible name." Being reasonably close was enough to cost six months. This is the third consistency requirement — **narrow enough that all variables with the name have the same behavior** — and this bug is why it exists.

## Worked Example — the Go style guide disagreement (§14.5)
Ousterhout presents the opposing view fairly. Some Go developers argue names should be very short, often single-character; Andrew Gerrand: **"long names obscure what the code does."** His example:
```go
func RuneCount(b []byte) int {
    i, n := 0, 0
    for i < len(b) {
        if b[i] < RuneSelf {
              i++
        } else {
              _, size := DecodeRune(b[i:])
              i += size
        }
        n++
    }
    return n
}
```
versus:
```go
func RuneCount(buffer []byte) int {
    index, count := 0, 0
    for index < len(buffer) {
        if buffer[index] < RuneSelf {
              index++
        } else {
              _, size := DecodeRune(buffer[index:])
              index += size
        }
        count++
    }
    return count
}
```
**Ousterhout's response:** he doesn't find the second harder to read; `count` gives a slightly better clue than `n`. "With the first version I ended up reading through the code trying to figure out what `n` means, whereas I didn't feel that need with the second version." **But** he concedes: if `n` is used consistently throughout the system to mean counts *and nothing else*, the short name will probably be clear.

His real objection is to the Go culture's habit of **using the same short name for multiple different things** — `ch` for character *or* channel, `d` for data *or* difference *or* distance. "To me, ambiguous names like these are likely to result in confusion and error, **just as in the `block` example.**" That is a consistency violation, not a length one.

**The resolution he proposes is a test, not a rule:** *"readability must be determined by readers, not writers."* If you write short names and readers find the code easy, fine. If you start getting complaints that your code is cryptic, use longer names. "Similarly, if I start getting complaints that long variable names make my code harder to read, then I'll consider using shorter ones." (Same principle as Ch 13's "if a reader thinks it's not obvious, then it's not obvious.")

## Key Takeaways
1. Judge a name by whether someone seeing it *in isolation* would guess correctly.
2. A good name says what the thing is **and what it is not**.
3. Two properties: precision and consistency — and consistency requires that the name's purpose be narrow enough for uniform behavior.
4. Boolean names should be predicates, so `true` is self-explanatory.
5. Short generic names are fine only when the entire span of use is visible at once; longer distance → longer name.
6. Names can also be too specific — don't bake a caller's context into a general parameter.
7. Difficulty naming something is a design smell; consider splitting the entity.
8. Never argue that your names are readable — that's the reader's call.
9. This is the investment mindset (Ch 3): frustrating and slow at first, then nearly free. "Choosing a mediocre name for a particular variable… probably won't have much impact on the overall complexity of a system. However, software systems have thousands of variables."

## Connects To
- **Ch 2**: complexity is incremental — thousands of small naming decisions compound; vague names are obscurity.
- **Ch 3**: naming as a continuous small investment.
- **Ch 13**: names and comments are complementary; a rename can beat a comment (`lineWidths` → `numLinesWithLength`).
- **Ch 15**: writing comments first surfaces hard-to-name entities early.
- **Ch 17**: consistency as a general design principle.
- **Ch 18**: good names are the first item on the list of things that make code obvious.
