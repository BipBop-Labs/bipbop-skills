# Chapter 8: Pull Complexity Downwards

## Core Idea
When you hit unavoidable complexity, absorb it inside the module rather than exposing it to callers: **it is more important for a module to have a simple interface than a simple implementation.**

## Frameworks Introduced
- **Pull complexity downward.**
  - The rule: if the complexity is related to the functionality the module provides, handle it internally.
  - The rationale: **most modules have more users than developers, so it is better for the developers to suffer than the users.** Strive to make life as easy as possible for your module's users, even at extra cost to yourself.
  - When to use: any time you discover a piece of unavoidable complexity while building a module.
- **The two ways developers push complexity *upward*** (both tempting, both wrong by default):
  1. **Throw an exception** when you're not sure how to handle a condition, and let the caller deal with it.
  2. **Add configuration parameters** when you're not sure what policy to implement, and let the administrator figure out the values.
  - Why they amplify complexity: "if a class throws an exception, every caller of the class will have to deal with it. If a class exports configuration parameters, every system administrator in every installation will have to learn how to set them." One person's uncertainty becomes many people's problem.
- **The configuration-parameter test (§8.2).** Before exporting a parameter, ask: **"will users (or higher-level modules) be able to determine a better value than we can determine here?"**
  - If no → compute it internally.
  - If yes → still try to compute a reasonable *default* automatically, so users supply values only under exceptional conditions.
  - The principle behind it: "each module should solve a problem completely; configuration parameters result in an incomplete solution."
  - Note the fair hearing Ousterhout gives the other side: sometimes low-level infrastructure genuinely can't know the best policy while the user can — a user may know some requests are more time-critical and should get higher priority. In those cases parameters do improve performance across a broader variety of domains. The failure is using parameters as *"an easy excuse to avoid dealing with important issues and pass them on to someone else."*

## Key Concepts
- **Pulling complexity downward**: moving complexity from callers into the module's implementation.
- **Moving complexity upward**: exposing exceptions or configuration parameters instead of resolving them.

## Anti-patterns
- **Solving the easy problems and punting the hard ones** — throwing an exception because you're unsure, or adding a knob because you haven't decided a policy.
- **Configuration parameters users can't reasonably set.** In many cases it's difficult or impossible for users or administrators to determine the right values; in others, the right value could have been computed automatically with a little extra implementation work. Parameters also **go out of date**, whereas a computed value adapts.
- **Line-oriented interface over line-oriented storage** — pushes line splitting and joining onto every caller.
- **Pulling complexity down that doesn't belong** — see "Taking it too far" below.

## Worked Example — retry interval, two ways
A network protocol must handle lost packets: if no response arrives within some period, resend.

**Complexity up:** expose a `retryInterval` configuration parameter. Every operator of every installation must now determine a good value, with little basis for doing so, and the value silently rots as conditions change.

**Complexity down:** the transport protocol **measures the response time of requests that succeed and uses a multiple of that as the retry interval.** Users never think about it, and the value adjusts automatically when operating conditions change.

The second is strictly better: it removes a decision from every user *and* produces a better-adapted value than a static setting could.

## Worked Example — the editor text class, third pass
Same class as Ch 6 and 7, now viewed through this lens.

**Line-oriented interface** (read/insert/delete whole lines): simple *implementation*, because storage is already line-based. But UI operations rarely involve whole lines — keystrokes insert single characters inside a line; deleting a selection can modify parts of several lines. So higher-level software must split and join lines itself.

**Character-oriented interface** (insert an arbitrary string at an arbitrary position; delete between two positions): the UI now inserts and deletes arbitrary ranges with no splitting or merging. **The text class's implementation gets more complex** — with line-based internal storage it must split and merge lines itself.

That trade is the right one: the complexity of splitting and merging is encapsulated in one class instead of scattered across every caller, so overall system complexity drops. This is the same conclusion Ch 7 reached from the "interface should differ from implementation" direction.

## Key Takeaways
1. Prefer a simple interface over a simple implementation (design principle #6).
2. More users than developers means developer suffering is the cheaper suffering.
3. Don't throw an exception merely because you're unsure how to handle a condition — every caller inherits it.
4. Before exporting a configuration parameter, ask whether the caller can really pick a better value than you can.
5. Compute values dynamically where you can; computed values adapt, parameters go stale.
6. Aim for each module to solve its problem *completely*.
7. **Taking it too far (§8.3)** — pulling complexity down makes sense only when all three hold: (a) the complexity is **closely related to the class's existing functionality**; (b) it will produce **many simplifications elsewhere**; (c) it **simplifies the class's interface**. The counter-example is the `backspace` method from Ch 6: putting UI knowledge in the text class looks like pulling complexity down, but it doesn't simplify higher-level code much and doesn't relate to the text class's core function — so it just produced information leakage.

## Connects To
- **Ch 4**: this is another route to deep classes.
- **Ch 5–6**: the failure mode of over-applying it is information leakage / the false `backspace` abstraction.
- **Ch 7**: the character-vs-line interface argument, from the layering angle.
- **Ch 10**: "Define Errors Out Of Existence" — the systematic treatment of the exception half of pushing complexity upward.
