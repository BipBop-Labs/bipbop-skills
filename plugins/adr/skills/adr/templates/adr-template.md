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

One paragraph in the active voice: "We use X for Y." State the rule an agent
must follow when touching the code listed in `paths`.

## Options considered

- **Chosen option.** Why it was chosen. Cite evidence when available.
- **Alternative.** Why it was not chosen. Only list alternatives that were
  genuinely considered or that someone would reasonably propose. No strawmen.

## Consequences

- **Good:** ...
- **Bad:** ...
- **Watch:** signals that this decision should be revisited.

## Rationale status

`confirmed` (the decider stated the why) or `unknown` (recovered from code or
history without confirmation; treat the Decision as binding but the why as a guess).

## Evidence

- `path/to/file.ext:line` – what it shows.
- commit `abc1234` – message or diff that shows the decision.
