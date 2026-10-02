---
name: pr
description: Abrir un pull request desde un agente con secciones estructuradas para quien revisa y para el cliente (resumen técnico, plan de pruebas y resumen en español). Úsala cuando la persona pide crear un PR o preparar su descripción.
---

# Pull request

Guía para que un agente abra un pull request cuya descripción sirve a quien revisa el código y también al cliente.

## When to use

- La persona pide crear un PR o escribir su descripción.
- La rama actual tiene commits que no están en la rama base.
- No usar para revisar un PR ajeno, mergear ni cerrar PRs.

## Precondiciones

- La persona pidió abrir el PR. Publicar es un efecto externo: no lo hagas por iniciativa propia.
- `gh auth status` responde autenticado.
- No hay un PR abierto para la rama. Si `gh pr view --json url` devuelve uno, actualízalo con `gh pr edit` en vez de crear otro.

## Procedure

1. **Reunir contexto**
   - Rama actual: `git branch --show-current`.
   - Rama base real: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`. No asumas `main`.
   - Commits que difieren: `git log <base>..HEAD --oneline`.
   - Cambios completos: `git diff <base>...HEAD`.
   - Incorpora el contexto extra que entregue la persona.
2. **Preguntar si hay dudas.** Si el objetivo del cambio no se deduce del diff, pregunta antes de escribir la descripción.
3. **Empujar la rama**: `git push -u origin <rama>`. Sin force push salvo instrucción explícita.
4. **Crear el PR** con `gh pr create --base <base> --title "<título conciso>" --body-file <archivo>`. Escribe el cuerpo en un archivo temporal: evita que las comillas y los backticks se rompan al pasar por el shell. Estructura del cuerpo:

````markdown
**Target:** `<rama-base>`

## Summary of Changes
- <descripción técnica y factual>

## Test Plan
- [ ] <paso de verificación concreto>

## Resumen para el cliente
```
- <cambio en español, sin detalles técnicos>
```
````

5. **Devolver la URL del PR.**

## Secciones

- **Summary of Changes** (inglés): factual, sin opiniones. Resume el cambio, no repitas la lista de commits. Breve y escaneable.
- **Test Plan**: pasos concretos que cubren los flujos afectados. Marca una casilla solo si de verdad ejecutaste ese paso; el resto queda sin marcar para quien revisa.
- **Resumen para el cliente** (español): dentro de un bloque de código para copiar y pegar. Solo cambios visibles para la persona usuaria, en lenguaje simple, sin detalle técnico.

## Pitfalls

- **Datos sensibles.** El cuerpo de un PR es público en repositorios abiertos: sin credenciales, rutas locales, nombres de clientes ni datos reales.
- **Base equivocada.** Verifica la rama base antes de crear; corregirla después mueve la revisión de sitio.
- **Descripción inflada.** Un PR chico lleva secciones cortas. No inventes riesgos, migraciones ni pruebas que no existen.
- **Trabajo pendiente.** Si dejaste algo fuera del alcance o un test falla, dilo en el cuerpo del PR, no solo en el chat.

## Verification

- `gh pr view --json url,title,body` muestra el PR con las tres secciones y la base correcta.
