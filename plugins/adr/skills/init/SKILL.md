---
name: init
description: Set up Architecture Decision Records in the current repository (folder, template, index, known-debt log, CLAUDE.md or AGENTS.md pointer, optional validation hook). Use when the user runs /adr:init or asks to add, bootstrap, or wire up ADRs. Idempotent and adopts existing ADR folders.
disable-model-invocation: true
argument-hint: "[--dir docs/adr] [--no-snippet]"
allowed-tools: Read, Glob, Grep, Bash(ls *), Bash(git *), Bash(python3 *), Bash(mkdir *), Bash(cp *), Write, Edit, AskUserQuestion
---

# /adr:init

Create or adopt the ADR setup. Running it twice must change nothing.
Standing rules: the `adr` skill in this plugin (`../adr/SKILL.md`).

Arguments: `$ARGUMENTS`. `--dir <path>` overrides the folder; `--no-snippet`
skips the CLAUDE.md/AGENTS.md edit.

## Procedure

1. **Detect existing ADRs.** Look for `docs/adr`, `doc/adr`, `docs/adrs`,
   `docs/decisions`, `docs/architecture/decisions`, `adr`, `adrs`, and any
   folder the README links as ADRs or decisions. If one exists with files
   matching `NNNN-*.md`, adopt it: keep its folder, numbering, and format
   (frontmatter `status:` or inline `**Status:**`). Report what you found and
   which convention you will follow. Do not rewrite existing ADRs.
2. **Create what is missing, nothing else.** Target folder is the adopted one,
   `--dir`, or `docs/adr`. For each file, create it only if absent:
   - `README.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/readme-index.md`.
     If a README exists without the `<!-- ADR-INDEX:START -->` markers, append
     the marker block at the end instead of replacing the file.
   - `template.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/adr-template.md`.
     Skip if the repository already has its own template (any `*template*.md`
     or `0000-*.md` in the folder).
   - `known-debt.md` from `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/known-debt.md`.
   Completion: `ls` of the folder shows all three, each either pre-existing
   or newly created, and you have stated which.
3. **Rebuild the index rows** between the markers from the ADR files present
   (ID, title, status, date, paths). If no markers exist in an adopted index,
   leave it alone and say so.
4. **Agent pointer.** Unless `--no-snippet`: pick `CLAUDE.md` if it exists,
   else `AGENTS.md` if it exists, else create `AGENTS.md`. If the file already
   contains `<!-- ADR:START -->`, do nothing. Otherwise append the block from
   `${CLAUDE_PLUGIN_ROOT}/skills/adr/templates/agents-snippet.md`, with
   `docs/adr/` replaced by the real folder. Show the user the diff.
5. **Validation.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" --adr-dir <folder>`.
   Report its output. With zero ADRs it exits 0 with a warning; that is fine.
6. **Offer wiring, do not impose.** Use AskUserQuestion if available, otherwise
   ask in plain text: copy the validator into the repository and add it as a
   pre-commit hook and/or CI step? Options: pre-commit framework, plain git
   hook, GitHub Actions step, none. On yes:
   - `cp "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" scripts/validate-adrs.py`
     (or the folder where the repository keeps scripts; ask if unclear);
   - add the snippet printed by
     `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" --print-setup`
     to the chosen place, following existing config style. The CI snippets
     run `--strict --fail-on-proposed`, so a pull request with an ADR still
     `proposed` fails until a person accepts or rejects it; keep that flag
     out of pre-commit hooks. Tell the user.
   Never write into `.git/hooks` without explicit approval.
7. **Report.** List created files, adopted conventions, skipped steps, and the
   next command: `/adr:distill` for an existing codebase, `/adr:new` for a
   fresh one.

## Idempotency check

Running `/adr:init` again must produce "nothing to do" for every step. If a
step would change a file on the second run, that is a bug in how you applied
step 2 to 4; fix the approach, not the file.

## Pitfalls

- Do not convert existing ADRs to the plugin template.
- Do not add the snippet twice; the `<!-- ADR:START -->` marker is the guard.
- Do not create `docs/adr` when ADRs already live elsewhere.
