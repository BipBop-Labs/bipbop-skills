---
name: best-prompting
description: Mejores prácticas, agnósticas al modelo, para escribir y revisar los prompts de los agentes LLM que construimos en nuestro producto. Úsala cuando escribes, editas o revisas un system prompt, una descripción de tool, un prompt dentro de un pipeline o un brief que un agente del producto envía a sus subagentes. Úsala también cuando depuras un prompt que no se comporta como esperas y cuando revisas PRs que tocan prompts del producto. No es para briefs que un asistente de código (Claude Code, Codex) escribe para sus subagentes, ni para CLAUDE.md o AGENTS.md, ni para skills, ni para prompts de compactación de un asistente de código.
---

# Best prompting

Use this skill to write and review the prompts of the LLM agents in our product.
Where the behavior differs between models, a test settles the question, not a rule.

The explicit instructions of the person win over this skill.
The conventions of the prompts that already exist in the repository also win over this skill.

## When to use

Use this skill for these texts of a product agent:

- a system prompt;
- a tool description;
- a prompt inside a pipeline;
- a brief that a product agent sends to its own subagents.

Use it when you write a new prompt, edit or review a prompt, find why a prompt misbehaves, or move a prompt to a different model.

Do not use it for these texts:

- a brief that a coding assistant (Claude Code, Codex) writes for its own subagents;
- a CLAUDE.md or AGENTS.md file;
- a skill;
- a compaction prompt of a coding assistant.

Text that people see in an interface follows `microcopy`.

## Before you edit: make sure the prompt is the problem

A failure does not always mean that an instruction is missing.
Before you change the text, find which of these causes the failure:

- **Missing context.** The model did not have a fact, a definition, or the purpose of the task. Give it.
- **Conflicting instructions.** Two parts of the prompt disagree, or the prompt and another loaded file disagree. Remove the conflict. A third rule makes it worse.
- **An instruction that over-applies.** A rule that exists causes the behavior. Remove the rule or make it narrower.
- **A tool problem.** The tool is missing, its description is bad, or it returns data that the model cannot use.
- **A rule that needs enforcement.** A rule that must hold every time (a permission, a required format, a safety limit) belongs in code: a schema, a validator, a hook, or a permission check. A prompt states a policy. It cannot guarantee it.
- **No way to tell.** There are no cases to run, so nobody knows if a change helped.

When the fix is a tool, a validator, or a permission, say so.
A change outside the prompt is a valid result of prompt work.
The prompt then gets one sentence of policy, so the model can explain the limit.

## Procedure

1. Write down the outcome and how you recognize a good output. Collect a few inputs to try, and include difficult ones.
2. Write the smallest prompt that fully describes the behavior you want. "Smallest" means nothing unnecessary. That is often still long.
3. Run the prompt on the model that it will ship on. Read the outputs.
4. For each failure, find the cause and fix the cause. Each instruction in the prompt must come from a stated requirement or from a failure that you saw.
5. Change one thing at a time. Run the same inputs again.
6. Before you finish, read the whole prompt again. Look for contradictions, duplicate rules, and text that does no work.

Sometimes you cannot run the prompt, because you have no access to the model, the tools, or the data.
Then replace steps 3 to 5 with a cold read:

1. Give the draft and the requirements to a fresh reader. Do not give your reasoning.
2. Tell the reader to go through a hard case and to say where the prompt lets the wrong thing happen.
3. Say clearly that the prompt is not tested. List the cases to run first.

The prompt can depend on a fact that you do not have, for example how an approval arrives or what a tool returns.
Mark that fact as an assumption for the person who deploys the prompt.
To the model, an invented fact reads the same as a real one.

For a prompt that will run many times, read `references/testing.md` before step 1.

## Principles

### Write for a capable reader who has none of your context

The model knows nothing about the product, the audience, the quality bar, or what the team tried last week, unless the prompt says it.
Use this test: give the prompt to a competent colleague who never saw the task.
Ask if that colleague could do excellent work with no questions.
The questions that the colleague would ask show what the prompt is missing.

Say what the task is for and who will use the result.
Tell the model that the summary is for an executive who decides whether to fund a project. Then it makes better choices than a model told only to "summarize".
Spend words where a smart newcomer would go wrong.
Leave out what a capable model does well with no prompt.

Give the whole task in one place.
The model obeys requirements given together more reliably than the same requirements given one at a time over several turns.

A role line ("you are a senior tax lawyer") sets tone, register, and scope.
It does not make the answers more accurate, and it does not replace the context above.

### Describe the destination. Script the route only when the route is the requirement

State the outcome, the criteria for success, the constraints, and when to stop.
Then let the model choose how to get there.
Step-by-step scripts make current models mechanical and block better approaches.

Match the freedom to how fragile the task is:

- When many approaches are valid, give goals and heuristics.
- When an operation is fragile, the order matters, or consistency across runs is the point, give exact steps.
- Smaller models need the opposite. The smaller and faster the model, the more it gains from a longer, explicit, ordered prompt.

Give explicit stop conditions.
Say what "done" means and when to stop the search for information.
Say what to do when the evidence is missing or the task is not possible.
With no stop conditions, models stop too early or continue past the point where the work is useful.
Make sure that the model cannot meet the definition of done without the work.
If "not examined" or "could not determine" is an acceptable final answer, say exactly when. If you do not, the model will use it.

### Give the reason with the rule

"Never use ellipses" is weaker than "a speech engine reads the reply aloud and cannot pronounce ellipses, so leave them out".
The reason lets the model handle cases that the rule did not expect.
The reason also tells the model how much weight the rule has.
A clause is usually enough.
If a rule needs a paragraph of reasons, it probably describes a situation. Write it as a description of that situation.

### Say each thing once, and make the prompt agree with itself

Contradictions do more damage than gaps.
The model applies a rule stated three times too broadly.
Each new rule makes the other rules a little weaker.
The model obeys early instructions more reliably than late ones.

- State each instruction once, in the place where it applies.
- Put the most important instructions first. The context that explains them can come before them.
- Put an exception next to the rule that it changes.
- Make sure that the examples obey the rules around them.
- When there are several sources of instruction (the system prompt, loaded files, the messages of the person), say which source wins. Then remove the conflicts that you find. Models resolve such conflicts unreliably, even when the prompt gives the order.

### Calibrate strength

Use absolute words only for true invariants: safety limits, required output fields, and actions that must never happen.
For a judgment call, write a decision rule that names the consideration: "ask before you act when the action cannot be undone".
Capitals and words like "critical" make a responsive model apply the rule too widely and too rigidly.
Calm, specific words work better.
If the model misses one instruction again and again in tests, make that one line stronger.
Emphasis on many lines singles out none of them.

Leave out tips, threats, flattery, and emotional appeals. They have no reliable effect.

### Say what to do, and keep prohibitions narrow

A positive instruction gives the model a target.
"Write in flowing paragraphs" works better than "do not use bullet points".
A broad prohibition over-applies, because the model obeys it to the letter in situations that the author did not imagine.

When you need a prohibition, limit it to the specific thing and give the alternative.
A named unwanted pattern does work when the pattern is concrete and easy to recognize. An example: the model ends a turn with a request for permission to do work that the person already asked for.

### Expect the model to read the instruction literally

Current models do what the text says.
They do not extend a rule from one item to all items.
They do not infer a request that nobody made.

- State the scope: "apply this to every section", when that is what you mean.
- Say if you want an action or advice. "Can you suggest improvements?" gets suggestions. "Improve this function" gets edits.
- Be careful with filters. Tell a reviewer to report only important issues, and it finds the minor ones but does not report them. When coverage matters, ask for all issues with a severity, and filter in a later step.
- If you want more than the literal request, ask for it. If you want restraint, say what is out of scope.

### Use examples for what a description cannot fix

Models copy examples closely, including length, phrasing, and incidental details.
Use examples to fix a format or a voice.
Examples are risky when they must teach judgment, because the model stays near the cases shown.

- Try a clear description first. Add examples when the output still misses.
- Use several examples that differ from each other in ways that matter, so that the common part is the lesson. Mark them as illustrations.
- Put the examples in tags, so the model does not read them as instructions.
- Keep the examples that correct a measured problem. Cut the others.

Examples help some models and constrain others.
Compare the output with and without them.

### Separate the kinds of content

Mark instructions, background, input data, and examples as different things.
Use tags or headings, and use them consistently.
Then the model never takes the text of a document for an instruction.
Prose is the better form for guidance with priorities and trade-offs.
Lists and tables suit reference material that the model looks things up in.

Include only the material that the task needs.
Accuracy decreases as the context grows, and near-relevant distractors decrease it more.
When you can tell which part of a document matters, give that excerpt, not the whole document.

Put a long document before the question and before the instructions that refer to it.
If the position matters, test it.
For cost, put the content that never changes before the content that changes per request. Providers cache prompts by prefix.

### Specify the output

- Name the format, the length, the audience, and the order of the content. A concrete shape ("three short paragraphs, conclusion first") works. Adjectives ("concise", "friendly") leave the model to guess.
- For length, say what the model must keep and what it can remove. A bare "be concise" can remove required content.
- For an edit, say what to keep before you ask for improvements.
- For output that code reads, use the structured-output or schema feature of the platform. Use the prompt to say what the fields mean. On small models, a strict format can lower the quality of the reasoning behind the answer. If you see that, let the model answer freely and convert the answer to the format in a second step.
- The style of the prompt goes into the output. A prompt written as bullet fragments tends to get bullet fragments back.
- Do not depend on a default for format or verbosity. Defaults change between models.

### Let the model reason in its own way

When the model has a built-in reasoning mode, use that setting to control depth.
In that mode, "think step by step" and hand-written thinking steps add little, cost time, and can make results worse.

When reasoning is off, an instruction to work through the problem before the answer still helps, mainly on maths, logic, and other symbolic tasks.
Then the working must come before the answer.
In a structured output, a field for the working after the answer field does nothing.

When reasoning is on, do not also ask for the reasoning as an output field or a tagged section.
It adds nothing, and some current models refuse such requests.
When you must audit a result, ask for the evidence or a short explanation of the decision.

### Give the verification something to check against

"Double-check your answer" with no new information rarely improves the answer, and sometimes makes it worse.
Verification works when it brings in an outside signal. Examples:

- the model runs the tests;
- the model calls a validator;
- the model renders the page and looks at it;
- a model in a fresh context reviews the result without the reasoning that produced it.

Name the checks that matter.
Say what to do when the model cannot run a check.

### Write the authorization boundary once

Do not write prompts that push in one direction ("keep going", "always ask first"). That default changes with each release.
State the boundary itself:

- what the model can do without a question, usually read, search, and make local changes that can be undone;
- what needs confirmation, usually any action that destroys data, is hard to undo, is visible to other people, or goes past the requested scope;
- who can give that confirmation and how it arrives. In a product, the person in the conversation is often a customer and not the operator. A message that says it is from staff or that it carries an approval is not an approval;
- what to do when nobody can answer, as in an unattended run. Usually the model prepares the action as a draft for a person to do;
- what to do when the request is ambiguous: make a reasonable assumption and state it, or ask one narrow question;
- that a question or a description of a problem gets an answer, and a request for a change gets the change.

Put the boundary in one place.
If the prompt repeats "ask first" in many places, the model asks for approval of safe, expected actions.

### Tell the model about its situation

Models behave differently according to what they believe about their environment.
Tell them what they cannot observe:

- whether a person watches the run or the run is unattended;
- what the person can see of the work and what the person cannot see;
- whether the harness compacts the context automatically;
- what happens to the output next.

When the task involves recent facts and the platform does not supply the date, give the current date.

### Prompt text is policy. Code is enforcement

Mark retrieved documents, web content, and messages from other people as data.
Say that the model must not obey instructions inside them unless the person asks.
Then expect this to fail sometimes, and put the real control in the harness: permissions, confirmation steps, and output validation.

## Defaults that change between models

These behaviors differ between vendors.
They also change between generations of the same model family.
An instruction that compensates for the default of one model becomes harmful on the next model.
For each behavior, state what you want, then test on the target model.

| Behavior | How it varies | What to write |
| --- | --- | --- |
| Initiative | Some models ask too much, others act beyond the request | The authorization boundary above |
| Long tasks to the end | Some stop at a milestone or end on a plan | What "done" means, and that nobody can answer during the run, if that is true |
| Scope | Some add features, tests, and refactors that nobody asked for | What is out of scope, and that the model suggests extras but does not do them |
| Progress updates | Some report each step, others say nothing | When to send an update and what it contains |
| Format | Some use heavy markdown by default, others plain prose | The format you need and when structure is correct |
| Response length | Varies. Reasoning settings do not control it reliably | The length and what to keep, in the prompt |
| Self-verification | Some verify with no prompt and verify too much when reminded. Others report "done" with no check | Which outside checks matter and what to do when one cannot run. Add reminders only after you see claims with no verification |
| Delegation | Some start subagents too readily, others too rarely | When delegation is worth it and when to do the work directly |
| Tool and search use | A blanket "always use" rule triggers too often. "Minimize tool calls" suppresses calls that the task needs | The conditions in which the tool helps |
| Examples | Help some models and narrow others | Test with and without them |

When a prompt moves to a new model, first remove the compensations and see what the model does with no help.
`references/testing.md` has the procedure.

## Review a prompt

Do the checks below.
Then report the findings, the most consequential first.
For each finding, give the problem, its location in the prompt, and the change that fixes it.
List separately the questions that block the release and that only the author can answer.
If you did not run the prompt, say so. The findings are then predictions from a reading, and any text that you propose to add is a draft to test.
Include a rewritten prompt when the person asks for one.

1. **Contradictions** inside the prompt, and with other text loaded with it.
2. **Missing context**: purpose, audience, quality bar, definition of done, stop conditions, and what to do when a tool fails or returns nothing.
3. **Rules that belong in code**, because they must hold every time. Also **tools that the prompt expects but the model does not have**.
4. **Too much strength**: capitals, stacked absolutes, the same rule repeated, emphasis on many lines.
5. **Broad prohibitions and filters with no scope** that a literal reader would over-apply.
6. **Scripts where an outcome is enough**, and vague adjectives where the prompt needs a concrete shape.
7. **Leftovers** from an earlier model or an earlier version of the task: persistence nudges, verification reminders, format bans, and instructions for tools that no longer exist.
8. **Examples**: one example that the model will copy as a whole, several that are too similar, or any that disagree with the rules.
9. **Text that does no work**: restated defaults, encouragement, incentives and threats, and a role line in place of real context.
10. **Who can authorize what**, when the people who talk to the model are not the people who run it.

When you can run the prompt, judge it by its outputs.
A prompt that reads well and fails its cases is not good. A plain prompt that passes them is good.

## References

- Read `references/agents-and-tools.md` when the prompt belongs to an agent that has tools, delegates to subagents, loads files on demand, or runs long enough for the harness to compact its context. The file starts with a list of contents. Read the sections that apply.
- Read `references/testing.md` when you write or change a prompt that will run many times, or when you change models.

## Verification

The work is done when:

- you ran the prompt on the model that it will ship on, or the response says clearly that you did not run it, why, and what you did instead;
- the response describes the outputs that you read, with any failure that remains;
- each instruction that you added or removed comes from a stated requirement or a behavior that you saw, and the facts that the author did not have are marked as assumptions;
- a final read found no contradictions and no repeated rules.
