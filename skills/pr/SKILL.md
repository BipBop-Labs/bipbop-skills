---
name: pr
description: Open a pull request as an agent, with sections for both reviewers and the client (technical summary, test plan, and a plain-language summary in Spanish). Use when asked to create a PR or to write its description.
---

# Pull request

How an agent opens a pull request whose description serves the code reviewer and the client alike.

## When to use

- The person asks to create a PR or to write its description.
- The current branch has commits that are not on the base branch.
- Not for reviewing someone else's PR, merging or closing PRs.

## Preconditions

- The person asked for the PR. Publishing is an outward-facing effect: never do it on your own initiative.
- `gh auth status` reports authenticated.
- No PR is open for the branch. If `gh pr view --json url` returns one, update it with `gh pr edit` instead of creating another.

## Procedure

1. **Gather context**
   - Current branch: `git branch --show-current`.
   - Real base branch: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`. Do not assume `main`.
   - Differing commits: `git log <base>..HEAD --oneline`.
   - Full changes: `git diff <base>...HEAD`.
   - Fold in any extra context the person gives.
2. **Ask when unsure.** If the purpose of the change cannot be read off the diff, ask before writing the description.
3. **Push the branch**: `git push -u origin <branch>`. No force push unless explicitly instructed.
4. **Create the PR** with `gh pr create --base <base> --title "<concise title>" --body-file <file>`. Write the body to a temporary file so quotes and backticks do not break passing through the shell. Body structure:

````markdown
**Target:** `<base-branch>`

## Summary of Changes
- <factual, technical description>

## Test Plan
- [ ] <concrete verification step>

## Resumen para el cliente
```
- <cambio en español, sin detalles técnicos>
```
````

5. **Return the PR URL.**

## Sections

- **Summary of Changes** (English): factual, no opinions. Summarize the change; do not replay the commit list. Brief and scannable.
- **Test Plan**: concrete steps covering the affected flows. Tick a box only for a step you actually ran; leave the rest unticked for the reviewer.
- **Resumen para el cliente** (Spanish): inside a code block so it can be copy-pasted. User-facing changes only, plain language, no technical detail.

## Pitfalls

- **Sensitive data.** A PR body is public on open repositories: no credentials, local paths, client names or real data.
- **Wrong base.** Verify the base branch before creating; fixing it afterwards moves the review elsewhere.
- **Inflated description.** A small PR gets short sections. Do not invent risks, migrations or tests that do not exist.
- **Unfinished work.** If something was left out of scope or a test fails, say so in the PR body, not only in the chat.

## Verification

- `gh pr view --json url,title,body` shows the PR with the three sections and the correct base.
