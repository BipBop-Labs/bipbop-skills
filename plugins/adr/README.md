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
| `new` | `/adr:new` | Record a decision from the conversation or diff, with the user confirming the decision and the why. Updates or consolidates related records. |
| `review` | `/adr:review` | Check a diff or branch against accepted ADRs. Report only. |

Plus `scripts/validate-adrs.py`, a dependency-free Python script for
structural validation, and an optional, off-by-default Stop hook that
suggests checking applicable ADRs and the eligibility filter (see [hooks/README.md](hooks/README.md)).

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

## Update

```text
/plugin marketplace update bipbop
/plugin update adr@bipbop
/reload-plugins
```

Codex CLI:

```bash
codex plugin marketplace upgrade bipbop
```

## Typical workflow

1. `/adr:init` in the target repository. It creates `docs/adr/` with
   `README.md` (index), `template.md`, `known-debt.md`, adds a short block to
   `CLAUDE.md` or `AGENTS.md`, and offers to wire the validator into
   pre-commit or CI. If ADRs already exist elsewhere, it adopts them.
2. `/adr:distill` on an existing codebase. Only qualifying candidates arrive,
   at most five at a time,
   with evidence, missing architectural intent, and future design risk.
   Zero candidates is a valid outcome. You accept, mark as debt, reject, or
   skip. State lives in `docs/adr/.distill-state.json`, so later runs do not
   re-ask and new code can be distilled incrementally.
3. `/adr:new` only when the [eligibility filter](skills/adr/SKILL.md#when-an-adr-is-warranted)
   identifies important, lasting architectural intent missing from authoritative
   sources. Implementation changes alone do not qualify; keep their rules in
   code, tests, or configuration.
4. `/adr:review` before merging, to see which accepted decisions a diff
   touches, which changes need an ADR, and which known-debt items it fixes.

## ADR format

`docs/adr/NNNN-slug.md` with YAML frontmatter:

```yaml
---
id: ADR-0003
title: Outbound HTTP goes through one client
status: accepted        # proposed | accepted
date: 2026-10-02
deciders: [maria]
tags: [http, dependencies]
paths: [src/net/**]
---
```

Sections: Context, Decision, Options considered, Consequences, Rationale
status (`confirmed` or `unknown`), Evidence. Full template in
[skills/adr/templates/adr-template.md](skills/adr/templates/adr-template.md).

Rules: keep a small, concise set of current constraints. Confirm substantive
changes, rewrite affected ADRs in place, consolidate overlap, and delete obsolete
or rejected documents. Renumber as needed to keep consecutive IDs and repair
all references in the same change. Git preserves history. Do not add `History` sections,
supersession metadata, archive copies, or replacement records. A
`@decision ADR-NNNN` comment in code means read that ADR before touching the
spot. `known-debt.md` lists things that look deliberate but are not; agents
may fix those.

## Validation script

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/validate-adrs.py" [--root .] [--adr-dir docs/adr] [--strict] [--fail-on-proposed] [--json] [--no-code-scan]
python3 "$CLAUDE_PLUGIN_ROOT/scripts/validate-adrs.py" --print-setup   # pre-commit and CI snippets
```

Checks: required frontmatter and allowed statuses; unique consecutive IDs matching
filenames; index in sync with the folder;
rejection of obsolete statuses and supersession metadata; referenced paths still existing (warning); `@decision`
tags pointing to existing ADRs. With `--fail-on-proposed`,
an ADR still `proposed` is an error. Exit codes: `0` clean, `1` errors (or
warnings with `--strict`), `2` no ADR folder or bad usage.

It does not judge whether code complies with a decision. That is
`/adr:review` and per-decision checks from
[skills/adr/references/enforcement-by-stack.md](skills/adr/references/enforcement-by-stack.md).

For CI, copy the script into the repository (`/adr:init` offers to) so the
job does not depend on a plugin cache path, and run it with
`--strict --fail-on-proposed` so an undecided draft does not merge. Remove rejected drafts.
Leave `--fail-on-proposed` out of pre-commit hooks: drafting a
`proposed` ADR locally is normal.

## Migrating existing collections

This lifecycle changes earlier plugin behavior. Adoption does not automatically
rewrite a repository. For an authorized migration, rewrite current decisions,
remove obsolete/rejected records, remove `History` and supersession fields, and
renumber as needed, and repair IDs, filenames, the index, and all references. The
validator reports legacy terminal statuses and supersession metadata as errors.

## Design notes

[RESEARCH.md](RESEARCH.md) covers the format choice, existing tooling, prior
Claude Code art, the enforcement table, and the evidence, including what is
not proven.
