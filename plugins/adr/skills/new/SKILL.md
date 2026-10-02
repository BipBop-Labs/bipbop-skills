---
name: new
description: Record a new Architecture Decision Record from the current conversation or diff, with context, options, decision, and consequences confirmed by the user, including superseding an older ADR. Use when the user runs /adr:new, says "write an ADR for this", or confirms a decision that matches an ADR trigger.
disable-model-invocation: true
argument-hint: "[title or decision summary] [--supersedes ADR-NNNN]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(python3 *), Write, Edit, AskUserQuestion
---

# /adr:new

Write one ADR for one decision. The user confirms the decision and the why;
you draft everything else from evidence. Standing rules: `../adr/SKILL.md`.

Arguments: `$ARGUMENTS`. Optional title and `--supersedes ADR-NNNN`.

## Procedure

1. **Locate the ADR folder and conventions.** Read the index. If there is no
   ADR folder, say so and offer `/adr:init`; stop. Note the numbering and
   whether statuses live in frontmatter or inline. Next number = highest
   existing + 1.
2. **Check for overlap.** Grep ADR titles, tags, and `paths` for the topic.
   If an accepted ADR already covers it, show it and ask: supersede, extend
   with evidence only, or abort. Do not write a duplicate.
3. **Draft from evidence, not memory.** Sources, in order: the conversation
   so far, `git diff` / `git diff --staged`, the files touched. Fill:
   - Context: the forcing situation, with `file:line` or commit evidence.
   - Decision: one paragraph, active voice, the rule agents must follow.
   - Options considered: the chosen one plus alternatives that were actually
     discussed or that an informed reviewer would raise. No strawmen.
   - Consequences: good, bad, watch.
   - `paths`: the globs the decision governs. Tight, not the whole repo.
   - `tags`: two to four.
4. **Confirm with the user before writing.** Show the draft. Facts are yours,
   decisions and reasons are theirs. Use AskUserQuestion if available:
   - "Is this the decision?" (yes / edit)
   - "Why?" with the main driver as options: performance, simplicity,
     team familiarity, ecosystem or tooling, specific feature, constraint
     inherited from elsewhere, other. Put your inferred reason first, marked
     "[inferred] … confirm?".
   - "Status now?" accepted (default when the user is the decider) or
     proposed (needs someone else's sign-off).
   If the user gives no reason, write `Rationale status: unknown` and keep
   the Options section to what the evidence shows. Never invent a reason.
5. **Write the ADR** as `NNNN-slug.md` from the repository's template (or
   `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/adr-template.md`). Slug: three to
   six lowercase words. `date` is today. `deciders` is the user's name or
   handle if known, else empty.
6. **Supersede, if applicable.** For `--supersedes` or a choice in step 2:
   - new ADR: `supersedes: [ADR-OLD]`;
   - old ADR: `status: superseded`, `superseded_by: [ADR-NEW]`. Change nothing
     else in it. In inline-status repos, edit the `**Status:**` line to
     `Superseded by ADR-NEW` and add a `Supersedes` line to the new one.
7. **Update the index** rows between the markers (or the repository's own
   index convention). Keep the old ADR listed with its new status.
8. **Offer `@decision` tags.** List one to three code locations where an agent
   is most likely to break the decision (the entry point of the governed
   `paths`, a config block, a boundary file). Ask before adding
   `@decision ADR-NNNN: <one line>` as a comment in the file's comment syntax.
   Do not add tags without a yes.
9. **Validate.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py"`; fix structural
   errors it reports. Then report: file written, status, superseded ADR if
   any, tags added, and whether the decision is enforceable per
   `../adr/references/enforcement-by-stack.md` (one sentence, no code unless
   asked).

## Pitfalls

- Several decisions in one conversation: one ADR each; ask which to write
  first.
- The user describes an intention, not a made decision: write it as
  `proposed`, not `accepted`.
- Do not touch an accepted ADR's Decision section, even to "clarify".
