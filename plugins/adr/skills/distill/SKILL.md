---
name: distill
description: Find qualifying lasting design constraints in code and history, filter out implementation-only or already documented choices, rank remaining candidates, and triage each with the user as accept (write ADR), accident (known debt), reject, or skip, with resumable state. Use when the user runs /adr:distill or asks to bootstrap, extract, or derive ADRs from existing code.
disable-model-invocation: true
argument-hint: "[--since <ref>] [--batch 5] [--reset]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(find *), Bash(wc *), Bash(python3 *), Write, Edit, AskUserQuestion
---

# /adr:distill

Inspect code and history for evidence of lasting architectural intent missing
from authoritative sources. Apply the eligibility filter before ranking; do not
turn an implementation inventory into ADRs. The user confirms intent. Standing
rules: `../adr/SKILL.md`.

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
- Read the index. Drop information already covered. If new qualifying intent
  belongs to an existing ADR, propose updating or consolidating affected ADRs
  instead of creating another record.
- Load the state file if present and tell the user how many candidates are
  already decided and how many are pending or skipped.

### 2. Detect the stack

From manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
`pom.xml`, `build.gradle*`, `*.csproj`, `Gemfile`, `composer.json`, `mix.exs`,
`Package.swift`, `pubspec.yaml`), lockfiles, Dockerfiles, CI config, and
top-level layout. One line per finding. This feeds candidate detection and the
enforcement suggestion at the end.

### 3. Collect candidates

Work from evidence you can cite. The sources below are investigation signals,
not automatic candidates. Apply the eligibility filter in `../adr/SKILL.md`
before retaining a candidate. Repetition alone does not establish a norm.
Record uncertain intent as a question to resolve before promoting a candidate.
Sources:

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
anything already fully covered by an ADR.

### 4. Rank

Score only candidates that passed the eligibility filter, 0 to 3 on each
axis, sum, sort descending:

- **Hard to reverse:** migration needed, vendor lock-in, public contract.
- **Easy for an agent to break:** an obvious "improvement" would undo it
  (e.g. replacing a hand-rolled client with the popular library the team
  deliberately avoided).
- **Cross-cutting:** touches many files, teams, or layers.

Drop candidates scoring 2 or less. Never retain a weak candidate to fill a
batch. Zero qualifying candidates is a successful outcome; report that no ADR
is warranted without creating ADR or replacement documentation files. Skip
triage and enforcement; finish with the scan-state update and report in steps
7 and 9.
Keep a "Left out as too thin" list for the final report.

### 5. Present in batches of at most 5

For each candidate show, in this order:

1. **Design constraint and evidence**, with inspected `path:line` and commit
   SHAs. Distinguish observed behavior from confirmed intent.
2. **Missing information and future design risk**: what an ADR would add
   beyond code, tests, configuration, and existing documentation.
3. **Confirmed rationale and alternatives**, only when supported. Otherwise
   state `Unknown`; ask rather than filling the gap with a plausible story.
4. Scores and rank.

Then ask for a verdict. Use AskUserQuestion if available, one question per
candidate, options exactly: **Accept**, **Accident / tech debt**, **Reject**,
**Skip**. Allow free text for corrections. Without the tool, number the
candidates and ask the user to reply with a verdict per number.

### 6. Act on each verdict

- **Accept:** confirm the constraint and ask for the rationale in one line (or
  "unknown"). Record the confirmed current constraint as `accepted` via `/adr:new`,
  preferring an existing ADR where its scope fits
  (template, numbering, index, optional `@decision` tag offer). Never create
  replacement chains or preserve obsolete records for history. If the user
  gave no reason, `Rationale status: unknown` and omit speculative reasons
  from the record. Acceptance does not waive the eligibility filter. Record
  `verdict: accepted`, `adr: ADR-NNNN`.
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
ADR-0003 isolated-extension-execution: enforceable (boundary rule).
  Suggested: dependency check preventing application imports of extension code.
ADR-0004 single-writer-journal: advisory. Rely on @decision tag + /adr:review.
```

Offer to add each check. Add nothing without a yes; when adding, follow the
repository's existing lint or test setup and show the diff.

### 9. Report

Summarise: candidates found, accepted (with IDs), debt entries, rejected,
skipped, left out as too thin, checks added, and the validator result from
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py"`.

## Pitfalls

- Inventing architectural intent or rationale from observed implementation.
- Proposing conventions ("we use 4-space indent") as decisions. Does not qualify.
- More than five per batch. The user's attention is the bottleneck.
- Forgetting the state file; the next run must not re-ask.
- A huge repository: scope by `--since`, or by top-level directory, and say
  what you did not scan.
