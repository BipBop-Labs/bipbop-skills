#!/usr/bin/env python3
"""Optional Stop hook: suggest /adr:new when a session looks like it made a decision.

Suggest-only. Never writes ADRs, never blocks. No LLM, no network, stdlib only.
Opt-in: this file is NOT wired in hooks/hooks.json. See hooks/README.md.

Input: Claude Code Stop hook JSON on stdin (session_id, transcript_path, stop_hook_active).
Output: {"systemMessage": "..."} when a trigger is found in the part of the
transcript not yet inspected; nothing otherwise. Exit code is always 0.

Heuristics (deterministic, cheap):
  - a Write/Edit tool call touched a dependency manifest, lockfile, migration,
    schema, CI, or Dockerfile;
  - assistant text contains decision language (switched to, replaced X with,
    instead of, we decided, migrate to, drop ...).
Suppressed when the same segment already wrote into an ADR folder.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MANIFEST_RE = re.compile(
    r"(^|/)(package\.json|pyproject\.toml|requirements[^/]*\.txt|go\.mod|Cargo\.toml|pom\.xml|"
    r"build\.gradle(\.kts)?|[^/]+\.csproj|Gemfile|composer\.json|mix\.exs|Package\.swift|pubspec\.yaml|"
    r"Dockerfile[^/]*|docker-compose[^/]*\.ya?ml|\.github/workflows/[^/]+|migrations?/[^/]+|schema[^/]*\.(sql|prisma|graphql|json))$",
    re.IGNORECASE,
)
DECISION_RE = re.compile(
    r"\b(switch(ed|ing)? to|replac(ed|ing) \S+ with|instead of|we (decided|chose|opted)|migrat(e|ed|ing) to|"
    r"dropp?(ed|ing) (the )?\S+ (dependency|backend|library|service)|adopt(ed|ing)|new (dependency|service|module|table|schema))\b",
    re.IGNORECASE,
)
ADR_DIR_RE = re.compile(r"(^|/)(docs?/adrs?|docs/decisions|docs/architecture/decisions|adrs?)/", re.IGNORECASE)
MIN_NEW_BYTES = 2048


def state_path(session_id: str) -> Path:
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.environ.get("TMPDIR") or "/tmp"
    folder = Path(base) / "adr-stop-suggest"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{re.sub(r'[^A-Za-z0-9_-]', '_', session_id)}.offset"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("stop_hook_active"):
        return 0
    transcript = payload.get("transcript_path")
    session_id = str(payload.get("session_id") or "unknown")
    if not transcript or not os.path.isfile(transcript):
        return 0

    marker = state_path(session_id)
    try:
        offset = int(marker.read_text()) if marker.is_file() else 0
    except ValueError:
        offset = 0
    size = os.path.getsize(transcript)
    if size < offset:
        offset = 0
    if size - offset < MIN_NEW_BYTES:
        return 0

    with open(transcript, "rb") as handle:
        handle.seek(offset)
        chunk = handle.read().decode("utf-8", errors="replace")
    marker.write_text(str(size))

    touched_manifest, decision_text, wrote_adr = [], [], False
    for line in chunk.splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = record.get("message") or {}
        if record.get("type") != "assistant" or message.get("role") != "assistant":
            continue
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                found = DECISION_RE.search(block.get("text") or "")
                if found:
                    decision_text.append(found.group(0))
            elif block.get("type") == "tool_use" and block.get("name") in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
                path = str((block.get("input") or {}).get("file_path") or "")
                if ADR_DIR_RE.search(path):
                    wrote_adr = True
                elif MANIFEST_RE.search(path):
                    touched_manifest.append(path)

    if wrote_adr or not (touched_manifest or decision_text):
        return 0

    reasons = []
    if touched_manifest:
        reasons.append("edited " + ", ".join(sorted(set(os.path.basename(p) for p in touched_manifest))[:3]))
    if decision_text:
        reasons.append("said \"" + decision_text[0] + "\"")
    print(json.dumps({
        "systemMessage": "ADR hint: this session " + " and ".join(reasons)
        + ". If that was a deliberate architectural decision, run /adr:new to record it. (Suggestion only.)"
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
