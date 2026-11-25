---
name: adr
description: Rules for reading existing ADRs, policies, and procedures, and for deciding which kind of doc, if any, a rule needs. Use when working under an existing ADR, policy, or procedure, evaluating an important lasting design constraint or team rule, or discussing ADRs. A dependency, schema, interface, or implementation change alone does not warrant a new doc.
user-invocable: false
---

# ADR rules

Architecture Decision Records make deliberate choices visible so agents do not
undo them. Policies and procedures hold the other rules a team writes down.
This skill holds the standing knowledge. The commands are:
`/adr:init` (set up), `/adr:distill` (recover rules from existing code),
`/adr:new` (record a rule), `/adr:review` (check a diff against rules).

## Three kinds of rule doc

| Kind | Folder | Holds | Metadata |
| --- | --- | --- | --- |
| ADR | `docs/adr/` | How the system is built, chosen from real options with a tradeoff | `id`, `title`, `status`, `date`, `deciders`, `tags`, `paths` |
| Policy | `docs/policies/` | A rule or definition people and agents must follow, whatever the code structure | `title`, `status`, `owner`, `paths`, `last_reviewed`, `review_in` |
| Procedure | `docs/procedures/` | Numbered steps to finish one task | `title`, `owner`, `paths`, `trigger`, `last_verified` |

Routing test. Apply the steps in order and stop at the first match:

1. Can code, a lint, a test, or config state the rule fully? Put it there.
   A doc gets one line with a link, or nothing.
2. Does it fix how the system is built (structure, boundaries, data ownership,
   dependencies, interfaces), with real options and a tradeoff? ADR.
3. Is it a numbered sequence that a person or agent runs to finish one task?
   Procedure.
4. Is it a rule or definition to follow? Policy.
5. Does it mix kinds? Split it. Each part goes to its kind and links to the
   others.

A rule with no tradeoff is a policy, not an ADR. Coding rules such as "no
magic numbers" are policies, or lint config with no doc. Definitions, such as
product metrics, are policies; if a machine-readable source holds the
definition (a SQL view, a metric catalog), the policy links to it.

**One rule, one doc; link, do not restate.** A rule lives in one place. Other
docs, ADRs, and agent instruction files link to it. Agent instruction files
(`CLAUDE.md`, `AGENTS.md`) keep one line per rule that names its source.

A policy file name is its ID (`docs/policies/product-metrics.md`): kebab-case,
no number, so there is no renumbering. Same for procedures. A procedure body
has prerequisites, numbered steps, a verify step, and a rollback step. When a
script replaces a procedure, delete the procedure.

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
- Policy and procedure templates: [templates/policy-template.md](templates/policy-template.md)
  and [templates/procedure-template.md](templates/procedure-template.md). Each
  folder has a `README.md` index between `<!-- POLICY-INDEX:START -->` or
  `<!-- PROCEDURE-INDEX:START -->` and the matching `END` marker.
- Pointer for agents: [templates/agents-snippet.md](templates/agents-snippet.md),
  added to `CLAUDE.md` or `AGENTS.md` by `/adr:init`.

**Adopt, do not convert.** If the repository already has ADRs (look in
`docs/adr`, `doc/adr`, `docs/decisions`, `docs/architecture/decisions`, `adr/`,
or anything linked from the README), keep their folder, numbering, and format.
Detect the status convention (frontmatter `status:` versus an inline
`**Status:**` line) and follow it. Only add `paths` when the existing format is
frontmatter-based; otherwise record it as a bullet list under the status.
Adoption does not authorize bulk rewrites or deletion of existing documents. Report legacy lifecycle conflicts
and propose a scoped consolidation before changing them. The same applies to
policies and procedures: if the repository keeps them in its own folders, or
keeps its own `## History` convention, follow the repository.

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
when essential architectural context is missing. Send policies and procedures
to their own folders with the routing test.

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

1. Read `docs/adr/README.md` (the index) first. Read the policy and procedure
   indexes when they exist.
2. Open only ADRs, policies, and procedures whose `paths`, tags, or title match
   the code you are about to change. Three is typical. Never load all of them.
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
and `@decision` tags. When `docs/policies/` or `docs/procedures/` exist, it
also checks their frontmatter, file names, index sync, links, numbered steps
in procedures, and expired `review_in` or `last_verified` dates (warning).
`--adrs-only` skips them. With `--fail-on-proposed` (meant for CI) an ADR still
`proposed` is an error. Exit 0 clean, 1 errors, 2 no ADR folder. It never judges
whether code complies with a decision; that is `/adr:review` and per-decision
checks.

## Pitfalls

- An ADR for a rule with no tradeoff. Route it as a policy.
- The same rule in an ADR, a policy, and `CLAUDE.md`. Keep one source; link
  from the others.
- Writing ADRs for everything. Over-documentation is the top complaint in
  practice; apply the eligibility filter before drafting.
- Appending a replacement ADR or an edit history instead of updating the
  current rule. Rewrite the affected records; Git preserves the old text.
- Loading the whole folder into context. Use the index and `paths`.
- Inventing history. If the repository is silent, say "unknown".
