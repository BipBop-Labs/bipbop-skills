---
name: pr
description: 'Abre un pull request desde un agente con secciones para quien revisa y para el cliente: resumen técnico, plan de pruebas y resumen en español. Úsala cuando la persona pide crear un PR o preparar su descripción.'
---

# Pull request

Esta guía ayuda a un agente a abrir un pull request. La descripción del PR sirve a quien revisa el código y también al cliente.

## When to use

- La persona pide crear un PR o escribir su descripción.
- La rama actual tiene commits que no están en la rama base.
- No uses esta skill para revisar un PR ajeno, mergear ni cerrar PRs.

## Precondiciones

- La persona pidió abrir el PR. Publicar un PR es un efecto externo, así que no lo hagas por iniciativa propia.
- `gh auth status` responde autenticado.
- La rama no tiene un PR abierto. Si `gh pr view --json url` devuelve uno, actualízalo con `gh pr edit`. No crees otro.

## Procedure

1. **Reúne el contexto**
   - Rama actual: `git branch --show-current`.
   - Rama base: la que da la sección [Rama base](#rama-base). Resuélvela antes de mirar los commits o el diff, porque git calcula los dos contra la base.
   - Commits que difieren: `git log <base>..HEAD --oneline`.
   - Cambios completos: `git diff <base>...HEAD`.
   - Agrega el contexto extra que entregue la persona.
2. **Pregunta si tienes dudas.** Si el diff no muestra el objetivo del cambio, pregunta antes de escribir la descripción.
3. **Empuja la rama**: `git push -u origin <rama>`. No uses force push, salvo que la persona lo pida explícitamente.
4. **Crea el PR** con `gh pr create --base <base> --title "<título conciso>" --body-file <archivo>`. Escribe el cuerpo en un archivo temporal, para que el shell no rompa las comillas ni los backticks. Usa esta estructura para el cuerpo:

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

5. **Devuelve la URL del PR.**

## Rama base

La rama base depende de dos datos:

- La rama en la que estás.
- Si el repositorio tiene una rama de integración.

La rama de integración es `stg` (o `staging`) cuando existe en el remoto.
Revisa el remoto con `git ls-remote --exit-code --heads origin stg`.
No uses la copia local, porque puede ser de una rama que alguien ya borró.
Obtén la rama por defecto del repositorio con `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.
Normalmente es `main`, pero no lo asumas.

**En una rama de trabajo**, apunta el PR a la rama de integración si existe. Si no existe, apunta el PR a la rama por defecto.
En un repositorio con `stg`, el equipo integra y prueba el trabajo en `stg` antes de producción.
Un PR de una rama de trabajo directo a `main` salta ese paso, aunque `main` sea la rama por defecto en GitHub.

**En la rama de integración**, el pedido puede significar dos cosas. El contexto casi siempre dice cuál.

- **Trabajo hacia `stg`.** La persona habla de un cambio concreto. Además, `stg` tiene commits locales que no están en `origin/stg`, o tiene cambios sin commitear. Crea una rama desde donde estás con `git switch -c <rama>`. La rama nueva se lleva esos commits. Abre el PR de esa rama a `stg`.
- **Promoción a producción.** La persona habla de publicar, liberar, promover o "pasar a producción". Además, `stg` está igual que `origin/stg` y va por delante de la rama por defecto. Abre el PR de `stg` a la rama por defecto, sin crear una rama. En la descripción, resume todo lo que entra a producción (`git log origin/<defecto>..origin/stg`).
- **Señales insuficientes o contradictorias.** Por ejemplo, la persona pide "el PR" a secas, `stg` tiene commits sin subir y además va por delante de `main`. Pregunta cuál de los dos PR quiere antes de empujar nada. Si eliges por tu cuenta, puedes publicar a producción trabajo que solo necesitaba revisión, o esconder un release dentro de una rama de trabajo.

**En la rama por defecto**, trata el pedido como trabajo nuevo: crea una rama desde ahí y aplica la regla de las ramas de trabajo.

Si la persona nombra la base ("ábrelo contra `main`", "esto es un hotfix a producción"), usa esa base.
Las reglas anteriores dan el valor por defecto, no una restricción.
Si la persona no nombra la base, no tomes la base de la documentación del repositorio ni de PRs anteriores cuando contradicen esta regla.
En ese caso, informa la contradicción y pregunta.

## Secciones

- **Summary of Changes** (inglés): escribe hechos, sin opiniones. Resume el cambio y no repitas la lista de commits. Hazlo breve y fácil de escanear.
- **Test Plan**: escribe pasos concretos que cubren los flujos afectados. Marca una casilla solo si ejecutaste ese paso. Deja el resto sin marcar para quien revisa.
- **Resumen para el cliente** (español): ponlo dentro de un bloque de código, para copiar y pegar. Incluye solo los cambios que la persona usuaria ve, en lenguaje simple y sin detalle técnico.

## Pitfalls

- **Datos sensibles.** En un repositorio abierto, el cuerpo del PR es público. No incluyas credenciales, rutas locales, nombres de clientes ni datos reales.
- **Base equivocada.** Resuelve la base con la sección Rama base antes de crear el PR. Si corriges la base después, la revisión cambia de sitio. El error típico es usar la rama por defecto de GitHub en un repositorio que tiene `stg`.
- **Promoción confundida con trabajo.** Estar en `stg` no dice por sí solo qué PR quiere la persona. Si dudas entre "rama nueva hacia `stg`" y "`stg` hacia `main`", y no tienes una señal de la persona o del estado de las ramas, pregunta.
- **Descripción inflada.** Un PR chico lleva secciones cortas. No inventes riesgos, migraciones ni pruebas que no existen.
- **Trabajo pendiente.** Si dejaste algo fuera del alcance o un test falla, dilo en el cuerpo del PR, no solo en el chat.

## Verification

- `gh pr view --json url,title,body,baseRefName,headRefName` muestra el PR con las tres secciones.
- `baseRefName` es la rama que dio la sección Rama base, o la rama que nombró la persona.
