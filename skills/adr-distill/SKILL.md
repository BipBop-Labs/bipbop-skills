---
name: adr-distill
description: Find qualifying lasting design constraints in code and history. Remove implementation-only choices and choices that docs already cover, rank the remaining candidates, and triage each one with the user as accept (write ADR), accident (known debt), reject, or skip. The state is saved so a run can resume. Use when the user runs /bipbop-skills:adr-distill or asks to bootstrap, extract, or derive ADRs from existing code.
disable-model-invocation: true
argument-hint: "[--since <ref>] [--batch 5] [--reset]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(find *), Bash(wc *), Bash(python3 *), Write, Edit, AskUserQuestion
---

# /bipbop-skills:adr-distill

Examine code and history for evidence of lasting architectural intent that authoritative
sources do not record. Apply the eligibility filter before you rank. Do
not turn an inventory of the implementation into ADRs. The user confirms intent. Standing
rules: `../adr/SKILL.md`.

Arguments: `$ARGUMENTS`. `--since <ref>` limits the history scan to commits
after a ref (incremental runs). `--batch N` sets the candidates per round
(default 5, maximum 5). `--reset` discards the saved state after the user confirms.

## State file

`<adr-folder>/.distill-state.json` lets the flow resume:

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

`stable-key` is a slug from the main file or dependency of the candidate
(`dep:httpx`, `boundary:services/billing`, `data:users-table`). With this key,
a new run recognizes the same candidate when your wording changes. Load the
file at the start. Never ask again about `accepted`, `debt`, or `rejected` keys.
Show `skipped` candidates again only when the user asks ("revisit
skipped") or when their evidence changed after `updated`.

## Procedure

### 1. Prepare

- An ADR folder is necessary. If there is none, offer `/bipbop-skills:adr-init` and stop.
- Read the index. Drop information that the index already covers. If new qualifying intent
  belongs to an existing ADR, propose to update or consolidate the affected ADRs.
  Do not create a new record for it.
- Load the state file if it exists. Tell the user how many candidates have
  a decision and how many are pending or skipped.

### 2. Detect the stack

Use manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
`pom.xml`, `build.gradle*`, `*.csproj`, `Gemfile`, `composer.json`, `mix.exs`,
`Package.swift`, `pubspec.yaml`), lockfiles, Dockerfiles, CI config, and the
top-level layout. Write one line per finding. This step feeds the candidate search and the
enforcement suggestion at the end.

### 3. Collect candidates

Examine the implementation, checks and configuration, existing documentation, and
relevant Git history for evidence of design intent. Cite only the files and commits that you
actually read. These sources are evidence. They are not automatic candidates.

Apply the routing test in "Three kinds of rule doc" in `../adr/SKILL.md`
to each candidate. A team rule with no tradeoff (a style rule, a metric
definition, a review gate) is a policy candidate. A repeated sequence of manual
steps is a procedure candidate. A rule that a lint or test can state is a
check candidate, not a doc. Label each candidate with its kind.

Apply "When an ADR is warranted" in `../adr/SKILL.md` before you keep an ADR
candidate. Ask the user when the intent is not certain. Drop information that docs already
cover fully. When new context fits in a related ADR, propose an update to that ADR.

### 4. Rank

Score only the candidates that passed the eligibility filter. Give 0 to 3 on each
axis, add the scores, and sort from highest to lowest:

- **Hard to reverse:** needs a migration, vendor lock-in, public contract.
- **Easy for an agent to break:** an obvious "improvement" would undo it
  and break a confirmed constraint.
- **Cross-cutting:** touches many files, teams, or layers.

Drop candidates with a score of 2 or less. Never keep a weak candidate to fill a
batch. Zero qualifying candidates is a successful result. In that case, report that no ADR
is warranted, and create no ADR or replacement documentation files. Skip
triage and enforcement. Finish with the scan-state update and the report in steps
7 and 9.
Keep a "Left out as too thin" list for the final report.

### 5. Show candidates in batches of 5 or fewer

For each candidate, show these items in this order:

1. **Design constraint and evidence**, with the `path:line` and commit
   SHAs that you examined. Keep observed behavior separate from confirmed intent.
2. **Missing information and future design risk**: what an ADR would add
   to code, tests, configuration, and existing documentation.
3. **Confirmed rationale and alternatives**, only when evidence supports them. Otherwise,
   write `Unknown`. Ask. Do not fill the gap with a plausible story.
4. Scores and rank.

Then ask for a verdict. Use AskUserQuestion if it is available, with one question per
candidate and exactly these options: **Accept**, **Accident / tech debt**, **Reject**,
**Skip**. Allow free text for corrections. If the tool is not available, number the
candidates and ask the user to reply with one verdict per number.

### 6. Act on each verdict

- **Accept a policy or procedure candidate:** write it with the "Policy or
  procedure" steps of `/bipbop-skills:adr-new`. Record `verdict: accepted` and
  `doc: <path>` in place of `adr`.
- **Accept an ADR candidate:** confirm the constraint. Ask for the rationale in one line (or
  "unknown"). Use `/bipbop-skills:adr-new` to record the confirmed current constraint as `accepted`.
  Prefer an existing ADR where its scope fits
  (template, numbering, index, optional offer of a `@decision` tag). Never create
  replacement chains, and never keep obsolete records for history. If the user
  gave no reason, use `Rationale status: unknown` and keep speculative reasons out of
  the record. Acceptance does not cancel the eligibility filter. Record
  `verdict: accepted`, `adr: ADR-NNNN`.
- **Accident / tech debt:** add an entry to `known-debt.md` between its
  markers: what, why it exists (as the user tells it, or "unknown"), fix when,
  date. Record `verdict: debt`.
- **Reject:** record `verdict: rejected`. Write nothing else.
- **Skip:** record `verdict: skipped`.

Save the state file after each verdict, not at the end. Then an interrupted
run loses nothing.

### 7. Next batch or finish

Offer the next batch until there are no more candidates or the user stops. Then set
`last_scanned_commit` to `git rev-parse HEAD`.

### 8. Enforcement suggestions

For each ADR that this run accepted, say if it is enforceable or
advisory. Use `../adr/references/enforcement-by-stack.md` and the detected
stack. Format:

```text
ADR-NNNN <current constraint>: enforceable or advisory.
  Suggested: <check that protects the constraint, if appropriate>.
```

Offer to add each check. Add nothing without a yes. When you add a check,
follow the existing lint or test setup of the repository and show the diff.

### 9. Report

Give a summary: candidates found, accepted (with IDs), debt entries, rejected,
skipped, left out as too thin, checks added, and the validator result from
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr/scripts/validate-adrs.py"`.

## Pitfalls

- Architectural intent or rationale invented from the observed implementation.
- Conventions ("we use 4-space indent") proposed as decisions. They do not qualify.
- More than five candidates per batch. The attention of the user is the bottleneck.
- A forgotten state file. The next run must not ask again.
- A very large repository. Limit the scope with `--since` or by top-level directory, and say
  what you did not scan.
