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
   - Rama base: la que resulta de la sección [Rama base](#rama-base). Resuélvela antes de mirar commits o diff, porque ambos se calculan contra ella.
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

## Rama base

La rama base sale de dos datos: en qué rama estás y si el repositorio tiene una rama de integración. La rama de integración es `stg` (o `staging`) cuando existe en el remoto, y se comprueba ahí con `git ls-remote --exit-code --heads origin stg`, porque una copia local puede ser de una rama que ya se borró. La rama por defecto del repositorio se obtiene con `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`; suele ser `main`, pero no lo asumas.

Si estás en una rama de trabajo, el PR apunta a la rama de integración cuando existe y a la rama por defecto cuando no. En un repositorio con `stg` el trabajo se integra y se prueba ahí antes de llegar a producción, así que un PR de una rama de trabajo directo a `main` se salta ese paso, aunque `main` sea la rama por defecto en GitHub.

Si estás en la rama de integración, el pedido puede significar dos cosas distintas y el contexto casi siempre dice cuál. Cuando la persona habla de un cambio concreto y `stg` tiene commits locales que no están en `origin/stg`, o cambios sin commitear, quiere un PR de ese trabajo hacia `stg`: crea una rama desde donde estás con `git switch -c <rama>`, que se lleva esos commits, y abre el PR de esa rama a `stg`. Cuando la persona habla de publicar, liberar, promover o "pasar a producción", y `stg` está igual que `origin/stg` y por delante de la rama por defecto, quiere promover lo ya integrado: abre el PR de `stg` a la rama por defecto, sin crear rama, y resume en la descripción todo lo que entra a producción (`git log origin/<defecto>..origin/stg`). Si las señales no alcanzan o se contradicen (por ejemplo, pide "el PR" a secas y `stg` tiene commits sin subir y además va por delante de `main`), pregunta cuál de las dos quiere antes de empujar nada. Elegir por tu cuenta en ese caso puede publicar a producción trabajo que solo debía revisarse, o esconder un release dentro de una rama de trabajo.

Si estás en la rama por defecto, trátalo como trabajo nuevo: crea una rama desde ahí y aplica la regla de las ramas de trabajo.

Si la persona nombra la base ("ábrelo contra `main`", "esto es un hotfix a producción"), usa esa; lo anterior es el valor por defecto, no una restricción. Sin esa indicación, no tomes la base de la documentación del repositorio ni de PRs anteriores cuando contradigan esta regla: dilo y pregunta.

## Secciones

- **Summary of Changes** (inglés): factual, sin opiniones. Resume el cambio, no repitas la lista de commits. Breve y escaneable.
- **Test Plan**: pasos concretos que cubren los flujos afectados. Marca una casilla solo si de verdad ejecutaste ese paso; el resto queda sin marcar para quien revisa.
- **Resumen para el cliente** (español): dentro de un bloque de código para copiar y pegar. Solo cambios visibles para la persona usuaria, en lenguaje simple, sin detalle técnico.

## Pitfalls

- **Datos sensibles.** El cuerpo de un PR es público en repositorios abiertos: sin credenciales, rutas locales, nombres de clientes ni datos reales.
- **Base equivocada.** Resuelve la base con la sección Rama base antes de crear el PR; corregirla después mueve la revisión de sitio. El error típico es usar la rama por defecto de GitHub en un repositorio que tiene `stg`.
- **Promoción confundida con trabajo.** Estar parado en `stg` no dice por sí solo qué PR se quiere. Si te descubres eligiendo entre "rama nueva hacia `stg`" y "`stg` hacia `main`" sin una señal de la persona o del estado de las ramas, esa duda es la señal para preguntar.
- **Descripción inflada.** Un PR chico lleva secciones cortas. No inventes riesgos, migraciones ni pruebas que no existen.
- **Trabajo pendiente.** Si dejaste algo fuera del alcance o un test falla, dilo en el cuerpo del PR, no solo en el chat.

## Verification

- `gh pr view --json url,title,body,baseRefName,headRefName` muestra el PR con las tres secciones, y `baseRefName` es la rama que resultó de la sección Rama base (o la que nombró la persona).
