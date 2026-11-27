---
name: microcopy
description: Escribe microcopy (botones, errores, estados vacíos, confirmaciones) con las convenciones de Revi. Úsala al agregar o cambiar texto de UI, emails del producto, placeholders, mensajes de estado o CTAs.
---

# Microcopy de Revi

Esta guía sirve para escribir textos cortos de interfaz en los productos Revi (Clara, Norman, Celeste).
Cubre botones, errores, estados vacíos, confirmaciones, tooltips, placeholders y toasts.
El microcopy es una conversación corta entre el producto y el funcionario.
Si una regla general choca con la voz de Revi, manda la voz de Revi.

## Principios base

1. **Específico, no genérico.** "Error" u "Ocurrió un problema" desperdician el
   espacio. Nombra el objeto real: "El plano no se pudo subir".
2. **Botones: verbo + objeto que describe el resultado.** No uses "Enviar", "OK",
   "Aceptar" ni "Submit". Escribe "Guardar borrador", "Subir expediente", "Ir a Revi".
   Usa sentence case, no MAYÚSCULAS.
3. **Errores: problema → razón → solución.** Di qué pasó, por qué y qué hacer.
   No culpes al usuario ni al sistema. "El archivo supera 110 MB. Comprímelo
   o sube solo el documento principal."
4. **Estados vacíos: patrón [valor] + [acción].** Un dashboard vacío explica
   qué hacer y no se disculpa. "Aún no hay expedientes asignados. Los verás
   aquí cuando te lleguen."
5. **Breve, pero sin ambigüedad.** Botones: de 3 a 7 palabras. Errores: una
   línea. Tooltips: 2 frases como máximo. Si el texto necesita más, no es un
   tooltip.
6. **Nombra completa la acción destructiva.** El botón de confirmación
   repite la acción ("Eliminar expediente"), nunca dice "Confirmar" ni "Sí". El
   cuerpo del diálogo muestra la consecuencia ("Los antecedentes asociados se
   perderán").
7. **Éxito discreto.** Confirma cerca de la acción, con las palabras del
   usuario y sin celebraciones ("Expediente enviado", no "¡Excelente!").
8. **Crisis: cero personalidad.** Si el sistema está caído o hay pérdida de
   datos, usa un tono directo, serio e informativo.
9. **No describas lo que se describe solo.** Antes de agregar una ayuda, un
   subtítulo o un eyebrow, pregúntate qué dice que el nombre no diga. "+ Nueva
   carpeta" ya dice qué hace. "Tus chats" ya dice qué hay ahí y no necesita
   "Los chats que no compartes". Si el título es suficientemente descriptivo,
   déjalo solo. Un subtítulo que repite el título con otras palabras es ruido
   y le quita peso al título.
10. **No uses el punto medio (`·`).** No lo uses para separar datos. En una
   interfaz, pon cada dato en su propio elemento (tag, etiqueta, columna). El
   componente separa los datos con espacio o borde, no con texto. En prosa,
   escribe una oración ("El permiso vence el 3 de marzo", no "Permiso · 3 mar").
11. **No uses las comillas angulares (`«` `»`).** Para citar, usa comillas
   normales (`"Borrador"`, no `«Borrador»`).

## Botones y etiquetas no son descripciones

Escribe un botón, un título o una etiqueta como fragmento: verbo + objeto
("Subir expediente") o sustantivo ("Tus chats").
Una descripción es prosa: el cuerpo de una card, un tooltip, una ayuda o el texto de un estado vacío.
Las descripciones siguen otras reglas:

- **Oraciones completas, con sujeto y verbo.** No partas una idea en una
  etiqueta y una frase sin sujeto ("El plazo del permiso. Vence a los 30
  días."). Escríbela como una oración ("El permiso vence a los 30 días.").
- **Sin remates.** No uses contrastes armados ni cierres que buscan efecto
  ("…y nunca más pierdes un plazo", "no es un trámite, es una decisión").

## Voz de Revi

- **Español de Chile, tuteo, verbo en presente, sin jerga legal innecesaria.**
  "Puedes", "Revisa", "Tu expediente". No uses "usted", salvo en comunicaciones
  formales del canal institucional. Los emails de CChC a municipios van en tuteo
  cordial (ver `backend/app/scripts/reactivation_campaign/email_copy.py`).
- **Sin emojis ni exclamaciones en serie.** La personalidad es **sobria,
  técnica e institucional**, nunca lúdica ni recargada. No escribas "¡Genial!"
  ni celebraciones que retrasen la siguiente decisión.
- **Un solo CTA por superficie.** Un email de Revi termina con un botón "Ir a
  Revi" y no pide responder ni agendar. En la UI aplica la misma regla: una
  acción primaria por pantalla.
- **Nada que suene a marketing.** No muestres UTMs. No uses frases de venta ni
  urgencia artificial ("¡Últimos días!").
- **El humano decide.** La IA asiste. El copy nunca dice "el sistema decidió".
  Cuando un resultado viene de un modelo, deja la acción al revisor
  ("Revisa y confirma la sugerencia").
- **Institucional, pero no frío.** Sé cordial y cercano, pero siempre útil.
  Prueba el copy así: léelo como un funcionario cansado que a las 4 AM se
  recupera de un error. Si el copy le empeora el ánimo, reescríbelo.

## Patrones por elemento

| Elemento | Regla | Ejemplo Revi |
|---|---|---|
| Botón primario | Verbo + objeto, resultado | "Ir a Revi", "Guardar revisión" |
| Botón destructivo | Acción completa, sin ambigüedad | "Eliminar expediente" |
| Error | Problema + razón + solución, sin culpar | "El archivo supera 110 MB. Sube una versión comprimida." |
| Estado vacío | Qué es + qué hacer, sin disculpas | "Aún no hay expedientes. Los nuevos aparecerán aquí." |
| Confirmación de riesgo | Consecuencia + botones diferenciados | "Se perderán los borradores no guardados." / [Descartar] [Seguir editando] |
| Placeholder | Muestra el formato esperado, nunca reemplaza al label | "Ej: Permiso ED-2026-0143" |
| Toast de éxito | Confirmación breve, cerca de la acción | "Informe enviado a la DIDP." |
| Carga | Qué pasa + duración estimada si dura más de 300 ms | "Analizando 12 documentos…" |
| Tooltip | 2 frases como máximo, valor extra (nunca info esencial) | (sin ejemplo) |
| Eyebrow / subtítulo | Solo si dice algo que el título no dice; si no, omítelo | "Tus chats", sin subtítulo |
| Descripción en card | Oraciones completas, sin remates | "Revisa los antecedentes antes de enviar el informe." |

## Checklist al escribir o revisar microcopy

- [ ] ¿Cada botón dice exactamente qué hace? (sin Enviar/OK/Aceptar)
- [ ] ¿Los errores dicen qué pasó, por qué y qué hacer?
- [ ] ¿El texto usa tuteo chileno, sin emojis ni exclamaciones de marketing?
- [ ] ¿Hay una sola acción primaria por superficie?
- [ ] ¿El copy funciona en estado de crisis (sin chistes ni personalidad)?
- [ ] ¿Los placeholders no reemplazan labels ni contienen info esencial?
- [ ] ¿Las confirmaciones destructivas repiten la acción en el botón?
- [ ] ¿Cada ayuda, subtítulo o eyebrow dice algo que su título no dice?
- [ ] ¿Las descripciones son oraciones completas y terminan sin remate?
