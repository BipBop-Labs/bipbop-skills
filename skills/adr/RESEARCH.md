# Research notes for the `adr` plugin

Short notes that justify the design. Checked 2026-10-02. Section 7 checked
2026-11-25. This is not a literature review.

## 1. Format: MADR-derived, trimmed

Candidates:

- **Nygard (2011).** Title, Context, Decision, Status, Consequences. The shortest format.
  It is the most common on GitHub (IEEE Access 2023, below). It got the highest overall score in
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
  Compact, but it is hard to attach metadata and paths to it.

Chosen: MADR's shape with Nygard's length. YAML frontmatter with `id`,
`title`, `status`, `date`, `deciders`, `tags`, `paths`; body sections Context, Decision, Options considered,
Consequences, Rationale status, Evidence. Reasons:

- `paths` lets agents select the relevant current constraints. They do not load
  every document. The standing skill defines the admission and maintenance policy.
- Short bodies are important because agents read several ADRs per task.
  Also, arXiv 2609.07375 (~550 OSS repos) found that real ADRs rarely fill the
  optional MADR sections.
- `Rationale status: unknown` is new. Every tool that Phase 0.5 evaluated
  invented a rationale when the history had none. The field marks a missing
  rationale and does not turn speculation into evidence.
- Sequential `NNNN-slug.md` numbering (adr-tools convention), not
  date stamps. When a consolidation renumbers records, the references change too.

## 2. Existing tooling

From [adr.github.io/adr-tooling](https://adr.github.io/adr-tooling/):

- **adr-tools** (bash, Nygard): the `NNNN-slug.md` naming
  convention that this plugin uses. Low activity, many clones.
- **log4brains** (Node, MADR 2.1.2): CLI plus static site. Slow maintenance.
- **adr-log**: index generator, listed as unmaintained. This plugin uses the
  index between markers in `README.md` in its place.
- **pyadr** (Python, MADR 2.1.2): lifecycle CLI, appears stale.
- **e-adr** ([adr/e-adr](https://github.com/adr/e-adr)): Java annotations
  `@MADR(...)` and `@ADR(n)` put decisions in code. The `@decision
  ADR-NNNN` comment is the version of `@ADR(n)` for any language.

## 3. Claude Code prior art

Phase 0.5 tested these tools on a Python repository with 21 commits.

- **adrchive** (PyPI 0.2.0, April 2026; the source repository returns 404). A Stop
  hook with two modes:
  - a subagent prompt on every Stop;
  - `adrchive auto`, with a gate on byte offset and message count, a Haiku classifier (7 criteria,
    confidence ≥ 0.75), and Sonnet drafts through the API.
  It writes drafts and
  edits CLAUDE.md without a question. Copied: the gate idea and the "only
  decisions actually made, be conservative" framing, in a hook that only suggests and is
  opt-in. Too much: the LLM pipeline, the two modes, the draft folder.
- **kayaman/effective-engineer-setup**: `/adr` skill, Nygard-style template
  with "at least three alternatives including do nothing", measurable
  consequence signals, and humans move ADRs to Accepted. Copied: humans accept;
  consequences with watch signals. Not copied: the three mandatory alternatives
  (they produce strawmen).
- **crowd.dev PR #4122**: `.claude/rules/adr-format.md`, template with
  deciders and risks, a guard hook that only warns, and the note that "patterns in
  transition" are the best first ADRs. Copied: AGENTS.md pointer, the
  warn-only approach. Not copied: the reviewer agent (`/bipbop-skills:adr-review` is a skill instead).
- **joestump/claude-plugin-sdd**: grill-first questioning ("facts are yours,
  decisions are theirs"), a Confirmation section naming files a reviewer can
  check, status format detection, "left out as too thin" lists. Copied all
  four. Not copied: the mandatory `qmd` dependency, 22 skills, mandatory diagrams.
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
saved review state. That is why this plugin exists.

## 4. Enforcement tools by stack

See [skills/adr/references/enforcement-by-stack.md](references/enforcement-by-stack.md).
The skill finds the stack at runtime and then picks from that table.

## 5. Evidence, stated honestly

- **Practitioners find ADRs useful but worry about effort.** Ahmeti, Linder,
  Wohlrab, womENcourage 2023 (poster, one company, two months): people found ADRs
  useful. Their concerns were how much to document and how to keep records current.
  Ahmeti, Linder, Groner, Wohlrab, ECSA 2024
  ([doi:10.1007/978-3-031-70797-1_22](https://doi.org/10.1007/978-3-031-70797-1_22),
  seven interviews, one company, three months): ADRs helped documentation
  culture, knowledge transfer, and cross-team cooperation. Documentation of
  distributed components stayed hard. Both studies are small, qualitative, and single-site.
- **Adoption is low and often abandoned.** Buchgeher et al., IEEE Access 2023
  ([ieeexplore 10155430](https://ieeexplore.ieee.org/document/10155430)):
  ADR use on GitHub is rare but it grows. About half of the repositories
  with ADRs have only one to five. This is why `/bipbop-skills:adr-distill` and the trigger
  list exist. The first five are the hard part. After that, over-documentation is the
  failure mode.
- **Context files for agents: no measured win.**
  [arXiv 2602.11988](https://arxiv.org/abs/2602.11988) (Gloaguen et al.,
  evaluating AGENTS.md): context files did not generally improve task success.
  They increased cost by more than 20%. Files that developers wrote showed a marginal
  gain. Files that an LLM generated showed a marginal loss. Repository overviews did not
  help. [arXiv 2607.27250](https://arxiv.org/abs/2607.27250) (Khatri, small
  ablation): no measurable correctness improvement.
  [arXiv 2602.20478](https://arxiv.org/abs/2602.20478) is a single-project
  experience report that claims benefits, with no control. We found no controlled study
  that reports efficiency gains. Consequence for this design: the
  CLAUDE.md snippet is five lines and points to an index. Agents load ADRs
  selectively by `paths`, never all of them.
- **Newer ADR work (2025 to 2026).** LLM drafting of decisions
  ([arXiv 2504.08207](https://arxiv.org/abs/2504.08207)); template comparison
  ([arXiv 2604.27333](https://arxiv.org/abs/2604.27333)); ADRs from meeting
  transcripts with a noted risk of unfaithful RAG content
  ([arXiv 2608.17694](https://arxiv.org/abs/2608.17694)); a mining study
  that shows that ADRs under-document alternatives and drivers
  ([arXiv 2609.07375](https://arxiv.org/abs/2609.07375)). No study measured
  ADR staleness or the effect of ADRs on agent behavior. The premise
  of this plugin is that ADRs stop agents from undoing decisions. Treat it as plausible and
  not measured.

## 6. Design consequences

| Finding | Design choice |
| --- | --- |
| Over-documentation is the main complaint | Falsifiable trigger list plus an explicit do-not list; batches of five |
| Repos stall at one to five ADRs | `/bipbop-skills:adr-distill` with resumable state and incremental `--since` |
| Tools invent rationale | `Guess (unconfirmed):` label, `Rationale status: unknown`, user verdicts |
| Context files cost tokens | Index first, `paths`-based selection, five-line snippet |
| Loading is not enforcing | Enforcement table, `@decision` tags, `/bipbop-skills:adr-review` as a report-only backstop |
| Stop-hook capture is noisy | Hook shipped disabled, suggest-only, no LLM |

## 7. ADR, policy, and procedure (2026-11-25)

The plugin now has three kinds of rule doc. Prior art for the split:

- **Scope of an ADR.** Nygard limits ADRs to "structure, non-functional
  characteristics, dependencies, interfaces, or construction techniques"
  ([cognitect.com, 2011](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)).
  Joel Parker Henderson says not to write an ADR when the decision is "not
  about architecture" or "already fully covered elsewhere such as by standards
  or policies"
  ([joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)).
  Many coding-rule ADRs (no magic numbers, comments in English, lint rules)
  are policies that a lint enforces.
- **One format with a kind field failed.** MADR renamed itself to "Any
  Decision Records" in 2022 and went back to "Architectural" in 2024
  ([adr.github.io/madr](https://adr.github.io/madr/)). The kinds have
  different lifecycles, so each kind gets its own folder and metadata.
- **Names.** ISO 9001 practice separates policy, procedure, work instruction,
  and record
  ([Advisera](https://advisera.com/9001academy/knowledgebase/how-to-structure-quality-management-system-documentation/)).
  NIST uses "policy" for a rule people must follow
  ([csrc.nist.gov](https://csrc.nist.gov/glossary/term/security_policy)).
  Rejected names: "guideline" (means optional), "standard" (clashes with
  external standards), "principle" (a criterion, not a rule), "convention"
  (only code style), "runbook" and "playbook" (alert response in SRE and
  PagerDuty practice), Diataxis "how-to" (not binding,
  [diataxis.fr](https://diataxis.fr/)).
- **Lifecycles.** The GDS Way keeps standards apart from manuals and gives
  each page a `review_in` period
  ([gds-way.digital.cabinet-office.gov.uk](https://gds-way.digital.cabinet-office.gov.uk/)).
  The Google SRE workbook says that procedures become stale as fast as production
  changes ([sre.google/workbook/on-call](https://sre.google/workbook/on-call/)),
  so a procedure has `last_verified`, and you delete it when a script replaces it.
- **One source of truth.** GitLab's handbook-first rule and docs-as-code
  practice ([handbook.gitlab.com](https://handbook.gitlab.com/handbook/about/handbook-usage/),
  [writethedocs.org](https://www.writethedocs.org/guide/docs-as-code/)) and
  Google's documentation guide
  ([google.github.io/styleguide/docguide/best_practices](https://google.github.io/styleguide/docguide/best_practices.html))
  support "one rule, one doc; link, do not restate", minimum viable docs, and
  doc changes in the same change as the code.

| Finding | Design choice |
| --- | --- |
| Coding rules end up as ADRs | Routing test: code first, then ADR, procedure, policy, split; "a rule with no tradeoff is a policy" |
| One format for all kinds was reverted (MADR) | Three folders, three templates, metadata per kind |
| Policies and procedures go stale | `review_in` and `last_verified`; the validator warns on expiry |
| Rules get copied into agent files | One line per rule in `CLAUDE.md` / `AGENTS.md`, naming its source |
| Renumbering breaks references | Policy and procedure file names are the ID; no numbers |
