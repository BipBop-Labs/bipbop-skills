# Chapter 4: Modules Should Be Deep

## Core Idea
The best modules are *deep*: a lot of functionality behind a simple interface. Module depth is cost/benefit — the interface is the cost imposed on the rest of the system, the functionality is the benefit.

## Frameworks Introduced
- **Deep vs. shallow modules** (the book's central image, Figure 4.1). Picture each module as a rectangle: area = functionality implemented, top edge = interface complexity.
  - **Deep** = large area, short top edge. Powerful functionality, simple interface. Only a small fraction of internal complexity is visible.
  - **Shallow** = interface complex relative to functionality provided. Doesn't hide much.
  - When to use: evaluating any class, method, service, or API you're about to add.
  - How: ask "is this interface *much* simpler than its implementation?" If no, redesign.
  - Why it works: two payoffs — a simple interface minimizes the complexity imposed on the rest of the system, *and* anything not in the interface can be changed later without affecting any other module.
- **Interface vs. implementation**: the interface is everything a developer in a *different* module must know to use this one — what it does, not how. The implementation carries out the interface's promises.
  - Rule for who must know what: a developer working in module M must understand M's interface and implementation, plus the interfaces of modules M invokes — and *nothing else's implementation*.
- **Formal vs. informal interface elements**:
  - **Formal** — specified in code, often language-checked: method signature (parameter names/types, return type, exceptions), public method signatures, public variable names/types.
  - **Informal** — expressible only in comments: high-level behavior (e.g. "this deletes the file named by this argument"), usage constraints (e.g. "call this before that).
  - Key claim: **for most interfaces the informal aspects are larger and more complex than the formal ones.** Rule of thumb — if a developer needs to know it to use the module, it *is* part of the interface.
- **Abstraction**: "a simplified view of an entity, which omits unimportant details." The word *unimportant* is load-bearing. Two failure modes:
  1. Including unimportant details → needlessly complicated, raises cognitive load.
  2. Omitting *important* details → obscurity. This is a **false abstraction**: looks simple, isn't.
  - How: the design task is to understand what's important, and then look for designs that *minimize the amount of information that is important*.
- **Design interfaces so the common case is as simple as possible** (design principle #5).
  - Corollary: "If an interface has many features, but most developers only need to be aware of a few of them, the effective complexity of that interface is just the complexity of the commonly used features." So bury the rare features rather than deleting them.

## Key Concepts
- **Module**: any unit of code with an interface and an implementation — a class, a method, a plain function, a subsystem, a service (interface may be kernel calls or HTTP requests).
- **Deep module**: lots of functionality, simple interface.
- **Shallow module**: interface nearly as complex as the implementation. Small modules tend to be shallow.
- **Abstraction**: simplified view omitting unimportant details.
- **False abstraction**: one that omits details that actually matter.
- **Classitis**: the belief that "classes are good, so more classes are better."

## Anti-patterns
- **Red Flag — Shallow Module**: the interface for a class or method isn't much simpler than its implementation. The benefit (not having to learn the internals) is negated by the cost of learning and using the interface.
- **Classitis**: minimizing functionality per class and adding classes when you need more. Individual classes are simple; the system gets worse. Many small classes → many interfaces → tremendous system-level complexity, plus verbose boilerplate.
- **"Any method longer than N lines should be split"** (N sometimes as low as 10): produces large numbers of shallow methods and raises overall complexity. Ousterhout names this conventional wisdom as wrong.
- **Requiring the common case to be assembled explicitly** (see the Java stream example) — error-prone, and the error is silent.

## Code Examples

**Deep — the entire Unix file I/O interface:**
```c
int     open(const char* path, int flags, mode_t permissions);
ssize_t read(int fd, void* buffer, size_t count);
ssize_t write(int fd, const void* buffer, size_t count);
off_t   lseek(int fd, off_t offset, int referencePosition);
int     close(int fd);
```
Five calls. Behind them, a modern implementation is *hundreds of thousands of lines* handling: on-disk file representation for efficient access; directory storage and hierarchical path resolution; permission enforcement; the split between interrupt handlers and background code and their safe communication; scheduling of concurrent accesses; in-memory caching of recent data; supporting disks and flash behind one file system. All invisible to callers. Implementations have changed radically over decades; **the five calls have not.** That stability is the payoff of depth.

Note the common-case design: sequential access is most common, so it's the default. Random access stays easy via `lseek`, but a developer doing only sequential I/O never needs to know `lseek` exists.

**Deepest possible — a garbage collector:** no interface at all. Adding GC *shrinks* the system's total interface, because it removes the interface for freeing objects. Enormous implementation complexity, zero exposed surface.

**Shallow — the extreme case** (from a student project):
```java
private void addNullValueForAttribute(String attribute) {
    data.put(attribute, null);
}
```
Every bit of functionality is visible through the interface. Callers probably need to know the value lands in `data`. It's no simpler to think about the interface than the implementation. Documented properly, the doc comment would be longer than the body. It even takes *more keystrokes* to call than to manipulate `data` directly. Pure cost, no benefit.

**Shallow — classitis in the Java library.** To read serialized objects from a file:
```java
FileInputStream fileStream =
        new FileInputStream(fileName);
BufferedInputStream bufferedStream =
        new BufferedInputStream(fileStream);
ObjectInputStream objectStream =
        new ObjectInputStream(bufferedStream);
```
Three objects for one conceptual operation. `FileInputStream` alone can't buffer or handle serialized objects; each wrapper adds one capability. The first two locals are never used again — everything goes through `objectStream`.

The real damage is that **buffering must be requested explicitly**. Forget the `BufferedInputStream` and there's no error, just slow I/O. The defense ("not everyone wants buffering, so keep it separate and let people choose") mistakes choice for good design: almost every user of file I/O wants buffering, so it should be the default, with a cleanly separated mechanism to disable it — a different constructor, or a method that disables or replaces buffering — so most developers never learn it exists.

## Reference Table

| | Deep module | Shallow module |
|---|---|---|
| Interface vs. implementation | Interface much simpler | Comparable complexity |
| Complexity imposed on system | Small | Large relative to benefit |
| Freedom to change internals | Large — much is hidden | Small — most is exposed |
| Examples | Unix I/O (5 calls), garbage collector | `addNullValueForAttribute`, linked-list class, Java stream wrappers |
| Typical cause | Designing for the common case | Classitis, "split every method over N lines" |

## Key Takeaways
1. Judge a module by the *ratio* of its interface complexity to its functionality — not by its size.
2. "Interfaces are good, but more, or larger, interfaces are not necessarily better."
3. Anything a caller must know is part of the interface, including the informal parts — which are usually the bigger half.
4. Design the interface so the **common case is simplest**; make rare features available but invisible.
5. Prefer one deep class over several shallow ones; resist classitis and mechanical line-count splitting.
6. Watch for false abstractions — simple-looking interfaces that hide details callers actually need.
7. A stable interface over a radically evolving implementation (Unix I/O) is what depth buys you.

## Connects To
- **Ch 5**: information hiding — the technique that makes modules deep.
- **Ch 6**: general-purpose modules are deeper.
- **Ch 7**: different layers should have different abstractions (pass-through methods are shallow).
- **Ch 8**: pull complexity downward — make the *implementation* absorb complexity to keep the interface simple.
- **Ch 10**: define errors out of existence — removing exceptions from an interface deepens it.
- **Ch 19**: the "many small classes/methods" convention this chapter contradicts.
