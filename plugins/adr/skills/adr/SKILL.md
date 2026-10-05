---
name: adr
description: Standing rules for Architecture Decision Records (ADRs) in any repository, independent of language or framework. Use when about to make or change an architectural decision (new dependency, module or service boundary, data model, hard-to-reverse choice), when code contains a `@decision ADR-NNNN` comment, or when the user mentions ADRs, design decisions, or why code is the way it is.
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
  `date`, `deciders`, `tags`, `paths`, `supersedes`, `superseded_by`.
- `paths` lists globs the decision governs. `/adr:review` and the validator use
  them. Keep the list tight.
- Pointer for agents: [templates/agents-snippet.md](templates/agents-snippet.md),
  added to `CLAUDE.md` or `AGENTS.md` by `/adr:init`.

**Adopt, do not convert.** If the repository already has ADRs (look in
`docs/adr`, `doc/adr`, `docs/decisions`, `docs/architecture/decisions`, `adr/`,
or anything linked from the README), keep their folder, numbering, and format.
Detect the status convention (frontmatter `status:` versus an inline
`**Status:**` line) and follow it. Only add the frontmatter fields this plugin
needs (`paths`, `supersedes`, `superseded_by`) when the existing format is
frontmatter-based; otherwise record them as a bullet list under the status.

## Status lifecycle

```text
proposed -> accepted -> superseded | deprecated
proposed -> rejected
```

- `proposed`: drafted, not yet binding. Only a human moves it to `accepted`.
- `accepted`: binding. Never edit its Decision. To change it, write a new ADR
  with `supersedes: [ADR-NNNN]`, set the old one to `superseded` with
  `superseded_by: [ADR-MMMM]`, and update the index. Typo fixes and added
  evidence are fine; changing meaning is not.
- `deprecated`: no longer applies and nothing replaces it. Say why in the body.
- `rejected`: considered and turned down. Keep it; it stops the idea from
  being re-proposed every quarter.

## When to write an ADR

Write one when a change does any of the following. Each is checkable from the
diff:

1. Adds, removes, or swaps a runtime dependency, framework, database, queue,
   or external service.
2. Creates, merges, or moves a module, package, service, or deployable unit, or
   changes who may import whom.
3. Changes a persisted data model, schema, storage format, or migration
   strategy.
4. Changes a public interface: API contract, CLI flags, file format, event
   shape, environment variables.
5. Is hard to reverse: affects more than one team, needs a migration, or
   locks in a vendor.
6. Is a choice a reasonable reviewer would question ("why not the obvious
   option?"), including choosing *not* to do something common.
7. Sets a cross-cutting convention: error handling, logging, auth, i18n,
   concurrency model, testing strategy.

Do **not** write an ADR for:

- a bug fix, refactor, or rename that keeps behaviour and boundaries;
- formatting, lint, or dependency version bumps without API change;
- anything already covered by an accepted ADR (link to it instead);
- a decision the user has not confirmed (propose, do not record);
- a local implementation detail nobody outside the file would question.

One ADR per decision. If a change hits several triggers, it is usually still
one decision.

## How agents read ADRs

1. Read `docs/adr/README.md` (the index) first.
2. Open only ADRs whose `paths`, tags, or title match the code you are about to
   change. Three is typical. Never load all of them.
3. A `@decision ADR-NNNN` comment in code means stop and read that ADR before
   editing that spot. The comment form is language-agnostic:
   `# @decision ADR-0007: queue writes go through the outbox`.
4. If your change conflicts with an accepted ADR, say so to the user before
   proceeding. Offer `/adr:new` to supersede. Do not silently comply or
   silently ignore.
5. An ADR whose `paths` no longer exist is a staleness signal. Mention it; do
   not delete the ADR.

## Known-debt log

`docs/adr/known-debt.md` lists things that look deliberate but are not:
accidents, rushed workarounds, copied code. Template:
[templates/known-debt.md](templates/known-debt.md). Agents may fix those
without an ADR. When fixing one, remove its entry in the same change.

## Rationale honesty

Never write a reason the user did not confirm. When recovering decisions from
code or history, set `Rationale status: unknown` and label guesses as guesses
("Likely because…, not confirmed"). The Decision is still binding; the why is
not evidence.

## Enforcement

Some decisions can become checks. Read
[references/enforcement-by-stack.md](references/enforcement-by-stack.md) when
deciding whether an ADR is enforceable (dependency rule, banned alternative,
pattern rule, config rule) or advisory. Suggest a check; add it only with
approval.

## Validation

`${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py` checks structure only:
frontmatter, numbering, index sync, supersede links both ways, stale paths,
and `@decision` tags. With `--fail-on-proposed` (meant for CI) an ADR still
`proposed` is an error. Exit 0 clean, 1 errors, 2 no ADR folder. It never judges
whether code complies with a decision; that is `/adr:review` and per-decision
checks.

## Pitfalls

- Writing ADRs for everything. Over-documentation is the top complaint in
  practice; stick to the trigger list.
- Editing an accepted ADR to "update" it. Supersede instead.
- Loading the whole folder into context. Use the index and `paths`.
- Inventing history. If the repository is silent, say "unknown".
