# Hooks

This plugin ships **no active hooks**. `hooks/hooks.json` does not exist on
purpose, so installing the plugin changes nothing about your sessions.

## Optional: Stop hook that suggests `/adr:new`

`scripts/stop-suggest.py` is an adrchive-style Stop hook reduced to a
suggestion. It never writes an ADR and never blocks. It reads only the part of
the transcript it has not inspected yet, and prints a one-line system message
when the session edited a dependency manifest, lockfile, migration, schema,
CI file, or Dockerfile, or when assistant text contains decision language
("switched to", "instead of", "we decided", "migrate to"). It stays quiet when
the session already wrote into an ADR folder.

Why it is off by default: Claude Code loads every hook in `hooks/hooks.json`
whenever the plugin is enabled, with no per-hook opt-out, and keyword
heuristics fire on ordinary refactors often enough to annoy. adrchive's own
dogfooding produced six drafts in one day with an LLM classifier; a
keyword one would be noisier. A suggestion the user can ignore is the most this
hook should do, and even that is a per-repository choice.

To enable it in one repository:

1. Copy the script: `cp "<plugin-root>/scripts/stop-suggest.py" scripts/adr-stop-suggest.py`
   (any path works; the hook config below assumes this one).
2. Merge `hooks/stop-suggest.example.json` into `.claude/settings.json` (or
   `.claude/settings.local.json` to keep it personal).
3. Start a new session. Run `/hooks` to confirm it is listed.

The per-session byte offset is stored under `$CLAUDE_PLUGIN_DATA` when set,
else `$TMPDIR`, else `/tmp`, in `adr-stop-suggest/<session>.offset`.
