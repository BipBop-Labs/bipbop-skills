---
name: init
description: Set up Architecture Decision Records in the current repository (folder, template, index, known-debt log, CLAUDE.md or AGENTS.md pointer, optional validation hook), and optionally policy and procedure folders. Use when the user runs /adr:init or asks to add, bootstrap, or wire up ADRs, policies, or procedures. A second run changes nothing, and the skill adopts existing folders.
disable-model-invocation: true
argument-hint: "[--dir docs/adr] [--no-snippet] [--no-rule-docs]"
allowed-tools: Read, Glob, Grep, Bash(ls *), Bash(git *), Bash(python3 *), Bash(mkdir *), Bash(cp *), Write, Edit, AskUserQuestion
---

# /adr:init

Create or adopt the ADR setup. A second run must change nothing.
Standing rules: the `adr` skill in this plugin (`../adr/SKILL.md`).

Arguments: `$ARGUMENTS`. `--dir <path>` overrides the folder. `--no-snippet`
skips the CLAUDE.md/AGENTS.md edit. `--no-rule-docs` skips step 3b.

## Procedure

1. **Find existing ADRs.** Look for `docs/adr`, `doc/adr`, `docs/adrs`,
   `docs/decisions`, `docs/architecture/decisions`, `adr`, `adrs`, and any
   folder that the README links as ADRs or decisions. If one of them has files that
   match `NNNN-*.md`, adopt it: keep its folder, numbering, and format
   (frontmatter `status:` or inline `**Status:**`). Report what you found and
   which convention you will follow. Do not rewrite existing ADRs. Report legacy
   terminal statuses, replacement chains, and mandatory history sections as
   incompatible with the current policy. Propose a separate scoped cleanup.
2. **Create only what is missing.** The target folder is the adopted folder,
   `--dir`, or `docs/adr`. Create each file only if it is absent:
   - `README.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/readme-index.md`.
     If a README exists without the `<!-- ADR-INDEX:START -->` markers, add
     the marker block at the end. Do not replace the file.
   - `template.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/adr-template.md`.
     Skip it if the repository already has its own template (any `*template*.md`
     or `0000-*.md` in the folder).
   - `known-debt.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/known-debt.md`.
   Completion: `ls` of the folder shows all three files. For each file, you said
   if it existed before or if you created it.
3. **Rebuild the index rows** between the markers from the ADR files that are present
   (ID, title, status, date, paths). If an adopted index has no markers,
   do not change it, and say so.
3b. **Policies and procedures.** Unless `--no-rule-docs`: look for the folders that
   the repository already uses for policies, standards, conventions, runbooks,
   or procedures, and adopt them. If there are none, ask if you can create
   `docs/policies/` and `docs/procedures/`. On yes, create in each folder only
   what is missing:
   - `README.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/policy-index.md`
     or `procedure-index.md` (add the marker block to an existing
     README that has no markers);
   - `template.md` from `policy-template.md` or `procedure-template.md` in
     the same templates folder.
   Do not move existing docs between kinds. List candidates for the user and
   point to the routing test in `../adr/SKILL.md`.
4. **Agent pointer.** Unless `--no-snippet`: pick `CLAUDE.md` if it exists,
   else `AGENTS.md` if it exists, else create `AGENTS.md`. If the file already
   contains `<!-- ADR:START -->`, do nothing. Otherwise, add the block from
   `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/agents-snippet.md` at the end, and replace
   `docs/adr/` with the real folder. Remove the policies and procedures
   paragraph when step 3b created neither folder. Use the real folder
   names when step 3b adopted different folders. If the file holds an older ADR block, offer
   to replace it with the new block. If the file restates rules that a policy
   holds, offer to replace each rule with one line that names the policy.
   Show the diff to the user.
5. **Validation.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" --adr-dir <folder>`.
   Report its output. With zero ADRs, it exits 0 with a warning. That is correct.
   It also checks `docs/policies/` and `docs/procedures/` when they exist.
6. **Offer wiring. Do not impose it.** Use AskUserQuestion if it is available. Otherwise,
   ask in plain text: copy the validator into the repository and add it as a
   pre-commit hook, a CI step, or both? Options: pre-commit framework, plain git
   hook, GitHub Actions step, none. On yes:
   - `cp "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" scripts/validate-adrs.py`
     (or the folder where the repository keeps scripts; ask if it is not clear);
   - add the snippet that
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" --print-setup` prints
     to the chosen place, in the existing config style. The CI snippets
     run `--strict --fail-on-proposed`. Thus a pull request with an ADR that is still
     `proposed` fails until a person accepts the ADR or removes the rejected draft. Keep that flag
     out of pre-commit hooks. Tell the user.
   Never write into `.git/hooks` without explicit approval.
7. **Report.** List the created files, adopted conventions, skipped steps, and the
   next command: `/adr:distill` for an existing codebase, `/adr:new` for a
   new one.

## Idempotency check

A second run of `/adr:init` must give "nothing to do" for each step. If a
step would change a file on the second run, you applied steps 2 to 4 incorrectly.
Fix the approach, not the file.

## Pitfalls

- Do not convert existing ADRs to the plugin template.
- Do not add the snippet two times. The `<!-- ADR:START -->` marker is the guard.
- Do not create `docs/adr` when ADRs already live in a different folder.
