<!-- ADR:START -->
## Architecture decisions, policies and procedures

Decisions that constrain this codebase live in `docs/adr/`. Before changing a
dependency, a module or service boundary, a data model, a public interface, or
anything marked `@decision ADR-NNNN`, read `docs/adr/README.md` and the ADRs
whose `paths` match what you are touching. Accepted ADRs are binding: to change
one, obtain confirmation and rewrite the affected records in place. Consolidate
overlap and remove obsolete records and references; never silently undo a
constraint. Keep the collection concise. Git preserves history; do not add
replacement chains or `History` sections.
`docs/adr/known-debt.md` lists things that look deliberate but are not; those you
may fix.

Rules to follow live in `docs/policies/`. Steps for a task live in
`docs/procedures/`. Read the index of each folder and open only the docs whose
`paths` match your work. One rule, one doc: in this file, keep one line per
rule that names its source; do not restate the rule.
<!-- ADR:END -->
