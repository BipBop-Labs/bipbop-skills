# Spanish

ASD-STE100 is a standard for English only.
It has no Spanish edition.
This file applies the same rule categories to Spanish text.
The adaptations are a decision of this skill, not text from the standard.

Use this file together with the rule table in `SKILL.md`.
A rule that does not appear here applies with no change.

## The rules in Spanish

| Rule                  | Do                                                                    | Do not                                                               |
| --------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------- |
| One meaning per word  | Pick one verb per action and reuse it: "revisar"                      | Rotate "revisar", "verificar", "comprobar", and "chequear"           |
| Verbs, not nouns      | "Revisa el log."                                                      | "Realiza la revisión del log."                                       |
| Active voice          | "El worker borra el archivo."                                         | "El archivo es borrado." / "Se borra el archivo."                    |
| Simple tenses         | "Recibimos el informe."                                               | "Hemos recibido el informe." / "Estamos recibiendo el informe."      |
| One idea per sentence | "Abre el archivo. Lee la línea 3."                                    | "Abre el archivo y lee la línea 3, verificando que coincida."        |
| Sentence length       | 25 words or fewer for instructions, 30 or fewer for descriptions      | Chains of "que", "el cual", and gerunds                              |
| Chains of "de"        | Two "de" in a row at most: "la válvula de la bomba de combustible"    | "la configuración del manejador de prioridad de la cola de tareas"   |
| No missing words      | Keep the article and the verb. Name the subject when it is not clear. | "Archivos sin respaldo se pierden."                                  |
| One hedge, at most    | "Probablemente el cliente está desactualizado."                       | "Podría eventualmente haber ocurrido un error debido a un posible…"  |
| Paragraphs            | One topic, 6 sentences or fewer                                       | Multi-topic paragraphs                                               |
| Lists                 | Use a list for 3 or more steps or conditions                          | A sequence buried in one sentence                                    |
| Jargon                | Keep the term the team uses, and use one form: "deploy"               | Alternate "deploy", "despliegue", and "puesta en producción"         |

## Detail behind the adaptations

**Verbs, not nouns.**
The English rule gives each word one part of speech.
Spanish word endings already show the part of speech, so that problem is rare.
The Spanish problem is the noun that hides a verb.
Write "pagar", not "efectuar el pago".
Write "decidir", not "tomar una decisión".

**Verb forms.**
Use the infinitive, the imperative, the present, the pretérito perfecto simple ("recibimos"), and the simple future.
Do not use the pretérito perfecto compuesto ("hemos recibido") or "estar" plus a gerund ("está procesando").
Do not use "ir a" or "proceder a" before the verb: write "el job borra", not "el job va a proceder a borrar".
Use the subjunctive only where the grammar requires it, for example after "cuando" or "para que".
Use the imperfect tense only for a state in the past: "la tabla tenía 3 columnas".

**Gerunds.**
Do not use a gerund to add a consequence or a second action.
Write "El job falló. La falla dejó la tabla vacía.", not "El job falló, dejando la tabla vacía."

**Voice.**
Spanish has two passive forms: "es borrado" and "se borra".
The two forms hide the actor.
Use them only in descriptive text, when the actor is unknown or does not matter to the reader: "La oficina se cierra a las 18:00."

**Subject.**
Spanish lets the writer drop the subject pronoun, and that is correct: "Recibimos el informe."
Name the subject when the verb ending does not identify it.
"Falló después del deploy" does not say what failed.
Write "El job de exportación falló después del deploy."

**"Su" and "sus".**
"Su" can refer to the reader, to a third person, or to a thing.
When more than one owner is possible, name the owner: "la clave del usuario", not "su clave".

**Sentence length.**
A Spanish sentence usually needs more words than its English equivalent.
For that reason the limits are 5 words higher than the English limits.

**Instructions.**
Use the imperative for steps, and use one form of address in the whole text: "tú" or "usted".
Open a safety instruction with the command or the condition: "No borres la tabla antes de que termine la exportación."

**Hedges.**
"Eventualmente" means "possibly" in Spanish, not "in the end".
Do not use it to translate "eventually".

**Jargon and English terms.**
Keep the English term when it is the term the team uses: "deploy", "commit", "pull request".
Do not translate the name of a tool, a command, a file, or an identifier.
Use the Spanish word when the reader uses it: "error", not "bug", in text for a non-technical reader.

**Punctuation.**
Do not use the raya (—) to insert a comment.
Use a comma, parentheses, or a new sentence.
Write the opening "¿" and "¡", and write every accent.

## Before and after

Every example below is invented to show a rule.

| Rule                 | Before                                                               | After                                                             |
| -------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| One meaning per word | "Verifica el flag, comprueba el rollout y chequea el payload."       | "Revisa el flag, el rollout y el payload."                        |
| Verbs, not nouns     | "Se debe efectuar la validación de los datos."                       | "Valida los datos."                                               |
| Simple tense         | "Hemos recibido 400 excepciones desde el martes."                    | "Recibimos 400 excepciones desde el martes."                      |
| Active voice         | "La entrada vencida es eliminada en la siguiente escritura."         | "La siguiente escritura elimina la entrada vencida del caché."    |
| Chain of "de"        | "la configuración del manejador de prioridad de la cola de tareas"   | "la configuración que define la prioridad de la cola de tareas"   |
| No missing words     | "Sesiones no muestreadas se descartan."                              | "El worker descarta cada sesión que el sampler no seleccionó."    |

### Report finding

Before:

> Al parecer podría existir un problema en la forma en que se está instrumentando el embudo de registro, dado que la propiedad que identifica el plan seleccionado no ha estado siendo enviada en el último paso desde aproximadamente mediados del mes pasado, lo que implicaría que cualquier desglose por plan estaría subcontando.

What it breaks: 52 words, three hedges, passive voice, a compound tense, a vague date.

After:

> El embudo de registro no envía la propiedad del plan en su último paso.
> La propiedad dejó de llegar el 12 de mayo.
> Todos los desgloses por plan subcuentan desde esa fecha.

### Instruction to another agent

Before:

> Una vez que el job anterior haya terminado y asumiendo que no se hayan producido errores, el agente debería proceder a consumir el artefacto de salida, teniendo en cuenta que a veces se generan artefactos parciales por timeout.

What it breaks: compound tenses, three facts in one sentence, a gerund that adds a condition, 38 words against a 25-word cap.

After:

> Espera a que el job anterior termine sin errores.
> Después lee el artefacto de salida.
> Un timeout puede generar un artefacto parcial. Revisa que el artefacto esté completo antes de usarlo.
