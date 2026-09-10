# Chapter 11: Design it Twice

## Core Idea
Your first idea about how to structure a module is unlikely to be the best; consider multiple radically different options for each major design decision, list their pros and cons, and often synthesize something better than any of them.

## Frameworks Introduced
- **Design it twice.** For each major design decision, sketch **two or more alternatives** before committing.
  - **Pick approaches that are radically different from each other** — "you'll learn more that way."
  - **Do it even when you're sure there's only one reasonable approach.** Consider a second design "no matter how bad you think it will be. It will be instructive to think about the weaknesses of that design and contrast them with the features of other designs."
  - Depth of sketch: you don't need to pin down every feature — **sketching a few of the most important methods is sufficient.**
  - Then **make a list of the pros and cons of each.**
- **The comparison criteria**, in priority order:
  1. **Ease of use for higher-level software** — "the most important consideration for an interface."
  2. Does one alternative have a **simpler interface**?
  3. Is one **more general-purpose**?
  4. Does one enable a **more efficient implementation**?
- **The three possible outcomes** of the comparison:
  1. The best choice is one of the alternatives.
  2. You **combine features of multiple alternatives** into a new design better than any original.
  3. **None is attractive** — then generate additional schemes, using the problems you identified to drive the new design.
- **Apply it at every level.** For a module: first to pick the interface, then **again for the implementation** — with different goals. For the interface, ease of use dominates; **for the implementation, "the most important things are simplicity and performance."** Also useful for choosing user-interface features and for decomposing a system into major modules.
- **The cost.** "Designing it twice does not need to take a lot of extra time." For a class, **an hour or two** to consider alternatives — trivial against the days or weeks of implementation. For larger modules the exploration takes longer, but so does the implementation, and the benefit of a better design is larger too.

## Key Concepts
- **Design alternative**: a rough sketch of an approach, a few key methods deep.
- **Gap buffer**: one of the candidate text-storage implementations (alongside a linked list of lines and fixed-size character blocks).

## Mental Models
- **"No-one is good enough to get it right with their first try"** for the design of large software systems.
- The process is a **skill-builder, not just an output-improver**: "the process of devising and comparing multiple approaches will teach you about the factors that make designs better or worse. Over time, this will make it easier for you to rule out bad designs and hone in on really great ones."
- Difficulty is the good news: "it's much more fun to work on a difficult problem where you have to think carefully, rather than an easy problem where you don't have to think at all."

## Anti-patterns
- **Implementing the first idea that comes to mind.** Ousterhout's observation about why smart people resist this chapter is worth quoting: growing up, smart people find their first quick idea earns a good grade, so they never learn to consider a second. Promoted into harder and harder problems, **everyone eventually reaches the point where first ideas are no longer good enough.** He sees smart people insisting on the first idea, which "causes them to underperform their true potential (it also makes them frustrating to work with)." The suspected cause: a subconscious belief that *smart people get it right the first time*, so trying multiple designs would prove they aren't smart. **"This is not the case. It isn't that you aren't smart; it's that the problems are really hard!"**

## Worked Example — the editor text class interface
Three radically different candidates for the class managing a file's text:

| Alternative | Shape | Cost to higher-level software | Other factors |
|---|---|---|---|
| **Line-oriented** | insert/modify/delete whole lines | Must **split and join lines** for partial-line and multi-line operations like cutting and pasting the selection | Simple interface |
| **Character-oriented** | insert/delete individual characters | Must write **loops** for any operation touching more than one character | Simple interface, but **likely significantly slower** — a separate call into the text module per character |
| **Range/string-oriented** | operate on arbitrary character ranges that may cross line boundaries | None of the above | The winner |

The reasoning that produces the third option is the part to imitate. Suppose you considered only line- and character-oriented. Both are awkward, **and awkward in the same way: each requires higher-level software to perform additional text manipulations.** That shared symptom is a red flag — *if there's going to be a text class, it should handle all of the text manipulation.* To eliminate the extra manipulation, the text interface must match the operations actually happening in higher-level software, and **those operations correspond to neither single characters nor single lines.** That line of reasoning lands on the range-oriented API.

Then design it twice **again** for the implementation, where simplicity and performance are what matter: a linked list of lines, fixed-size blocks of characters, or a gap buffer.

## Key Takeaways
1. Sketch at least two radically different alternatives for every major design decision.
2. Do it even when you're certain — the weak alternative teaches you about the strong one.
3. A few key method signatures per alternative is enough; don't fully specify them.
4. Judge interfaces primarily by ease of use for callers; judge implementations by simplicity and performance.
5. Look for the synthesis: the best design is often a combination, or a fourth option the comparison reveals.
6. When alternatives share a weakness, that shared weakness is the clue to the better design.
7. An hour or two per class is the actual cost — it pays for itself against weeks of implementation.
8. Needing a second design is evidence the problem is hard, not that you aren't smart.

## Connects To
- **Ch 3**: this is the highest-leverage *proactive* investment in strategic programming (design principle #12).
- **Ch 6–8**: the range-oriented text API is the design that Chapters 6, 7, and 8 each independently arrive at.
- **Ch 20**: "design around the critical path" is design-it-twice applied to performance.
