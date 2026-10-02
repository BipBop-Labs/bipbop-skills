# adr

Architecture Decision Records (ADRs) for any repository, built for coding
agents. The plugin tells agents *why* code is the way it is, stops them from
undoing deliberate decisions, and turns the important ones into checks.
Nothing in it assumes a language or framework.

## What it does

| Skill | Invoke as | Purpose |
| --- | --- | --- |
| `adr` | automatic | Standing rules: format, status lifecycle, when to write an ADR, how agents read them, known-debt log, rationale honesty. |
| `init` | `/adr:init` | Create or adopt the ADR folder, template, index, `known-debt.md`, and the CLAUDE.md/AGENTS.md pointer. Idempotent. |
| `distill` | `/adr:distill` | Recover implicit decisions from code and git history, rank them, and triage each as accept, accident/tech debt, reject, or skip. Resumable. |
| `new` | `/adr:new` | Record a decision from the conversation or diff, with the user confirming the decision and the why. Handles superseding. |
| `review` | `/adr:review` | Check a diff or branch against accepted ADRs. Report only. |

Plus `scripts/validate-adrs.py`, a dependency-free Python script for
structural validation, and an optional, off-by-default Stop hook that
suggests `/adr:new` (see [hooks/README.md](hooks/README.md)).

## Install

```text
/plugin marketplace add BipBop-Labs/bipbop-skills
/plugin install adr@bipbop
```

Codex CLI:

```bash
codex plugin marketplace add BipBop-Labs/bipbop-skills --ref main
codex plugin add adr@bipbop
```

## Typical workflow

1. `/adr:init` in the target repository. It creates `docs/adr/` with
   `README.md` (index), `template.md`, `known-debt.md`, adds a short block to
   `CLAUDE.md` or `AGENTS.md`, and offers to wire the validator into
   pre-commit or CI. If ADRs already exist elsewhere, it adopts them.
2. `/adr:distill` on an existing codebase. Candidates arrive five at a time
   with evidence, a clearly labelled guess at the rationale, and the
   alternatives apparently avoided. You accept, mark as debt, reject, or
   skip. State lives in `docs/adr/.distill-state.json`, so later runs do not
   re-ask and new code can be distilled incrementally.
3. `/adr:new` whenever a change hits a trigger (new dependency, boundary,
   data model, public interface, hard-to-reverse or questionable choice).
4. `/adr:review` before merging, to see which accepted decisions a diff
   touches, which changes need an ADR, and which known-debt items it fixes.

## ADR format

`docs/adr/NNNN-slug.md` with YAML frontmatter:

```yaml
---
id: ADR-0003
title: Outbound HTTP goes through one client
status: accepted        # proposed | accepted | superseded | deprecated | rejected
date: 2026-10-02
deciders: [maria]
tags: [http, dependencies]
paths: [src/net/**]
supersedes: []
superseded_by: []
---
```

Sections: Context, Decision, Options considered, Consequences, Rationale
status (`confirmed` or `unknown`), Evidence. Full template in
[skills/adr/templates/adr-template.md](skills/adr/templates/adr-template.md).

Rules: an accepted ADR's Decision is never edited; supersede it. A
`@decision ADR-NNNN` comment in code means read that ADR before touching the
spot. `known-debt.md` lists things that look deliberate but are not; agents
may fix those.

## Validation script

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/validate-adrs.py" [--root .] [--adr-dir docs/adr] [--strict] [--json] [--no-code-scan]
python3 "$CLAUDE_PLUGIN_ROOT/scripts/validate-adrs.py" --print-setup   # pre-commit and CI snippets
```

Checks: required frontmatter and allowed statuses; unique, sequential
numbers matching filenames; index in sync with the folder; supersede links
resolving both ways; referenced paths still existing (warning); `@decision`
tags pointing to existing, non-superseded ADRs. Exit codes: `0` clean, `1`
errors (or warnings with `--strict`), `2` no ADR folder or bad usage.

It does not judge whether code complies with a decision. That is
`/adr:review` and per-decision checks from
[skills/adr/references/enforcement-by-stack.md](skills/adr/references/enforcement-by-stack.md).

For CI, copy the script into the repository (`/adr:init` offers to) so the
job does not depend on a plugin cache path.

## Design notes

[RESEARCH.md](RESEARCH.md) covers the format choice, existing tooling, prior
Claude Code art, the enforcement table, and the evidence, including what is
not proven.
