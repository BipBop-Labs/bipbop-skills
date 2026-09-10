---
name: commit
description: Create atomic, well-written commits as an agent - read the real diff, stage explicitly, split when the tree mixes topics, follow the repository's message conventions and respect its hooks. Use when asked to commit, "make a commit", or when given a message to use as a guide.
---

# Commit

How an agent creates commits another person can read, review and revert without surprises.

## When to use

- The person asks to commit the current changes.
- The person gives a message or context to base the commit on.
- Not for pushing, opening PRs, rebasing, amending published commits or rewriting history.

## Preconditions

- The person asked for a commit. An agent does not commit on its own initiative.
- The branch is not the main one. If `git branch --show-current` returns `main` or `master`, create a branch first.

## Procedure

1. **Read the real state, not the session's memory**
   - `git status` for modified, staged and untracked files.
   - `git diff` and `git diff --staged` for the actual content, not just filenames.
   - `git log --oneline -10` to copy the repository's format, language and conventions.
2. **Decide the scope, and split when needed**
   - One commit per logical unit: what gets reverted together belongs together.
   - Split when the tree mixes topics: a refactor and a feature, bulk formatting and logic, unrelated backend and frontend work, a new dependency and its usage.
   - Do not split what cannot build or pass tests on its own. When two changes are genuinely coupled, leave them in one commit.
   - To split, repeat stage → commit per topic, in dependency order: what the rest needs first (renames, helpers, migrations), then what uses it.
   - If one file mixes two topics and there is no interactive terminal (`git add -p` needs one), save one topic's hunks to a patch with `git diff` and apply it with `git apply --cached`. If that is not workable, commit the whole file and say so in the response.
   - Leave out what belongs in no commit: experiments, debug prints, scratch files, local configuration.
3. **Stage explicitly**
   - `git add <path>` file by file or by narrow directory.
   - Avoid `git add -A`, `git add .` and `git commit -a`: they drag in files nobody reviewed.
   - Re-read `git diff --staged` before committing. It is the only thing that lands in history.
4. **Write the message**
   - Use the repository's format. For conventional commits: `type(scope): description`, with types `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `chore`.
   - First line under 72 characters, imperative mood, in the language the repository already uses.
   - The body explains why and any non-obvious decision. The what is already in the diff.
   - Bullets only when there are several significant changes.
   - No agent attribution or co-authorship unless the repository or the person asks for it.
5. **Commit**
   - `git commit` with the generated message.

## Pitfalls

- **Hooks.** If a hook fails, no commit was created. Fix the cause, re-stage whatever the hook rewrote and commit again. Never `--no-verify`.
- **Secrets and noise.** Do not commit `.env`, credentials, tokens, dumps, build artifacts, logs or the agent's temporary files. When unsure, check whether the file belongs in `.gitignore`.
- **Destructive commands.** Do not run `git reset --hard`, `git checkout .`, `git clean -fd` or `git stash drop` to "tidy up" before committing: they delete work that is not yours.
- **Published history.** No `--amend` and no force push on commits already on the remote, unless explicitly instructed.
- **Inflated messages.** Do not describe intent, impact or motivation the diff does not support.
- **Honest reporting.** Say in the response what was left uncommitted, which test fails, and which files a hook changed.

## Verification

- `git log -1 --stat` shows the commit with the expected message and only the intended files.
- `git status` leaves behind nothing that was meant to be included.
