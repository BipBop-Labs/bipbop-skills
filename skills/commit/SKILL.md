---
name: commit
description: Crear commits atómicos y bien redactados desde un agente: revisar el diff real, elegir qué se stagea, seguir el estilo del repositorio y respetar los hooks. Úsala cuando la persona pide commitear, "haz un commit" o entrega un mensaje como guía.
---

# Commit

Guía para que un agente cree commits que otra persona pueda leer, revisar y revertir sin sorpresas.

## When to use

- La persona pide commitear los cambios en curso.
- La persona entrega un mensaje o contexto para usar como base.
- No usar para push, PR, rebase, amend de commits ya empujados ni reescritura de historia.

## Precondiciones

- La persona pidió commitear. Un agente no commitea por iniciativa propia.
- La rama no es la principal. Si `git branch --show-current` devuelve `main` o `master`, crea una rama antes de commitear.

## Procedure

1. **Leer el estado real, no la memoria de la sesión**
   - `git status` para ver qué está modificado, staged y sin trackear.
   - `git diff` y `git diff --staged` para revisar el contenido, no solo los nombres.
   - `git log --oneline -10` para copiar formato, idioma y convenciones del repositorio.
2. **Decidir el alcance y dividir si hace falta**
   - Un commit por unidad lógica: lo que se revierte junto, va junto.
   - Divide cuando el árbol mezcla temas: refactor y feature, formateo masivo y lógica, backend y frontend sin relación, o dependencias nuevas y su uso.
   - No dividas lo que no compila ni pasa tests por separado. Ante la duda entre dos commits acoplados, deja uno.
   - Para dividir, repite el ciclo stagear → commitear por tema, en orden de dependencia: primero lo que el resto necesita (renombres, utilidades, migraciones), después lo que lo usa.
   - Si un mismo archivo mezcla dos temas y no tienes terminal interactiva (`git add -p` la necesita), guarda los hunks de un tema en un parche con `git diff` y aplícalo con `git apply --cached`. Si no es viable, commitea el archivo completo y dilo en la respuesta.
   - Deja fuera lo que no pertenece a ningún commit: experimentos, prints de depuración, archivos de scratch, configuración local.
3. **Stagear explícitamente**
   - `git add <ruta>` archivo por archivo o por directorio acotado.
   - Evita `git add -A`, `git add .` y `git commit -a`: arrastran archivos que nadie revisó.
   - Antes de commitear, relee `git diff --staged`. Es lo único que va a quedar en la historia.
4. **Escribir el mensaje**
   - Formato del repositorio. Si usa conventional commits: `type(scope): descripción`, con tipos `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `chore`.
   - Primera línea bajo 72 caracteres, en imperativo y en el idioma que ya usa el repositorio.
   - El cuerpo explica el porqué y las decisiones no obvias. El qué ya está en el diff.
   - Viñetas solo si hay varios cambios significativos.
   - Sin atribución de agente ni coautoría, salvo que el repositorio o la persona lo pidan.
5. **Commitear**
   - `git commit` con el mensaje generado.

## Pitfalls

- **Hooks.** Si un hook falla, el commit no se creó. Corrige la causa, vuelve a stagear lo que el hook modificó y commitea de nuevo. Nunca `--no-verify`.
- **Secretos y ruido.** No commitees `.env`, credenciales, tokens, dumps, artefactos de build, logs ni archivos temporales del agente. Ante la duda, revisa si el archivo debería estar en `.gitignore`.
- **Comandos destructivos.** No uses `git reset --hard`, `git checkout .`, `git clean -fd` ni `git stash drop` para "ordenar" antes de commitear: borran trabajo que no es tuyo.
- **Historia publicada.** No hagas `--amend` ni force push sobre commits que ya están en el remoto, salvo instrucción explícita.
- **Mensaje inflado.** No describas intención, impacto ni motivación que el diff no respalde.
- **Reporte honesto.** Si algo quedó sin commitear, si un test falla o si un hook cambió archivos, dilo en la respuesta.

## Verification

- `git log -1 --stat` muestra el commit con el mensaje esperado y solo los archivos previstos.
- `git status` no deja residuos que se pretendía incluir.
