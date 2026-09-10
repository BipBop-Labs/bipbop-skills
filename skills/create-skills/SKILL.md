---
name: create-skills
description: Create or revise portable agent skills and validate their packaging. Use when adding a SKILL.md workflow for Claude Code, Codex, or ChatGPT, or when reviewing a skill for quality, safety, and distribution.
---

# Create skills

Create focused, portable agent skills that activate for the right requests, guide a repeatable workflow, and provide observable completion criteria. Use the common subset supported by Claude Code, Codex, and ChatGPT unless the task explicitly targets one host.

## When to use

Use this skill when:

- creating a new `SKILL.md`;
- restructuring or improving an existing skill;
- moving a skill into a plugin or marketplace;
- reviewing skill activation, instructions, support files, or safety;
- preparing a skill for public distribution.

Do not create a skill for a one-off fact, temporary task state, project progress, or a workflow too small to justify reusable instructions. Prefer improving an existing skill when the proposed one substantially overlaps it.

## 1. Establish the contract

Before writing files, determine:

1. **User goal:** the recognizable outcome the skill supports.
2. **Triggers:** requests that should cause the model to consider the skill.
3. **Counter-triggers:** similar requests that belong elsewhere.
4. **Inputs:** information, files, credentials, tools, or services required.
5. **Actions:** read-only steps and possible side effects.
6. **Output:** what the user receives and in which format.
7. **Success evidence:** the command, artifact, ID, URL, test, or state that proves completion.
8. **Hosts:** Claude Code, Codex, ChatGPT, or a host-specific subset.

If different use cases have different triggers, inputs, permissions, or success criteria, split them into separate skills. Do not create a router skill whose main purpose is only to point at sibling skills.

## 2. Inspect before authoring

1. Read repository-level instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and the README.
2. Search existing skills for overlapping triggers, procedures, and names.
3. Read two or three neighboring skills to match repository conventions.
4. Check current official host documentation before changing plugin manifests or relying on host-specific frontmatter.
5. Inspect any source material directly. Do not write from remembered or inaccessible documents.

Completion criterion: the target location, ownership, supported hosts, overlap decision, and applicable repository rules are known.

## 3. Choose the directory layout

Use one self-contained directory per skill:

```text
skills/<skill-name>/
├── SKILL.md
├── references/   # optional detailed material
├── scripts/      # optional deterministic automation
└── assets/       # optional static resources
```

Use lowercase `kebab-case` for the folder and skill name. Keep all relative links within the plugin root. Do not depend on machine-local paths or symlinks that escape the repository.

Use supporting directories deliberately:

- `references/`: detailed guidance, API notes, schemas, checklists, or source summaries loaded only when needed;
- `scripts/`: deterministic work that is difficult or error-prone to reproduce through ordinary tools;
- `assets/`: templates, images, fixtures, or other static inputs used in outputs.

Do not add empty directories or duplicate the skill tree for different hosts.

## 4. Write portable frontmatter

The portable minimum is:

```yaml
---
name: example-skill
description: Perform a specific workflow. Use when the user asks for X or needs Y.
---
```

Rules:

- `name` matches the directory exactly.
- `name` is stable, descriptive, and uses `kebab-case`.
- `description` states both the capability and activation conditions.
- Put detailed procedure, output formatting, and safety rules in the body, not the description.
- Keep the description precise enough to avoid broad accidental activation.
- Add host-specific fields only when the current official schema supports them and the skill needs them.

The description controls discovery. If the skill activates at the wrong time, fix the description before adding defensive prose to the body.

## 5. Write an actionable body

Use only sections that change behavior. A strong default structure is:

```markdown
# Skill title

Short scope statement.

## When to use
- Positive triggers.
- Counter-triggers.

## Prerequisites
- Exact tools, access, files, and setup.

## Procedure
1. Action with a checkable completion criterion.

## Pitfalls
- Specific failure modes and recoveries.

## Verification
- Evidence that proves the workflow succeeded.
```

### Procedure rules

- Order dependent steps explicitly.
- End important steps with an observable completion criterion.
- Name the correct tool or integration when the choice matters.
- Use parallel execution only for independent work.
- State what to do when an input or tool is missing.
- Distinguish drafting an action from executing it in an external system.
- Require verification after writes instead of trusting a success message.
- Preserve explicit user instructions over defaults in the skill.

### Writing rules

- Prefer direct instructions over background explanation.
- State a rule once and keep terminology consistent.
- Pair important prohibitions with the allowed replacement behavior.
- Explain the reason only when it helps generalize to edge cases.
- Reserve absolute language for requirements with no legitimate exception.
- Use invented examples that teach the desired pattern without exposing real data.

## 6. Use progressive disclosure

Keep `SKILL.md` focused on routing, decisions, and the canonical procedure. Move large or specialized material into supporting files and link each file from `SKILL.md` with a clear loading condition.

Good:

```text
Read references/api.md only when the task calls the service API.
Run scripts/validate.py after modifying generated configuration.
```

Avoid:

- an oversized `SKILL.md` containing material needed only in rare cases;
- orphan support files that the main skill never references;
- copied documentation that should remain an external link;
- scripts for tasks existing tools already perform reliably.

## 7. Design safe side effects

For any workflow that can modify data or external systems:

1. separate discovery from mutation;
2. retrieve live state before deciding what to change;
3. define the allowed scope precisely;
4. require confirmation for destructive, costly, public, or difficult-to-reverse actions unless the user already authorized that exact action;
5. use least-privilege tools and credentials;
6. verify the resulting state through a direct read, ID, URL, or test;
7. explain rollback or recovery when practical.

Never instruct an agent to bypass authorization, disable safeguards, expose secrets, or use destructive commands as a shortcut around an error.

## 8. Prepare for public distribution

Before publishing, inspect every file and the Git diff for:

- credentials, tokens, private keys, cookies, webhooks, and internal endpoints;
- customer names, personal data, government identifiers, private emails, and phone numbers;
- workspace, database, channel, page, ticket, or document IDs;
- recognizable stories derived from real conversations or incidents;
- proprietary code, internal architecture, or confidential operating procedures;
- third-party text, images, examples, or code without compatible permission and attribution.

Invent public examples from scratch. Merely replacing a person's name is not sufficient when the rest of the scenario remains identifiable.

For third-party material, record the source and license. Link to the original when a summary is enough. Do not publish a chapter-by-chapter substitute for a book, extensive quotations, or copied examples merely because they were transformed into Markdown.

## 9. Test activation and behavior

Create a small evaluation set before declaring the skill complete:

- **positive cases:** representative requests that should activate it;
- **negative cases:** similar requests that should not activate it;
- **ambiguous cases:** requests where the model should inspect context or ask a narrow question;
- **failure cases:** missing files, unavailable tools, denied permissions, empty results, and partial responses;
- **side-effect cases:** confirmation, scope enforcement, verification, and rollback behavior.

Evaluate two layers separately:

1. **Activation:** did the model choose the right skill? If not, revise `description`.
2. **Execution:** did it follow the correct workflow and produce consistent output? If not, revise the body or supporting resources.

Do not tune against one anecdote. Keep examples diverse enough that the model learns the decision rule rather than surface wording.

## 10. Validate the package

At minimum:

1. parse all JSON manifests;
2. validate YAML frontmatter and require non-empty `name`, `description`, and body;
3. check folder-name equality, unique names, and `kebab-case`;
4. resolve relative links and reject path traversal;
5. inspect symlinks and executable files;
6. run repository tests, linters, and secret scanning;
7. run the current first-party host validator when available;
8. install the plugin from an isolated local marketplace;
9. verify every expected `SKILL.md` exists in the installed cache;
10. repeat from the Git-backed branch or tag before announcing distribution success.

A manifest that parses is not proof that clients discover or install the skill.

For this repository, run:

```bash
python3 scripts/validate.py
claude plugin validate .
```

Then follow the isolated Claude and Codex installation commands in the repository README.

## 11. Update repository metadata

When adding a skill to a versioned marketplace:

1. add it to the README catalog;
2. update the changelog;
3. bump the plugin version according to repository policy;
4. keep duplicate compatibility manifests synchronized;
5. avoid repeating the version in marketplace entries when the plugin manifest is authoritative;
6. run validation again after metadata changes.

Treat a new backward-compatible skill as a minor release. Treat removals, renames, incompatible behavior, or new mandatory permissions as major changes.

## Pitfalls

- **Description as documentation:** a long description harms routing; move procedure into the body.
- **One giant skill:** unrelated goals with different triggers become unpredictable.
- **Router-only skill:** indirection duplicates the catalog without adding workflow value.
- **Manifest-only confidence:** JSON validity does not prove installation or discovery.
- **Duplicated trees:** copies for different clients drift over time.
- **Machine-local assumptions:** absolute paths and personal configuration break portability.
- **Unverified side effects:** a tool's success message is not the resulting state.
- **Private examples:** sanitized names can still leave a recognizable incident.
- **Unlicensed source material:** summaries can still become substitutes when they preserve an entire work's sequence, examples, and detail.
- **Premature scripting:** code adds maintenance and security surface without necessarily improving reliability.
- **Overfitting tests:** activation that works only for the evaluation phrasing is not robust.

## Verification checklist

- [ ] The skill supports one recognizable goal.
- [ ] Positive and negative triggers are explicit.
- [ ] `name` matches the `kebab-case` folder.
- [ ] `description` states capability and activation conditions.
- [ ] Prerequisites, failures, side effects, and output are clear.
- [ ] Important steps end with observable completion criteria.
- [ ] Supporting files are necessary, linked, and loaded conditionally.
- [ ] Paths remain inside the plugin root.
- [ ] Public files contain no private or proprietary data.
- [ ] Third-party material has compatible provenance and attribution.
- [ ] Positive, negative, ambiguous, failure, and side-effect cases were tested.
- [ ] Repository validators and client installation tests passed.
- [ ] Installed caches contain the expected skill files.
- [ ] README, changelog, and synchronized versions were updated.
- [ ] Git-backed installation was verified before release.

## Official references

Check these sources again before relying on changing manifest or client behavior:

- [OpenAI: Build skills](https://developers.openai.com/plugins/build/skills)
- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [OpenAI: Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management)
- [Claude Code: Create plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code: Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
