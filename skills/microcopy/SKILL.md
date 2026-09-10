---
name: microcopy
description: Escribir microcopy (botones, errores, vacíos, confirmaciones) siguiendo las convenciones de Revi. Úsalo al agregar o cambiar texto de UI, emails del producto, placeholders, mensajes de estado o CTAs.
---

# Microcopy de Revi

Guía para escribir textos de interfaz cortos (botones, errores, estados vacíos,
confirmaciones, tooltips, placeholders, toasts) en los productos Revi (Clara,
Norman, Celeste). El criterio general: **el microcopy es una mini-conversación
entre el producto y el funcionario**. La web de UX writing y lo que hacemos en
Revi coinciden en casi todo; donde difieren, manda la voz de Revi.

## Principios base (mejores prácticas de UX writing, aplicadas)

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

## Voz de Revi (esto nos diferencia; contrastado con lo anterior)

- **Español de Chile, tuteo.** "Puedes", "Revisa", "Tu expediente". Nunca
  usted salvo en comunicaciones formales del canal institucional (emails de
  CChC a municipios van en tuteo cordial; ver `email_copy.py` como referencia).
- **Trato de tú, verbo en presente, sin jerga legal innecesaria.** Somos
  asistentes de revisión, no la regulación.
- **Sin emojis, sin exclamaciones en serie, sin marketing.** La personalidad
  es **sobria, técnica e institucional** (ver `frontend/DESIGN.md` de
  revi-dga-mono: "nunca lúdica ni recargada"). Nada de "¡Genial!" ni
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

## Checklist al escribir o revisar microcopy

- [ ] ¿Cada botón dice qué hace exactamente? (sin Enviar/OK/Aceptar)
- [ ] ¿Los errores dicen qué pasó, por qué y qué hacer?
- [ ] ¿Tuteo chileno, sin emojis, sin exclamaciones de marketing?
- [ ] ¿Una sola acción primaria por superficie?
- [ ] ¿El copy funciona en estado de crisis (sin chistes ni personalidad)?
- [ ] ¿Los placeholders no reemplazan labels ni contienen info esencial?
- [ ] ¿Las confirmaciones destructivas repiten la acción en el botón?

## Referencias externas

- Microcopy patterns (errors P-R-S, empty states, confirmations):
  https://vaishvanara.github.io/techwritingkb/technical-writing/ux-writing
- Principios y ejemplos: https://courseux.com/microcopy-examples
- Límites de caracteres por elemento: https://typecount.com/blog/microcopy-ux-writing-guide
- Copys de referencia del producto: `backend/app/scripts/reactivation_campaign/email_copy.py`
- Tono visual: `frontend/DESIGN.md` en revi-dga-mono
