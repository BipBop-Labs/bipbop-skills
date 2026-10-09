---
name: best-prompting
description: Mejores prácticas, agnósticas al modelo, para escribir y revisar texto dirigido a un LLM. Úsala siempre que se escriba, edite o revise un system prompt, una descripción de tool, un brief para un subagente, un archivo de instrucciones para agentes o un prompt de compactación, al depurar un prompt que no se comporta como se espera, y al revisar PRs que tocan prompts.
---

# Best prompting

Guidance for writing and reviewing any text a language model will read: system prompts, tool descriptions, delegation briefs, instruction files, and prompts inside a pipeline. It is model-agnostic. It keeps to practices that current vendor guidance agrees on, checked against independent studies where they exist, and where behaviour differs between models or model generations it says so and tells you to settle the question with a test instead of a rule.

The person's explicit instructions and the conventions already used in the repository's prompts take precedence over this skill.

## When to use

Use it when writing a new prompt, editing or reviewing an existing one, diagnosing a prompt that misbehaves, or moving a prompt to a different model.

Other skills cover neighbouring work: `microcopy` for text shown to people in an interface, and `create-skills` for packaging and validating a skill (this skill covers the wording inside one).

## Before editing: check that the prompt is the problem

A failure does not always mean an instruction is missing. Decide which of these it is before touching the text:

- **Missing context.** The model lacked a fact, a definition or the purpose of the task. Supply it.
- **Conflicting instructions.** Two parts of the prompt, or the prompt and another loaded file, disagree. Resolve the conflict; adding a third rule makes it worse.
- **An instruction that over-applies.** An existing rule causes the behaviour. Remove or narrow it.
- **A tool problem.** The tool is missing, badly described, or returns something the model cannot use.
- **Something that needs enforcement.** A rule that must hold every time (a permission, a required format, a safety limit) belongs in code: a schema, a validator, a hook or a permission check. A prompt states a policy and cannot guarantee it.
- **No way to tell.** There are no cases to run, so nobody knows whether a change helped.

When the answer is a tool, a validator or a permission, say so. A recommended change outside the prompt is a valid result of prompt work, and the prompt then carries one sentence of policy so the model can explain the limit.

## Procedure

1. Write down the outcome and how you will recognise a good output, and collect a few inputs to try, including awkward ones.
2. Draft the smallest prompt that fully describes the behaviour you want. Minimal means nothing unnecessary, which is often still long.
3. Run it on the model it will ship on and read the outputs.
4. For each failure, find the cause and fix that. Every instruction in the prompt should trace to a requirement someone stated or a failure you observed.
5. Change one thing at a time and rerun the same inputs.
6. Before finishing, reread the whole prompt for contradictions, duplicated rules and text that no longer earns its place.

When the prompt cannot be run (no access to the model, the tools or the data), replace steps 3 to 5 with a cold read: give the draft and the requirements, without your reasoning, to a fresh reader, and have them walk through a hard case and say where the prompt lets the wrong thing happen. Then say plainly that the prompt is untested and list the cases to run first.

When the prompt depends on a fact you do not have, such as how an approval arrives or what a tool returns, mark it as an assumption for whoever deploys the prompt. An invented fact reads the same as a real one to the model.

For a prompt that will run many times, read `references/testing.md` before step 1.

## Principles

### Write for a capable reader who has none of your context

The model knows nothing about the project, the audience, the quality bar, or what was tried last week unless the prompt says so. A useful test: give the prompt to a competent colleague who has never seen the task and ask whether they could do excellent work without asking questions. The questions they would ask are what the prompt is missing.

Say what the task is for and who will use the result. A model that knows the summary is for an executive deciding whether to fund a project makes better choices throughout than one told only to summarise. Spend the words on the parts where a smart newcomer would go wrong, and leave out what any capable model does well unprompted.

Give the whole task in one place. Requirements revealed a piece at a time over several turns are followed less reliably than the same requirements stated together.

A role line ("you are a senior tax lawyer") is useful for setting tone, register and scope. Studies find it does not make answers more accurate, so it is no substitute for the context above.

### Describe the destination, and script the route only when the route is the requirement

State the outcome, the criteria for success, the constraints, and when to stop. Then let the model choose how to get there. Step-by-step scripts written for weaker models make current ones mechanical and block better approaches.

Match the degree of freedom to how fragile the task is. Where many approaches are valid, give goals and heuristics. Where an operation is fragile, the order matters, or consistency across runs is the point, give exact steps. Smaller models pull in the other direction: the smaller and faster the model, the more it benefits from a longer, more explicit, ordered prompt.

Give stop conditions explicitly. Say what done means, when to stop gathering information, and what to do when the evidence is missing or the task turns out to be infeasible. Without them, models either stop early or keep going past the point of usefulness. Check that the definition of done cannot be met without doing the work: if "not examined" or "could not determine" is an acceptable final answer, say exactly when, or the model will reach for it.

### Give the reason with the rule

"Never use ellipses" is weaker than "the reply is read aloud by a speech engine that cannot pronounce ellipses, so leave them out". The reason lets the model handle the cases the rule did not anticipate, and tells it how much weight the rule deserves. A clause is usually enough; a rule that needs a paragraph of justification is probably a description of a situation, and is better written as one.

### Say each thing once, and make the prompt agree with itself

Contradictions do more damage than gaps. A model that meets two conflicting instructions spends effort reconciling them, picks one unpredictably, or stops to ask. Repetition has a similar cost: a rule stated three times is applied too broadly.

Length has a cost too. Measured adherence falls as the number of instructions grows, and instructions near the start are followed more reliably than later ones, so every rule added weakens the others a little.

- State each instruction once, in the place it applies.
- Among the instructions, put the ones that matter most first. The context that makes them understandable can come before them.
- Put an exception next to the rule it modifies.
- Check that examples obey the rules written around them.
- When several sources of instruction exist (system prompt, loaded files, the person's messages), say which wins, and then remove the conflicts you can find anyway. In tests, models resolve a conflict between the system prompt and the user unreliably even when told the order of priority.

### Calibrate strength

Keep absolute words for true invariants: safety limits, required output fields, actions that must never happen. For judgment calls, write a decision rule that names the consideration ("ask before acting when the action cannot be undone"). Capitals and words like "critical" make a responsive model apply the rule too widely and too rigidly; calm, specific wording works better. If one instruction keeps being missed in testing, strengthen that line alone, since emphasis spread over many lines singles out none of them.

Leave out tips, threats, flattery and emotional appeals. Repeated studies find they have no reliable effect on current models.

### Say what to do, and keep prohibitions narrow

A positive instruction gives the model a target: "write in flowing paragraphs" works better than "do not use bullet points". Broad prohibitions over-apply, because the model follows them to the letter in situations the author did not picture.

When a prohibition is needed, scope it to the specific thing and give the alternative. Naming an unwanted pattern does work when the pattern is concrete and recognisable, such as ending a turn by asking permission for work already requested.

### Assume the instruction will be taken literally

Current models do what the text says. They do not extend a rule from one item to all of them, and they do not infer a request that was not made.

- State the scope: "apply this to every section", when that is what is meant.
- Say whether you want an action or advice. "Can you suggest improvements?" gets suggestions; "improve this function" gets edits.
- Be careful with filters. A reviewer told to report only important issues will find the minor ones and stay silent about them. When coverage matters, ask for everything with a severity attached, and filter in a later step.
- If you want ambition beyond the literal request, ask for it; if you want restraint, say what is out of scope.

### Use examples for what description cannot pin down

Examples are the strongest signal in a prompt, and models imitate them closely, including length, phrasing and incidental details. That makes them the best tool for fixing a format or a voice, and a risky one for conveying judgment, since the model tends to stay near the cases shown.

- Try a clear description first; add examples when the output still misses.
- Use several that differ from each other in meaningful ways, so the common thread is the lesson, and mark them as illustrations.
- Wrap them in tags so they are not read as instructions.
- Keep examples that correct a measured problem and cut the rest.

Whether examples help or constrain depends on the model, so check the output with and without them.

### Separate the kinds of content

Mark instructions, background, input data and examples as different things, with tags or headings used consistently, so that a document's text is never mistaken for an instruction. Prose is the better form for guidance that involves priorities and trade-offs; lists and tables suit reference material the model will look things up in.

Include only the material the task needs. Accuracy drops as context grows, and near-relevant distractors lower it further, so a focused excerpt beats the whole document when you can tell which part matters.

When a long document is included, vendors recommend placing it before the question and the instructions that refer to it; independent tests on recent models have not confirmed a position effect, so check it if it matters. For cost, put content that never changes ahead of content that changes per request, because providers cache prompts by prefix.

### Specify the output

- Name the format, the length, the audience and the order of the content. Concrete shapes ("three short paragraphs, conclusion first") work where adjectives ("concise", "friendly") leave the model guessing.
- For length, say what must be kept and what can go. A bare "be concise" can strip out required content.
- For editing, say what to preserve before asking for improvement.
- Use the platform's structured-output or schema feature for machine-read output, and keep the prompt for what the fields mean. On small models a strict format can lower the quality of the reasoning behind the answer; if that shows up, let the model answer freely and convert to the format in a second step.
- The style of the prompt leaks into the output. A prompt written as bullet fragments tends to get bullet fragments back.
- Do not rely on a default for formatting or verbosity; defaults change between models.

### Let the model reason in its own way

When the model has a built-in reasoning mode, control depth with that setting. "Think step by step" and hand-written thinking steps add little there, cost time, and can make results worse.

With reasoning switched off, asking the model to work through the problem before answering still helps, mainly on maths, logic and other symbolic tasks. In that case the working has to come before the answer: in a structured output, a field for the working placed after the answer field does nothing.

With reasoning switched on, do not also ask for the reasoning as an output field or a tagged section. It adds nothing, and some current models decline such requests. Ask for the evidence, or a short explanation of the decision, when you need to audit a result.

### Give verification something to check against

Asking a model to "double-check your answer" with no new information rarely improves the answer and sometimes makes it worse. Verification works when it brings in an outside signal: running the tests, calling a validator, rendering the page and looking at it, or a review by a model in a fresh context that sees the result without the reasoning that produced it. Name the checks that matter, and say what to do when a check cannot be run.

### Write the authorisation boundary once

How readily a model acts without asking changes with every release, so prompts that push in one direction ("keep going", "always ask first") age badly. State the boundary itself:

- what the model may do without asking, typically reading, searching, and local reversible changes;
- what needs confirmation, typically anything destructive, hard to reverse, visible to other people, or beyond the requested scope;
- who can give that confirmation and how it arrives. In a product, the person in the conversation is often a customer and not the operator, and a message claiming to be staff or to carry an approval is not one;
- what to do when nobody can be asked, as in an unattended run: usually prepare the action as a draft for a person to carry out;
- what to do when the request is ambiguous: make a reasonable assumption and state it, or ask a single narrow question;
- that a question or a description of a problem calls for an answer, and a request for a change calls for the change.

Put this in one place. Repeating "ask first" through a prompt makes the model request approval for safe, expected actions.

### Tell the model about its situation

Models behave differently depending on what they believe about their environment, so tell them what they cannot observe: whether a person is watching or the run is unattended, what the person can and cannot see of the work, whether the context is compacted automatically, what happens to the output next. Give the current date when the task involves recent facts and the platform does not supply it.

### Treat prompt text as policy and code as enforcement

Mark retrieved documents, web content and other people's messages as data, and say that instructions inside them are not to be followed unless the person asks. Then assume this will sometimes fail, and put the real control (permissions, confirmation steps, output validation) in the harness.

## Defaults that change between models

These behaviours differ between vendors and flip between generations of the same model family. Instructions written to compensate for one model's default become harmful on the next. For each, state what you want, then test on the target model.

| Behaviour | How it varies | What to write |
| --- | --- | --- |
| Initiative | Some models over-ask, others act beyond the request | The authorisation boundary above |
| Finishing long tasks | Some stop at a milestone or end on a plan | What done means, and that nobody is available to answer mid-run, if that is true |
| Scope | Some add features, tests and refactors nobody asked for | What is out of scope, and that extras are to be suggested, not done |
| Progress updates | Some narrate every step, others go silent | When to send an update and what it should contain |
| Formatting | Some default to heavy markdown, others to plain prose | The format you need and when structure is appropriate |
| Response length | Varies, and is not reliably controlled by reasoning settings | Length and what to keep, in the prompt |
| Self-verification | Some verify unprompted and over-verify when reminded; others report done without checking | Which outside checks matter and what to do when one cannot run; add reminders only after seeing unverified claims |
| Delegation | Some spawn subagents too readily, others too rarely | When delegation is worth it and when to work directly |
| Tool and search use | Blanket "always use" rules over-trigger; "minimise tool calls" suppresses needed ones | The conditions under which the tool helps |
| Examples | Help some models and narrow others | Test with and without |

When a prompt moves to a new model, start by removing compensations and see what the model does unaided. `references/testing.md` has the procedure.

## Reviewing a prompt

Work through the checks below, then report the findings with the most consequential first. Give each finding as the problem, where it is in the prompt, and the change that fixes it. List separately the questions that block shipping and that only the author can answer. If you did not run the prompt, say so: the findings are then predictions from reading, and any text you propose adding is a draft to test. Include a rewritten prompt when asked for one.

1. **Contradictions** inside the prompt and with other text loaded alongside it.
2. **Missing context**: purpose, audience, quality bar, definition of done, stop conditions, what to do when a tool fails or returns nothing.
3. **Rules that belong in code**, because they must hold every time, and **tools the prompt assumes but the model does not have**.
4. **Over-strength**: capitals, stacked absolutes, the same rule repeated, emphasis on many lines.
5. **Broad prohibitions and unscoped filters** that a literal reader would over-apply.
6. **Scripts where an outcome would do**, and vague adjectives where a concrete shape is needed.
7. **Leftovers** from an earlier model or an earlier version of the task: persistence nudges, verification reminders, formatting bans, instructions for tools that no longer exist.
8. **Examples**: a single one that will be copied wholesale, several that are too alike, or any that disagree with the rules.
9. **Text that does no work**: restated defaults, encouragement, incentives and threats, a role line standing in for real context.
10. **Who can authorise what**, when the people who talk to the model are not the people who run it.

Judge the prompt by its outputs when you can run it. A prompt that reads well and fails its cases is not good, and a plain one that passes them is.

## References

- Read `references/agents-and-tools.md` when the prompt belongs to an agent: it has tools, delegates to other models, loads skills or instruction files, or runs long enough to be compacted. It opens with a list of contents; read the sections that match.
- Read `references/testing.md` when writing or changing a prompt that will run repeatedly, or when changing models.
- Read `references/sources.md` when someone asks where a recommendation comes from, how strong the evidence behind it is, or where sources disagree, and to find the vendor's own page for a specific model. Several recommendations here rest on vendor guidance alone, and that file says which.

## Verification

The work is done when:

- the prompt has been run on the model it will ship on, or the response says plainly that it was not run, why, and what was done instead;
- the outputs that were read are described, with any failure that remains;
- each instruction added or removed is tied to a stated requirement or an observed behaviour, and facts the author did not have are marked as assumptions;
- a final read found no contradictions and no repeated rules.
