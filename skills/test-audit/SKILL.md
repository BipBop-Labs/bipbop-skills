---
name: test-audit
description: "Use whenever you write, change, review, or sweep tests. It gives a gate for new tests and an audit workflow for tests that are low-value, coupled to the implementation, or duplicated, and for the test-only production seams that those tests need."
---

# Test Audit

The skill has three modes and one value bar.

- Authoring mode applies a gate to each new or changed test when you write it.
- Audit mode runs focused sweeps. It looks for tests that re-assert the source,
  duplicate a stronger proof, couple behavior to the implementation, or keep
  test-only production seams alive.
- Campaign mode prunes the whole test surface of one subsystem: every test file
  that a plugin or a core area owns. Before you start a campaign, read
  [CAMPAIGN.md](CAMPAIGN.md).

## Authoring gate

Before you add a test, answer the four questions below. If an answer is
missing, do not add the test yet.

1. What observable behavior, invariant, or independent contract does the test
   protect?
2. What credible regression makes the test fail?
3. Why does the current coverage not catch that failure already? Each contract
   has one primary test owner at the strongest boundary. A test at another layer
   needs its own distinct risk, such as a transport or lifecycle failure that the
   owner cannot reach. Extend a table-driven case or a shared fixture instead of
   adding a near-duplicate test. Consolidate duplicated setup in the same change.
4. Does the test need a production seam (export, flag, wrapper, injection hook)
   that no production caller needs? If yes, move the test to the real boundary.

Then compare the test with each [junk pattern](#junk-patterns). A match fails the
gate, unless the [retention bar](#retention-bar) names the contract that the test
guards independently.
A test that breaks under a behavior-preserving refactor asserts the
implementation, not the behavior. Rewrite it at the owning boundary before you
land it.

A bug regression test must fail on the pre-fix code for the intended reason. It
must pass after the repair at the owner boundary. One regression test at the
owner boundary covers the bug. Do not replay the same scenario at each layer
that the bug crosses.

## Junk patterns

All modes use this checklist.

- assertion-free coverage probes;
- self-comparisons and identity copiers;
- copied fixtures, inventories, manifests, or export lists;
- exact source, import, or string greps;
- tests of a private predicate or call shape that duplicate tests at real
  boundaries;
- duplicate invocations of the same contract;
- provider-local replays of shared helpers;
- tests that only keep test-only exports, globals, or wrappers alive;
- dead production code that only tests call;
- expected values that the helper or renderer under test produces;
- mocks that implement the asserted behavior, or one identical mock that stands
  in for different APIs;
- fixtures that supply the receipt, the admission, or the callback order that
  the owner must produce;
- persistence asserted against a store that the path never writes;
- capability tests that restate declared flags, and do not exercise the
  delivery or the acknowledgement that the flag promises;
- negative controls that pass for an unrelated reason, such as a denial from a
  different guard or a rejection that the production path never reaches;
- names or fixtures that promise more than the input exercises, such as a
  "retires the window" test that asserts that the window was not cleared.

## Value bar

A test must pay for its maintenance cost. It must protect a behavior, a
credible regression, or an independently meaningful contract.
In an audit, an existing test that must change for a behavior-preserving source
reorganization is suspect. It is not automatically deletable. The authoring gate
still rejects new tests of this kind.

Before you judge a candidate, read these items:

- the complete test and its production owner;
- the entry point, the callers, and the callees of the owner;
- sibling implementations and overlapping tests;
- the CI routing and the relevant history.

Read the root and the scoped `AGENTS.md` files first.
If the test claims a behavior that depends on a dependency, read the source or
the types of that dependency directly.

## Discovery

Keep discovery read-only. Report the evidence before you edit.
For a broad scope, run parallel discovery lanes when they are available:

- core and packages (`src/`, `packages/`);
- plugins and extensions;
- UI, apps, scripts, and tooling;
- a cross-cutting pattern sweep.

Outside campaign mode, report a few high-confidence candidates, not a large
speculative inventory. Look for the [junk patterns](#junk-patterns).

## Retention bar

Keep a test when it independently enforces one of these contracts: public API,
plugin SDK, protocol, config, migration, storage, security, platform, default,
prompt-byte, generated cross-language, package, release, or architecture.
Also keep these tests:

- a test of call order, when the order is observable behavior;
- a regression test with a credible failure mode;
- a source inspection, when it is the cheapest independent guard. It fails when
  the contract changes (the user-facing key, byte, or path), and it survives a
  refactor that only changes identifiers;
- a retained test that fails on the baseline. Treat the failure as a possible
  product bug. Reproduce it, and repair the owner. Do not delete the test.

A static or slow test is not a reason to delete it.
A test that looks like the implementation can still be the independent
contract. Prove that it is not before you remove it.

## Candidate evidence

Record each field below before you edit. If a field is missing, the candidate is
not ready for deletion.

- the exact test name and location;
- the failure that the test can actually detect;
- the non-test callers of the production seam or support seam that the test
  covers;
- the stronger owner-boundary proof that remains, or the reason that no proof
  is necessary;
- the relevant history, and the reason that the test or seam exists;
- the production or test-support code that the deletion unlocks;
- the risk, and the focused validation command.

## Edit shape

Choose one coherent batch at one owner boundary.
Delete obsolete test-only exports, globals, wrappers, and dead production paths.
Do not keep aliases for them.
Move retained regression tests to their canonical owners.
Consolidate repeated package or dependency assertions into one generic contract.

Aim for a net-negative count of production LOC.
Do not add replacement tests that restate the same implementation.
Do not turn uncertain candidates into cleanup to increase the deletion count.

## Validation

Never edit source or tests while the test runner runs in the checkout.
Obey the testing instructions of the repository. Send heavy proof through the
path that those instructions give.

1. Run the smallest owner and sibling tests with the test command of the
   repository. Filter the command to the path or the test name.
2. For removed source greps or plan assertions, run the executable script or
   the dry-run that owns the real contract.
3. Run targeted formatting. Then run `git diff --check`.
4. Classify the changed paths. Then run the changed gate that the repository
   policy requires.
5. Inspect `git diff --numstat`. Report production and tooling separately from
   tests and test support.
6. After the final audit edits, run the review step that the repository requires.

## Landing and continuation

Commit, push, open a PR, or land only when you have authorization.
Use the PR flow of the repository.
Land one coherent PR at a time.
After you land a PR, refresh from the current `main`. Then run read-only
discovery again for the next high-confidence batch.

## Handoff

Report:

- the root cause and the low-value categories that you removed;
- the simplifications to production owners;
- the retained false positives, and why they stay valuable;
- the focused proof and the full proof that you actually ran;
- production LOC versus test LOC;
- the PR state and the merge state;
- named follow-ups.
