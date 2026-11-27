# Known debt

Things in this codebase that look deliberate but are not. Agents and people can
fix these without an ADR. When you fix one, delete its entry.

Format: one entry per item. Keep each entry shorter than five lines.

<!-- KNOWN-DEBT:START -->
<!-- KNOWN-DEBT:END -->

<!--
Example entry:

## Duplicate HTTP client in `services/billing/http.py`

- **What:** a second HTTP client with its own retry logic.
- **Why it exists:** copied during a rush; nobody chose it.
- **Fix when:** touching billing networking. Reuse `lib/http/client.py`.
- **Added:** 2026-10-02 by distill run.
-->
