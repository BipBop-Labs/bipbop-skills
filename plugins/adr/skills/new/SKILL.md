---
name: new
description: Record a new rule doc (an ADR, a policy, or a procedure) from the current conversation or diff, after the user confirms it. This includes updates to related docs and their consolidation. Use when the user runs /adr:new, says "write an ADR for this", "write a policy" or "document these steps", or asks to record a lasting architectural constraint or team rule. Apply the routing test and the eligibility filter before you write a draft.
disable-model-invocation: true
argument-hint: "[--kind adr|policy|procedure] [title or summary]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(python3 *), Write, Edit, AskUserQuestion, Agent
---

# /adr:new

Record one qualifying concern concisely. Prefer an existing doc with the
same scope to a new file. The user confirms the decision and the reason.
You write everything else from evidence. Standing rules: `../adr/SKILL.md`.

Arguments: `$ARGUMENTS`. Optional `--kind` and title. Treat a legacy `--supersedes` request
as a proposal to rewrite or consolidate the affected ADRs. Never treat it as a
replacement chain.

## Choose the kind

Use `--kind` if the user gives it. Otherwise, apply the routing
test in "Three kinds of rule doc" in `../adr/SKILL.md`. If the rule fits in
code, a lint, a test, or config, offer that and stop. If the kind is not
clear, ask with the three options. If the text mixes kinds, split it. Do
the steps below one time for each part.

- **Policy or procedure:** do the steps in "Policy or procedure" below.
- **ADR:** do the steps in "ADR procedure".

## ADR procedure

0. **Check eligibility.** Apply "When an ADR is warranted" in
   `../adr/SKILL.md` before you create files. If the concern does not qualify, explain
   briefly and stop. A run of this command does not establish eligibility.

1. **Find the ADR folder and conventions.** Read the index. If there is no
   ADR folder, say so, offer `/adr:init`, and stop. Note the numbering, and
   note if statuses are in frontmatter or inline. Next number = highest
   existing + 1.
2. **Find its home.** Read related ADRs by title, tags, and `paths`. Apply
   "Keep the collection compact and current" in `../adr/SKILL.md`. First, update or
   consolidate existing records. Create a new record only for a separate concern.
   If an existing record already covers the concern fully, link to it and stop.
3. **Write the draft from evidence, not memory.** Sources, in order: the conversation
   so far, `git diff` / `git diff --staged`, the files touched. Fill:
   - Context: the situation that forces the decision, with `file:line` or commit evidence.
   - Decision: the qualifying design constraint and its scope. Link to code,
     tests, or configuration for implementation details. Do not copy them.
   - Options considered: the chosen option plus the alternatives that the team actually
     discussed. Label each new alternative as a proposal, not a past decision.
   - Consequences: good, bad, watch.
   - `paths`: the globs that the decision governs. Tight, not the whole repo.
   - `tags`: two to four.
4. **Confirm missing intent before you write.** Show the draft. Ask only
   about decisions, rationale, or status that the session did not already confirm.
   Do not infer a reason to fill the template. If the user confirms the qualifying decision
   but its reason is not available, use `Rationale status: unknown`.
5. **Write the confirmed current text.** Update existing ADRs in place. Create
   `NNNN-slug.md` only if step 2 justified a new file. Use the repository
   template or `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/adr-template.md`,
   with no obsolete lifecycle metadata and no `History` sections. For a new file,
   use the next ID from step 1.
   `date` is the current decision date. `deciders` is the known handle or empty.
6. **Consolidate and remove obsolete content.** Remove the redundant or inapplicable
   ADRs that the confirmed change includes. Renumber the remaining records as necessary
   to keep consecutive IDs. Before you rename, make one mapping from the original identities to the final
   IDs. Apply it with no cascading replacements. Do not overwrite
   files when you reuse a retired ID. Update filenames, frontmatter IDs, titles,
   saved distillation-state IDs, and `@decision` references in the whole
   repository. Remove a reference when no applicable constraint remains.
7. **Update the index.** List only the remaining documents with their current
   titles, scope, date, status, and consecutive IDs.
8. **Offer `@decision` tags.** List one to three code locations where an agent
   is most likely to break the decision (the entry point of the governed
   `paths`, a config block, a boundary file). Ask before you add
   `@decision ADR-NNNN: <one line>` as a comment in the comment syntax of the file.
   Do not add tags without a yes.
9. **Validate.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py"`. Fix the structural
   errors that it reports. Then report: files updated, created, or removed, status,
   references repaired, tags added, and if the decision is enforceable according to
   `../adr/references/enforcement-by-stack.md` (one sentence, no code unless the user
   asks).
10. **Test with a fresh agent.** Ask the user first: the test costs one subagent
   run. Start a subagent with no context from this session. Give it a normal
   task in the governed `paths` that the rule must change, written as a user
   would ask for it. Do not name the doc, its kind, its ID, or the rule, so that the
   test does not lead the agent to the doc. Ask for a plan only, with no edits.
   Ask the agent to list the docs that constrain its plan.
   - **Pass:** the agent finds the doc and its plan obeys the rule.
   - **Fail:** the agent does not find the doc, breaks the rule, or follows an old
     copy in a different file. Fix the cause (`paths`, the index row, the title,
     a one-line pointer in an agent file, a restated copy) and test again, at
     most two times.
   Report the prompt that you used and the result.

## Policy or procedure

1. **Find the folder.** Use the folder that the repository uses for this kind.
   Default: `docs/policies/` or `docs/procedures/`. If the folder does not exist, offer
   `/adr:init` and stop.
2. **Find its home.** Read the folder index. If a doc already covers the rule
   or task, update that doc. Do not restate a rule that a different doc holds.
   Link to that doc.
3. **Write the draft.** Use the repository template, or
   `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/policy-template.md` or
   `procedure-template.md`. The file name is kebab-case with no number, for
   example `product-metrics.md` or `deploy-backend.md`. A procedure has
   numbered steps, a verify step, and a rollback step. Set `last_reviewed` or
   `last_verified` to today only when a person checked the content today.
4. **Confirm.** Show the draft. Ask for the owner and for each rule or step that
   the session did not confirm. A policy that the user did not accept stays
   `proposed`.
5. **Write and index.** Write the file. Add a row with a link to the folder
   index between its markers.
6. **Agent files.** If `CLAUDE.md` or `AGENTS.md` restates the rule, offer to
   replace the text with one line that names the new doc.
7. **Validate.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py"`. Fix the
   errors that it reports. Report the files that you changed.
8. **Test with a fresh agent.** Ask the user first: the test costs one subagent
   run. Start a subagent with no context from this session. Give it a normal
   task in the governed `paths` that the rule must change, written as a user
   would ask for it. Do not name the doc, its kind, its ID, or the rule, so that the
   test does not lead the agent to the doc. Ask for a plan only, with no edits.
   Ask the agent to list the docs that constrain its plan.
   - **Pass:** the agent finds the doc and its plan obeys the rule.
   - **Fail:** the agent does not find the doc, breaks the rule, or follows an old
     copy in a different file. Fix the cause (`paths`, the index row, the title,
     a one-line pointer in an agent file, a restated copy) and test again, at
     most two times.
   Report the prompt that you used and the result.

## Pitfalls

- A rule with no tradeoff in an ADR. It is a policy.
- A procedure for a fixed sequence that a script can run. Offer the script.
- Several decisions in one conversation. Group related constraints by scope,
  update their existing homes, and keep unrelated concerns separate.
- The user describes an intention, not a decision that the team made. Write it as
  `proposed`, not `accepted`.
- A change to an accepted decision needs the confirmation of the user and a
  rewrite of all affected current records, as the standing lifecycle says.
