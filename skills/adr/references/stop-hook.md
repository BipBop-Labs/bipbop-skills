# Optional Stop hook

The `adr` skills add **no active hook**. The plugin `hooks/hooks.json` does not
load this hook, so the plugin install does not run it in your sessions.

## What the hook does

`../scripts/stop-suggest.py` is an adrchive-style Stop hook that only gives a
suggestion. It never writes an ADR and never blocks. It reads only the part of
the transcript that it did not examine before. It prints a one-line system message
in two cases:

- the session edited a dependency manifest, lockfile, migration, schema,
  CI file, or Dockerfile;
- assistant text contains decision language
  ("switched to", "instead of", "we decided", "migrate to").

It stays quiet when
the session already wrote into an ADR folder. The message tells the agent to
check the applicable ADRs and to apply the standing eligibility filter before it suggests
a new ADR. These heuristics cannot show if a new ADR qualifies.

Why the hook is off by default:

- Claude Code loads every hook in `hooks/hooks.json`
  when the plugin is enabled. There is no opt-out per hook.
- Keyword heuristics fire on ordinary refactors often enough to annoy.
- The adrchive dogfood run produced six drafts in one day with an LLM classifier. A
  keyword classifier would be noisier.

The most this hook should do is a suggestion that the user can ignore. Even that
is a choice for each repository.

To enable the hook in one repository:

1. Copy the script: `cp "<plugin-root>/skills/adr/scripts/stop-suggest.py" scripts/adr-stop-suggest.py`
   (any path works; the hook config below uses this one).
2. Merge `../assets/stop-suggest.example.json` into `.claude/settings.json` (or
   `.claude/settings.local.json` to keep it personal).
3. Start a new session. Run `/hooks` to make sure that the hook is in the list.

The hook stores the byte offset of each session under `$CLAUDE_PLUGIN_DATA` when it is set,
else `$TMPDIR`, else `/tmp`, in `adr-stop-suggest/<session>.offset`.
