# Prompts for product agents: placement, tools, delegation, long runs

Read this file when the prompt belongs to a product agent that has tools, delegates to subagents, loads files on demand, or runs long enough for the harness to summarize its context.
The principles in `SKILL.md` still apply. This file covers what is specific to agents.

## Contents

- [Where each piece of text belongs](#where-each-piece-of-text-belongs)
- [Tool names, descriptions, and schemas](#tool-names-descriptions-and-schemas)
- [Tool results and errors](#tool-results-and-errors)
- [Delegation briefs](#delegation-briefs)
- [Files the agent loads on demand](#files-the-agent-loads-on-demand)
- [Long runs: compaction, handoffs, and state](#long-runs-compaction-handoffs-and-state)
- [Text that the harness adds during a run](#text-that-the-harness-adds-during-a-run)

## Where each piece of text belongs

An agent reads several layers of text.
A rule in the wrong layer costs tokens on each request, or is missing when the agent needs it.

| Content | Where it goes | Why |
| --- | --- | --- |
| What the product is, who uses it, what the agent is for, tone, the authorization policy | System prompt | Nearly every request needs it. |
| Safety, legal, and brand constraints | System prompt, at any frequency | They must be present before the first action. A load on demand can fail. |
| Guidance for about a third of the requests or more | System prompt | A load on demand would cost an extra turn most of the time. |
| Procedures and knowledge for a minority of the requests | A file that the agent loads on demand, with a description that says when to load it | Text in the system prompt that the agent rarely needs dilutes the rest, and each request pays for it. |
| How and when to use one specific tool | The description of that tool | The guidance travels with the tool and has no duplicate. |
| Policy across tools: order, choice between similar tools, whether an action is allowed and who approves it | System prompt | No single description owns it. The tool description states the facts that make the policy matter (it sends immediately, it cannot be undone). The rule stays in the system prompt, so the two cannot drift apart. |
| Live state: time, current mode, a file that changed, the budget that remains | A short factual message added to the end of the conversation | A change to the system prompt during the run discards the cached prefix, and can confuse the model about what changed. |
| Plans, task lists, approvals, progress | A file or store that the agent reads and updates | The harness summarizes the context and the detail is lost. A file survives. |
| Behavior that must occur every time | Code: a hook, a validator, a schema, a permission check | A prompt states a policy. It cannot enforce one. |

Put the stable content of the request first and the volatile content last, in this order:

1. tool definitions;
2. the system prompt;
3. stable reference material;
4. the conversation;
5. the content that changes per request.

Most providers cache a prompt by its prefix.
A timestamp or a value per user near the top makes each request pay full price.
For the same reason, keep dynamic text out of tool descriptions, and keep the same set of examples in the prompt for all requests.

## Tool names, descriptions, and schemas

The model reads a tool definition at the moment it decides what to do.
Thus a tool definition is a prompt, and it needs the same care as the system prompt.

**Design tools around tasks.**
The model selects a tool that does one recognizable job ("schedule a meeting") more easily than three tools that copy API endpoints.
If an engineer on the team cannot say with confidence which of two tools applies in a situation, the model cannot either. Merge the two tools or make the boundary sharper.
Overlap between tools hurts selection more than the number of tools.
Keep about twenty tools or fewer loaded at one time, and put the rest behind a search or discovery step. The number is a rough guide.

**Give tools names with one meaning.**
Use one term per capability, a shared prefix for related tools, and parameter names that say what the value is (`user_id`, not `user`).
When the effect of a tool is risky, say so in the name. For example, use a `draft_` and `send_` pair, not a single `email` tool.

**Describe what the model cannot guess.**
A description must let a new colleague use the tool correctly with nothing else. Give:

- what the tool does;
- when to use it, and when a similar tool is the better choice;
- the format of arguments that are not obvious;
- side effects;
- what an error means.

Put the most important rule first.
The length comes from that test. A tool with a schema that already makes the use clear needs one sentence. A third-party tool with an unusual query syntax needs a paragraph.

**Let the schema carry the rules.**
An enum, a required field, or a structured object makes a wrong call impossible. That is more reliable than a sentence that tells the model not to make the call.
Do not ask the model for arguments that the code already knows.
Merge tools that the model always calls in sequence.

**Add an example call only where the schema cannot express the format**, for example a date convention or a query language.
Examples of when to call the tool tend to narrow the behavior of the model to the cases shown.

**Do not add a parameter that asks the model to write out its reasoning.**
Some current models refuse such requests, and the parameter rarely improves the call.
Ask for a short justification or the evidence.

## Tool results and errors

All that a tool returns becomes part of the context, and the model plans its next step from it.

- Return the fields that the model reasons with, under names that it can read. Replace opaque identifiers with meaningful ones. Keep an identifier only when a later call needs it.
- Limit the size: paginate, filter, and truncate with sensible defaults. When the tool cuts a result, say that it cut the result and how to get the rest.
- Write errors for the model. State what went wrong and what to try next, for example "No availability without a product ID; call `search_products` first". Do not return only a status code or a stack trace.
- When the data does not make the next step obvious, say what the next step is.
- Content from outside (web pages, documents, other users) is data. Keep it inside the tool result. Do not let the harness format it as something that looks like an instruction from the system or the user.

## Delegation briefs

This section is for the briefs that a product agent sends to its own subagents.

A subagent that gets a delegated task usually sees only the brief.
It did not read the conversation, the files that the delegator opened, or the rules that the delegator obeys.
So a fact that is missing from the brief is missing from its world.
One-line briefs are the most frequent cause of delegated work that repeats effort, leaves gaps, or solves an easier problem than the real one.

A brief that works covers these items:

- **The goal and what it serves.** A subagent that knows what the result is for does the task better than a subagent that gets a bare task.
- **What "done" looks like.** State the finish line. Say when to stop and report instead of continue.
- **What is already known.** Include what the delegator ruled out and what it tried, so the subagent does not repeat it.
- **What makes the task hard.** Name the approach that looks right but is wrong, when there is one.
- **Boundaries.** Give the scope, the actions that need confirmation, the things not to touch, and an effort budget. Models judge badly how much work a task deserves unless the brief tells them.
- **Rules that must carry over.** A constraint on the delegator does not bind the subagent unless the brief states it again.
- **The shape of the answer.** Say what to return and in what order. Tell the subagent to separate what it verified from what it inferred, and to say where it looked when it found nothing.

Treat the result as evidence to check, in proportion to what depends on it.
Ask for the result in a form that you can check without the work again. Examples: the counts and sums under a total, or the file and line that a claim comes from.
When the result is large, tell the subagent to write it to a file and return the path. Then no detail is lost in a summary of a summary.

Delegate when the work is independent or parallel, or when it would fill the main context with material that the agent needs only once.
Keep tightly coupled or sequential work in one context. Each handoff loses state, and coordination costs tokens.

For a reviewer or a verifier, give the artifact, the criteria, and the means to check.
Do not give the reasoning of the author, so the review is independent.
Tell the reviewer what counts as a finding. A reviewer told to find problems reports some, even in sound work.

## Files the agent loads on demand

These rules apply to the text of a file that a product agent loads when it needs it.

- **The description decides whether the agent loads the file.** Write it as the conditions to load: what the file does, when to use it, and the words that a person uses to ask for it. Put the main use case first, because the harness can truncate a long description.
- **Write only what the model would not do by default.** Content that states default behavior again adds cost and changes nothing. The most valuable part of most such files is the list of pitfalls from real failures.
- **Match how specific the text is to how fragile the task is.** Use prose and judgment where many approaches are valid. Use exact commands where an operation is fragile or the sequence matters.
- **Write standing instructions.** A loaded file stays in context and the model does not read it again. "Run the tests after each change" works. "Run the tests" occurs once and the model forgets it.
- **Put the critical instructions at the top.** After the harness summarizes the context, some harnesses keep only the start of a loaded file.
- **Link detail one level deep, and give each link a condition.** "Read `references/payments.md` before any action that moves money" tells the model when to open the file. "See references for more" does not.
- **Look for contradictions across layers.** A system prompt and a loaded file written at different times often disagree. The model then spends effort to reconcile them, or picks one at random.

## Long runs: compaction, handoffs, and state

Summaries lose detail. Constraints and exact values go first.

- **Keep durable state in files.** A task list, a progress log, and the decisions belong in files. The agent reads them at the start of a session and updates them as it works. Tell the agent to keep them current.
- **Say what must survive a summary.** A compaction prompt must ask for:
  - the goal and the definition of done;
  - the constraints and decisions of the person, close to the words of the person;
  - the current state;
  - what the agent tried and why it stopped that approach;
  - what remains;
  - exact values that are costly to find again (paths, identifiers, commands, error text);
  - the state of each approval;
  - work that the agent must not do again.
- **Write a handoff as an operational briefing.** The test: can the next model continue without the need to find the task again? A recap of the conversation fails that test.
- **A summary records that a person gave an approval. It does not carry the approval.** Make the harness check the record. Do not trust the prose of the summary.
- **Tell the model how the harness manages its context.** If the harness compacts the context automatically, say so. Then the model does not end early to save space. If nobody watches the run, say so. Then the model does not stop to ask a question that nobody will answer.
- **Make an interrupted run leave something true.** When the output is a report or a file, tell the agent to write it early, with all items marked as not done. The agent updates it as work completes. Then a run that stops early does not leave a confident half-result.
- **Ask for claims with evidence.** Tell the model to compare each statement in a progress report with something that it observed in the session. Tell it to mark what it could not verify.

## Text that the harness adds during a run

Harnesses often add text during the conversation: reminders, budget counters, messages from the person.
Models can take this text for an injection attempt, or react to it too strongly.

- Send a message that the person writes during the task as a user message. Inside a tool result, it has the same standing as untrusted data.
- Keep system notices and the words of the person in separate blocks.
- Use few reminders and keep them factual. A notice after each step reads as pressure. Frequent countdowns of the remaining budget push models to finish early.
- Add new messages at the end and do not change earlier ones. A change to the history invalidates caches and, on some models, earlier reasoning.
