# Eligibility evaluation cases

Use these synthetic cases when revising the eligibility policy. Load the
standing skill and the new, review, and distill workflows on a supported host.
Ask for an outcome and explanation for each case without creating files.
Compare with the expectations below; inspect reasoning as well as labels.
These cases exercise policy execution, not automatic skill discovery.

| Case | Scenario | Expected behavior |
| --- | --- | --- |
| 1 | Add a date library and lockfile; no lasting design constraint discussed. | No ADR. Dependency changes alone are insufficient. |
| 2 | Confirm extensions must run outside the application process to protect availability, accepting latency cost. The lasting boundary and tradeoff are absent from authoritative sources; future in-process integrations could violate it. | ADR candidate. Preserve the confirmed missing constraint and tradeoff. |
| 3 | Describe the exact history-pruning algorithm, thresholds, and phases already in code and tests. | No ADR or replacement Markdown. |
| 4 | Many endpoints use one response wrapper; intent is unknown. | Ask about intent; repetition alone does not establish a norm. |
| 5 | A migration is expensive to reverse, but all available intent and procedure are already authoritative. | No ADR. Reversal cost does not establish a documentation gap. |
| 6 | Change a handler governed by an accepted authentication-authority ADR. | Read and respect the existing ADR. The new filter does not invalidate it. |
| 7 | A dependency check already captures the entire intended rule, scope, and reason. | No ADR unless essential missing context is identified. |
| 8 | Distillation finds only two low-scoring implementation choices; the user requests five records. | No quota filling. Finish with zero candidates, scan state, and a report. |
| 9 | Invoke /adr:new for a sorting function fully explained by code and tests. | Explain that no ADR is warranted before creating files. |
| 10 | Repository access fails; only dependency and migration filenames are available. | Report insufficient evidence. Do not assert missing ADRs or claim the inaccessible repository needs none. |
| 11 | Confirm a lasting overlapping-version deployment policy and accepted compatibility overhead absent from authoritative sources. Future migrations could break that guarantee. | ADR candidate about the guarantee and scope, not migration steps. |
| 12 | Record a statutory retention deadline as an architectural decision. | Keep the requirement in its authoritative policy source. Importance and longevity alone are insufficient. |

Also inspect workflow consistency: existing accepted decisions follow the
standing lifecycle; zero-candidate runs skip triage but still finish reporting.

Security review for the optional Stop hook: verify it remains opt-in, reads the
same local transcript and offset as before, never writes ADRs, makes no network
calls, and suggests eligibility assessment rather than automatic creation.
