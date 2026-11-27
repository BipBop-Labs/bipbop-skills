---
id: ADR-NNNN
title: Short noun phrase stating the decision
status: proposed
date: YYYY-MM-DD
deciders: []
tags: []
paths: []
---

# ADR-NNNN: Short noun phrase stating the decision

## Context

The situation that forces a decision. Two to five sentences. Facts only, with evidence
(`path/to/file.ext:line`, commit SHA, issue link). No opinions here.

## Decision

State the lasting design constraint and its scope. State the essential intent or
tradeoff that other authoritative sources do not record. Explain which future changes
the constraint governs. Link to the implementation and the enforcement. Do not copy algorithm
steps, schemas, signatures, thresholds, or configuration values.

## Options considered

- **Chosen option.** Why the team chose it. Cite evidence when it is available.
- **Alternative.** Why the team did not choose it. List only alternatives that the team
  really considered or that someone would reasonably propose. No strawmen.

## Consequences

- **Good:** ...
- **Bad:** ...
- **Watch:** signs that the team must examine this decision again.

## Rationale status

`confirmed` (the decider stated the reason) or `unknown` (someone confirmed the qualifying
constraint, but its rationale is not available). Observed behavior
alone does not establish a binding decision. Omit speculative reasons.

## Evidence

- `path/to/file.ext:line` – what it shows.
- commit `abc1234` – message or diff that shows the decision.
