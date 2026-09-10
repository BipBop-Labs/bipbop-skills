# Chapter 9: Better Together Or Better Apart?

## Core Idea
Subdivision is not free — it adds interfaces, management code, separation, and duplication — so combine code when it's closely related, separate it when it isn't, judging by information hiding, dependencies, and interface depth.

## Frameworks Introduced
- **The four costs of subdivision** (the case *against* reflexive splitting):
  1. **Number of components** — more components are harder to track and harder to search; subdivision usually means more interfaces, and every interface adds complexity.
  2. **Management code** — code that used one object may now have to manage several.
  3. **Separation** — subdivided components end up farther apart, possibly in different files. If the components are truly independent, separation is *good* (focus on one at a time). **If there are dependencies, separation is bad**: developers flip back and forth, and — worse — may not notice the dependencies at all, which leads to bugs.
  4. **Duplication** — code present once before may be needed in each component.
- **Four indications two pieces of code are related** (i.e. belong together):
  1. **They share information** — e.g. both depend on the syntax of a particular document type.
  2. **They are used together** — anyone using one is likely to use the other. **Only compelling if bidirectional.** Counter-example: a disk block cache almost always uses a hash table, but hash tables serve many purposes unrelated to block caches — so keep them separate.
  3. **They overlap conceptually** — a simple higher-level category covers both. Substring search and case conversion are both string manipulation; flow control and reliable delivery are both network communication.
  4. **It is hard to understand one without looking at the other.**
- **Four reasons to bring code together:**
  - **§9.1 Shared information** — the HTTP read/parse case (Ch 5): reading a request requires parsing most of it, so both halves knew the format. Combined, "the code got shorter and simpler."
  - **§9.2 Simpler interface** — combining eliminates the interface that passed intermediate state between the parts (the request string). It also lets you do things **automatically**: a combined `FileInputStream` with buffering by default means "the vast majority of users would never even need to be aware of the existence of buffering," with methods to disable or replace it that most users never learn.
  - **§9.3 Eliminate duplication** — two techniques below.
  - **§9.8 Join methods** — replace two shallow methods with one deeper one; eliminate duplication, dependencies, or intermediate data structures; improve encapsulation; or simplify the interface.
- **Two ways to eliminate duplication (§9.3):**
  1. **Factor the repeated code into a method.** Most effective when the snippet is **long** and the replacement method has a **simple signature**. Weak when the snippet is only one or two lines, or when it interacts complexly with its environment (accessing numerous locals) so the extracted method needs a complex signature — e.g. many pass-by-reference arguments.
  2. **Restructure so the snippet executes in only one place.** Ousterhout's example: a method that returns errors at several points, each needing the same cleanup first. Move the cleanup to the end of the method and `goto` it from each error-return point (Figures 9.1→9.2). His judgment: "Goto statements are generally considered a bad idea, and they can result in indecipherable code if used indiscriminately, but they are useful in situations like this where they are used to escape from nested code."
- **Separate general-purpose from special-purpose code (§9.4)** — design principle #8.
  - The rule: a module containing a general-purpose mechanism should provide *just* that mechanism — no code specializing it for a particular use, and no other general-purpose mechanisms. Special-purpose code belongs in a different module, typically the one associated with that purpose.
  - **The direction is upward:** lower layers tend to be general-purpose, upper layers special-purpose (the topmost layer is entirely application-specific). So separate by **pulling special-purpose code up into higher layers, leaving the lower layers general-purpose.**
  - When you find a class with both general- and special-purpose features for the same abstraction, try splitting into two classes, the special-purpose one layered on the general one.
  - **Important scoping caveat:** this applies to code *related to one mechanism*. It's often fine to combine special-purpose code for one mechanism with general-purpose code for another. The text class is the example: general-purpose text management *plus* special-purpose undo code for text modifications. That undo code shouldn't go into the general `History` infrastructure, but it belongs in the text class because it's closely related to the other text functions.
- **Method design: "Each method should do one thing and do it completely."** The method should have a clean simple interface so callers needn't hold much in their heads, and should be deep. **"If a method has all of these properties, then it probably doesn't matter whether it is long or not."**
- **The two valid method splits (Figure 9.3):**
  - **(b) Extract a subtask** — *the best way.* Produces a child with the subtask and a parent with the remainder; the parent's interface is unchanged. Valid when the subtask is cleanly separable, meaning **(a) someone reading the child needn't know anything about the parent, and (b) someone reading the parent needn't understand the child's implementation.** Typically the child is relatively general-purpose — conceivably usable by other methods. **If after splitting you find yourself flipping between parent and child to understand how they work together, that's the Conjoined Methods red flag and the split was probably wrong.**
  - **(c) Split into two methods both visible to callers** — valid only when the original interface was overly complex because it did multiple unrelated things. Each resulting interface must be **simpler than the original**, and ideally **most callers invoke only one of the two**. It's a good sign if the new methods are more general-purpose than the original. This "doesn't make sense very often," and risks landing in **(d): several shallow methods**. If callers must invoke both and pass state between them, don't split. Judge it purely by whether it simplifies things for callers.

## Key Concepts
- **Subdivision cost**: the complexity created by the act of splitting, absent before.
- **Bidirectional use**: both pieces imply each other — the only version of "used together" that justifies combining.
- **Fence**: a marker in a history list separating groups of related actions.
- **Special-general mixture**: a general mechanism carrying code specialized to one of its uses.
- **Conjoined methods**: two methods neither of which can be understood alone.

## Anti-patterns
- **Red Flag — Repetition**: the same code, or nearly the same, appearing over and over means you haven't found the right abstractions.
- **Red Flag — Special-General Mixture**: a general-purpose mechanism containing code specialized for one particular use. Makes the mechanism more complicated and creates information leakage between mechanism and use case — future changes to the use case will require changes to the underlying mechanism.
- **Red Flag — Conjoined Methods**: you can't understand one method's implementation without understanding another's. Generalizes beyond methods: **any two physically separated pieces of code where each can only be understood by looking at the other.**
- **"Split up any method longer than 20 lines!"** — "length by itself is rarely a good reason for splitting up a method. In general, developers tend to break up methods too much."
- **Wrapper methods for logging** — see the example below.

## Code Examples

**Bad — a separate class of one-line logging methods:**
```java
try {
    rpcConn = connectionPool.getConnection(dest);
} catch (IOException e) {
    NetworkErrorLogger.logRpcOpenError(req, dest, e);
    return null;
}
```
```java
private static class NetworkErrorLogger {
    /**
     *  Output information relevant to an error that occurs when trying
     *  to open a connection to send an RPC.
     *
     *  @param req
     *       The RPC request that would have been sent through the
     *       connection
     *  @param dest
     *       The destination of the RPC
     *  @param e
     *       The caught error
     */
    public static void logRpcOpenError(RpcRequest req, AddrPortTuple
                  dest, Exception e) {
        logger.log(Level.WARNING, "Cannot send message: " + req + ". \n" +
                "Unable to find or open connection to " + dest + " :" +
                e);
    }
...
}
```
The class held several such methods (`logRpcSendError`, `logRpcReceiveError`, …). "This separation added complexity with no benefit": each method is one line but needs substantial documentation; each is invoked in exactly one place; and they're **conjoined** with their call sites in both directions — a reader of the call site flips to the logging method to check what's logged, and a reader of the logging method flips to the call site to learn its purpose.
→ Fix: delete the logging methods and put the logging statements where the errors are detected.

**Good — extracting the general-purpose core of undo:**
```java
public class History {
    public interface Action {
        public void redo();
        public void undo();
    }

    History() {...}

    void addAction(Action action) {...}
    void addFence() {...}

    void undo() {...}
    void redo() {...}
}
```
`History` manages a collection of `History.Action` objects and **knows nothing about what they store or how they undo/redo**. It maintains a list of all actions executed over the application's lifetime and walks backwards/forwards through it. Grouping uses **fences**: each undo walks back through the list undoing actions until it reaches the next fence, and higher-level code decides where fences go via `addFence`.

## Worked Example — the editor undo mechanism (§9.7)
Requirement: multi-level undo/redo not just for text but for the selection, insertion cursor, and view. Select text, delete it, scroll elsewhere, undo → the editor must restore the deleted text, reselect it, and scroll it back into view.

**What students did:** put the whole mechanism in the text class. The text class held the undoable-change list, added entries automatically on text changes, and exposed extra methods so the UI could add entries for selection/cursor/view changes. On undo, the UI called into the text class, which processed entries — handling text entries internally and **calling back into the UI** for the others.

**Why it was wrong:** the general-purpose core (managing a list of executed actions and stepping through it) sat in the text class alongside special-purpose handlers for text and selection. The selection/cursor handlers had nothing to do with anything else in the text class. Consequences: information leakage between the text class and the UI, extra methods in each module to pass undo information back and forth, and **any new undoable entity would require changes to the text class**, including new entity-specific methods.

**The fix and its shape:** extract the general-purpose core into `History`. That single decision splits undo into three independently implementable categories:

| Category | Implemented in | Knows about |
|---|---|---|
| General mechanism for managing/grouping actions and invoking undo/redo | `History` class | Nothing about specific action types — reusable across applications |
| Specifics of particular actions | Many small classes: `UndoableInsert`, `UndoableDelete` (text class), `UndoableSelection`, `UndoableCursor` (UI code) | One kind of action each |
| Policy for grouping actions | High-level UI code, via `History.addFence` | Overall application behavior |

Ousterhout's summary: **"The key design decision was the one that separated the general-purpose part of the undo mechanism from the special-purpose parts and put the general-purpose part in a class by itself. Once that was done, the rest of the design fell out naturally."**

## Worked Example — cursor and selection: related, but not enough (§9.5)
The editor showed a blinking insertion cursor (always visible) and a selection (sometimes empty). They're genuinely related: the cursor always sits at one end of the selection; click-drag sets both; text insertion first deletes the selection then inserts at the cursor. One team therefore used a single object storing two file positions plus booleans for which end was the cursor and whether a selection existed.

It was awkward:
- **No benefit to higher-level code** — the UI still treated them as distinct entities and manipulated them separately (delete the selected text via one method, then retrieve the cursor position via another to insert).
- **More complex to implement than separate objects** — it avoided storing the cursor position directly, but had to store a boolean for which end was the cursor, and testing that boolean to answer "where is the cursor?"

Separating them simplified both usage and implementation. And the revised version used **no special classes for either**: a new general-purpose `Position` class (line number + character within line) represented a location; the selection became two `Position`s and the cursor one. `Position` then found other uses in the project.

The lesson: "related in some ways" is not the test. Ask whether combining actually simplifies callers and the implementation.

## Key Takeaways
1. Subdivision has real costs — count them before splitting; more, smaller components is not automatically simpler.
2. Combine when code shares information, is *bidirectionally* used together, overlaps conceptually, or can't be understood separately.
3. Combining often both simplifies the interface *and* lets you do things automatically that callers no longer need to know about.
4. Separate general-purpose from special-purpose code **for the same mechanism**, pulling the special-purpose part upward.
5. Method length is not a splitting criterion; "each method should do one thing and do it completely," and long deep methods are fine.
6. Prefer extract-a-subtask splits, and only when parent and child can each be read without the other.
7. Treat Repetition, Special-General Mixture, and Conjoined Methods as stop-and-redesign signals.
8. Decide split-vs-join by which structure gives the best information hiding, fewest dependencies, and deepest interfaces.

## Connects To
- **Ch 4**: shallow methods are the failure mode of over-splitting; depth is the criterion.
- **Ch 5**: shared information → leakage; this chapter's §9.1 is the general form of the HTTP example.
- **Ch 6**: general-purpose interfaces; `Position` replacing `Cursor` recurs here.
- **Ch 7**: the four pass-through refactorings (expose/redistribute/merge) are instances of this decision.
- **Ch 19**: the "small classes and methods" convention, and design patterns.
