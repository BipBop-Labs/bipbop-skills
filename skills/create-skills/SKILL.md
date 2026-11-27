---
name: create-skills
description: Create or revise portable agent skills, and validate their packaging. Use when you add a SKILL.md workflow for Claude Code, Codex, or ChatGPT, or when you review a skill for quality, safety, and distribution.
---

# Create skills

Create focused, portable skills. Each skill has clear triggers, a repeatable workflow, and observable completion criteria.
Use the subset of features that Claude Code, Codex, and ChatGPT all support. Use host-specific features only when the task targets one host.

## When to use

Use this skill when you:

- create a new `SKILL.md`;
- restructure or improve an existing skill;
- move a skill into a plugin or marketplace;
- review the activation, instructions, support files, or safety of a skill;
- prepare a skill for public distribution.

Do not create a skill for a one-off fact, temporary task state, or project progress.
Do not create a skill for a workflow that is too small to need reusable instructions.
If the proposed skill overlaps an existing skill by a large amount, improve the existing skill.

## 1. Set the contract

Before you write files, find out:

1. **User goal:** the outcome that the skill supports, in terms the user recognizes.
2. **Triggers:** the requests that must make the model consider the skill.
3. **Counter-triggers:** similar requests that belong to a different skill.
4. **Inputs:** the information, files, credentials, tools, or services that the skill needs.
5. **Actions:** the read-only steps and the possible side effects.
6. **Output:** what the user receives, and in which format.
7. **Success evidence:** the command, artifact, ID, URL, test, or state that proves completion.
8. **Hosts:** Claude Code, Codex, ChatGPT, or a host-specific subset.

If two use cases have different triggers, inputs, permissions, or success criteria, put them in separate skills.
Do not create a router skill that only points at sibling skills.

## 2. Inspect before you write

1. Read the repository instructions, such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and the README.
2. Search the existing skills for triggers, procedures, and names that overlap.
3. Read two or three neighbor skills, and match the conventions of the repository.
4. Read the current official host documentation before you change plugin manifests or use host-specific frontmatter.
5. Read the source material directly. Do not write from memory or from documents that you cannot open.

Completion criterion: you know the target location, the owner, the supported hosts, the overlap decision, and the repository rules that apply.

## 3. Choose the directory layout

Use one self-contained directory for each skill:

```text
skills/<skill-name>/
├── SKILL.md
├── references/   # optional detailed material
├── scripts/      # optional deterministic automation
└── assets/       # optional static resources
```

Use lowercase `kebab-case` for the folder name and the skill name.
Keep all relative links inside the plugin root.
Do not use machine-local paths, or symlinks that point outside the repository.

Add a support directory only when the skill needs it:

- `references/`: detailed guidance, API notes, schemas, checklists, or source summaries that the model loads only when it needs them;
- `scripts/`: deterministic work that is difficult to do correctly with ordinary tools;
- `assets/`: templates, images, fixtures, or other static inputs that the outputs use.

Do not add empty directories. Do not copy the skill tree for each host.

## 4. Write portable frontmatter

The portable minimum is:

```yaml
---
name: example-skill
description: Perform a specific workflow. Use when the user asks for X or needs Y.
---
```

Rules:

- `name` is the same as the directory name.
- `name` is stable and descriptive, and uses `kebab-case`.
- `description` states the capability and the activation conditions.
- Put the detailed procedure, the output format, and the safety rules in the body, not in the description.
- Make the description precise, so that the skill does not activate for unrelated requests.
- Add a host-specific field only when the current official schema supports it and the skill needs it.

If the skill activates at the wrong time, fix the description first. Do not add defensive text to the body for this problem.

## 5. Write an actionable body

Use only sections that change behavior. The default structure is:

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

- Put dependent steps in an explicit order.
- End each important step with an observable completion criterion.
- Name the correct tool or integration when the choice matters.
- Run work in parallel only when the tasks are independent.
- State what the model does when an input or a tool is missing.
- Keep a draft of an action separate from its execution in an external system.
- After a write, require a check of the result. Do not trust a success message.
- When an explicit user instruction and a default in the skill disagree, the user instruction wins.

### Writing rules

- Give direct instructions. Do not give background explanation.
- State each rule once, and use the same term for the same thing every time.
- With each important prohibition, state the behavior that is allowed in its place.
- Give the reason for a rule only when the reason helps the model with edge cases.
- Use absolute words ("always", "never") only for requirements that have no valid exception.
- Use invented examples that teach the correct pattern and show no real data.

## 6. Use progressive disclosure

Keep `SKILL.md` focused on routing, decisions, and the main procedure.
Move large or specialized material into support files.
Link each support file from `SKILL.md`, and state when the model loads it.

Good:

```text
Read references/api.md only when the task calls the service API.
Run scripts/validate.py after modifying generated configuration.
```

Avoid:

- a large `SKILL.md` that contains material that only rare cases need;
- orphan support files that the main skill does not link to;
- copied documentation that must stay an external link;
- scripts for tasks that existing tools already do reliably.

## 7. Design safe side effects

For each workflow that can change data or external systems:

1. keep discovery separate from changes;
2. read the live state before you decide what to change;
3. define the allowed scope precisely;
4. require confirmation for an action that is destructive, costly, public, or difficult to reverse, unless the user already authorized that exact action;
5. use the tools and credentials with the fewest privileges that the task needs;
6. check the result with a direct read, an ID, a URL, or a test;
7. when practical, explain how to roll back or recover.

Never tell an agent to bypass authorization, disable safeguards, or expose secrets.
Never tell an agent to use destructive commands to get past an error.

## 8. Prepare for public distribution

Before you publish, inspect every file and the Git diff for:

- credentials, tokens, private keys, cookies, webhooks, and internal endpoints;
- customer names, personal data, government identifiers, private emails, and phone numbers;
- workspace, database, channel, page, ticket, or document IDs;
- recognizable stories that come from real conversations or incidents;
- proprietary code, internal architecture, or confidential operating procedures;
- third-party text, images, examples, or code that has no compatible permission and attribution.

Invent public examples from the start.
If you only replace the name of a person, and a reader can still identify the scenario, the example is not safe.

For third-party material, record the source and the license.
If a summary is enough, link to the original.
Do not publish a chapter-by-chapter substitute for a book, long quotations, or copied examples. This rule applies also when you convert them to Markdown.

## 9. Test activation and behavior

Before you declare the skill complete, create a small evaluation set:

- **positive cases:** typical requests that must activate the skill;
- **negative cases:** similar requests that must not activate the skill;
- **ambiguous cases:** requests where the model must inspect the context or ask a narrow question;
- **failure cases:** missing files, unavailable tools, denied permissions, empty results, and partial responses;
- **side-effect cases:** confirmation, scope limits, checks of the result, and rollback.

Evaluate the two layers separately:

1. **Activation:** did the model choose the correct skill? If not, revise `description`.
2. **Execution:** did the model follow the correct workflow and produce consistent output? If not, revise the body or the support files.

Do not tune the skill against one anecdote.
Use examples that are different enough that the model learns the decision rule, not the surface words.

## 10. Validate the package

At minimum:

1. parse all JSON manifests;
2. validate the YAML frontmatter, and require a `name`, a `description`, and a body that are not empty;
3. check that each folder name is the same as its skill name, that the names are unique, and that they use `kebab-case`;
4. resolve relative links, and reject path traversal;
5. inspect symlinks and executable files;
6. run the repository tests, the linters, and the secret scan;
7. run the current first-party host validator when it is available;
8. install the plugin from an isolated local marketplace;
9. check that each expected `SKILL.md` is in the installed cache;
10. do these steps again from the Git-backed branch or tag before you announce that the distribution succeeded.

For this repository, run:

```bash
python3 scripts/validate.py
claude plugin validate .
```

Then run the isolated Claude and Codex installation commands in the repository README.

## 11. Update repository metadata

When you add a skill to a versioned marketplace:

1. add the skill to the README catalog;
2. update the changelog;
3. increase the plugin version as the repository policy says;
4. keep duplicate compatibility manifests in sync;
5. do not repeat the version in marketplace entries when the plugin manifest is the source of truth;
6. run the validation again after you change the metadata.

A new skill that is backward-compatible is a minor release.
A removal, a rename, an incompatible behavior, or a new mandatory permission is a major change.

## Verification checklist

- [ ] The skill supports one recognizable goal.
- [ ] The positive and negative triggers are explicit.
- [ ] `name` is the same as the `kebab-case` folder name.
- [ ] `description` states the capability and the activation conditions.
- [ ] The prerequisites, failures, side effects, and output are clear.
- [ ] Each important step ends with an observable completion criterion.
- [ ] Each support file is necessary, linked, and loaded only when needed.
- [ ] All paths stay inside the plugin root.
- [ ] The public files contain no private or proprietary data.
- [ ] Third-party material has compatible provenance and attribution.
- [ ] You tested the positive, negative, ambiguous, failure, and side-effect cases.
- [ ] The repository validators and the client installation tests passed.
- [ ] The installed caches contain the expected skill files.
- [ ] You updated the README, the changelog, and the synchronized versions.
- [ ] You checked the Git-backed installation before the release.
