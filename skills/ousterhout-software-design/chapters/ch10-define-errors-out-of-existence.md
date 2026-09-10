# Chapter 10: Define Errors Out Of Existence

## Core Idea
Exception handling is one of the worst sources of complexity in software; the fix is to **reduce the number of places where exceptions must be handled** — best of all by redefining semantics so the normal behavior covers every situation and there is nothing exceptional to report.

## Frameworks Introduced
- **The four techniques for reducing exception handlers**, in order of preference:
  1. **Define errors out of existence (§10.3)** — change the API so the error case is a normal case.
  2. **Mask exceptions (§10.6)** — detect and handle low, so higher levels never learn of the condition.
  3. **Aggregate exceptions (§10.7)** — handle many exceptions with a single handler high up.
  4. **Just crash (§10.8)** — for errors not worth handling.
- **Define errors out of existence.** The move is to **redefine what the operation means** so the previously-erroneous input is within normal behavior.
  - The canonical transformation: not "delete a variable" (which can't do its job if the variable is absent) but **"ensure a variable no longer exists"** (in which case the work is already done — just return).
  - Why it works: it simplifies the API *and* increases functionality, which makes the method **deeper**.
- **Mask exceptions.** Detect and handle at a low level so higher levels are unaware. Common in distributed systems: **TCP** masks packet loss by resending internally, so all data eventually gets through and clients never see drops.
  - Properties: results in deeper classes — it shrinks the interface (fewer exceptions to know about) and adds functionality (the masking code). **Exception masking is an example of pulling complexity downward (Ch 8).**
  - Placement rule: masking works best **low**, in a library method used by many callers, because letting the exception propagate would multiply the handlers.
- **Aggregate exceptions.** Handle many exceptions with one piece of code, positioned high.
  - Placement rule: works best when the exception **propagates several levels up** — the more methods it passes, the more handlers you eliminate. **This is the opposite of masking**, but the two share a principle: *position the handler where it catches the most exceptions.*
  - **The generally useful design pattern**: if a system processes a series of requests, define an exception that **aborts the current request, cleans up state, and continues with the next**, caught in a single place near the top of the request-handling loop. It can be thrown anywhere during request processing; different subclasses cover different conditions. **Keep these clearly distinguished from exceptions that are fatal to the entire system.**
  - **Error promotion** — a variant: promote many small errors into one larger one so you maintain fewer recovery mechanisms.
- **Just crash.** For errors that are difficult or impossible to handle and don't occur often, print diagnostics and abort.
  - The C `malloc` case: returning `NULL` assumes *every single caller* checks and acts. Applications contain numerous `malloc` calls, so checking each adds significant complexity — and if a programmer forgets (fairly likely), the app dereferences a null pointer, **producing a crash that camouflages the real problem.**
  - The fix: define `ckalloc`, which calls `malloc`, checks the result, and aborts with an error message if memory is exhausted. **The application never calls `malloc` directly.**
  - In C++/Java, `new` throws on exhaustion — but there's little point catching it, since the handler will probably also try to allocate and also fail. Dynamically allocated memory is so fundamental that continuing makes no sense.
  - Also reasonable to crash on: I/O errors on an open file (a disk hard error), inability to open a network socket, and internal errors like an inconsistent data structure (which probably indicates a bug). These are infrequent enough not to affect usability.
  - **But it depends on the application**: for a replicated storage system, aborting on an I/O error is *not* acceptable — it must recover from replicas. That recovery adds considerable complexity, but recovering lost data "is an essential part of the value the system provides to its users."
- **Design special cases out of existence (§10.9).** Same logic applied beyond errors. Special cases produce code "riddled with `if` statements," which is hard to understand and leads to bugs. **The best way to eliminate them is to design the normal case so it automatically handles the special cases with no extra code.**

## Key Concepts
- **Exception** (the book's broad sense): any uncommon condition that alters normal control flow — including a method returning a special value, not just formal throw/catch.
- **Exception masking**: handling a condition at a low level so higher levels never see it.
- **Exception aggregation**: one handler for many exceptions, placed high.
- **Error promotion**: converting many small errors into one larger error class to reduce recovery mechanisms.

## Anti-patterns
- **Over-defensive exception proliferation.** Programmers taught to detect and report errors interpret it as "the more errors detected, the better," rejecting anything that looks slightly suspicious. Each unnecessary exception increases system complexity.
- **Throwing because you don't know what to do.** "If you are having trouble figuring out what to do for the particular situation, there's a good chance that the caller won't know what to do either." The claim that it "empowers callers" doesn't survive this.
- **Forgetting that exceptions are interface.** "The exceptions thrown by a class are part of its interface; classes with lots of exceptions have complex interfaces, and they are shallower than classes with fewer exceptions." An exception is a *particularly* complex interface element because it can propagate up several stack levels, affecting higher-level callers and their interfaces too.
- **A state variable for an absent thing** (a "does the selection exist?" boolean) — see the worked example.
- **Masking everything** — see "Taking it too far."

## The case against exceptions, in full (§10.1)
Four reasons exception handling is disproportionately costly:

1. **It's inherently harder to write.** Two options, both complicated: (a) *move forward* despite the exception (resend the lost packet, recover from a redundant copy); or (b) *abort and report upward* — complicated because the exception may occur where **system state is inconsistent** (a partially initialized data structure), so the handler must restore consistency by unwinding changes.
2. **Handling code creates more exceptions.** Resend a "lost" packet that was merely delayed → duplicate packets arrive, a new condition the peer must handle. Recover from a redundant copy → what if that copy is also lost? **"Secondary exceptions occurring during recovery are often more subtle and complex than the primary exceptions."** To stop an unending cascade, someone must eventually handle an exception without introducing more.
3. **Language support is verbose and clunky.** In the Java example below, the try-catch boilerplate is more lines than the normal-case code, before any actual handling. It's also hard to tell *where* each exception comes from. Splitting into many small `try` blocks makes origins clear but breaks up the code's flow and can duplicate handler code.
4. **It's hard to know the handlers work.** I/O errors can't easily be generated in tests; exceptions rarely execute in production, so bugs go undetected for a long time and the code likely fails when finally needed. **"Code that hasn't been executed doesn't work."** Empirically: **a study found more than 90% of catastrophic failures in distributed data-intensive systems were caused by incorrect error handling** (Yuan et al., OSDI 2014). And when handlers fail, they're hard to debug because they occur so infrequently.

## Code Examples

**The verbosity problem** — reading serialized tweets in Java:
```java
try (
   FileInputStream fileStream =
            new FileInputStream(fileName);
   BufferedInputStream bufferedStream =
            new BufferedInputStream(fileStream);
   ObjectInputStream objectStream =
            new ObjectInputStream(bufferedStream);
) {
   for (int i = 0; i < tweetsPerFile; i++) {
        tweets.add((Tweet) objectStream.readObject());
   }
}
catch (FileNotFoundException e) {
   ...
}
catch (ClassNotFoundException e) {
   ...
}
catch (EOFException e) {
   // Not a problem: not all tweet files have full
   // set of tweets.
}
catch (IOException e) {
   ...
}
catch (ClassCastException e) {
   ...
}
```
Three lines of real work; five catch clauses.

## Worked Example — Tcl `unset`, the author's own mistake
Tcl's `unset` removes a variable. Ousterhout defined it to **throw an error if the variable doesn't exist** — reasoning that deleting a nonexistent variable must be a bug worth reporting.

What actually happened: one of the most common uses of `unset` is cleaning up temporary state from a previous operation. It's often hard to predict exactly what state was created — **especially if the operation aborted partway through** — so the simplest thing is to delete every variable that *might* have been created. His definition made that awkward: developers wrapped `unset` calls in `catch` statements to swallow the errors.

His verdict: **"In retrospect, the definition of the unset command is one of the biggest mistakes I made in the design of Tcl."**

The fix is a one-word change in the specification: not *"delete a variable"* but *"ensure a variable no longer exists."* Under the first definition an absent variable makes the job impossible, so an exception is sensible. Under the second, being called with an absent variable is perfectly natural — the work is already done, so return. The error case no longer exists.

## Worked Example — file deletion, Windows vs. Unix
**Windows** won't delete a file that is open in a process. Users must hunt down the process holding it and kill that process; **"sometimes users give up and reboot their system, just so they can delete a file."**

**Unix** marks the file for deletion and **returns successfully**. The name is removed from its directory — so no other process can open the old file, and a new file with that name can be created — but the existing data persists. Processes that already have it open keep reading and writing normally. Once all accessors close it, the data is freed.

This defines away **two** errors:
1. Delete no longer returns an error when the file is in use.
2. Deleting an in-use file creates no exceptions for the processes using it.

Note the rejected alternative: delete immediately and disable all existing opens, so other processes' reads and writes fail. That would have **created new errors for those processes to handle** — trading one error for several. Delaying the deletion is what defines them away.

"It may seem strange that Unix allows a process to continue to read and write a doomed file, but I have never encountered a situation where this caused significant problems."

## Worked Example — Java `substring`, and the "but errors catch bugs" objection
`substring(beginIndex, endIndex)` throws `IndexOutOfBoundsException` if either index is outside the string. But a common need is "extract all characters overlapping this range," where one or both indices may be out of range. That forces the caller to clamp each index up to zero or down to the end — **"a one-line method call now becomes 5–10 lines of code."**

The better API: *"returns the characters of the string (if any) with index greater than or equal to `beginIndex` and less than `endIndex`."* Now behavior is well-defined for negative indices and for `beginIndex > endIndex`. This **simplifies the API while increasing functionality — making the method deeper.** Python already does this: out-of-range list slices return empty results.

**The objection, and the answer.** People counter that throwing errors catches bugs, so defining them away yields buggier software. Ousterhout's response: the error-ful approach may catch some bugs, but it **increases complexity, which causes other bugs** — developers must write extra code to avoid or ignore the errors (more chances for bugs), or they forget to write it and get unexpected runtime exceptions. Defining errors away simplifies APIs and reduces code written. **"Overall, the best way to reduce bugs is to make software simpler."**

## Worked Example — the NFS hang, a deliberately controversial masking case
If an NFS server crashes or stops responding, clients reissue requests over and over until it recovers. The client file-system code reports **no** exception to the application, which simply hangs, while the console prints *"NFS server xyzzy not responding still trying."*

Users hate this and often propose that NFS abort with an exception instead. Ousterhout argues that would be **worse**, by elimination:
- There's not much an application can do if it loses access to its files.
- It could retry the operation — but that still hangs the application, **and it's easier to retry in one place in the NFS layer than at every file-system call in every application** ("a compiler shouldn't have to worry about this!").
- Or applications abort and return errors to their callers — whose callers won't know what to do either, so they abort too, **collapsing the user's whole working environment.** Users still can't work while the server is down, and now they must restart everything when it returns.

So masking and hanging is best: applications need no code for server problems and resume seamlessly. If users tire of waiting, they can abort manually.

## Worked Example — aggregating web-server parameter errors
A web server dispatches an incoming URL to a URL-specific service method; each service method calls `getParameter` to extract what it needs, and `getParameter` throws `NoSuchParameter` if it's absent.

**What students did (Figure 10.1):** wrapped *each* `getParameter` call in its own handler. Many handlers, all doing essentially the same thing — generate an error response.

**Aggregated (Figure 10.2):** let the exceptions propagate to the **top-level dispatch method**, where one handler catches them all and generates the error response.

**Pushed further:** many other errors also just produce an error response — a parameter with wrong syntax (expected an integer, got `"xyz"`), or a permission failure. They differ **only in the message**. So *all* conditions producing an error response get one top-level handler, with the message generated where the exception is thrown and carried as a field in the exception record. `getParameter` produces `"parameter 'quantity' not present in URL"`; a syntax check produces `"bad value 'xyz' for 'quantity' parameter; must be positive integer"`; the top-level handler extracts the message and wraps it in a response.

**Why this is good information hiding** — note how cleanly the knowledge divides:
- The top-level handler knows **how to generate error responses** but nothing about specific errors.
- `getParameter` knows **how to extract a parameter** *and* **how to describe extraction failures in human-readable form** — two closely related pieces of knowledge, correctly co-located.
- `getParameter` knows nothing about HTTP error-response syntax.

**And it extends for free:** new methods that throw exceptions the same way — inheriting from the same superclass and carrying a message — **plug into the existing system with no other changes.**

## Worked Example — RAMCloud's error promotion
RAMCloud keeps multiple copies of each object across storage servers. It could handle a corrupted object by restoring that one object from a backup. **It doesn't: it crashes the entire server containing the object.**

The reasoning: crash recovery is complex, and a mechanism for crashed servers was unavoidable anyway, so reusing it for smaller errors **minimized the number of distinct recovery mechanisms**. Two benefits: less code, and **server-crash recovery gets invoked more often — so bugs in recovery are more likely to be found and fixed.** (Compare "code that hasn't been executed doesn't work.")

The cost: recovery becomes much more expensive per incident. Acceptable because object corruption is rare. **The limit:** "error promotion may not make sense for errors that happen frequently… it would not be practical to crash a server anytime one of its network packets is lost."

One way to see aggregation: it replaces several special-purpose mechanisms with a single general-purpose one — another instance of Ch 6's argument.

## Worked Example — designing the "no selection" special case away
Students implementing text selection introduced a state variable for whether a selection exists — natural, since sometimes no selection is visible. The result was **numerous checks for the "no selection" condition** scattered through the code.

The fix: **the selection always exists.** When nothing is visible on screen, represent it internally as an **empty selection whose start and end positions are equal.** Now the selection code has no "no selection" checks at all:
- **Copying**: an empty selection inserts 0 bytes at the destination. (Implemented correctly, there's no need for a special 0-byte check either.)
- **Deleting**, for a selection within one line: take the part of the line before the selection, concatenate the part after it, and that's the new line. **If the selection is empty, this regenerates the original line** — correct with no special case.

This is also "different layer, different abstraction" (Ch 7): "no selection" is real in how the *user* thinks about the interface, but that doesn't mean it must be represented explicitly inside the application. A selection that always exists but is sometimes empty and invisible yields a simpler implementation.

## Key Takeaways
1. Reduce the *number of places* exceptions must be handled — that's the whole chapter in one line.
2. First reach for redefining semantics so the error case becomes a normal case; this deepens the method.
3. Exceptions are part of your interface, and a costly part, since they propagate through callers you don't control.
4. Don't throw because you're unsure — the caller will be no wiser.
5. Mask **low** (in shared library code); aggregate **high** (near the request loop). Both put the handler where it catches the most.
6. For request-processing systems, define one abort-this-request exception caught near the top of the loop, kept distinct from system-fatal ones.
7. Consider promoting rare small errors into an existing larger recovery path — fewer mechanisms, better-exercised code.
8. Crash on errors that are rare and unhandleable; wrap the raw call (`ckalloc`) so no caller has to remember.
9. Design special cases out of existence by making the normal path handle them — an always-present-but-empty value beats an existence flag.
10. **Taking it too far (§10.10)**: defining away or masking only makes sense if the information isn't needed outside the module. A student team masked *all* network exceptions — caught, discarded, continued as if fine — so applications couldn't tell whether messages were lost or a peer had failed, **making robust applications impossible.** There the module must expose the exceptions despite the interface complexity. "Things that are not important should be hidden, and the more of them the better. But when something is important, it must be exposed."

## Connects To
- **Ch 4**: fewer exceptions → simpler interface → deeper module.
- **Ch 6**: aggregation as a general-purpose mechanism replacing special-purpose ones.
- **Ch 8**: masking *is* pulling complexity downward; throwing is pushing it up.
- **Ch 5 / Ch 10.10**: the same "hide what's unimportant, expose what's important" boundary.
- **Ch 18**: special cases and `if`-riddled code as obstacles to obvious code.
- **Ch 19.3**: "code that hasn't been executed doesn't work" recurs in the discussion of unit tests.
