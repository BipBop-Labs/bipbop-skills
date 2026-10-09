# Prompts for agents: placement, tools, delegation, long runs

Read this when the prompt belongs to an agent: it has tools, delegates to other models, loads skills or instruction files, or runs long enough for its context to be summarised. The principles in `SKILL.md` still apply; this file covers what is specific to agents.

## Contents

- [Where each piece of text belongs](#where-each-piece-of-text-belongs)
- [Tool names, descriptions and schemas](#tool-names-descriptions-and-schemas)
- [Tool results and errors](#tool-results-and-errors)
- [Delegation briefs](#delegation-briefs)
- [Skills and instruction files](#skills-and-instruction-files)
- [Long runs: compaction, handoffs and state](#long-runs-compaction-handoffs-and-state)
- [Text injected during a run](#text-injected-during-a-run)

## Where each piece of text belongs

An agent reads several layers of text, and a rule placed in the wrong layer either costs tokens on every request or is missing when it is needed.

| Content | Where it goes | Why |
| --- | --- | --- |
| What the product is, who uses it, what the agent is for, tone, the authorisation policy | System prompt | Needed on nearly every request. |
| Safety, legal and brand constraints | System prompt, whatever their frequency | They must be present before the first action, and loading them on demand can fail. |
| Guidance relevant to roughly a third or more of requests | System prompt | Loading it on demand would cost an extra turn most of the time. |
| Procedures and knowledge relevant to a minority of requests | A skill or a file loaded on demand, with a description that says when to load it | Rarely needed text in the system prompt dilutes the rest and is paid for on every request. |
| How and when to use one specific tool | That tool's description | The guidance travels with the tool and is not duplicated. |
| Policy that spans tools: ordering, choosing between similar tools, whether an action is allowed and who approves it | System prompt | No single description owns it. The tool's description states the facts that make the policy matter (it sends immediately, it cannot be undone) and leaves the rule to the system prompt, so the two cannot drift apart. |
| Facts about the project that the model cannot infer from the files | The always-loaded project instruction file | Anything derivable from the code is noise there. |
| Live state: time, current mode, a file that changed, remaining budget | A short factual message appended to the conversation | Editing the system prompt mid-run discards the cached prefix and can confuse the model about what changed. |
| Plans, task lists, approvals, progress | A file or store the agent reads and updates | Conversation context is summarised and lost; a file survives. |
| Behaviour that must happen every time | Code: a hook, a validator, a schema, a permission check | A prompt states a policy; it cannot enforce one. |

Order the request so that stable content comes first and volatile content last: tool definitions, then the system prompt, then stable reference material, then the conversation, then anything that changes per request. Most providers cache a prompt by its prefix, so a timestamp or a per-user value near the top makes every request pay full price. For the same reason, keep dynamic text out of tool descriptions and keep the set of examples in the prompt fixed between requests.

## Tool names, descriptions and schemas

A tool definition is a prompt the model reads at the moment it decides what to do, so it deserves the same care as the system prompt.

**Choose tools around tasks.** A tool that does one recognisable job ("schedule a meeting") is easier to select than three that mirror API endpoints. If an engineer on the team could not say with confidence which of two tools applies in a given situation, the model will not manage either: merge them or sharpen the boundary. Overlap between tools hurts selection more than the raw count does. Vendors suggest keeping roughly twenty or fewer loaded at once and deferring the rest behind a search or discovery step; treat the number as a rough guide, since the studies behind such thresholds are weak.

**Name them unambiguously.** Use one term per capability, a shared prefix for related tools, and parameter names that say what the value is (`user_id`, not `user`). Tools whose effect is risky benefit from saying so in the name, for example a `draft_` and `send_` pair instead of a single `email` tool.

**Describe what the model could not guess.** A description should let a new colleague use the tool correctly with nothing else to go on: what it does, when to use it and when a neighbouring tool is the better choice, the format of non-obvious arguments, side effects, and what an error means. Put the rule that matters most first. Length follows from that test; a tool whose schema already makes the usage clear needs a sentence, and a third-party tool with unusual query syntax needs a paragraph.

**Let the schema carry the rules.** An enum, a required field or a structured object makes a wrong call impossible, which is more reliable than a sentence asking the model not to make it. Do not ask the model for arguments the code already knows, and merge tools that are always called in sequence.

**Add an example call only where the schema cannot express the format**, such as a date convention or a query language. Examples of when to call the tool tend to narrow the model's behaviour to the cases shown.

**Do not add a parameter that asks the model to write out its reasoning.** Some current models decline such requests, and it rarely improves the call. Ask for a short justification or the evidence instead.

## Tool results and errors

Whatever a tool returns becomes part of the context, and the model plans its next step from it.

- Return the fields the model will reason with, under names it can read. Resolve opaque identifiers to meaningful ones, and keep an identifier only when a later call needs it.
- Bound the size: paginate, filter and truncate with sensible defaults. When a result is cut, say that it was cut and how to get the rest.
- Write errors for the model. State what went wrong and what to try next, for example "No availability without a product ID; call `search_products` first", instead of a status code or a stack trace.
- When the next step is not obvious from the data, say what it is.
- Content that came from outside (web pages, documents, other users) is data. Keep it inside the tool result, and do not let it be reformatted into something that looks like an instruction from the system or the user.

## Delegation briefs

A model that receives a delegated task usually sees only the brief. It has not read the conversation, the files already opened, or the rules the delegating model is following, so anything missing from the brief is missing from its world. One-line briefs are the most common cause of delegated work that duplicates effort, leaves gaps, or solves an easier problem than the real one.

A brief that works covers:

- **The goal and what it serves.** A bare task differs from a task the recipient can do well because it knows what the result is for.
- **What done looks like.** State the finish line, and when to stop and report instead of continuing.
- **What is already known.** Include what was ruled out and what was tried, so it is not repeated.
- **What makes the task hard.** Name the obvious-but-wrong approach when there is one.
- **Boundaries.** Scope, actions that need confirmation, things not to touch, and an effort budget; models judge poorly how much work a task deserves unless told.
- **Rules that must carry over.** A constraint the delegator is under does not bind the recipient unless the brief restates it.
- **The shape of the answer.** Say what to return and in what order. Ask it to separate what it verified from what it inferred, and to say where it looked when it found nothing.

Treat what comes back as evidence to check, in proportion to what depends on it. Ask for the result in a form that can be checked without redoing the work, such as the counts and sums a total rests on, or the file and line a claim comes from. When the result is large, have the recipient write it to a file and return the path, so detail is not lost in a summary of a summary.

Delegate when the work is independent, parallel, or would flood the main context with material that is only needed once. Keep tightly coupled or sequential work in one context, since every handoff loses state and coordination costs tokens.

For a reviewer or verifier, pass the artifact, the criteria and the means to check, and leave out the author's reasoning so the review is independent. Tell it what counts as a finding: a reviewer asked to find problems will report some even in sound work.

## Skills and instruction files

These rules apply to the text inside skills and always-loaded instruction files. For packaging, frontmatter and distribution of skills, use the `create-skills` skill.

- **The description decides whether the skill loads.** Write it as the conditions for loading: what the skill does, when to use it, and the words a person would use when asking. Put the main use case first, because long descriptions get truncated.
- **Write only what the model would not do by default.** Content that restates default behaviour adds cost without changing anything. The most valuable part of most skills is the list of pitfalls collected from real failures.
- **Match specificity to fragility.** Use prose and judgment where many approaches are valid, and exact commands where an operation is fragile or the sequence matters.
- **Write standing instructions.** A loaded skill stays in context and is not re-read, so "run the tests after each change" works where "run the tests" is done once and forgotten.
- **Put the critical instructions at the top.** After the context is summarised, some harnesses keep only the beginning of a loaded file.
- **Link detail one level deep**, and give each link a condition: "Read `references/payments.md` before any action that moves money" tells the model when to open it, and "see references for more" does not.
- **Keep always-loaded files short.** An instruction file competes with everything else for attention, and adherence falls as it grows. For each line, ask whether removing it would cause a mistake; if not, remove it.
- **Look for contradictions across layers.** A system prompt, a project file and a skill written at different times often disagree, and the model then spends effort reconciling them or picks one arbitrarily.

## Long runs: compaction, handoffs and state

Over a long task the context fills up and is summarised, or a fresh model picks up where another stopped. Summaries lose detail, and the details lost first are constraints and exact values.

- **Keep durable state in files.** A task list, a progress log and the decisions made belong in files the agent reads at the start of a session and updates as it goes, along with an instruction to maintain them.
- **Say what must survive a summary.** A compaction prompt should ask for: the goal and the definition of done; the person's constraints and decisions in close to their own words; the current state; what was tried and why it was set aside; what remains; exact values that would be costly to rediscover (paths, identifiers, commands, error text); the state of any approvals; and work that should not be redone.
- **Write a handoff as an operational briefing.** The test is whether the next model can continue without rediscovering the task. A recap of the conversation fails that test.
- **A summary records that an approval was given; it does not carry the approval.** Have the harness check the record instead of trusting the summary's prose.
- **Tell the model how its context is managed.** If context is compacted automatically, say so, so it does not wrap up early to save space. If nobody is watching the run, say so, so it does not stop to ask a question no one will answer.
- **Make an interrupted run leave something true.** When the output is a report or a file, have the agent write it early with everything marked as not yet done, and update it as work completes, so a run that is cut off does not leave a confident half-result.
- **Ask for claims backed by evidence.** Have the model check each statement in a progress report against something it actually observed in the session, and mark what it could not verify.

## Text injected during a run

Harnesses often add text mid-conversation: reminders, budget counters, messages from the person. Models can mistake this text for an injection attempt, or over-react to it.

- Deliver a person's mid-task message as a user message. Placing it inside a tool result gives it the same standing as untrusted data.
- Keep system notices and the person's words in separate blocks.
- Use reminders sparingly and keep them factual. A notice after every step reads as pressure, and frequent countdowns of remaining budget push models to finish early.
- Append new messages and leave earlier ones unchanged. Rewriting history invalidates caches and, on some models, earlier reasoning.
