---
name: new
description: Record a new Architecture Decision Record from the current conversation or diff, with context, options, decision, and consequences confirmed by the user, including updating or consolidating related ADRs. Use when the user runs /adr:new, says "write an ADR for this", or asks to record a lasting architectural constraint. Apply the standing eligibility filter before drafting.
disable-model-invocation: true
argument-hint: "[title or decision summary]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(python3 *), Write, Edit, AskUserQuestion
---

# /adr:new

Record one qualifying concern concisely, preferring an existing ADR with the
same scope over a new file. The user confirms the decision and the why;
you draft everything else from evidence. Standing rules: `../adr/SKILL.md`.

Arguments: `$ARGUMENTS`. Optional title. Legacy `--supersedes` requests are handled
as proposals to rewrite or consolidate the affected ADRs, never as a
replacement chain.

## Procedure

0. **Check eligibility.** Apply "When an ADR is warranted" in
   `../adr/SKILL.md` before creating files. If it does not qualify, explain
   briefly and stop. Invoking this command does not establish eligibility.

1. **Locate the ADR folder and conventions.** Read the index. If there is no
   ADR folder, say so and offer `/adr:init`; stop. Note the numbering and
   whether statuses live in frontmatter or inline. Next number = highest
   existing + 1.
2. **Find its home.** Read related ADRs by title, tags, and `paths`. Apply
   "Keep the collection compact and current" in `../adr/SKILL.md`: update or
   consolidate existing records first; create only for a separate concern.
   If fully covered already, link and stop.
3. **Draft from evidence, not memory.** Sources, in order: the conversation
   so far, `git diff` / `git diff --staged`, the files touched. Fill:
   - Context: the forcing situation, with `file:line` or commit evidence.
   - Decision: the qualifying design constraint and its scope. Link to code,
     tests, or configuration for implementation details; do not copy them.
   - Options considered: the chosen one plus alternatives that were actually
     discussed. Label any new alternatives as proposals, not past decisions.
   - Consequences: good, bad, watch.
   - `paths`: the globs the decision governs. Tight, not the whole repo.
   - `tags`: two to four.
4. **Confirm missing intent before writing.** Show the draft and ask only
   about decisions, rationale, or status not already confirmed in the session.
   Do not infer a reason to fill the template. If the qualifying decision is
   confirmed but its reason is unavailable, use `Rationale status: unknown`.
5. **Write the confirmed current text.** Update existing ADRs in place or
   create `NNNN-slug.md` only if step 2 justified a new file. Use the repository
   template or `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/adr-template.md`,
   without obsolete lifecycle metadata or `History` sections. For a new file,
   use the next ID chosen in step 1.
   `date` is the current decision date; `deciders` is the known handle or empty.
6. **Consolidate and remove obsolete content.** Remove redundant or inapplicable
   ADRs included in the confirmed change. Renumber remaining records as needed
   to keep consecutive IDs. Plan one mapping from original identities to final
   IDs before renaming; apply it without cascading replacements or overwriting
   files when a retired ID is reused. Update filenames, frontmatter IDs, titles,
   saved distillation-state IDs, and `@decision` references throughout the
   repository; remove references when no applicable constraint remains.
7. **Update the index** to list only the remaining documents and their current
   titles, scope, date, status, and consecutive IDs.
8. **Offer `@decision` tags.** List one to three code locations where an agent
   is most likely to break the decision (the entry point of the governed
   `paths`, a config block, a boundary file). Ask before adding
   `@decision ADR-NNNN: <one line>` as a comment in the file's comment syntax.
   Do not add tags without a yes.
9. **Validate.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py"`; fix structural
   errors it reports. Then report: files updated, created or removed, status,
   references repaired, tags added, and whether the decision is enforceable per
   `../adr/references/enforcement-by-stack.md` (one sentence, no code unless
   asked).

## Pitfalls

- Several decisions in one conversation: group related constraints by scope,
  update their existing homes, and keep unrelated concerns separate.
- The user describes an intention, not a made decision: write it as
  `proposed`, not `accepted`.
- Changes to an accepted decision require the user's confirmation and a
  rewrite of all affected current records, following the standing lifecycle.
