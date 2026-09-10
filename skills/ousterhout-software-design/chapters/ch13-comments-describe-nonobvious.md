# Chapter 13: Comments Should Describe Things that Aren't Obvious from the Code

## Core Idea
The guiding principle: **comments should describe things that aren't obvious from the code** — which means they must sit at a *different level of detail* than the code, either lower (adding precision) or higher (adding intuition).

## Frameworks Introduced
- **The four comment categories, and the rule for each (§13.1):**

| Category | What it is | Rule |
|---|---|---|
| **Interface** | Block immediately preceding a class, data structure, function, or method declaration | **Required.** Every class and every method gets one |
| **Data structure member** | Next to a field declaration (instance or static variable) | **Required.** Every class variable gets one |
| **Implementation** | Inside a method, describing how the code works internally | **Often unnecessary** (§13.6) |
| **Cross-module** | Describes dependencies crossing module boundaries | **Rarest, hardest to place, very important when needed** (§13.7) |

  The first two are the most important. Occasionally a declaration is so obvious there's nothing to add (getters and setters sometimes qualify), but this is rare — **"it is easier to comment everything rather than spend energy worrying about whether a comment is needed."**
- **Pick conventions first.** If your language has a doc-compilation tool — Javadoc, Doxygen, godoc — follow its conventions: "None of these conventions is perfect, but the tools provide enough benefits to make up for that." Otherwise adopt conventions from a similar language or project. Conventions serve two purposes: **consistency**, and **ensuring you actually write comments** — "if you don't have a clear idea what you are going to comment and how, it's easy to end up writing no comments at all."
- **The two useful directions for comments:**
  - **Lower level → precision.** Most useful for variable declarations (instance variables, method arguments, return values), where name and type are typically not very precise.
  - **Higher level → intuition.** Omits details, conveys overall intent and structure. Used inside methods and for interface comments.
  - **Same level as the code → repeats the code.** This is the failure mode.
- **The precision checklist for variable declarations (§13.3)** — what a name and type can't say:
  - What are the **units**?
  - Are boundary conditions **inclusive or exclusive**?
  - If **null** is permitted, what does it imply?
  - If it refers to a resource that must be **freed or closed, who is responsible**?
  - Are there **invariants** — e.g. "this list always contains at least one entry"?
  - Scope note: "when I say that the comment for a declaration should describe things that aren't obvious from the code, 'the code' refers to the code next to the comment (the declaration), not 'all of the code in the application.'"
- **"When documenting a variable, think nouns, not verbs."** Focus on what the variable *represents*, not how it's manipulated. A comment that mirrors the code structure ("toggled to TRUE when…, toggled to FALSE when…") is both longer and less useful than one stating the meaning — from which the toggling is inferable.
- **The three questions for writing a higher-level comment** (harder than lower-level, because you must think about the code differently):
  1. **What is this code trying to do?**
  2. **What is the simplest thing you can say that explains everything in the code?**
  3. **What is the most important thing about this code?**
  - A good higher-level comment "expresses one or a few simple ideas that provide a conceptual framework, such as 'append to an existing RPC.'"
  - Why this is the hard part: "Engineers tend to be very detail-oriented… But, great software designers can also step back from the details and think about a system at a higher level… **This is the essence of abstraction.**"
- **"How we get here" comments.** Beyond describing *what* code does, explain *why it is executed* — "very useful for helping people to understand code." When documenting a method, describe the conditions under which it's likely to be invoked, **especially if it's only invoked in unusual situations.**
- **What a method's interface comment must contain (§13.5)** — five items:
  1. A sentence or two on the **behavior as perceived by callers** (the higher-level abstraction).
  2. **Each argument and the return value** — very precise, including constraints on values and **dependencies between arguments**.
  3. **Side effects** — "any consequence of the method that affects the future behavior of the system but is not part of the result" (adding to an internal data structure retrievable later; writing to the file system).
  4. **Any exceptions** that can emanate from the method.
  5. **Preconditions** — another method must be called first; a binary search's list must be sorted. "It is a good idea to minimize preconditions, but any that remain must be documented."
- **Separate interface comments from implementation comments — and they had better be different.** "If interface comments must also describe the implementation, then the class or method is shallow." **The act of writing comments provides clues about the quality of a design** (Ch 15).
- **Implementation comments: what and why, not how (§13.6).** "The main goal of implementation comments is to help readers understand *what* the code is doing (not how it does it). Once readers know what the code is trying to do, it's usually easy to understand how the code works."
  - Short methods need none — the code does one thing, already described by the interface comment.
  - Longer methods: **a comment before each major block** giving a high-level description (`// Phase 1: Scan active RPCs to see if any have completed.`).
  - **Loops**: a comment before the loop describing what happens in *each iteration* — only for longer or more complex loops.
  - **Why**: document tricky aspects that won't be obvious. For a bug fix whose purpose isn't obvious, say why the code is needed; where a good bug report exists, **refer to it rather than repeating it** (`Fixes RAM-436, related to device driver crashes in Linux 2.4.x`).
  - **Local variables**: most don't need documentation if well named. "If all of the uses of a variable are visible within a few lines of each other," let readers read the code. **If the variable is used over a large span of code, add a comment.**

## Key Concepts
- **Interface comment**: defines the abstraction; what you need to know to *use* the thing.
- **Implementation comment**: how it works internally.
- **Side effect**: a consequence affecting future system behavior that isn't part of the result.
- **Precondition**: something that must hold before invocation.
- **designNotes file**: a central, topic-sectioned file for cross-module documentation.

## Anti-patterns
- **Red Flag — Comment Repeats Code**: the information is already obvious from the adjacent code. One instance: **the comment uses the same words that make up the name of the thing it describes.**
  - **The test:** *"Could someone who has never seen the code write the comment just by looking at the code next to the comment?"* If yes, the comment adds nothing. "Comments like these are why some people think that comments are worthless."
  - **The first fix:** *"use different words in the comment from those in the name of the entity being described."* Pick words that add information about meaning rather than restating the name.
- **One comment per line, at the code's level of detail** — "Comments like this are rarely useful."
- **Red Flag — Implementation Documentation Contaminates Interface**: interface documentation describing implementation details not needed to use the thing. **"This is one of the most common errors in interface comments."** Useful implementation documentation should move *inside* the method, where it's clearly separated.
- **Vague variable comments** — "current offset" (current in what sense?), or a comment on a map that fails to say which of key/value is which, or what the units are.
- **Documenting how a variable is manipulated** instead of what it represents.

## Code Examples

**Comments that repeat the code** — from a research paper:
```python
ptr_copy = get_copy(obj)                         # Get pointer copy
if is_unlocked(ptr_copy):                        # Is obj free?
  return obj                                     # return current obj
if is_copy(ptr_copy):                            # Already a copy?
  return obj                                     # return obj
thread_id = get_thread_id(ptr_copy)
if thread_id == ctx.thread_id:                   # Locked by current ctx
  return ptr_copy                                # Return copy
```
Only "Locked by current ctx" carries information that isn't obvious.

**Comments echoing the name** — the only word in the second comment not already in the code is *"to"*:
```java
/*
* Obtain a normalized resource name from REQ.
*/
private static String[] getNormalizedResourceNames(
        HTTPRequest req) ...

/*
* Downcast PARAMETER to TYPE.
*/
private static Object downCastParameter(String parameter, String type)
        ...

/*
* The horizontal padding of each line in the text.
*/
private static final int textHorizontalPadding = 4;
```
Note what's *missing*: what is a "normalized resource name," and what are the array's elements? What does "downcast" mean? **What are the units of padding, and is it on one side or both?**

**Fixed** — adds units, both-sides, and explains the term rather than repeating it:
```java
/*
* The amount of blank space to leave on the left and
* right sides of each line of text, in pixels.
*/
private static final int textHorizontalPadding = 4;
```

**Vague → precise:**
```c
// Current offset in resp Buffer
uint32_t offset;
```
```c
// Position in this buffer of the first object that hasn't
// been returned to the client.
uint32_t offset;
```
```java
// Contains all line-widths inside the document and
// number of appearances.
private TreeMap<Integer, Integer> lineWidths;
```
```java
// Holds statistics about line lengths of the form <length, count>
// where length is the number of characters in a line (including
// the newline), and count is the number of lines with
// exactly that many characters. If there are no lines with
// a particular length, then there is no entry for that length.
private TreeMap<Integer, Integer> numLinesWithLength;
```
Three separate improvements: a longer **name** conveying more; **"width" → "length"** because that word suggests characters rather than pixels; and documenting **what a missing entry means.**

**Nouns not verbs:**
```java
/* FOLLOWER VARIABLE: indicator variable that allows the Receiver and the
* PeriodicTasks thread to communicate about whether a heartbeat has been
* received within the follower's election timeout window.
* Toggled to TRUE when a valid heartbeat is received.
* Toggled to FALSE when the election timeout window is reset. */
private boolean receivedValidHeartbeat;
```
```java
/* True means that a heartbeat has been received since the last time
* the election timer was reset. Used for communication between the
* Receiver and PeriodicTasks threads. */
private boolean receivedValidHeartbeat;
```
Shorter *and* more useful — and the toggling behavior is now inferable.

**Too low-level → higher-level intuition.** Original:
```c
// If there is a LOADING readRpc using the same session
// as PKHash pointed to by assignPos, and the last PKHash
// in that readRPC is smaller than current assigning
// PKHash, then we put assigning PKHash into that readRPC.
int readActiveRpcId = RPC_ID_NOT_ASSIGNED;
for (int i = 0; i < NUM_READ_RPC; i++) {
    if (session == readRpc[i].session
           && readRpc[i].status == LOADING
           && readRpc[i].maxPos < assignPos
           && readRpc[i].numHashes < MAX_PKHASHES_PERRPC) {
        readActiveRpcId = i;
        break;
    }
}
```
It partly repeats the code ("if there is a LOADING readRPC" duplicates `status == LOADING`) *and* never says what the code is for. Replacement:
```c
// Try to append the current key hash onto an existing
// RPC to the desired server that hasn't been sent yet.
```
From that one sentence a reader can now explain nearly every line: the loop iterates over existing RPCs; the `session` test finds one destined for the right server; `LOADING` implies RPCs have states, some unsafe to add to; `MAX_PKHASHES_PERRPC` implies a per-RPC limit. Only the `maxPos` test remains unexplained. **And it gives readers a basis to judge correctness** — does the code do everything needed to append the hash? The original comment made that impossible to assess.

**A good comment doing both jobs** — the second sentence says *what*, the first says *how we got here*:
```c
if (numProcessedPKHashes < readRpc[i].numHashes) {
    // Some of the key hashes couldn't be looked up in
    // this request (either because they aren't stored
    // on the server, the server crashed, or there
    // wasn't enough space in the response message).
    // Mark the unprocessed hashes so they will get
    // reassigned to new RPCs.
    for (size_t p = removePos; p < insertPos; p++) {
       ...
    }
}
```

**A model class interface comment** — capabilities, what an instance represents, and limitations, with no implementation details:
```java
/**
* This class implements a simple server-side interface to the HTTP
* protocol: by using this class, an application can receive HTTP
* requests, process them, and return responses. Each instance of
* this class corresponds to a particular socket used to receive
* requests. The current implementation is single-threaded and
* processes one request at a time.
*/
public class Http {...}
```

**A model method interface comment** (Doxygen conventions) — note it documents special cases *because the method defined the errors out of existence* (Ch 10), and a caller never needs to read the body:
```c
/**
* Copy a range of bytes from a buffer to an external location.
*
* \param offset
*          Index within the buffer of the first byte to copy.
* \param length
*          Number of bytes to copy.
* \param dest
*          Where to copy the bytes: must have room for at least
*          length bytes.
*
* \return
*          The return value is the actual number of bytes copied,
*          which may be less than length if the requested range of
*          bytes extends past the end of the buffer. 0 is returned
*          if there is no overlap between the requested range and
*          the actual buffer.
*/
uint32_t
Buffer::copy(uint32_t offset, uint32_t length, void* dest)
```

## Worked Example — rewriting the `IndexLookup` documentation (§13.5)
`IndexLookup` performs indexed range queries against a distributed storage system. Usage:
```java
query = new IndexLookup(table, index, key1, key2);
while (true) {
    object = query.getNext();
    if (object == NULL) {
        break;
    }
    ... process object ...
}
```
The implementation is genuinely complex: objects may be spread across many servers, indexes across a *different* set of servers, so the class must first collect range information from index servers and then fetch values from the object servers.

**The exercise Ousterhout poses** — does a user need to know each of these? (his answers, from §13.9):

| Information | Needed? | Why |
|---|---|---|
| Format of messages sent to index/object servers | **No** | Implementation detail, hidden in the class |
| Comparison function for the range (integer? float? string?) | **Yes** | Users need this |
| Data structure storing indexes on servers | **No** | Encapsulated on the servers — *not even `IndexLookup`'s implementation* needs it |
| Whether multiple requests are issued concurrently | **Possibly** | If special techniques improve performance, give high-level information, since users may care about performance |
| Mechanism for handling server crashes | **No** | RAMCloud recovers automatically, so crashes are invisible to applications. *If crashes were reflected up, the docs would need to describe how they manifest — but not how recovery works* |

**The original comment**, and everything wrong with it:
```c
/*
* This class implements the client side framework for index range
* lookups. It manages a single LookupIndexKeys RPC and multiple
* IndexedRead RPCs. Client side just includes "IndexLookup.h" in
* its header to use IndexLookup class. Several parameters can be set
* in the config below:
* - The number of concurrent indexedRead RPCs
* - The max number of PKHashes a indexedRead RPC can hold at a time
* - The size of the active PKHashes
* ...
*/
```
- **Most of the first paragraph is implementation, not interface** — users don't need the names of the RPCs used to talk to servers, and the configuration parameters listed are **private variables relevant only to the class's maintainer.**
- **Several things are obvious** — no need to tell a C++ programmer to include the header; "by providing all necessary information" says nothing.

**The replacement:**
```c
/*
* This class is used by client applications to make range queries
* using indexes. Each instance represents a single range query.
*
* To start a range query, a client creates an instance of this
* class. The client can then call getNext() to retrieve the objects
* in the desired range. For each object returned by getNext(), the
* caller can invoke getKey(), getKeyLength(), getValue(), and
* getValueLength() to get information about that object.
*/
```
Three judgment calls worth noting: the last paragraph *duplicates* per-method comments and isn't strictly necessary, but **usage examples in class documentation help for deep classes with nonobvious usage patterns.** It deliberately **omits `getNext`'s NULL return** — the class comment isn't meant to document every detail, just how the methods work together. And it **omits server crashes**, because those are invisible to users.

**The same fix applied to a method.** Original `isReady` documentation:
```c
/**
* Check if the next object is RESULT_READY. This function is
* implemented in a DCFT module, each execution of isReady() tries
* to make small progress, and getNext() invokes isReady() in a
* while loop, until isReady() returns true.
*
* isReady() is implemented in a rule-based approach. We check
* different rules by following a particular order, and perform
* certain actions if some rule is satisfied.
* ...
*/
```
Problems: the DCFT reference and the entire second paragraph are implementation; the first sentence is cryptic (*what is `RESULT_READY`?*); important information is missing; and describing `getNext`'s implementation here is unnecessary.

```c
/*
* Indicates whether an indexed read has made enough progress for
* getNext to return immediately without blocking. In addition, this
* method does most of the real work for indexed reads, so it must
* be invoked (either directly, or indirectly by calling getNext) in
* order for the indexed read to make progress.
*
* \return
*          True means that the next invocation of getNext will not block
*          (at least one object is available to return, or the end of the
*          lookup has been reached); false means getNext may block.
*/
```
This says precisely what "ready" means **and adds the critical fact that the method must eventually be invoked for the read to progress** — which the original never stated.

## Worked Example — documenting cross-module decisions (§13.7)
"In a perfect world, every important design decision would be encapsulated within a single class." Real systems have decisions spanning classes — a network protocol affects both sender and receiver. These are "often complex and subtle, and they account for many bugs, so good documentation for them is crucial." **The biggest challenge is finding a place where developers will naturally discover it.**

**Case 1 — there is an obvious central place.** RAMCloud's `Status` enum: adding a status requires edits across many files. Everyone adding one must visit the enum declaration, so the checklist goes *there* — and at the **end** of the list, since new values are appended there and that's where it will be seen:
```c
typedef enum Status {
    STATUS_OK = 0,
    ...
    STATUS_MAX_VALUE                          = 30,

    // Note: if you add a new status value you must make the following
    // additional updates:
    // (1)   Modify STATUS_MAX_VALUE to have a value equal to the
    //       largest defined status value, and make sure its definition
    //       is the last one in the list. STATUS_MAX_VALUE is used
    //       primarily for testing.
    // (2)   Add new entries in the tables "messages" and "symbols" in
    //       Status.cc.
    // (3)   Add a new exception class to ClientException.h
    // (4)   Add a new "case" to ClientException::throwException to map
    //       from the status value to a status-specific ClientException
    //       subclass.
    // (5)   In the Java bindings, add a static class for the exception
    //       to ClientException.java
    // (6)   Add a case for the status of the exception to throw the
    //       exception in ClientException.java
    // (7)   Add the exception to the Status enum in Status.java, making
    //       sure the status is in the correct position corresponding to
    //       its status code.
}
```

**Case 2 — there is no obvious central place.** RAMCloud's zombie servers (servers the cluster believes dead that are still running) required interdependent code in several modules with no natural home. Both obvious options are bad: **duplicating** the documentation in each location is awkward and hard to keep current; putting it in **one** of the places means developers won't find it.

Ousterhout's experiment: a central **`designNotes`** file, divided into clearly labeled sections by topic —
```
Zombies
-------
A zombie is a server that is considered dead by the rest of the
cluster; any data stored on the server has been recovered and will
be managed by other servers. However, if a zombie is not actually
dead (e.g., it was just disconnected from the other servers for a
while) two forms of inconsistency can arise:
* A zombie server must not serve read requests once replacement servers
  have taken over; otherwise it may return stale data ...
* The zombie server must not accept write requests once replacement
  servers have begun replaying its log during recovery; if it does,
  these writes may be lost ...
```
— with a one-line pointer at each relevant code site:
```c
// See "Zombies" in designNotes.
```
**Single copy, findable.** He names the tradeoff honestly: "the documentation is not near any of the pieces of code that depend on it, so it may be difficult to keep up-to-date as the system evolves" — which cuts against Ch 16's "keep comments near the code."

## Key Takeaways
1. Write comments at a *different* level than the code — lower for precision, higher for intuition. Same level = repetition.
2. Apply the test: could someone write this comment from the adjacent code alone? Then it's worthless.
3. Use different words than the entity's name; explain the term rather than restating it.
4. For declarations, specify units, inclusivity, null meaning, ownership of resources, and invariants.
5. Document what a variable *represents*, not how it's manipulated.
6. Interface comments must cover behavior, every argument and return, side effects, exceptions, and preconditions.
7. Keep implementation details out of interface comments — and note that needing them signals a shallow module.
8. Inside methods, comment *what* and *why*, per major block, not *how* per line.
9. Reference bug IDs rather than duplicating bug reports.
10. For cross-module decisions, put the documentation where developers will inevitably look; failing that, centralize it and point to it.
11. **"Obvious" is from the reader's perspective, not yours.** "If your code is undergoing review and a reviewer tells you that something is not obvious, don't argue with them; if a reader thinks it's not obvious, then it's not obvious." Find what confused them and fix it — with better comments *or* better code.

## Connects To
- **Ch 4**: comments carry the informal part of an interface; interface comments define the abstraction.
- **Ch 10**: the `Buffer::copy` comment documents special cases *because* errors were defined out of existence.
- **Ch 12**: why comments exist at all.
- **Ch 14**: better names remove the need for some comments — and the `numLinesWithLength` rename here is a Ch 14 fix.
- **Ch 15**: writing comments first, and comments as a design-quality signal.
- **Ch 16**: keeping comments near the code and avoiding duplication — in tension with `designNotes`.
- **Ch 18**: the shared goal of making the system obvious to readers.
