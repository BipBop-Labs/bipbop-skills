---
name: adr
description: Rules to read existing ADRs, policies, and procedures, and to decide which kind of doc a rule needs, if any. Use when you work under an existing ADR, policy, or procedure, when you evaluate an important lasting design constraint or team rule, or when you discuss ADRs. A dependency, schema, interface, or implementation change alone does not need a new doc.
user-invocable: false
---

# ADR rules

Architecture Decision Records (ADRs) make deliberate choices visible, so that agents do not
undo them. Policies and procedures hold the other rules that a team writes down.
This skill holds the standing knowledge. The commands are:
`/bipbop-skills:adr-init` (set up), `/bipbop-skills:adr-distill` (recover rules from existing code),
`/bipbop-skills:adr-new` (record a rule), `/bipbop-skills:adr-review` (check a diff against rules).

## Three kinds of rule doc

| Kind | Folder | Holds | Metadata |
| --- | --- | --- | --- |
| ADR | `docs/adr/` | How the system is built, chosen from real options with a tradeoff | `id`, `title`, `status`, `date`, `deciders`, `tags`, `paths` |
| Policy | `docs/policies/` | A rule or definition that people and agents must obey, whatever the code structure | `title`, `status`, `owner`, `paths`, `last_reviewed`, `review_in` |
| Procedure | `docs/procedures/` | Numbered steps to finish one task | `title`, `owner`, `paths`, `trigger`, `last_verified` |

Routing test. Apply the steps in order. Stop at the first match:

1. Can code, a lint, a test, or config state the rule fully? Put the rule there.
   A doc gets one line with a link, or nothing.
2. Does the rule fix how the system is built (structure, boundaries, data ownership,
   dependencies, interfaces), with real options and a tradeoff? ADR.
3. Is it a numbered sequence that a person or agent runs to finish one task?
   Procedure.
4. Is it a rule or definition to obey? Policy.
5. Does it mix kinds? Split it. Each part goes to its kind and links to the
   other parts.

A rule with no tradeoff is a policy, not an ADR. Coding rules such as "no
magic numbers" are policies, or lint config with no doc. Definitions, such as
product metrics, are policies. If a machine-readable source holds the
definition (a SQL view, a metric catalog), the policy links to that source.

**One rule, one doc. Link, do not restate.** A rule lives in one place. Other
docs, ADRs, and agent instruction files link to it. Agent instruction files
(`CLAUDE.md`, `AGENTS.md`) keep one line per rule that names its source.

The file name of a policy is its ID (`docs/policies/product-metrics.md`): kebab-case,
no number, so you never renumber. The same applies to procedures. The body of a procedure
has prerequisites, numbered steps, a verify step, and a rollback step. When a
script replaces a procedure, delete the procedure.

## Folder and format

Use these defaults when the repository has no ADRs yet:

- `docs/adr/NNNN-slug.md`, four-digit sequential numbers that start at `0001`.
- `docs/adr/README.md` is the index. Regenerate it between
  `<!-- ADR-INDEX:START -->` and `<!-- ADR-INDEX:END -->`.
- `docs/adr/known-debt.md` is the known-debt log.
- Template: [templates/adr-template.md](templates/adr-template.md). Short,
  YAML frontmatter, one paragraph per section. Fields: `id`, `title`, `status`,
  `date`, `deciders`, `tags`, `paths`.
- `paths` lists the globs that the decision governs. `/bipbop-skills:adr-review` and the validator use
  them. Keep the list tight.
- Policy and procedure templates: [templates/policy-template.md](templates/policy-template.md)
  and [templates/procedure-template.md](templates/procedure-template.md). Each
  folder has a `README.md` index between `<!-- POLICY-INDEX:START -->` or
  `<!-- PROCEDURE-INDEX:START -->` and the matching `END` marker.
- Pointer for agents: [templates/agents-snippet.md](templates/agents-snippet.md).
  `/bipbop-skills:adr-init` adds it to `CLAUDE.md` or `AGENTS.md`.

**Adopt, do not convert.** The repository can already have ADRs. Look in
`docs/adr`, `doc/adr`, `docs/decisions`, `docs/architecture/decisions`, `adr/`,
and any folder that the README links. If you find ADRs, keep their folder, numbering, and format.
Find the status convention (frontmatter `status:` or an inline
`**Status:**` line) and follow it. Add `paths` to the frontmatter only when the existing format
uses frontmatter. Otherwise, record `paths` as a bullet list under the status.
Adoption does not permit bulk rewrites or deletion of existing documents.
Report legacy lifecycle conflicts, and propose a scoped consolidation before you change them.
The same applies to policies and procedures. If the repository keeps them in its own folders, or
keeps its own `## History` convention, follow the repository.

## When an ADR is warranted

Use ADRs for important, lasting design decisions that guide future development.
The decision must be one that code, tests, configuration, or existing
documentation cannot reliably show. The record must add essential intent, scope, or a design tradeoff.
If that information is lost, maintainers could undo the intended architecture.

Before you propose an ADR, explain which information is missing and which future
design choice needs it. If the answer only describes how the implementation
works, no ADR is warranted. Importance, complexity, or difficulty of reversal
alone is not sufficient. Do not invent intent from repeated code. Do not invent a
rationale to make a candidate qualify.

Keep one source of truth: link to the implementation and the enforcement. Do not
copy their rules. A rule that is already explicit in a different place warrants an ADR only
when essential architectural context is missing. Use the routing test to send policies and procedures
to their own folders.

The three contrasts below show the level of decision. They are not automatic triggers:

| Potential ADR, if essential context is missing | Keep in code, tests, or configuration |
| --- | --- |
| A shared design convention: how to divide responsibilities, its scope, and why future features must follow it | The classes, functions, and call sequence that implement that convention |
| A system boundary: which component owns a capability and which tradeoff justifies that boundary | The current module layout, dependencies, and interface definitions |
| A lasting architectural guarantee: what must stay true when implementations change, and which costs or limits the team accepts | The algorithm, checks, parameters, and deployment steps that give the guarantee now |

"No ADR warranted" is a successful result. Keep implementation explanations
in their existing sources. Use a local code comment when it is sufficient. Do not
create replacement Markdown for a rejected ADR. If the intent is not clear, ask.

## Keep the collection compact and current

Keep a small number of concise ADRs. Each one describes only a decision that applies now.
First, update or consolidate related records. Add a new record only for a qualifying concern
that does not fit coherently in an existing record. Do not merge unrelated
concerns only to reduce the count.

Rewrite all affected records together. Remove obsolete rules. Delete records
that no longer apply or whose proposals were rejected. Do not supersede records.
Do not keep archives, tombstones, or `History` sections: Git keeps the history.
Keep the rationale that a reader needs to understand the current decision.

When you delete or consolidate records, renumber as necessary. Update filenames,
IDs, titles, index entries, code tags, saved distillation-state IDs, and other
repository references together. Remove references that have no current replacement.

## Status and confirmation

- `proposed`: waits for human confirmation. Not binding.
- `accepted`: the current confirmed decision. Binding until someone changes it explicitly.

Get confirmation for substantive changes, including consolidation or deletion, before you write.
A change to this skill, or the adoption of an existing collection, does not permit bulk
rewrites. It does not permit silent changes to accepted decisions.

## How agents read ADRs

1. Read `docs/adr/README.md` (the index) first. Read the policy and procedure
   indexes when they exist.
2. Open only the ADRs, policies, and procedures whose `paths`, tags, or title match
   the code that you will change. Three is typical. Never load all of them.
3. A `@decision ADR-NNNN` comment in code means: stop, and read that ADR before you
   edit that spot. The comment form does not depend on the language:
   `# @decision ADR-0007: queue writes go through the outbox`.
4. If your change conflicts with an accepted ADR, tell the user before you
   continue. Offer to edit the ADR. Do not silently obey it and do not
   silently ignore it.
5. An ADR whose `paths` no longer exist is a sign that it is stale. Mention it. Do
   not delete the ADR.

## Known-debt log

`docs/adr/known-debt.md` lists things that look deliberate but are not:
accidents, rushed workarounds, copied code. Template:
[templates/known-debt.md](templates/known-debt.md). Agents can fix those items
without an ADR. When you fix one, remove its entry in the same change.

## Rationale honesty

Never write a reason that the user did not confirm. Code and history show behavior.
They do not establish a binding architectural intention. Confirm the intended
constraint with the user before you record it. A confirmed qualifying constraint
can have `Rationale status: unknown`. Do not put speculative reasons in the record.
An unknown rationale alone does not justify an ADR.

## Enforcement

Some decisions can become checks. Read
[references/enforcement-by-stack.md](references/enforcement-by-stack.md) when you
decide if an ADR is enforceable (dependency rule, banned alternative,
pattern rule, config rule) or advisory. Suggest a check. Add it only with
approval.

## Validation

`${CLAUDE_PLUGIN_ROOT}/skills/adr/scripts/validate-adrs.py` checks structure only:
frontmatter, consecutive unique IDs, index sync, obsolete lifecycle metadata, stale paths,
and `@decision` tags. When `docs/policies/` or `docs/procedures/` exist, it
also checks their frontmatter, file names, index sync, links, numbered steps
in procedures, and expired `review_in` or `last_verified` dates (warning).
`--adrs-only` skips them. With `--fail-on-proposed` (for CI), an ADR that is still
`proposed` is an error. Exit codes: 0 clean, 1 errors, 2 no ADR folder. The validator never judges
if code obeys a decision. `/bipbop-skills:adr-review` and per-decision
checks do that.

## Pitfalls

- An ADR for a rule with no tradeoff. Route it as a policy.
- The same rule in an ADR, a policy, and `CLAUDE.md`. Keep one source. Link
  to it from the other files.
- ADRs for everything. Over-documentation is the top complaint in
  practice. Apply the eligibility filter before you write a draft.
- A replacement ADR or an edit history added in place of an update to the
  current rule. Rewrite the affected records. Git keeps the old text.
- The whole folder loaded into context. Use the index and `paths`.
- Invented history. If the repository has no information, say "unknown".
