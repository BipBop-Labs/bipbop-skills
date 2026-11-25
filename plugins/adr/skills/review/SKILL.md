---
name: review
description: Check the current diff or branch against accepted Architecture Decision Records, policies, and procedures, and flag likely violations, changes that need a new or changed doc, and touches to known debt. Report only, never block or fix. Use when the user runs /adr:review or asks whether a change respects the ADRs, policies, or design decisions.
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
   - the same `paths` match against the policy and procedure indexes, when
     those folders exist.
   Open only those. List them with the reason each was selected.
3. **Check for violations.** For each relevant accepted ADR, compare its
   Decision paragraph to what the diff does. Report a finding only when the
   diff plausibly contradicts the Decision; cite the ADR, the file and hunk,
   and quote the sentence of the Decision at stake. Rate confidence
   high / medium / low. Legacy superseded, deprecated, or rejected documents are not binding.
   Report them as collection-maintenance issues; do not treat them as current
   constraints or silently delete them.
3b. **Check policies and procedures.** For each relevant accepted policy,
   report a diff that plausibly breaks its Rule section, in the same form as
   step 3. For each relevant procedure, report a diff that makes a step,
   the verify step, or the rollback step wrong, and suggest an update to the
   procedure in the same change. If the diff adds or edits a rule doc, check
   that its kind is right (routing test in `../adr/SKILL.md`) and that it does
   not restate a rule that another doc holds.
4. **Check unrecorded design intent.** Apply "When an ADR is warranted" and
   "Keep the collection compact and current" in `../adr/SKILL.md`. Cite the
   evidence and essential missing context for each candidate; suggest updating
   related ADRs first. A technical change alone is not a finding. Report
   uncertain intent or unavailable evidence as such, not as a missing ADR.
   Also flag contradictory records and references left behind by consolidation.
5. **Check known debt.** For each changed file, grep `known-debt.md` for its
   path or the item's keywords. If the diff touches a listed item, say that
   changing it is allowed, and if the diff appears to fix it, suggest removing
   the entry.
6. **Validator.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate-adrs.py" --no-code-scan`
   only if the diff touches the ADR, policy, or procedure folder; include its errors.
7. **Report** in this shape and nothing else:

```text
ADR review of <range> (<n> files)

Relevant docs: ADR-0003 (paths), ADR-0007 (@decision tag in src/x.py),
policies/product-metrics.md (paths)

Likely violations
- [high] ADR-0003: src/net/client.py adds `import requests`; Decision says
  "all outbound HTTP goes through httpx". Edit the ADR or revert.

Likely policy or procedure breaks
- [medium] policies/product-metrics.md: src/metrics/active.py counts daily
  users; Rule says "active means one session in the last 7 days".

Qualifying ADR candidates
- <evidence of the intended constraint, missing architectural context, and
  affected existing ADRs or a justified new record; omit when none qualify>

Known debt touched
- src/legacy/parser.py is listed; change allowed. Looks fixed: remove entry.

Nothing else found.
```

Omit empty sections. Never edit files or add `@decision` tags from this
skill. Report validator failures without turning this review into a merge gate.

## Pitfalls

- Reading every ADR. Use `paths`, tags, and topic matching.
- Reporting style disagreements as violations. Only the Decision text counts.
- Guessing an ADR's intent beyond its text; if ambiguous, say "ambiguous" and
  rate low.
