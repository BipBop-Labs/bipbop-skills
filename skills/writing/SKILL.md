---
name: writing
description: 'Write text a reader cannot misread: one meaning per word, active voice, simple tenses, one idea per sentence, short sentences, in English and Spanish. Use every time you write text for a person or another agent: chat replies to the user, status updates, reports, findings, PR descriptions, commit messages, code comments, docs, messages, prompts, tool descriptions, and error messages. Also use on request: "simplify this", "make this clearer", "too dense", "STE".'
---

# Writing

Apply these rules to every text you write for someone else, while you write it. Do not write a dense draft and clean it up afterward.

Leave quoted text as it is.
Do not use the rules for marketing or persuasive copy.
Interface text also follows `microcopy`. Text for non-technical readers also follows `simple-writing`.

## The rules

| Rule                        | Do                                                                   | Do not                                                      |
| --------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| One meaning per word        | Pick one verb per action and reuse it every time                     | Rotate "check", "verify", and "confirm" for the same action |
| One part of speech per word | "Apply oil to the valve"                                             | "Oil the valve"                                             |
| Active voice                | "The worker deletes the file."                                       | "The file is deleted."                                      |
| Simple tenses               | "We received the report."                                            | "We have received the report."                              |
| One idea per sentence       | "Open the file. Read line 3."                                        | "Open the file and read line 3, then check it matches."     |
| Sentence length             | 20 words or fewer for instructions, 25 or fewer for descriptions     | Chains of subordinate clauses                               |
| Noun clusters               | 3 words or fewer ("fuel pump valve")                                 | "high pressure fuel pump inlet valve assembly"              |
| No missing words            | Keep the subject, the verb, and the article, even if it reads longer | "Files not backed up will be lost", which hides which files |
| One hedge, at most          | "The client version is probably out of date."                        | "An error may have occurred which could be caused by..."    |
| Paragraphs                  | One topic, 6 sentences or fewer                                      | Multi-topic paragraphs                                      |
| Lists                       | Use a list for 3 or more steps or conditions                         | A sequence buried in one sentence                           |
| Jargon                      | Keep the technical term you need, and define it once                 | Use an internal name the reader has never seen              |

The house style of the project sits on top of these rules and wins where the two disagree.
If the project has no house style, use sentence case and the Oxford comma.
Do not use the em-dash.

## Rule details

- Verb forms: use the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. Use an "-ing" form only inside a technical noun, never as a verb form.
- Passive voice: use it only in descriptive text, and only when the actor is unknown or does not matter to the reader. Never use it in instructions.
- Safety instructions: open the instruction with the command or the condition. Do not put it mid-sentence.

## Spanish

The rules do not change when you write in Spanish.
The language that the reader uses decides the language of the text, and the rules apply to both.
Some rules take a different form in Spanish.
Read `references/spanish.md` before you write Spanish text.

## How to rewrite

1. Read the text once for meaning. Do not start rewriting before you know what it must still say.
2. Go sentence by sentence. Name the rule each sentence breaks.
3. Rewrite the sentence to fix that break. Keep every fact, number, condition, and qualifier.
4. Check the result against the rules again. A rewrite often introduces a new long sentence.

Precision beats brevity.
If a shorter sentence would drop a safety condition, a scope qualifier, or a number, keep the longer sentence and say why.

If the text already follows the rules, say so.
Do not change compliant text.

## Self-check

Before you send the text, read it once and ask:

- Does any sentence run past 25 words?
- Does any sentence carry two instructions?
- Does the same action appear under two different verbs?
- Can a passive sentence name its actor?
- Would a reader who joins here, with no context, know what to do next?

## References

- `references/before-after.md`: worked examples of the rewrite, including agent output.
- `references/spanish.md`: the same rules for Spanish text, with examples.
