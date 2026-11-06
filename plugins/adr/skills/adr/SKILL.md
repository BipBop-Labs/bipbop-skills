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
frontmatter-based; otherwise
record it as a bullet list under the status. Adoption does not authorize bulk
rewrites or deletion of existing documents. Report legacy lifecycle conflicts
and propose a scoped consolidation before changing them.

## Keep the collection compact and current

Maintain a small set of concise ADRs describing the architecture that applies
now. Before adding a record, inspect related ADRs. Prefer rewriting or
consolidating the affected documents when the decision belongs to their scope.
Create a separate ADR only for an independently qualifying concern that would
make those documents less coherent if combined. Do not combine unrelated
constraints merely to reduce the file count.

Rewrite all affected ADRs together so they remain consistent. Preserve their
scope when it still applies; when consolidating, keep the best-fitting
record and remove redundant ones. Renumber remaining ADRs as needed to keep
numbering consecutive. Update frontmatter IDs, filenames, titles, the index,
`@decision` tags, saved distillation-state ADR IDs, and all other repository
references in the same change.
Remove a reference when no current constraint replaces it.

Do not supersede an ADR with another, retain obsolete or rejected ADRs, or add
`History` sections, tombstones, replacement chains, or change logs. Git provides
history. Remove obsolete rules from otherwise current records; delete a record
when no applicable decision remains. Keep current rationale and accepted
tradeoffs needed to understand today's constraint, without retelling its edits.

## Status lifecycle

- `proposed`: a draft awaiting human confirmation; not binding.
- `accepted`: the current confirmed constraint; binding until explicitly
  changed. Obtain confirmation for substantive changes and show the proposed
  current text, including any consolidation or deletion.
- If a proposal is rejected or a decision ceases to apply, remove its document
  and references. Do not preserve it under a terminal status.

Changing this skill alone does not authorize rewriting existing repositories
or change the meaning of their accepted ADRs. When an authorized change affects
an existing collection, follow the compact-current policy above.

## When to write an ADR

An ADR preserves important, lasting architectural intent that would otherwise
be lost. It must not become a second source of truth for implementation behavior.

Create an ADR only when ALL of these conditions hold:

1. It establishes a consequential design constraint that should guide future
   changes beyond the current implementation.
2. It adds essential information that cannot be reliably recovered from code,
   tests, configuration, or an existing authoritative document: intended
   boundaries, scope, rationale, or an accepted tradeoff.
3. Losing that information creates a concrete risk of future changes violating
   the intended architecture. Ordinary maintenance difficulty or a hypothetical
   need to explain the code is insufficient.

Before proposing an ADR, identify the constraint, the missing information, and
the future design mistake the record would help prevent. If these cannot be
stated specifically, do not propose one. One ADR per qualifying decision.

## Keep one source of truth

Code, tests, and configuration remain authoritative for algorithms, conditions,
thresholds, schemas, interfaces, and execution behavior. Do not reproduce those
details in an ADR. Link to their sources when needed to explain a qualifying
architectural decision.

If an architectural rule is already explicit in an automated check or another
authoritative source, an ADR must contribute essential missing intent or
context. Restating the rule does not qualify. If an accepted ADR covers the
information, link to it instead of creating a duplicate.

Do not manufacture architectural significance by reframing an implementation
detail as a principle. "We must use algorithm X" does not qualify merely
because it is written as a lasting rule.

## Examples and boundaries

These examples illustrate the filter; they are not automatic triggers.

| May warrant an ADR when the filter is satisfied | Keep in its authoritative source |
| --- | --- |
| Which domain owns a business capability, and why other applications must access it through that boundary | Module locations, imports, endpoint signatures |
| A requirement to support overlapping application versions during deployments, and its accepted constraints | Migration sequence, compatibility branches, rollback commands |
| Treating a search index as disposable derived data, including which source remains authoritative | Index schema, rebuild algorithm, scheduling |
| A deliberate isolation boundary for untrusted execution, with its accepted operational cost | Worker configuration, queue names, resource limits |
| A project-specific division of responsibility between routers and application services, including why it must persist | Individual handlers, method signatures, existing lint rules |
| A portability requirement that constrains future infrastructure choices, with its accepted limitations | Current provider, SDK version, adapter implementation |

A new library, a difficult migration, repeated code, or a familiar design
pattern is not sufficient evidence. Repetition does not establish intent.
Generic advice such as "follow SOLID" does not qualify.

Important business policies, legal requirements, and operational procedures
belong in their respective authoritative sources. Importance and longevity
alone do not make something an architectural decision.

## When no ADR is warranted

"No ADR warranted" is a valid outcome. Leave implementation details in code,
tests, or configuration. Do not create another Markdown document as a fallback
for a rejected ADR. If only a local explanation is missing, prefer a focused
code comment.

If design intent is uncertain, ask rather than inventing a constraint or
rationale to make a candidate qualify. Confirm the decision before recording it.

Apply this filter to new records. Existing accepted ADRs retain their status
until explicitly changed through their lifecycle.

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
An unknown rationale does not waive the eligibility filter.

## Enforcement

Some decisions can become checks. Read
[references/enforcement-by-stack.md](references/enforcement-by-stack.md) when
deciding whether an ADR is enforceable (dependency rule, banned alternative,
pattern rule, config rule) or advisory. Suggest a check; add it only with
approval.

## Validation

When changing this policy or its command workflows, run the synthetic scenarios
in [references/eligibility-cases.md](references/eligibility-cases.md) on a
supported host. Distinguish policy execution from automatic skill discovery.

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
