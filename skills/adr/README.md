# adr

Architecture Decision Records (ADRs), policies, and procedures for any
repository, built for coding agents. The `adr` skills do three things:

- It tells agents *why* the code is as it is.
- It stops agents from undoing deliberate decisions.
- It turns the important decisions into checks.

Nothing in it assumes a language or framework.

## Three kinds of rule doc

| Kind | Folder | Holds |
| --- | --- | --- |
| ADR | `docs/adr/NNNN-slug.md` | How the system is built, with real options and a tradeoff |
| Policy | `docs/policies/<name>.md` | A rule or definition to obey (writing rule, metric definition, review gate) |
| Procedure | `docs/procedures/<name>.md` | Numbered steps for one task (deploy order, backfill) |

Routing test, in order:

1. Code, lint, test, or config.
2. ADR.
3. Procedure.
4. Policy.
5. Split a doc that mixes kinds.

One rule, one doc: other docs
and agent instruction files link to the rule and do not restate it. A rule with no
tradeoff is a policy. The full rules are in [skills/adr/SKILL.md](SKILL.md).

Policy frontmatter: `title`, `status`, `owner`, `paths`, `last_reviewed`,
`review_in`. Procedure frontmatter: `title`, `owner`, `paths`, `trigger`,
`last_verified`. The file name is the ID, so you never renumber.

## What it does

| Skill | Invoke as | Purpose |
| --- | --- | --- |
| `adr` | automatic | Standing rules: format, status lifecycle, when to write an ADR, how agents read ADRs, known-debt log, rationale honesty. |
| `adr-init` | `/bipbop-skills:adr-init` | Create or adopt the ADR folder, template, index, `known-debt.md`, and the CLAUDE.md/AGENTS.md pointer. Offers `docs/policies/` and `docs/procedures/`. A second run changes nothing. |
| `adr-distill` | `/bipbop-skills:adr-distill` | Recover implicit decisions from code and git history, rank them, and triage each one as accept, accident/tech debt, reject, or skip. A stopped run can resume. |
| `adr-new` | `/bipbop-skills:adr-new` | Record an ADR, policy, or procedure from the conversation or diff. Chooses the kind with the routing test. Updates or consolidates related records. |
| `adr-review` | `/bipbop-skills:adr-review` | Check a diff or branch against accepted ADRs, policies, and procedures. Report only. |

The `adr` skill also has [`scripts/validate-adrs.py`](scripts/validate-adrs.py), a Python script with no dependencies
that validates structure. It also has an optional Stop hook, off by default, that
suggests a check of the applicable ADRs and the eligibility filter (see [references/stop-hook.md](references/stop-hook.md)).

These skills ship in the `bipbop-skills` plugin. To install it, see the
[root README](../../README.md).

## Typical workflow

1. Run `/bipbop-skills:adr-init` in the target repository. It creates `docs/adr/` with
   `README.md` (index), `template.md`, and `known-debt.md`. It adds a short block to
   `CLAUDE.md` or `AGENTS.md`. It offers to wire the validator into
   pre-commit or CI. If ADRs already exist in a different folder, it adopts them.
2. Run `/bipbop-skills:adr-distill` on an existing codebase. It shows only qualifying candidates,
   five or fewer at a time,
   with evidence, missing architectural intent, and future design risk.
   Zero candidates is a valid result. You accept, mark as debt, reject, or
   skip each one. The state is in `docs/adr/.distill-state.json`. Thus later runs do not
   ask again, and you can distill new code incrementally.
3. Run `/bipbop-skills:adr-new` only when the [eligibility filter](SKILL.md#when-an-adr-is-warranted)
   finds important, lasting architectural intent that authoritative
   sources do not record. Implementation changes alone do not qualify. Keep their rules in
   code, tests, or configuration.
4. Run `/bipbop-skills:adr-review` before you merge. It shows which accepted decisions a diff
   touches, which changes need an ADR, and which known-debt items the diff fixes.

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
[skills/adr/templates/adr-template.md](templates/adr-template.md).

Rules:

- Keep a small, concise set of current constraints.
- Confirm substantive changes. Rewrite the affected ADRs in place. Consolidate overlap.
  Delete obsolete or rejected documents.
- Renumber as necessary to keep consecutive IDs. Repair
  all references in the same change.
- Git keeps the history. Do not add `History` sections,
  supersession metadata, archive copies, or replacement records.
- A `@decision ADR-NNNN` comment in code means: read that ADR before you touch the
  spot.
- `known-debt.md` lists things that look deliberate but are not. Agents
  can fix those.

## Validation script

```bash
python3 "$CLAUDE_PLUGIN_ROOT/skills/adr/scripts/validate-adrs.py" [--root .] [--adr-dir docs/adr] [--policy-dir docs/policies] [--procedure-dir docs/procedures] [--adrs-only] [--strict] [--fail-on-proposed] [--json] [--no-code-scan]
python3 "$CLAUDE_PLUGIN_ROOT/skills/adr/scripts/validate-adrs.py" --print-setup   # pre-commit and CI snippets
```

Checks for ADRs:

- required frontmatter and permitted statuses;
- unique consecutive IDs that match the filenames;
- an index in sync with the folder;
- no obsolete statuses and no supersession metadata;
- referenced paths that still exist (warning);
- `@decision` tags that point to existing ADRs.

With `--fail-on-proposed`, an ADR or policy that is still `proposed` is an error.

Checks for `docs/policies/` and `docs/procedures/` (when they exist):

- kebab-case file names with no number;
- no ADR in the wrong folder;
- required frontmatter for each kind;
- numbered steps in a procedure;
- an index in sync;
- `ADR-NNNN` mentions and relative links that resolve;
- stale `paths` (warning);
- an expired review (warning): `last_reviewed` + `review_in` for a policy, `last_verified` +
  `review_in` (default 6 months) for a procedure.

`--adrs-only` skips both
folders. Exit codes: `0` clean, `1` errors (or
warnings with `--strict`), `2` no ADR folder or bad usage.

The script does not judge if code obeys a decision. `/bipbop-skills:adr-review` and the per-decision checks from
[skills/adr/references/enforcement-by-stack.md](references/enforcement-by-stack.md) do that.

For CI, copy the script into the repository (`/bipbop-skills:adr-init` offers to do this). Then the
job does not depend on a plugin cache path. Run it with
`--strict --fail-on-proposed`, so that a draft with no decision does not merge. Remove rejected drafts.
Keep `--fail-on-proposed` out of pre-commit hooks: a local draft of a
`proposed` ADR is normal.

## Migrating existing collections

This lifecycle changes the earlier behavior of these skills. Adoption does not automatically
rewrite a repository. For an authorized migration, do these steps:

1. Rewrite the current decisions.
2. Remove obsolete and rejected records.
3. Remove `History` and supersession fields.
4. Renumber as necessary, and repair IDs, filenames, the index, and all references.

The validator reports legacy terminal statuses and supersession metadata as errors.

## Design notes

[RESEARCH.md](RESEARCH.md) covers the format choice, existing tooling, prior
Claude Code art, the enforcement table, and the evidence. It also says what is
not proven.
