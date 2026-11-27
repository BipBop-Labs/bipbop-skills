---
name: fix
description: "Fix a bug at its root cause, with a failing repro first and proof on the same surface. Use for /fix, or when the user reports a bug, an error, a crash, a regression, or a failing test, or asks to fix, debug, or \"arregla\" something."
---

# Fix

Every line you ship must come from runtime evidence. A change that "might help" is a hypothesis, not a fix: do not ship it. If the evidence refutes a hypothesis, revert the changes it caused.

## Procedure

1. **Reproduce.** Reproduce the bug yourself, on the surface where it happens (browser, API, CLI, worker, test). If it does not reproduce, make the trigger: tighten the conditions, build the input, or add logging until it fires. Ask the user only when you cannot reach that surface, and say why.
2. **Find the cause.** Write the candidate hypotheses. Each pass, pick the check that removes the most hypotheses, run it, and read the real state (logs, values, queries, git history of the code). Do not guess. Stop when one mechanism is left and runtime evidence confirms it.
3. **Decide what is wrong.** The root cause is the first place where the system does something it must not do, or does not handle a state it must handle.
   - If the state that triggered the bug is legitimate, handle it where the code broke.
   - If the state must never exist, find the code that produced it. A guard, retry, swallowed error, or default at the symptom only hides the bug.
4. **Fix the pattern.** Search for every place with the same fault and fix them all.
5. **Leave it better.** If the design of the section caused the bug (a decision in two places, booleans that must stay in sync, a wrapper that hides state), refactor that section in the same change, with `code-principles`. Keep the refactor inside the code the bug touches. Ship the smallest change that fixes the cause.
6. **Test first.** When the bug has a cheap local test, write a test that fails on the bug. Commit it before the fix, so the history shows it failing and then passing. Skip the test when it would be expensive or unclear, and say why.
7. **Verify on the same surface.** Run the original repro again on the surface from step 1. "Inconclusive" or a different surface is not a pass. Unit tests show branch behavior, not that the bug is gone.
8. If the cause took a deep search to find, propose the cheap, always-on signal (a log, a metric, an assertion) that would have shown it at once.

## Reply

What was broken, the root cause, the fix, what you refactored and why, and how you verified. Paste the repro output before and after the fix, as it is.
