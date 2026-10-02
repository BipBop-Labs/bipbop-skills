# Research notes for the `adr` plugin

Short notes that justify the design. Checked 2026-10-02. Not a literature
review.

## 1. Format: MADR-derived, trimmed

Candidates:

- **Nygard (2011).** Title, Context, Decision, Status, Consequences. Shortest;
  dominates on GitHub (IEEE Access 2023, below) and scored highest overall in
  a 2026 template comparison (arXiv 2604.27333, EASE 2026). No frontmatter, no
  machine-readable links.
- **MADR 4.0** ([adr/madr](https://github.com/adr/madr)). YAML frontmatter
  (`status`, `date`, `decision-makers`, `consulted`, `informed`), sections for
  Context and Problem Statement, Decision Drivers, Considered Options, Decision
  Outcome with Consequences and Confirmation, Pros and Cons. Status values
  `proposed | rejected | accepted | deprecated | superseded by ADR-XXXX`. Has
  `minimal` and `bare` variants. Best structural detail (same study).
- **Y-statements (Zimmermann).** One sentence: "In the context of…, facing…,
  we decided for…, and neglected…, to achieve…, accepting…, because…".
  Compact, but hard to attach metadata and paths to.

Chosen: MADR's shape with Nygard's length. YAML frontmatter with `id`,
`title`, `status`, `date`, `deciders`, `tags`, `paths`, `supersedes`,
`superseded_by`; body sections Context, Decision, Options considered,
Consequences, Rationale status, Evidence. Why:

- Agents need fields they can grep and match (`paths`, `supersedes`), which
  Nygard lacks and MADR has only partly (its `superseded by ADR-XXXX` is a
  status string, not a list).
- Both-ways supersede links are what lets a validator catch dangling
  references without parsing prose.
- Short bodies matter because agents read several ADRs per task, and
  arXiv 2609.07375 (~550 OSS repos) found real ADRs rarely fill MADR's
  optional sections anyway.
- `Rationale status: unknown` is new. Every tool evaluated in Phase 0.5
  invented rationale when the history was silent; the field makes the
  guess explicit.
- Sequential `NNNN-slug.md` numbering (adr-tools convention) rather than
  date stamps, because it gives stable IDs for `@decision` tags.

## 2. Existing tooling

From [adr.github.io/adr-tooling](https://adr.github.io/adr-tooling/):

- **adr-tools** (bash, Nygard): the `NNNN-slug.md` and `supersede` CLI
  conventions this plugin follows. Low activity, widely cloned.
- **log4brains** (Node, MADR 2.1.2): CLI plus static site. Slow maintenance.
- **adr-log**: index generator, listed as unmaintained. Replaced here by the
  marker-delimited index in `README.md`.
- **pyadr** (Python, MADR 2.1.2): lifecycle CLI, appears stale.
- **e-adr** ([adr/e-adr](https://github.com/adr/e-adr)): Java annotations
  `@MADR(...)` and `@ADR(n)` embedding decisions in code. The `@decision
  ADR-NNNN` comment is the language-agnostic version of `@ADR(n)`.

## 3. Claude Code prior art

Evaluated hands-on in Phase 0.5 on a 21-commit Python repository.

- **adrchive** (PyPI 0.2.0, April 2026; source repository returns 404). Stop
  hook in two modes: a subagent prompt on every Stop, or `adrchive auto` with
  byte-offset and message-count gating, a Haiku classifier (7 criteria,
  confidence ≥ 0.75) and Sonnet drafting through the API. Writes drafts and
  edits CLAUDE.md without asking. Copied: the gating idea and the "only
  decisions actually made, be conservative" framing, in a suggest-only,
  opt-in hook. Overkill: the LLM pipeline, dual modes, draft folder.
- **kayaman/effective-engineer-setup**: `/adr` skill, Nygard-style template
  with "at least three alternatives including do nothing", measurable
  consequence signals, humans move to Accepted. Copied: humans accept;
  consequences with watch signals. Not copied: the forced three alternatives
  (produces strawmen).
- **crowd.dev PR #4122**: `.claude/rules/adr-format.md`, template with
  deciders and risks, a warn-only guard hook, and the note that "patterns in
  transition" are the best first ADRs. Copied: AGENTS.md pointer, warn-only
  stance. Not copied: the reviewer agent (`/adr:review` is a skill instead).
- **joestump/claude-plugin-sdd**: grill-first questioning ("facts are yours,
  decisions are theirs"), a Confirmation section naming files a reviewer can
  check, status format detection, "left out as too thin" lists. Copied all
  four. Not copied: the hard `qmd` dependency, 22 skills, mandatory diagrams.
- **kschlt/adr-kit**: frontmatter schema with `policy` blocks and an
  adapter taxonomy (clause kind → tool → stage). Copied as the "enforceable
  vs advisory" rule in the stack table. Not copied: MCP-first design, 5.6 GB
  of dependencies, a quality gate that rejects honest "unknown" rationale.
- **laurigates blueprint-derive-plans**: driver option set for the "why"
  question, evidence block per ADR, index between markers. Copied all three.
  Not copied: PRD/PRP generation.
- **hailcpy/gen-adr**: evidence citations verified by a script, diff scoring
  with version-bump exclusion, workaround logs with a removal condition.
  Copied: scoring axes, HACK/WORKAROUND scan as debt candidates, removal
  condition in `known-debt.md`. Not copied: commit clustering.

None of them had accept / debt / reject / skip triage, a known-debt log, or
persisted review state, which is why this plugin exists.

## 4. Enforcement tools by stack

See [skills/adr/references/enforcement-by-stack.md](skills/adr/references/enforcement-by-stack.md).
The skill picks from that table at runtime after detecting the stack.

## 5. Evidence, stated honestly

- **Practitioners find ADRs useful but worry about effort.** Ahmeti, Linder,
  Wohlrab, womENcourage 2023 (poster, one company, two months): ADRs perceived
  as useful; concerns about how much to document and keeping records current.
  Ahmeti, Linder, Groner, Wohlrab, ECSA 2024
  ([doi:10.1007/978-3-031-70797-1_22](https://doi.org/10.1007/978-3-031-70797-1_22),
  seven interviews, one company, three months): ADRs helped documentation
  culture, knowledge transfer and cross-team cooperation; documenting
  distributed components stayed hard. Both are small, qualitative, single-site.
- **Adoption is low and often abandoned.** Buchgeher et al., IEEE Access 2023
  ([ieeexplore 10155430](https://ieeexplore.ieee.org/document/10155430)):
  ADR use on GitHub is rare though growing, and about half of repositories
  with ADRs have only one to five. This is why `/adr:distill` and the trigger
  list exist: the first five are the hard part, and over-documentation is the
  failure mode after that.
- **Context files for agents: no measured win.**
  [arXiv 2602.11988](https://arxiv.org/abs/2602.11988) (Gloaguen et al.,
  evaluating AGENTS.md): context files did not generally improve task success
  and raised cost by more than 20%; developer-written files showed a marginal
  gain, LLM-generated ones a marginal loss, and repository overviews did not
  help. [arXiv 2607.27250](https://arxiv.org/abs/2607.27250) (Khatri, small
  ablation): no measurable correctness improvement.
  [arXiv 2602.20478](https://arxiv.org/abs/2602.20478) is a single-project
  experience report claiming benefits, without a control. No controlled study
  found reporting efficiency gains. Consequence for this design: the
  CLAUDE.md snippet is five lines and points to an index; ADRs are loaded
  selectively by `paths`, never wholesale.
- **Newer ADR work (2025 to 2026).** LLM drafting of decisions
  ([arXiv 2504.08207](https://arxiv.org/abs/2504.08207)); template comparison
  ([arXiv 2604.27333](https://arxiv.org/abs/2604.27333)); ADRs from meeting
  transcripts with a noted risk of unfaithful RAG content
  ([arXiv 2608.17694](https://arxiv.org/abs/2608.17694)); a mining study
  showing ADRs under-document alternatives and drivers
  ([arXiv 2609.07375](https://arxiv.org/abs/2609.07375)). Nothing measured
  ADR staleness or the effect of ADRs on agent behaviour. Treat the premise
  of this plugin, that ADRs stop agents undoing decisions, as plausible and
  unmeasured.

## 6. Design consequences

| Finding | Design choice |
| --- | --- |
| Over-documentation is the main complaint | Falsifiable trigger list plus an explicit do-not list; batches of five |
| Repos stall at one to five ADRs | `/adr:distill` with resumable state and incremental `--since` |
| Tools invent rationale | `Guess (unconfirmed):` label, `Rationale status: unknown`, user verdicts |
| Context files cost tokens | Index first, `paths`-based selection, five-line snippet |
| Loading is not enforcing | Enforcement table, `@decision` tags, `/adr:review` as a report-only backstop |
| Stop-hook capture is noisy | Hook shipped disabled, suggest-only, no LLM |
