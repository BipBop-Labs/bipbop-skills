---
name: distill
description: Recover implicit architecture decisions from an existing codebase and git history, rank them, and triage each with the user as accept (write ADR), accident (known debt), reject, or skip, with resumable state. Use when the user runs /adr:distill or asks to bootstrap, extract, or derive ADRs from existing code.
disable-model-invocation: true
argument-hint: "[--since <ref>] [--batch 5] [--reset]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(find *), Bash(wc *), Bash(python3 *), Write, Edit, AskUserQuestion
---

# /adr:distill

Turn what the code already decided into ADRs the user confirms. You find and
rank candidates; the user decides. Standing rules: `../adr/SKILL.md`.

Arguments: `$ARGUMENTS`. `--since <ref>` limits history scanning to commits
after a ref (incremental runs). `--batch N` sets candidates per round
(default 5, maximum 5). `--reset` discards saved state after confirmation.

## State file

`<adr-folder>/.distill-state.json` makes the flow resumable:

```json
{
  "version": 1,
  "last_scanned_commit": "abc1234",
  "candidates": {
    "<stable-key>": {
      "title": "...",
      "verdict": "accepted | debt | rejected | skipped | pending",
      "adr": "ADR-0003",
      "evidence": ["path:line", "commit sha"],
      "updated": "2026-10-02"
    }
  }
}
```

`stable-key` is a slug derived from the main file or dependency the candidate
is about (`dep:httpx`, `boundary:services/billing`, `data:users-table`), so
re-runs recognise the same candidate even if your wording changes. Load the
file at start; never re-ask about `accepted`, `debt`, or `rejected` keys.
`skipped` candidates are shown again only when the user asks ("revisit
skipped") or when their evidence changed since `updated`.

## Procedure

### 1. Prepare

- Require an ADR folder; otherwise offer `/adr:init` and stop.
- Read the index. Existing ADRs are not candidates; a candidate that overlaps
  one becomes "already covered" and is dropped.
- Load the state file if present and tell the user how many candidates are
  already decided and how many are pending or skipped.

### 2. Detect the stack

From manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
`pom.xml`, `build.gradle*`, `*.csproj`, `Gemfile`, `composer.json`, `mix.exs`,
`Package.swift`, `pubspec.yaml`), lockfiles, Dockerfiles, CI config, and
top-level layout. One line per finding. This feeds candidate detection and the
enforcement suggestion at the end.

### 3. Collect candidates

Work from evidence you can cite. Sources, all of them:

- **Dependencies:** each runtime dependency that has a well-known alternative
  (ORM, HTTP client, queue, framework, state manager, test runner). Note
  pinned or vendored versions and `patches/` directories.
- **Boundaries:** top-level modules, packages, services; explicit import rules
  (lint config, `tsconfig` paths, `__init__` re-exports, visibility
  modifiers); shared libraries; the "do not import X from Y" comments.
- **Data:** schemas, migrations, storage formats, serialisation choices, ID
  strategies, soft-delete versus hard-delete, time zones.
- **Interfaces:** API style, versioning, error shape, CLI conventions, config
  sources and precedence, environment variables.
- **Cross-cutting conventions:** error handling, logging, auth, retries,
  concurrency model, feature flags, i18n.
- **Git history:** run `git log --format='%h %ad %s' --date=short` (bounded by
  `--since`). Look for messages with `migrate`, `switch`, `replace`, `adopt`,
  `drop`, `remove`, `revert`, `instead of`, `because`, `BREAKING`. Read the
  bodies of those commits. Reverts and revert-of-revert pairs are strong
  signals. For odd code (a hand-rolled thing where a library exists, a
  disabled feature, an unusual flag), run `git log -L` or `git blame` on that
  spot and read the commit.
- **Comments:** `HACK`, `WORKAROUND`, `FIXME`, `TODO: remove`, `temporary`,
  `do not` and `don't` in comments. These are often known-debt candidates,
  not decisions.

Skip: version bumps, formatting commits, test-only or docs-only changes,
anything already covered by an ADR.

### 4. Rank

Score each candidate 0 to 3 on each axis, sum, sort descending:

- **Hard to reverse:** migration needed, vendor lock-in, public contract.
- **Easy for an agent to break:** an obvious "improvement" would undo it
  (e.g. replacing a hand-rolled client with the popular library the team
  deliberately avoided).
- **Cross-cutting:** touches many files, teams, or layers.

Drop candidates scoring 2 or less unless there are fewer than five in total.
Keep a "Left out as too thin" list for the final report.

### 5. Present in batches of at most 5

For each candidate show, in this order:

1. **What the code does**, with evidence: `path:line` and commit SHAs. Do not
   cite line numbers you have not opened.
2. **Guess at why**, prefixed exactly `Guess (unconfirmed):`. One or two
   sentences. If you have no plausible guess, write `No guess.`
3. **Alternatives apparently avoided**, only when evidence suggests they were
   considered (a removed dependency, a commit message, a comment). Otherwise
   `None visible.`
4. Scores and rank.

Then ask for a verdict. Use AskUserQuestion if available, one question per
candidate, options exactly: **Accept**, **Accident / tech debt**, **Reject**,
**Skip**. Allow free text for corrections. Without the tool, number the
candidates and ask the user to reply with a verdict per number.

### 6. Act on each verdict

- **Accept:** ask for the rationale in one line (or confirm your guess, or
  "unknown"). Write the ADR as `accepted` via the `/adr:new` procedure
  (template, numbering, index, optional `@decision` tag offer). If the user
  gave no reason, `Rationale status: unknown` and keep the guess out of the
  Decision section. Record `verdict: accepted`, `adr: ADR-NNNN`.
- **Accident / tech debt:** add an entry to `known-debt.md` between its
  markers: what, why it exists (as told by the user, or "unknown"), fix when,
  date. Record `verdict: debt`.
- **Reject:** record `verdict: rejected`. Write nothing else.
- **Skip:** record `verdict: skipped`.

Save the state file after every verdict, not at the end, so an interrupted
run loses nothing.

### 7. Next batch or finish

Offer the next batch until candidates run out or the user stops. Then set
`last_scanned_commit` to `git rev-parse HEAD`.

### 8. Enforcement suggestions

For every ADR accepted in this run, say whether it is enforceable or
advisory using `../adr/references/enforcement-by-stack.md` and the detected
stack. Format:

```text
ADR-0003 only-httpx-for-outbound-http: enforceable (banned alternative).
  Suggested: import-linter contract forbidding `requests`, `urllib3`.
ADR-0004 single-writer-journal: advisory. Rely on @decision tag + /adr:review.
```

Offer to add each check. Add nothing without a yes; when adding, follow the
repository's existing lint or test setup and show the diff.

### 9. Report

Summarise: candidates found, accepted (with IDs), debt entries, rejected,
skipped, left out as too thin, checks added, and the validator result from
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py"`.

## Pitfalls

- Writing rationale the user did not give. The guess label is not optional.
- Proposing conventions ("we use 4-space indent") as decisions. Not a trigger.
- More than five per batch. The user's attention is the bottleneck.
- Forgetting the state file; the next run must not re-ask.
- A huge repository: scope by `--since`, or by top-level directory, and say
  what you did not scan.
