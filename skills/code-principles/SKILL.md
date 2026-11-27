---
name: code-principles
description: "Design checks for code: one decision in one place, low reader load, domain models, types at boundaries, simple interfaces, subtraction, root-cause fixes, safe state changes, names and comments. Use when reviewing a diff for design or designing a module or interface. Not for bugs, security, style, or tests."
---

# Code principles

Report a finding only when a check fails for code the diff adds or makes worse.

## Checks

1. **One decision, one place.** A format, rule, limit, or list of allowed values lives in one module. When the project generates types from a schema, use them. Test: name a likely change and count the files it touches. Two or more is a finding. Skip trivial repeated lines.
2. **Low reader load.** Remove wrappers with one caller, adapters with one implementation, and methods that only forward. Keep state in the smallest scope: return over mutate, local over field, field over module state. Derive values. Do not sync copies. Test: can a reader find where X is set and what changes it? Split a long function only when a part has its own name and its own reason to change.
3. **Model the domain.** Use a state machine, discriminated union, map, or typed model in place of scattered booleans, phase checks, or if/else chains across files. Test: does the feature add one more branch to a chain, or a second boolean that must stay in sync with the first? Keep plain code when the shape is local and will not grow.
4. **Types at the boundary.** Parse external data (requests, config, env, rows, API responses) into domain types where it enters. Inside, trust the types: no repeated validation, no redundant null checks. Give two primitives different types when the code can mix them up. Narrow types so bad values cannot exist. Handle a case inside the module when the caller cannot do anything useful with it. Errors that the caller must decide on (permissions, user input, remote failures) stay errors.
5. **Simple interface over simple implementation.** Do not add a parameter, flag, or exception that makes every caller choose what the module can choose with a good default. Keep a parameter when callers need different values. A default for missing data falls under check 7.
6. **Subtract.** Do not add speculative guards, parsers, options, or edge cases that the spec does not need. When an API changes, migrate every caller in the same change or stack. Delete the old path in that change or stack too, unless outside users depend on it.
7. **Fix the cause.** A guard, retry, swallowed error, clamped value, or default that hides a state that should never exist is a finding. Fix the code that produces the state. Fix every place with the same fault.
8. **Safe state changes.** An operation that changes state must give the correct result when it runs twice, or after a crash at any point. To do this, read the current state. Apply the difference in one transaction, or with an upsert or a unique constraint. For files, write to a temp path, then rename it. Each concurrent actor writes its own key, file, or row. Merge them on read. Lock (`SELECT FOR UPDATE`, a lockfile) only when one shared target is a real invariant.
9. **Names and comments.** A thing that is hard to name, or needs a long comment to explain how it works, has a design problem. Fix the design. Flag vague names (`data`, `info`, `manager`). Comments give the reason, units, invariants, and edge cases. They never repeat what the code already says.

## Review

1. Read the project ADRs and conventions. A choice that a project rule makes is not a finding.
2. For each changed module, read its full interface and at least two callers.
3. For each finding, name the future change or failure that it causes. Write the fix. If a finding has no cost or no fix, drop it.

## Output

- At most 3 findings, highest cost first, each marked as a suggestion unless the calling review sets the severity.
- Each: `file:line`, check name, the change or failure it causes, the fix. One to three lines.
- No praise, no "this is fine", no summary.
- No findings: one line.
- In a combined review: give every candidate in that review's format. That review verifies, labels, and caps them.

## Design

1. Write the interface comment first. If it is long or hard to write, change the design.
2. Sketch two different designs. Compare them with the checks. Pick one.
3. For each new class, function, parameter, or error, name what it removes. If it removes nothing, do not add it.
