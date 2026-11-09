---
name: adr
description: Rules for reading existing ADRs and deciding whether a new ADR is warranted. Use when working under an existing ADR, evaluating an important lasting design constraint, or discussing ADRs. A dependency, schema, interface, or implementation change alone does not warrant a new ADR.
user-invocable: false
---

# ADR rules

Architecture Decision Records make deliberate choices visible so agents do not
undo them. This skill holds the standing knowledge. The commands are:
`/adr:init` (set up), `/adr:distill` (recover decisions from existing code),
`/adr:new` (record a decision), `/adr:review` (check a diff against decisions).

## Folder and format

Defaults, used when the repository has no ADRs yet:

- `docs/adr/NNNN-slug.md`, four-digit sequential numbers starting at `0001`.
- `docs/adr/README.md` is the index, regenerated between
  `<!-- ADR-INDEX:START -->` and `<!-- ADR-INDEX:END -->`.
- `docs/adr/known-debt.md` is the known-debt log.
- Template: [templates/adr-template.md](templates/adr-template.md). Short,
  YAML frontmatter, one paragraph per section. Fields: `id`, `title`, `status`,
  `date`, `deciders`, `tags`, `paths`.
- `paths` lists globs the decision governs. `/adr:review` and the validator use
  them. Keep the list tight.
- Pointer for agents: [templates/agents-snippet.md](templates/agents-snippet.md),
  added to `CLAUDE.md` or `AGENTS.md` by `/adr:init`.

**Adopt, do not convert.** If the repository already has ADRs (look in
`docs/adr`, `doc/adr`, `docs/decisions`, `docs/architecture/decisions`, `adr/`,
or anything linked from the README), keep their folder, numbering, and format.
Detect the status convention (frontmatter `status:` versus an inline
`**Status:**` line) and follow it. Only add `paths` when the existing format is
frontmatter-based; otherwise record it as a bullet list under the status.
Adoption does not authorize bulk rewrites or deletion of existing documents. Report legacy lifecycle conflicts
and propose a scoped consolidation before changing them.

## When an ADR is warranted

Use ADRs for important, lasting design decisions that guide future development
and cannot be reliably recovered from code, tests, configuration, or existing
documentation. The record must add essential intent, scope, or a design tradeoff
whose loss could lead maintainers to undo the intended architecture.

Before proposing one, explain what information is missing and which future
design choice needs it. If the answer merely describes how the implementation
works, no ADR is warranted. Importance, complexity, or difficulty of reversal
alone is insufficient. Do not invent intent from repeated code or invent a
rationale to make a candidate qualify.

Keep one source of truth: link to implementation and enforcement instead of
copying their rules. A rule already explicit elsewhere warrants an ADR only
when essential architectural context is missing. Business policies and
operating procedures belong in their own authoritative sources.

These three contrasts illustrate the level of decision, not automatic triggers:

| Potential ADR, if essential context is missing | Keep in code, tests, or configuration |
| --- | --- |
| A shared design convention: how responsibilities must be divided, its scope, and why future features must follow it | The classes, functions, and call sequence implementing that convention |
| A system boundary: which component owns a capability and what tradeoff justifies that boundary | Current module layout, dependencies, and interface definitions |
| A lasting architectural guarantee: what must hold as implementations change, and which costs or limitations are accepted | The algorithm, checks, parameters, and deployment steps that currently provide it |

"No ADR warranted" is a successful outcome. Keep implementation explanations
in their existing sources; use a local code comment when sufficient. Do not
create replacement Markdown for a rejected ADR. If intent is unclear, ask.

## Keep the collection compact and current

Keep a few concise ADRs describing only decisions that apply now. First update
or consolidate related records; add a new one only for a qualifying concern
that does not fit coherently in an existing record. Do not merge unrelated
concerns just to reduce the count.

Rewrite all affected records together. Remove obsolete rules and delete records
that no longer apply or whose proposals were rejected. Do not supersede records
or retain archives, tombstones, or `History` sections: Git preserves history.
Retain the rationale needed to understand the current decision.

When deleting or consolidating records, renumber as needed and update filenames,
IDs, titles, index entries, code tags, saved distillation-state IDs, and other
repository references together. Remove references with no current replacement.

## Status and confirmation

- `proposed`: awaiting human confirmation; not binding.
- `accepted`: the current confirmed decision; binding until explicitly changed.

Confirm substantive changes, including consolidation or deletion, before writing.
Changing this skill or adopting an existing collection does not authorize bulk
rewrites or silently change accepted decisions.

## How agents read ADRs

1. Read `docs/adr/README.md` (the index) first.
2. Open only ADRs whose `paths`, tags, or title match the code you are about to
   change. Three is typical. Never load all of them.
3. A `@decision ADR-NNNN` comment in code means stop and read that ADR before
   editing that spot. The comment form is language-agnostic:
   `# @decision ADR-0007: queue writes go through the outbox`.
4. If your change conflicts with an accepted ADR, say so to the user before
   proceeding. Offer to edit the ADR. Do not silently comply or
   silently ignore.
5. An ADR whose `paths` no longer exist is a staleness signal. Mention it; do
   not delete the ADR.

## Known-debt log

`docs/adr/known-debt.md` lists things that look deliberate but are not:
accidents, rushed workarounds, copied code. Template:
[templates/known-debt.md](templates/known-debt.md). Agents may fix those
without an ADR. When fixing one, remove its entry in the same change.

## Rationale honesty

Never write a reason the user did not confirm. Code and history show behavior;
they do not establish a binding architectural intention. Confirm the intended
constraint with the user before recording it. A confirmed qualifying constraint
may have `Rationale status: unknown`; omit speculative reasons from the record.
Unknown rationale does not by itself justify an ADR.

## Enforcement

Some decisions can become checks. Read
[references/enforcement-by-stack.md](references/enforcement-by-stack.md) when
deciding whether an ADR is enforceable (dependency rule, banned alternative,
pattern rule, config rule) or advisory. Suggest a check; add it only with
approval.

## Validation

`${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py` checks structure only:
frontmatter, consecutive unique IDs, index sync, obsolete lifecycle metadata, stale paths,
and `@decision` tags. With `--fail-on-proposed` (meant for CI) an ADR still
`proposed` is an error. Exit 0 clean, 1 errors, 2 no ADR folder. It never judges
whether code complies with a decision; that is `/adr:review` and per-decision
checks.

## Pitfalls

- Writing ADRs for everything. Over-documentation is the top complaint in
  practice; apply the eligibility filter before drafting.
- Appending a replacement ADR or an edit history instead of updating the
  current rule. Rewrite the affected records; Git preserves the old text.
- Loading the whole folder into context. Use the index and `paths`.
- Inventing history. If the repository is silent, say "unknown".
