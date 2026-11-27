---
name: microcopy
description: Escribir microcopy (botones, errores, vacíos, confirmaciones) siguiendo las convenciones de Revi. Úsalo al agregar o cambiar texto de UI, emails del producto, placeholders, mensajes de estado o CTAs.
---

# Microcopy de Revi

Guía para escribir textos de interfaz cortos (botones, errores, estados vacíos,
confirmaciones, tooltips, placeholders, toasts) en los productos Revi (Clara,
Norman, Celeste). El microcopy es una conversación corta entre el producto y el
funcionario. Si una regla general choca con la voz de Revi, manda la voz de Revi.

## Principios base

1. **Específico, no genérico.** "Error" o "Ocurrió un problema" desperdician el
   espacio. Nombrar el objeto real: "El plano no se pudo subir".
2. **Botones = verbo + objeto, describen el resultado.** Nunca "Enviar", "OK",
   "Aceptar", "Submit". "Guardar borrador", "Subir expediente", "Ir a Revi".
   Sentence case, no MAYÚSCULAS.
3. **Errores: Problema → Razón → Solución.** Qué pasó, por qué, qué hacer.
   Nunca culpar al usuario ni al sistema. "El archivo supera 110 MB. Comprímelo
   o sube solo el documento principal."
4. **Estados vacíos: patrón [valor] + [acción].** Un dashboard vacío explica
   qué hacer, no se disculpa. "Aún no hay expedientes asignados. Los verás
   aquí cuando te lleguen."
5. **Breve pero sin ambigüedad.** Sweet spot 3-7 palabras en botones; una
   línea en errores; máximo 2 frases en tooltips (si necesita más, no es un
   tooltip).
6. **La acción destructiva se nombra completa.** El botón de confirmación
   repite la acción ("Eliminar expediente"), nunca "Confirmar" o "Sí". El
   cuerpo del diálogo muestra la consecuencia ("Los antecedentes asociados se
   perderán").
7. **Estado de éxito discreto.** Confirmar cerca de la acción, en palabras del
   usuario, sin celebraciones ("Expediente enviado", no "¡Excelente!").
8. **Crisis: cero personalidad.** Si el sistema está caído o hay pérdida de
   datos, el tono es directo, serio e informativo.
9. **No describir lo que se describe solo.** Antes de agregar una ayuda, un
   subtítulo o un eyebrow, pregúntate qué dice que el nombre no diga. "+ Nueva
   carpeta" ya dice qué hace; "Tus chats" ya dice qué hay ahí, y no necesita
   "Los chats que no compartes". Si el título es suficientemente descriptivo,
   va solo: un subtítulo que lo repite con otras palabras es ruido y le quita
   peso al título.
10. **Evitar el punto medio (`·`).** No lo uses para separar datos. En una
   interfaz, cada dato va en su propio elemento (tag, etiqueta, columna) y el
   componente los separa con espacio o borde: la separación no depende del
   texto. En prosa, escribe una oración ("El permiso vence el 3 de marzo", no
   "Permiso · 3 mar").
11. **Evitar las comillas angulares (`«` `»`).** Para citar, usa comillas
   normales (`"Borrador"`, no `«Borrador»`).

## Botones y etiquetas no son descripciones

Un botón, un título o una etiqueta se escriben como fragmento: verbo + objeto
("Subir expediente") o sustantivo ("Tus chats"). Una descripción, en cambio, es
prosa: el cuerpo de una card, un tooltip, una ayuda, el texto de un estado
vacío. Ahí aplican otras reglas:

- **Oraciones completas, con sujeto y verbo.** No partir una idea en una
  etiqueta y una frase sin sujeto ("El plazo del permiso. Vence a los 30
  días."); escribirla como una oración ("El permiso vence a los 30 días.").
- **Sin remates.** Nada de contrastes armados ni cierres que buscan efecto
  ("…y nunca más pierdes un plazo", "no es un trámite, es una decisión").

## Voz de Revi

- **Español de Chile, tuteo, verbo en presente, sin jerga legal innecesaria.**
  "Puedes", "Revisa", "Tu expediente". Nunca usted salvo en comunicaciones
  formales del canal institucional (emails de CChC a municipios van en tuteo
  cordial; ver `backend/app/scripts/reactivation_campaign/email_copy.py`).
- **Sin emojis, sin exclamaciones en serie.** La personalidad es **sobria,
  técnica e institucional**, nunca lúdica ni recargada. Nada de "¡Genial!" ni
  celebraciones que retrasen la siguiente decisión.
- **Un solo CTA por superficie.** Un email de Revi termina con un botón "Ir a
  Revi" y no pide responder ni agendar. Aplica igual en UI: una acción
  primaria por pantalla.
- **Nada que lea a marketing.** Sin UTMs visibles, sin frases de venta, sin
  urgencia artificial ("¡Últimos días!").
- **El humano decide.** La IA asiste; el copy nunca dice "el sistema decidió".
  Cuando un resultado viene de un modelo, dejar la acción al revisor
  ("Revisa y confirma la sugerencia").
- **Institucional sin frío.** Cordial y cercano, pero siempre útil. Buen
  test: leerlo como funcionario cansado a las 4 AM recuperándose de un error;
  si el copy empeora el ánimo, reescribir.

## Patrones por elemento

| Elemento | Regla | Ejemplo Revi |
|---|---|---|
| Botón primario | Verbo + objeto, resultado | "Ir a Revi", "Guardar revisión" |
| Botón destructivo | Acción completa, sin ambigüedad | "Eliminar expediente" |
| Error | Problema + razón + solución, sin culpar | "El archivo supera 110 MB. Sube una versión comprimida." |
| Estado vacío | Qué es + qué hacer, sin disculpas | "Aún no hay expedientes. Los nuevos aparecerán aquí." |
| Confirmación de riesgo | Consecuencia + botones diferenciados | "Se perderán los borradores no guardados." / [Descartar] [Seguir editando] |
| Placeholder | Muestra formato esperado, nunca reemplaza al label | "Ej: Permiso ED-2026-0143" |
| Toast de éxito | Confirmación breve, cerca de la acción | "Informe enviado a la DIDP." |
| Carga | Qué está pasando + duración estimada si > 300ms | "Analizando 12 documentos…" |
| Tooltip | Máx 2 frases, valor extra (nunca info esencial) | — |
| Eyebrow / subtítulo | Solo si dice algo que el título no dice; si no, se omite | "Tus chats", sin subtítulo |
| Descripción en card | Oraciones completas, sin remates | "Revisa los antecedentes antes de enviar el informe." |

## Checklist al escribir o revisar microcopy

- [ ] ¿Cada botón dice qué hace exactamente? (sin Enviar/OK/Aceptar)
- [ ] ¿Los errores dicen qué pasó, por qué y qué hacer?
- [ ] ¿Tuteo chileno, sin emojis, sin exclamaciones de marketing?
- [ ] ¿Una sola acción primaria por superficie?
- [ ] ¿El copy funciona en estado de crisis (sin chistes ni personalidad)?
- [ ] ¿Los placeholders no reemplazan labels ni contienen info esencial?
- [ ] ¿Las confirmaciones destructivas repiten la acción en el botón?
- [ ] ¿Cada ayuda, subtítulo o eyebrow dice algo que su título no dice?
- [ ] ¿Las descripciones son oraciones completas y terminan sin remate?
