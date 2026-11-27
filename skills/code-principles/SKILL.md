---
name: code-principles
description: "The coding mindset: nine principles for all code, in any language. Use every time you design, write, fix, or refactor code. The plugin loads them at the start of each session."
---

# Code principles

Apply these principles to all code you write or change. Apply them while you design, while you write, and before you report the work as done.

## Principles

1. **One decision, one place.** Keep a format, rule, limit, or list of allowed values in one module. When the project generates types from a schema, use them. Test: name a likely change and count the files it touches. Two or more files fail the test. Trivial repeated lines do not count.
2. **Low reader load.** Do not write wrappers with one caller, adapters with one implementation, or methods that only forward. Keep state in the smallest scope: return over mutate, local over field, field over module state. Derive values. Do not sync copies. Test: can a reader find where X is set and what changes it? Split a long function only when a part has its own name and its own reason to change.
3. **Model the domain.** Use a state machine, discriminated union, map, or typed model in place of scattered booleans, phase checks, or if/else chains across files. Test: does the change add one more branch to a chain, or a second boolean that must stay in sync with the first? Keep plain code when the shape is local and will not grow.
4. **Types at the boundary.** Parse external data (requests, config, env, rows, API responses) into domain types where it enters. Inside, trust the types: no repeated validation, no redundant null checks. Give two primitives different types when the code can mix them up. Narrow types so bad values cannot exist. Handle a case inside the module when the caller cannot do anything useful with it. Errors that the caller must decide on (permissions, user input, remote failures) stay errors.
5. **Simple interface over simple implementation.** Do not add a parameter, flag, or exception that makes every caller choose what the module can choose with a good default. Keep a parameter when callers need different values. A default for missing data falls under principle 7.
6. **Subtract.** Remove before you add. Do not add speculative guards, parsers, options, or edge cases that the spec does not need. When an API changes, migrate every caller in the same change or stack, and delete the old path, unless outside users depend on it.
7. **Fix the cause.** Do not hide a state that should never exist with a guard, retry, swallowed error, clamped value, or default. Fix the code that produces the state. Fix every place with the same fault.
8. **Safe state changes.** An operation that changes state must give the correct result when it runs twice, or after a crash at any point. Read the current state. Apply the difference in one transaction, or with an upsert or a unique constraint. For files, write to a temp path, then rename it. Each concurrent actor writes its own key, file, or row. Merge them on read. Lock (`SELECT FOR UPDATE`, a lockfile) only when one shared target is a real invariant.
9. **Names and comments.** If a thing is hard to name, or needs a long comment to explain how it works, change the design. Do not use vague names (`data`, `info`, `manager`). Comments give the reason, units, invariants, and edge cases. They never repeat what the code already says.

## When you code

1. Read the project ADRs and conventions first. A project rule wins over these principles.
2. Get the data shape and types right before the logic.
3. For a new module or interface, write the interface comment first. If it is long or hard to write, change the design. Sketch two different designs and pick one.
4. For each new class, function, parameter, or error, name what it removes. If it removes nothing, do not add it.
5. Before you report the work as done, read your diff against the principles. Fix what fails.

