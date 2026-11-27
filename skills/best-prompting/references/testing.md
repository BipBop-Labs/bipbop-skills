# Test and improve a prompt

Read this file when a prompt will run more than a few times, when you change a prompt that already works, or when you move a prompt to a different model.

## Define success before you write the prompt

Write down what a good output is, in terms that two people would judge the same way.
"Answers correctly and politely" leaves the edge cases open.
"Cites the policy clause it relied on, offers the refund only inside the 30-day window, and hands off to a person when the order is not found" is a criterion that you can check.
Most prompts need several criteria at the same time: correctness, format, tone, latency, and cost.

## Build a small set of cases

Twenty to fifty cases are enough to start. Early changes to a prompt usually move the results by amounts that you can see at that size.
Add cases when the effects that you measure become smaller.

- Take cases from real use first: transcripts, bug reports, support tickets, and the checks that a person already does by hand before a release.
- Pair each case where a behavior must occur with a similar case where it must not occur: act and ask, answer and decline, load a file and skip it. A set with only one side pushes the prompt to do that thing always.
- Include inputs that are long, messy, or contradictory. Clean cases make the quality look better than it is.
- Choose a hard case only when a person can explain why it is hard. A collection of all the cases that the current model fails records the quirks of that model and says little about the task.
- Keep a held-out part that nobody reads while they edit the prompt.

## Grade the outputs

- Use checks in code when the criterion allows it (exact fields, a valid schema, a test suite that passes). Use a model as judge for what code cannot check, and compare a sample of its verdicts with the verdicts of a person.
- Grade the result and leave the route free, unless a specific route is a requirement. A required fixed sequence of tool calls penalizes valid solutions.
- Give a judge model a rubric of claims that it can check. Let it reason before the verdict. Allow the answer "cannot tell". When possible, use a different model from the model under test. Pass or fail and side-by-side comparison are more stable than numeric scales.
- Run each case several times. Decide before the run whether one success in several runs is enough, or whether every run must pass.
- When a case fails on every run, suspect the case or the grader before the prompt.

## Read the outputs

Scores tell you that something changed. Transcripts tell you what changed.
After each round, read a sample of full outputs, including outputs that passed.
For agents, read the tool calls and the final message.
Some patterns show only there: an answer that is right for the wrong reason, a rule applied where it does not apply, or a phrase from the prompt that the model repeats.

When an output is wrong, find the sentence in the prompt that produced it.
Ask the model which instruction caused its behavior. This often finds the cause faster than a guess. Its answer is a lead: check it against the prompt.

## Improve without overfitting

- Change one thing per round and run the same cases again. Then you know which change caused the effect.
- Fix the cause of a failure. If the model did not have a piece of context, add the context. A patch that names the failing input teaches the model about that input only. Never paste failing cases into the prompt as examples.
- Rewrite the section that caused a failure. Do not add a new rule below it. Added rules accumulate and start to contradict each other.
- Ignore differences that are smaller than the variation from run to run.
- When the visible cases improve and the held-out cases do not, the last change fitted the cases. Revert it.
- When progress stops, stop the edits and sort the remaining failures by cause. Some failures are ambiguous cases, grader errors, or variance.
- Keep the cases next to the prompt. Run them again each time the prompt, the tools, or the model change.

## Remove before you add

Before you add a rule to fix a failure, find out if an instruction that exists causes the failure.
Remove one group of instructions at a time and run the cases again.
If you remove all of them at once, you cannot tell which parts mattered.

## Change models

1. Run the prompt with no change on the new model. Read the outputs.
2. First look for instructions that now over-apply. Usually these are persistence nudges, emphasis, verification reminders, format prohibitions, and step-by-step scripts.
3. Remove them one group at a time. Run the cases again after each group.
4. For each regression that remains, add the smallest instruction that fixes it.
5. Test every model that the prompt will run on. A prompt tuned on a large model often needs more explicit structure on a small model.

To select a model, first run all candidate models on the same prompt.
Only then tune the prompt for each model, on cases that are separate from the cases that you use to report the result.
