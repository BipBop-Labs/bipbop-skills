---
name: review
description: Check the current diff or branch against accepted Architecture Decision Records and flag likely violations, changes that need a new ADR, and touches to known debt. Report only, never block or fix. Use when the user runs /adr:review or asks whether a change respects the ADRs or design decisions.
disable-model-invocation: true
argument-hint: "[base-ref] [--staged]"
allowed-tools: Read, Glob, Grep, Bash(git *), Bash(ls *), Bash(python3 *)
---

# /adr:review

Read-only. Compare a change set to accepted decisions and report.
Standing rules: `../adr/SKILL.md`.

Arguments: `$ARGUMENTS`. `base-ref` (default: the merge base with the default
branch, else `HEAD`) or `--staged`.

## Procedure

1. **Get the change set.**
   - `--staged`: `git diff --staged --name-only` and the diff.
   - Otherwise: `git merge-base <base> HEAD` then `git diff <merge-base>...HEAD`
     plus uncommitted changes (`git diff`). If there is no diff, say so and
     stop.
2. **Find relevant ADRs**, without loading all of them:
   - index rows whose `paths` globs match any changed file;
   - `@decision ADR-NNNN` tags inside changed files or within 30 lines of a
     changed hunk (`git diff -U30` and grep the hunk);
   - index titles and tags that share a topic with the diff (dependency names
     in manifests, module names in paths, words in commit messages).
   Open only those. List them with the reason each was selected.
3. **Check for violations.** For each relevant accepted ADR, compare its
   Decision paragraph to what the diff does. Report a finding only when the
   diff plausibly contradicts the Decision; cite the ADR, the file and hunk,
   and quote the sentence of the Decision at stake. Rate confidence
   high / medium / low. Superseded or deprecated ADRs are not violations;
   mention them only if the diff still references them in a tag.
4. **Check for missing ADRs.** Run the trigger list from `../adr/SKILL.md`
   against the diff: new or removed runtime dependency, new or moved module or
   service, schema or migration change, public interface change, cross-cutting
   convention change. For each hit without a covering ADR, report it and
   suggest `/adr:new` with a one-line proposed title.
5. **Check known debt.** For each changed file, grep `known-debt.md` for its
   path or the item's keywords. If the diff touches a listed item, say that
   changing it is allowed, and if the diff appears to fix it, suggest removing
   the entry.
6. **Validator.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" --no-code-scan`
   only if the diff touches the ADR folder; include its errors.
7. **Report** in this shape and nothing else:

```text
ADR review of <range> (<n> files)

Relevant ADRs: ADR-0003 (paths), ADR-0007 (@decision tag in src/x.py)

Likely violations
- [high] ADR-0003: src/net/client.py adds `import requests`; Decision says
  "all outbound HTTP goes through httpx". Supersede with /adr:new or revert.

Changes that need an ADR
- services/billing/ moved into packages/billing/ (trigger 2). Suggest
  /adr:new "billing is a separate package".

Known debt touched
- src/legacy/parser.py is listed; change allowed. Looks fixed: remove entry.

Nothing else found.
```

Omit empty sections. Never edit files, never fail a command, never add
`@decision` tags from this skill.

## Pitfalls

- Reading every ADR. Use `paths`, tags, and topic matching.
- Reporting style disagreements as violations. Only the Decision text counts.
- Guessing an ADR's intent beyond its text; if ambiguous, say "ambiguous" and
  rate low.
