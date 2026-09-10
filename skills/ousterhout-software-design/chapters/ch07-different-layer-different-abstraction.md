# Chapter 7: Different Layer, Different Abstraction

## Core Idea
In a well-designed layered system the abstraction changes with every method call; adjacent layers with *similar* abstractions are a red flag that the class decomposition is wrong.

## Frameworks Introduced
- **The "different layer, different abstraction" rule.** Follow an operation up and down through layers — the abstraction should change at each call.
  - Healthy examples: a file system's top layer offers a variable-length byte array read/written in byte ranges; below it, a cache of fixed-size disk blocks; below that, device drivers moving blocks between storage and memory. Or TCP: a reliably delivered byte stream on top of best-effort bounded-size packets that may be lost or reordered.
- **The net-gain test for design infrastructure** — the chapter's most general and most useful idea.
  - "Each piece of design infrastructure added to a system, such as an interface, argument, function, class, or definition, adds complexity, since developers must learn about this element. In order for an element to provide a net gain against complexity, it must eliminate some complexity that would be present in the absence of the design element."
  - How to apply: for any class/method/argument you're about to add, name the complexity it *removes*. If you can't, don't add it. The "different layer, different abstraction" rule is just this test applied to layers.
- **Four refactorings for pass-through methods** (Figure 7.1). Given C1 whose methods just call same-signature methods in C2:
  1. **(b) Expose C2 directly** to C1's callers, removing C1's responsibility for the feature entirely.
  2. **(c) Redistribute functionality** between C1 and C2 to avoid the calls between them.
  3. **(d) Merge** the classes, if they can't be disentangled.
  - Diagnostic question to pick one: "Exactly which features and abstractions is each of these classes responsible for?" You'll usually find overlapping responsibility.
- **When same-signature methods are fine**: the test is whether each method contributes significant functionality.
  - **Dispatchers** — a method that uses its arguments to select one of several other methods and passes most or all arguments along. Same signature, real functionality: it *chooses*. (A web server examining an incoming URL to decide between returning a file and invoking PHP/JavaScript; the rule-matching can be intricate.)
  - **Multiple implementations of one interface** — e.g. disk drivers. Each supports a different device behind an identical interface. This *reduces* cognitive load: having used one, you can use the others without learning a new interface. Such methods are usually in the same layer and don't invoke each other.
- **Interface should differ from implementation (§7.4)**: the internal representation should differ from the abstraction in the interface. If they're similar, the class probably isn't deep — and that difference *is* the value the class provides.
- **Context object (§7.5)** — the author's preferred fix for pass-through variables.
  - What: one object per system instance holding all application global state — configuration options, shared subsystems, performance counters.
  - How to keep it from becoming a pass-through variable itself: store a reference to the context as an instance variable in most major objects. When creating a new object, pass the context from the creator's own reference to the constructor. The context is then available everywhere but **appears as an explicit argument only in constructors**.
  - Benefits: adding a new global affects only the context's constructor/destructor; global state is identifiable in one place; multiple instances can coexist in one process; tests can reconfigure the application by setting context fields.

## Key Concepts
- **Pass-through method**: does almost nothing except pass its arguments to another method with a similar or identical signature.
- **Dispatcher**: selects among several methods and forwards arguments — legitimate same-signature duplication.
- **Decorator / wrapper**: takes an existing object and extends its functionality behind a similar or identical API.
- **Pass-through variable**: a variable threaded down a long chain of methods that don't use it.
- **Context**: an object holding all of a system instance's global state.

## Anti-patterns
- **Red Flag — Pass-Through Method**: does nothing except pass its arguments to another method, usually with the same API. Indicates there is not a clean division of responsibility between the classes.
  - Costs: makes classes **shallower** (adds interface complexity, adds no functionality) and creates dependencies — change `TextArea.insertString`'s signature and `TextDocument.insertString` must change to match.
  - Underlying cause: confusion over division of responsibility. **"The interface to a piece of functionality should be in the same class that implements the functionality."**
- **Overusing decorators**: a new class for every small feature → an explosion of shallow classes (the Java I/O example). Decorators "tend to be shallow: they introduce a large amount of boilerplate for a small amount of new functionality" and often contain many pass-through methods.
- **Interface mirroring the internal representation** (a line-oriented API over line-oriented storage): forces every caller to split and join lines, and that nontrivial code gets duplicated and scattered across the UI.
- **Pass-through variables**: force all intermediate methods to know about a variable they have no use for; adding one later can mean modifying a large number of interfaces and methods along every relevant path.
- **Global variables as the fix for pass-through variables**: "almost always create other problems" — notably you can no longer create two independent instances of the system in one process, which matters most for *testing*.

## Code Examples

**Pass-through methods** — from a student GUI text editor. **13 of the class's 15 public methods were pass-throughs:**
```java
public class TextDocument ... {
    private TextArea textArea;
    private TextDocumentListener listener;
    ...
    public Character getLastTypedCharacter() {
        return textArea.getLastTypedCharacter();
    }
    public int getCursorOffset() {
        return textArea.getCursorOffset();
    }
    public void insertString(String textToInsert,
              int offset) {
        textArea.insertString(textToInsert, offset);
    }
    public void willInsertString(String stringToInsert, int offset) {
        if (listener != null) {
            listener.willInsertString(this, stringToInsert, offset);
        }
    }
    ...
}
```
Of the four shown, only the last has any functionality — and it merely null-checks one variable. `TextDocument` offers `insertString` while `TextArea` implements all of it.

**The fix:** three classes with intertwined responsibilities (`TextDocument`, `TextArea`, `TextDocumentListener`) became **two**, by moving methods between them and collapsing — with clearly differentiated responsibilities.

## Reference Table — before creating a decorator, try these (§7.3)

| Alternative | When it applies |
|---|---|
| Add the functionality directly to the underlying class | The functionality is fairly general-purpose, logically related to the class, or most users will want it. (Virtually everyone creating a Java `InputStream` also creates a `BufferedInputStream`, and buffering is a natural part of I/O — those should have been one class.) |
| Merge it with the specific use case | The functionality is specialized for one caller |
| Merge it into an *existing* decorator | Yields one deeper decorator instead of several shallow ones |
| Implement as a stand-alone class, not a wrapper | The functionality needn't wrap the base at all — scrollbars can probably be built separately from the window rather than wrapping all its functionality |

"Sometimes decorators make sense, but there is usually a better alternative."

## Worked Example — eliminating a pass-through variable (Figure 7.2)
A datacenter service takes a command-line argument describing certificates for secure communication. Only the low-level method `m3` needs it — it calls a library to open a socket — but `cert` is threaded from `main` through `m1` and `m2`, appearing in every intermediate signature.

Four options, in the order Ousterhout evaluates them:

**(a) Pass it through** — the problem. `m1` and `m2` must know about a variable they never use.

**(b) Store it in an object already shared by `main` and `m3`** — e.g. an existing object holding other network-communication information. Good if such an object exists. The catch: *"if there is such an object, then it may itself be a pass-through variable (how else does m3 get access to it?)."*

**(c) Make it a global variable** — avoids the threading, but breaks multiple independent instances in one process, which you want for testing.

**(d) A context object** — the author's usual choice. `cert` joins other system-wide state (timeout values, performance counters) in a context; objects whose methods need it store a context reference, so it appears as an explicit argument only in constructors.

Ousterhout is candid that (d) is imperfect: *"Contexts are far from an ideal solution."* Context variables have most of the disadvantages of globals — it may not be obvious why a variable is there or where it's used. Without discipline a context becomes "a huge grab-bag of data that creates nonobvious dependencies throughout the system." It can also create thread-safety issues; **the best defense is making context variables immutable**. "Unfortunately, I haven't found a better solution than contexts."

## Key Takeaways
1. If two adjacent layers have the same abstraction, the decomposition is probably wrong.
2. For every element you add (class, method, argument, interface), name the complexity it removes — otherwise omit it.
3. Pass-through methods add interface complexity and zero functionality; refactor by exposing, redistributing, or merging.
4. Put the interface to a piece of functionality in the class that implements it.
5. Same signatures are fine when each method does something distinct — dispatchers and multiple implementations of one interface.
6. Design the interface around a *different* abstraction than the internal representation; that difference is the class's value.
7. Try the four alternatives before writing a decorator.
8. Prefer a context object over pass-through variables or globals — and keep its contents immutable and disciplined.

## Connects To
- **Ch 4**: pass-through methods and decorators are how classes become shallow.
- **Ch 5**: interface mirroring implementation is a form of information leakage.
- **Ch 6**: the character-oriented-API-over-line-storage example continues the text-class thread.
- **Ch 8**: pull complexity downward — the positive version of "give the lower layer real work."
- **Ch 9**: when to merge vs. separate classes, formalizing the refactorings here.
- **Ch 19**: design patterns (including decorator) applied uncritically.
