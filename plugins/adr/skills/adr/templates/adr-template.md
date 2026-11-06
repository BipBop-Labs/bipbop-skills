---
id: ADR-NNNN
title: Short noun phrase stating the decision
status: proposed
date: YYYY-MM-DD
deciders: []
tags: []
paths: []
supersedes: []
superseded_by: []
---

# ADR-NNNN: Short noun phrase stating the decision

## Context

What situation forces a decision. Two to five sentences. Facts only, with evidence
(`path/to/file.ext:line`, commit SHA, issue link). No opinions here.

## Decision

State the lasting design constraint, its scope, and the essential intent or
tradeoff missing from other authoritative sources. Explain what future changes
it governs. Link to implementation and enforcement; do not copy algorithm
steps, schemas, signatures, thresholds, or configuration values.

## Options considered

- **Chosen option.** Why it was chosen. Cite evidence when available.
- **Alternative.** Why it was not chosen. Only list alternatives that were
  genuinely considered or that someone would reasonably propose. No strawmen.

## Consequences

- **Good:** ...
- **Bad:** ...
- **Watch:** signals that this decision should be revisited.

## Rationale status

`confirmed` (the decider stated the why) or `unknown` (the qualifying
constraint was confirmed, but its rationale is unavailable). Observed behavior
alone does not establish a binding decision. Omit speculative reasons.

## Evidence

- `path/to/file.ext:line` – what it shows.
- commit `abc1234` – message or diff that shows the decision.

## History

One line per change to the decision, added when the ADR is edited.

- YYYY-MM-DD: what changed and why.
