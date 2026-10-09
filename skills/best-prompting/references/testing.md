# Testing and iterating on a prompt

Read this when a prompt will run more than a handful of times, when changing a prompt that already works, or when moving a prompt to a different model. A prompt is a hypothesis about how a model will behave, and the only evidence is what the model produces.

## Define success before drafting

Write down what a good output is in terms two people would judge the same way. "Answers correctly and politely" leaves the edge cases open; "cites the policy clause it relied on, offers the refund only inside the 30-day window, and hands off to a person when the order is not found" can be checked. Most prompts need several criteria at once (correctness, format, tone, latency, cost), and writing them down often shows that the team does not yet agree on what it wants.

## Build a small set of cases

Twenty to fifty cases are enough to start; early prompt changes usually move results by amounts visible at that size. Grow the set when the effects being measured get smaller.

- Draw cases from real use first: transcripts, bug reports, support tickets, the things already checked by hand before a release.
- Pair every case where a behaviour should happen with a nearby case where it should not: act and ask, answer and decline, load a skill and skip it. A set with only one side optimises the prompt toward doing that thing always.
- Include inputs that are long, messy or contradictory, since clean cases overstate quality.
- Choose hard cases because a person can explain why they are hard. Collecting whatever the current model fails records that model's quirks and says little about the task.
- Keep a held-out part that is never read while editing the prompt.

## Grade outputs

- Prefer checks in code where the criterion allows it (exact fields, valid schema, a test suite passing). Use a model as judge for what code cannot check, and compare a sample of its verdicts with a person's.
- Grade the result and leave the route free, unless a specific route is itself a requirement. Requiring a fixed sequence of tool calls penalises valid solutions.
- Give a judging model a rubric made of checkable claims, let it reason before the verdict, allow it to answer "cannot tell", and use a different model from the one under test where possible. Pass or fail and side-by-side comparison are more stable than numeric scales.
- Run each case several times. Decide beforehand whether one success in several is enough or whether every run must pass.
- When a case fails on every run, suspect the case or the grader before the prompt.

## Read the outputs

Scores say that something changed; transcripts say what. Read a sample of full outputs after every round, including ones that passed, and for agents read the tool calls as well as the final message. Patterns such as an answer that is right for the wrong reason, a rule applied where it should not be, or a phrase from the prompt echoed back only show up there.

When an output is wrong, find the sentence in the prompt that produced it. Asking the model which instruction led to its behaviour often locates the cause faster than guessing, though its account is a lead to verify against the prompt.

## Iterate without overfitting

- Change one thing per round and rerun the same cases, so the effect can be attributed.
- Fix the cause of a failure. If the model lacked a piece of context, add the context; a patch that names the failing input teaches the model about that input only. Never paste failing cases into the prompt as examples.
- Prefer rewriting the section that caused a failure to appending a new rule beneath it. Appended rules accumulate and start to contradict each other.
- Ignore differences smaller than the run-to-run variation.
- When the visible cases improve and the held-out cases do not, the last change fitted the cases. Revert it.
- When progress stalls, stop editing and sort the remaining failures by cause. Some will be ambiguous cases, grader errors or variance.
- Keep the cases next to the prompt and rerun them whenever the prompt, the tools or the model change.

## Remove before adding

Prompts collect instructions written to compensate for a model that has since been replaced, and those instructions keep their cost after their reason is gone. Before adding a rule to fix a failure, check whether an existing instruction causes it. Remove one group of instructions at a time and rerun the cases; removing everything at once makes it impossible to tell which parts mattered.

## Changing models

1. Run the existing prompt unchanged on the new model and read the outputs.
2. Look first for instructions that now over-apply: persistence nudges, emphasis, verification reminders, formatting prohibitions and step-by-step scripts are the usual ones.
3. Remove them one group at a time, rerunning the cases after each.
4. Add the smallest instruction that fixes each regression that remains.
5. Test every model the prompt will run on. A prompt tuned on a large model often needs more explicit structure on a small one.

When comparing models for selection, run them first on the same prompt, and only then tune the prompt per model on cases kept apart from the ones used to report the result.
