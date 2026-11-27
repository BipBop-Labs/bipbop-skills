---
name: simple-writing
description: "Write and rewrite text so that a reader with no context, no patience, and no technical background understands it on the first read. Two levels: plain language (the default) and easy read (maximum simplicity, for readers who struggle with text). Use it when a message must reach non-technical users: client emails, release notes for non-developers, instructions for support or admin staff, in-app copy, error messages, and onboarding docs. Also use it on request: \"make this simpler\", \"explain it like they have no idea\", \"lenguaje simple\", \"lectura fácil\", \"escríbelo para que lo entiendan\", \"hazlo más corto y claro\". Also use it every time you write a message that a person reads: Discord or Slack messages, emails, PR and issue comments, and replies to other developers. Works in English and Spanish."
---

# Simple writing

Change the text so that a tired, distracted, non-expert reader understands it on the first read.
Make the text shorter only so that the reader understands it, not for its own sake.

The skill has two levels. Pick one before you write:

| Level | For | Sentence length | Look |
| --- | --- | --- | --- |
| **Plain language** (default) | Any non-technical reader: clients, staff, users | 15-20 words average | Normal prose, short paragraphs |
| **Easy read** | Readers who struggle with text, high stress, or a second language | One idea per sentence, ideally one line | Lots of white space, headings, numbered steps |

If you do not know which level to use, ask.
If you cannot ask, write plain language and offer the easy read version.

## Messages to people

Use this skill every time you write a message that a person reads, not only when someone asks for a rewrite.
That covers Discord and Slack messages, emails, PR and issue comments, and replies to another developer.
Apply the rules while you write the message.

- Use the plain language level.
- Write in the language of the channel or of the person you answer.
- When the reader is a developer, keep the technical terms that the developer already uses (file names, commands, tool names, error text). Do not explain these terms. Every other rule still applies.
- A technical artifact (a PR description, a commit message, a report, a prompt) follows `writing`. A message that carries technical detail follows both skills.

## The rules

The two levels share these rules. Easy read applies them more strictly.

1. **Answer first.** Put the thing that the reader must do in the first paragraph. Put reasons, context, and caveats after it.
2. **One idea per sentence.** If an "and" joins two ideas in a sentence, split the sentence.
3. **Short sentences.** Plain language: 15-20 words on average. Easy read: fewer than 15 words, and each sentence starts on its own line.
4. **Everyday words.** Say *send*, not *submit*. Say *change*, not *modify*. Say *fix*, not *remediate*. Keep a technical term only if the reader already uses it, and explain it once.
5. **Active voice, real subject.** Write "You change the RUT", not "the RUT must be changed". The reader must know **who does what**.
6. **Present tense.** "The email arrives" is better than "the email will have been sent".
7. **Say it positively.** "Reply to us" is better than "do not fail to notify us". Never use two negatives in one sentence.
8. **Steps as a numbered list.** Write each thing that the reader must *do* as a numbered step (1, 2, 3). Use one action per step, in the order that the actions happen.
9. **Repeat what matters.** Repeat the key action at the end.
10. **No irony, no metaphor, no idioms.**
11. **Concrete over abstract.** "Next Tuesday" is better than "in the coming days". "The green button that says Send" is better than "the corresponding control".
12. **Numbers as digits.** Write "3 points", not "three points".

## What NOT to do

- **Do not talk down to the reader.** Never write "this is very easy", "as we already explained", or "just do X". Use simple words and an adult tone. If the text implies that the reader is slow, the text fails, even if every sentence is short.
- **Do not delete information.** To simplify, change the order and the words. Do not drop the inconvenient parts. If a part matters legally or operationally, keep it. Move it to its own short sentence, in plain words.
- **Do not start with the refusal or the constraint.** "We can't do X, because..." tells the reader *we won't help*. Start with what happens now. Then give the reason.
- **Do not invent certainty.** Simple text is not absolute text. If a thing is not decided, say "we don't know yet" in short words.

## How to rewrite

1. **Read the original and write down the one action** that the reader must take. If there is no action, write down the one fact that the reader must remember. Everything else is support.
2. **Write the opening with the answer first**: what happens now, or what the reader must do.
3. **Split every sentence until it has one idea.** Cut every word that carries no meaning: "in order to" → "to", "at this point in time" → "now", "we would like to inform you that" → delete.
4. **Write the how-to as numbered steps.**
5. **Move the reasons to the end**, in one or two short sentences.
6. **Read the text again as the reader.** Find each place where the reader can stop and think "what does that mean?". Only this problem matters. Fix it and stop.

Length check: if the rewrite is longer than the original, you explained instead of simplified.
Go back to step 1.

## Spanish (lectura fácil)

Use the same rules, and add these rules for Spanish:

- **Tuteo o usted, uno solo.** Elige uno según el contexto. No los mezcles en el mismo texto.
- **Sin gerundios.** Escribe "Cuando cambian la clave", no "cambiando la clave".
- **Sin voz pasiva ni impersonal con "se".** Escribe "Ustedes cambian el RUT", no "se debe modificar el RUT".
- **Verbos simples, en presente.** Escribe "Les llega un correo", no "les será enviado un correo".
- **Frases de una línea.** Si una frase ocupa dos líneas, la frase tiene dos ideas.
- **Sin anglicismos ni siglas sin explicar.** La primera vez, escribe el término completo.

## Example

Client email, before (one paragraph, reason first, action hidden):

> Estimado usuario: respecto de la clave de acceso, informamos que por motivos de seguridad los
> enlaces de recuperación tienen una vigencia limitada de 24 horas, por lo que habiendo
> transcurrido dicho plazo el enlace enviado ya no se encuentra operativo, debiendo solicitarse
> uno nuevo desde la página de inicio de sesión.

After (answer first, steps, reason last):

> Hola:
>
> El enlace para cambiar la clave ya no sirve.
>
> Haga esto:
>
> 1. Entre a la página de inicio de sesión.
> 2. Toque "Olvidé mi clave".
> 3. Escriba su correo.
> 4. Abra el correo nuevo y cambie la clave.
>
> El enlace nuevo dura 24 horas.
>
> El enlace vence por seguridad. Así nadie más puede usarlo.

The two texts carry the same information. After 20 seconds, the reader knows what to do.
