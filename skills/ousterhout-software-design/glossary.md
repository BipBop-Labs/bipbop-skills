# APOSD Glossary

**Abstraction** — A simplified view of an entity, which omits unimportant details. "Unimportant" is load-bearing: omitting *important* details makes a false abstraction. (Ch 4)

**Back-door leakage** — Information leakage where shared knowledge appears in no interface, e.g. two classes that both understand a file format. More pernicious than interface leakage because nothing points at it. (Ch 5)

**Change amplification** — A seemingly simple change requiring code modifications in many places. One of the three symptoms of complexity. (Ch 2)

**Classitis** — The mistaken view that "classes are good, so more classes are better." Produces many shallow classes, verbose boilerplate, and high system-level complexity. (Ch 4)

**Cognitive leverage** — Knowledge acquired once applying safely in many places; the benefit consistency provides. (Ch 17)

**Cognitive load** — How much a developer needs to know to complete a task. Raised by large APIs, global variables, inconsistency, and inter-module dependencies. One of the three symptoms. (Ch 2)

**Comment, cross-module** — A comment describing dependencies that cross module boundaries. Rarest and hardest to place. (Ch 13)

**Comment, implementation** — A comment inside a method describing how the code works internally. Often unnecessary. (Ch 13)

**Comment, interface** — A comment block immediately preceding a class, data structure, function, or method declaration, defining its abstraction. Required for every class and method. (Ch 13)

**Complexity** — "Anything related to the structure of a software system that makes it hard to understand and modify the system." Caused by dependencies and obscurity; manifests as change amplification, cognitive load, and unknown unknowns. (Ch 2)

**Conjoined methods** — Two methods where you can't understand one's implementation without understanding the other's. Generalizes to any two separated pieces of code each requiring the other. Red flag. (Ch 9)

**Context** — An object holding all of one system instance's global state, used to eliminate pass-through variables. Should hold immutable variables. (Ch 7)

**Critical path** — The minimum amount of code that must execute in the most common case. (Ch 20)

**Death by a thousand cuts** — Diffuse inefficiency from ignoring performance entirely; 5–10x slower with no single fixable hotspot. (Ch 20)

**Deep module** — A module with a lot of functionality behind a simple interface. The goal for all modules. (Ch 4)

**Dependency** — Exists when code cannot be understood and modified in isolation. Unavoidable and intentionally created; the goal is fewer, simpler, more obvious ones. One of the two causes of complexity. (Ch 2)

**designNotes** — A central file with labeled topic sections, holding cross-module documentation that has no natural single home, referenced by short pointer comments. (Ch 13, 16)

**Dispatcher** — A method that uses its arguments to select one of several other methods and forwards most or all arguments. Legitimate same-signature duplication, because choosing is real functionality. (Ch 7)

**Error promotion** — Converting many small errors into one larger error class to reduce the number of recovery mechanisms. Viable only for rare errors. (Ch 10)

**Exception** (broad sense) — Any uncommon condition that alters normal control flow, including a method returning a special value — not only formal throw/catch. (Ch 10)

**Exception aggregation** — Handling many exceptions with one handler, placed high so it catches the most. (Ch 10)

**Exception masking** — Detecting and handling a condition at a low level so higher levels never learn of it. A form of pulling complexity downward. (Ch 10)

**False abstraction** — An interface that appears simple but omits details callers actually need. Creates obscurity. (Ch 4, 6)

**Fence** — A marker placed in a history list to separate groups of related actions, so one undo request restores a whole group. (Ch 9)

**Formal interface** — The parts of an interface specified explicitly in code and often checkable by the language: signatures, parameter names and types, return types, public variables. (Ch 4)

**Gap buffer** — One candidate implementation for text storage, alongside a linked list of lines and fixed-size character blocks. (Ch 11)

**Implementation inheritance** — A parent class providing default method implementations that subclasses inherit or override. Reduces change amplification but creates parent↔subclass dependencies and information leakage. Use with caution; prefer composition. (Ch 19)

**Informal interface** — The parts of an interface expressible only in comments: high-level behavior, meaning of results, usage constraints, design rationale. **Usually larger and more complex than the formal parts.** (Ch 4)

**Information hiding** — Encapsulating design decisions in a module's implementation so they never appear in its interface. The most important technique for achieving deep modules. Parnas, 1972. (Ch 5)

**Information leakage** — A design decision reflected in multiple modules. "One of the most important red flags in software design." (Ch 5)

**Interface** — Everything a developer working in a *different* module must know to use this one. Describes what a module does, not how. (Ch 4)

**Interface inheritance** — A parent class defining signatures without implementations, each subclass implementing them differently. More implementations → deeper interface. (Ch 19)

**Invariant** — A property of a variable or structure that is always true (e.g. every line ends with a newline). Reduces the special cases code must consider. (Ch 17)

**Micro-benchmark** — A small program measuring the cost of a single operation in isolation; the best way to learn what's expensive. (Ch 20)

**Module** — Any unit of code with an interface and an implementation: a class, a method, a plain function, a subsystem, or a service. (Ch 4)

**Nonobvious code** — Code whose behavior or meaning can't be understood with a quick reading. Red flag. (Ch 18)

**Obscurity** — Important information not being obvious: generic names, undocumented units, hidden dependencies, inconsistency. One of the two causes of complexity. (Ch 2)

**Obvious code** — Code a reader can skim, without much thought, and guess correctly about on the first try. (Ch 18)

**Overexposure** — An API forcing users of common features to learn about rarely used ones. Red flag. (Ch 5)

**Pass-through method** — A method doing almost nothing except passing its arguments to another method with a similar signature. Indicates unclear division of responsibility. Red flag. (Ch 7)

**Pass-through variable** — A variable threaded down a long chain of methods that don't use it. (Ch 7)

**Precondition** — Something that must hold before a method is invoked. Minimize them; document any that remain. (Ch 13)

**Red flag** — A sign that code is probably more complicated than it needs to be. Stop and look for an alternate design. (Ch 1)

**Repetition** — The same or nearly the same code appearing over and over; means you haven't found the right abstractions. Red flag. (Ch 9)

**Shallow module** — A module whose interface is nearly as complex as its implementation. The benefit (not learning the internals) is negated by the cost of learning the interface. Small modules tend to be shallow. Red flag. (Ch 4)

**Side effect** — Any consequence of a method that affects future system behavior but isn't part of the result (adding to an internal structure, writing to the file system). Must be documented. (Ch 13)

**Somewhat general-purpose** — Functionality reflecting current needs, interface general enough for multiple uses. The sweet spot. (Ch 6)

**Special-general mixture** — A general-purpose mechanism containing code specialized for one of its uses. Red flag. (Ch 9)

**Strategic programming** — Making a great design the primary goal, funded by continuous investment; working code is a constraint, not the objective. (Ch 3)

**Tactical programming** — Focusing on getting a feature or fix working as quickly as possible, accepting small complexities. Self-reinforcing and hard to escape. (Ch 3)

**Tactical tornado** — A prolific programmer who ships faster than anyone while working entirely tactically, leaving a wake of destruction for others to clean up. (Ch 3)

**Temporal decomposition** — Module structure based on the order operations execute rather than on information hiding. Tempting because execution order is what's on your mind. Red flag. (Ch 5)

**Unknown unknowns** — You need to know something and there is no way to discover what it is. **The worst of the three symptoms** — the only certain remedy is reading every line, which is impossible. (Ch 2)

**Vague name** — A name broad enough to refer to many different things; conveys little and invites misuse. Red flag. (Ch 14)

**Waterfall model** — Discrete sequential phases with design frozen up front. Fails for software because implementation reveals design problems too late to fix structurally. (Ch 1)

**Zombie server** — A server the cluster considers dead that is in fact still running; the book's example of a cross-module design decision with no natural documentation home. (Ch 13)
