# Test-pruning campaign

Campaign mode prunes the whole test surface of one subsystem in one PR. The
subsystem is a plugin, such as a Telegram integration, or one core area.
The value bar, the retention bar, the candidate evidence, and the validation in
[SKILL.md](SKILL.md) apply to every lane. This file adds the order of work.
Each step ends on its completion criterion. Do not start the next step early.

## 1. Baseline

At a pinned `main` SHA, record these items:

- the test line count and the support line count of the subsystem;
- the pass or fail state of each test file.

Keep the baseline failures in a separate list.

Done when each in-scope test file has a recorded baseline result.

## 2. Lanes and inventory

Split the surface into **lanes** along production owner boundaries, not along
file prefixes. For a messaging plugin, the lanes are: accounts, commands,
context, dispatch, inbound, outbound, persistence, transport, shared, harness,
and live/QA scenarios.
Include the cases of the subsystem at shared core boundaries. Also include its
QA tests and its live-proof harness tests.

Done when each test file and QA scenario that the subsystem owns belongs to
exactly one lane.

## 3. Read-only ledger per lane

Give each lane to its own read-only agent.
The agent reads each assigned test in full, with its parameter tables.
The agent also reads the production owners, with their entry points, callers,
history, and CI routing.
The agent writes each test declaration into a **ledger** with one mark.
A parameterized test (such as an `it.each`) is one declaration. If its rows
need different marks, mark each row.

- `R`: retain. Name the contract and the bug that the test catches. A retained
  test that only moves to a file with a better name stays `R`, with a note of
  the move.
- `F`: retain the contract, but repair the assertion. An example is a vacuous
  negative that passes when only one of several items is missing.
- `C`: consolidate. First name the owner that absorbs the assertion: a sibling
  table case, a stronger boundary suite, or the shared owner in another package.
- `D`: delete. Name the proof that remains, or the reason that no contract
  exists.

Judge a test by its assertions, not by its name.

Done when each declaration in the lane has a mark and an evidence line.

## 4. Layer plan per lane

Use the per-test ledger as input, not as the edit list.
A second read-only pass starts from the ledger and looks for the redundant
**layer**. An example is several suites that replay the same shared helper
through one mock, around a stronger real-boundary suite.
Name the **keeper** suite for each contract.
Prefer the real transport boundary with a fake network to a mocked
collaborator.
Correct each ledger error that this pass finds.

Done when each lane plan names these items:

- its retired files;
- its keeper for each contract;
- the assertions to carry into the keepers;
- the test-only production seams that the plan unlocks.

## 5. Cutover

Edit one lane at a time.
Send all changes to shared harnesses and support files through one owner, one
change after the other.
With each lane, remove the test-only production seams that the lane unlocks:
injection parameters, getters, reset exports, and indirection layers.
Register moved suites in the CI routing and the test inventories.
Update shrink-only line-cap baselines where the repository keeps them.
Write durable test-ownership rules in the `AGENTS.md` of the subsystem. Take the
rules only from mistakes that this campaign actually found.

Done when each lane plan is applied and the keepers of each lane pass.

## 6. Preservation review

Before you claim completion, have independent reviewers compare the deleted
coverage with the keepers. Use one reviewer for each boundary group.
The reviewers look for contracts that lost their only proof.
They also look for new assertions that cannot fail, such as a rejection row that
the production code never reaches.

For each restored contract, make one deliberate **mutation** of the production
owner. Make sure that the keeper goes red. Then restore the source byte for byte.

Done when each reported gap is restored, or rejected with source evidence, and
each restored contract has a caught mutation.

## 7. Product defects

A baseline failure that survives into a keeper is a bug report.
Fix it at its owner, in a separate commit.
Prove the fix through the real user flow, with a **control** run that reverts
the fix and shows the old behavior.
If you find unrelated product discrepancies, record them as follow-ups. Do not
fix them in the campaign.

Done when each repaired defect has a failing control and a passing candidate on
the same harness.

## 8. Reconcile and hand off

Merge `main`. Do not rebase a long campaign with many commits.
When `main` changed a file that the campaign deleted, keep the deletion. Port
the new contract into the keeper.
Make sure that each new regression test that `main` added still has a home.
Run the whole subsystem suite again, and repeat the live proof on the merged
head.

On a diff this large, review tooling probably shows a truncated file list.
Record maintainer decisions about generic compatibility flags in the PR
evidence. Do not edit the gates.

Hand off with the [SKILL.md](SKILL.md) report, plus:

- the baseline and final test and support line counts, with production counted
  separately;
- the lanes, the retired layers, and the keepers;
- the preservation gaps found, and their mutations;
- the product defects, with control proof and candidate proof.
