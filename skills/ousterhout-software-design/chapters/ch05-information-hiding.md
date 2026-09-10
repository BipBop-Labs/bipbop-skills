# Chapter 5: Information Hiding (and Leakage)

## Core Idea
The most important technique for achieving deep modules is information hiding: each module encapsulates a few design decisions in its implementation that never appear in its interface.

## Frameworks Introduced
- **Information hiding** (Parnas, 1972). Each module encapsulates a few pieces of knowledge representing design decisions, embedded in the implementation and invisible in the interface.
  - Examples of hideable knowledge: how to store and efficiently access a B-tree; how to map a logical file block to a physical disk block; how to implement TCP; how to schedule threads on a multi-core processor; how to parse JSON. It includes data structures and algorithms, low-level details (page size), and high-level assumptions ("most files are small").
  - When to use: whenever designing a new module — ask "what information can be hidden here?"
  - Why it works, two ways: (1) simplifies the interface, lowering cognitive load; (2) makes evolution easy — nothing outside the module depends on hidden information, so a change to it affects one module. If TCP adds a new congestion-control mechanism, the implementation changes and higher-level senders/receivers don't.
- **`private` ≠ information hiding.** Private members *help*, but information about them can still be fully exposed through public getters and setters — at which point the variable's nature and usage are as exposed as if it were public.
- **Partial information hiding is still valuable.** If a feature is needed by only a few users and reached through separate methods so it's invisible in the common case, it's mostly hidden and creates far fewer dependencies. Defaults are the canonical instance.
- **Information leakage** — the opposite, and "one of the most important red flags in software design."
  - Definition: a design decision is reflected in multiple modules, creating a dependency — change the decision, change every involved module.
  - Two forms: **through an interface** (if information appears in the interface, it is by definition leaked), and **back-door leakage** — e.g. two classes that both know a file format, one reading and one writing, neither exposing it. Back-door leakage is *more pernicious because it isn't obvious.*
  - How to fix: ask "How can I reorganize these classes so that this knowledge only affects a single class?" Two moves: (a) **merge** the classes, if they're small and closely tied to the leaked information; (b) **extract** the information into a new class — but only if you can find a simple interface that abstracts the details. Otherwise you've merely traded back-door leakage for interface leakage.
- **Information hiding can often be improved by making a class slightly larger.** Two reasons: bring together all code related to one capability, and raise the level of the interface (one method for a whole computation rather than three for its steps). Ch 9 covers the limits.

## Key Concepts
- **Information hiding**: encapsulating design decisions inside a module's implementation.
- **Information leakage**: the same knowledge reflected in multiple modules.
- **Back-door leakage**: shared knowledge that appears in no interface — hence invisible.
- **Temporal decomposition**: module structure mirroring execution order.
- **Overexposure**: an API that forces users of common features to learn rare ones.

## Anti-patterns
- **Red Flag — Information Leakage**: the same knowledge used in multiple places (two classes that both understand one file format).
- **Red Flag — Temporal Decomposition**: execution order reflected in code structure; operations happening at different times live in different methods or classes. If the same knowledge is used at different points in execution, it gets encoded in multiple places → leakage.
  - Why it's tempting: the order operations must occur in is what's on your mind while coding.
  - The corrective rule: **"When designing modules, focus on the knowledge that's needed to perform each task, not the order in which tasks occur."** Order usually does matter and will be reflected *somewhere* — just not in the module structure, unless the stages genuinely use totally different information.
- **Red Flag — Overexposure**: an API for a commonly used feature forces users to learn about rarely used features, raising cognitive load for people who don't need them.
- **Exposing internal data structures** through a getter that returns the internal collection.
- **Inadequate defaults**: requiring the caller to supply a value they're unlikely to know.

## Code Examples

**Bad — leaking the internal representation** (student HTTP projects):
```java
public Map<String, String> getParams() {
    return this.params;
}
```
Four separate problems: it's shallow; it exposes the internal representation, so any representation change (often done for performance) breaks the interface and all callers; the caller must make two calls (get the map, then look up a key); and callers must somehow *know* not to modify the returned `Map`, since doing so mutates the request's internal state.

**Better:**
```java
public String getParameter(String name) { ... }
public int getIntParameter(String name) { ... }
```
`getParameter` hides the internal representation. `getIntParameter` also absorbs the string→int conversion, hiding that mechanism from the caller. Add `getDoubleParameter` etc. as needed. (Both throw if the parameter is missing or unconvertible; declarations elided.)

## Worked Example — the HTTP server projects
Students implemented HTTP request handling. Four lessons, two good and two bad:

**Mistake 1 — too many classes (§5.5).** One team used two classes to receive a request: one read it from the socket into a string, a second parsed the string. Classic temporal decomposition — "first we read, then we parse." But **an HTTP request can't be read without parsing much of it**: `Content-Length` specifies the body length, so you must parse headers to know the total request length. Result: both classes understood most of the request structure and parsing code was *duplicated in both*. Callers also had to invoke two methods in two classes in a specific order.
→ Fix: merge into one class handling reading and parsing. All knowledge of the request format is isolated, and callers invoke one method. The merged class is *deeper* than either original.

**Good choice 1 — hiding where parameters came from.** Server code doesn't care whether a parameter appeared in the first line or the body, so students merged both sources and hid the distinction.

**Good choice 2 — hiding URL encoding.** The parser decodes before returning, so `comment` comes back as `What a cute baby!`, not `What+a+cute+baby%21`.

**Mistake 2 — inadequate defaults (§5.7).** One team required callers to specify the HTTP protocol version when creating a response. But the response version must match the request's, and the request is *already* passed when sending the response (it says where to send it). So the library can supply it automatically. A caller is unlikely to know the right value, and making them specify it leaks information between library and caller. Same for the `Date` header — the library should default it.

The governing rule: **"Whenever possible, classes should 'do the right thing' without being explicitly asked."** The Java buffering example (Ch 4) is the negative case — buffering is so universally desirable that no one should have to ask for it or even know it exists. **"The best features are the ones you get without even knowing they exist."**

## Key Takeaways
1. Ask of every new module: what knowledge can be hidden here? More hidden → simpler interface → deeper module.
2. Making things `private` is not information hiding if getters/setters expose them anyway.
3. Develop high sensitivity to information leakage; it is among the most important red flags.
4. Watch for back-door leakage — shared knowledge in no interface — because nothing points at it.
5. Decompose by *knowledge needed*, not by *order of operations*.
6. Merging two leaky classes, or making one class slightly larger, often improves hiding and deepens the interface.
7. Provide defaults; don't ask callers for values they can't sensibly know.
8. **Taking it too far (§5.9)**: information hiding only makes sense when the information isn't needed outside the module. If callers genuinely need to tune performance-affecting configuration parameters, expose them. Minimize what's needed outside (self-tuning beats exposed knobs), but *recognize* what's needed and expose it.
9. Apply hiding *within* a class too: design private methods to each encapsulate a capability, and minimize the number of places each instance variable is used.

## Connects To
- **Ch 4**: hiding is the mechanism that makes modules deep; not hiding much guarantees shallowness.
- **Ch 6**: general-purpose interfaces hide more than special-purpose ones.
- **Ch 7**: interface should differ from implementation — a direct corollary.
- **Ch 9**: when it *is* right to split classes, bounding the "make the class larger" advice.
- **Parnas 1972**, "On the Criteria to be Used in Decomposing Systems into Modules" — the original source.
