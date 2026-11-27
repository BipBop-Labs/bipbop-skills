---
name: commit
description: 'Crea commits atómicos y bien redactados desde un agente: revisa el diff real, elige qué stagear, sigue el estilo del repositorio y respeta los hooks. Úsala cuando la persona pide commitear, dice "haz un commit" o entrega un mensaje como guía.'
---

# Commit

Esta guía ayuda a un agente a crear commits que otra persona puede leer, revisar y revertir sin sorpresas.

## When to use

- La persona pide commitear los cambios en curso.
- La persona entrega un mensaje o contexto como base.
- No uses esta skill para push, PR, rebase, amend de commits ya empujados ni reescritura de historia.

## Precondiciones

- La persona pidió commitear. No commitees por iniciativa propia.
- La rama no es la principal. Si `git branch --show-current` devuelve `main` o `master`, crea una rama antes de commitear.

## Procedure

1. **Lee el estado real, no la memoria de la sesión**
   - Usa `git status` para ver los archivos modificados, staged y sin trackear.
   - Usa `git diff` y `git diff --staged` para revisar el contenido, no solo los nombres.
   - Usa `git log --oneline -10` para copiar el formato, el idioma y las convenciones del repositorio.
2. **Decide el alcance y divide si hace falta**
   - Haz un commit por unidad lógica: los cambios que revertirías juntos van en el mismo commit.
   - Divide cuando el árbol mezcla temas: refactor y feature, formateo masivo y lógica, backend y frontend sin relación, o dependencias nuevas y su uso.
   - No dividas cambios que por separado no compilan o no pasan los tests. Si dudas entre dos commits acoplados, deja uno.
   - Para dividir, repite el ciclo stagear → commitear por tema. Sigue el orden de dependencia: primero lo que el resto necesita (renombres, utilidades, migraciones), después lo que lo usa.
   - Si un archivo tiene cambios de dos temas, usa `git add -p` para stagear solo los hunks de un tema.
   - Deja fuera lo que no pertenece a ningún commit: experimentos, prints de depuración, archivos de scratch, configuración local.
3. **Stagea explícitamente**
   - Usa `git add <ruta>` archivo por archivo o por directorio acotado.
   - No uses `git add -A`, `git add .` ni `git commit -a`. Estos comandos agregan archivos que nadie revisó.
   - Antes de commitear, relee `git diff --staged`. Solo ese contenido queda en la historia.
4. **Escribe el mensaje**
   - Sigue el formato del repositorio. Si el repositorio usa conventional commits, usa `type(scope): descripción`, con los tipos `feat`, `fix`, `refactor`, `test`, `docs`, `style` y `chore`.
   - Escribe la primera línea con menos de 72 caracteres, en imperativo y en el idioma que ya usa el repositorio.
   - En el cuerpo, explica el porqué y las decisiones no obvias. El diff ya muestra el qué.
   - Usa viñetas solo si hay varios cambios significativos.
   - No agregues atribución de agente ni coautoría, salvo que el repositorio o la persona lo pidan.
5. **Commitea**
   - Ejecuta `git commit` con el mensaje que escribiste.

## Pitfalls

- **Hooks.** Si un hook falla, git no creó el commit. Corrige la causa. Vuelve a stagear los archivos que el hook modificó y commitea de nuevo. Nunca uses `--no-verify`.
- **Secretos y ruido.** No commitees `.env`, credenciales, tokens, dumps, artefactos de build, logs ni archivos temporales del agente. Si dudas, revisa si el archivo debe estar en `.gitignore`.
- **Comandos destructivos.** No uses `git reset --hard`, `git checkout .`, `git clean -fd` ni `git stash drop` para "ordenar" antes de commitear. Estos comandos borran trabajo que no es tuyo.
- **Historia publicada.** No uses `--amend` ni force push sobre commits que ya están en el remoto, salvo que la persona lo pida explícitamente.
- **Mensaje inflado.** No describas intención, impacto ni motivación que el diff no respalde.
- **Reporte honesto.** Si algo quedó sin commitear, si un test falla o si un hook cambió archivos, dilo en la respuesta.

## Verification

- `git log -1 --stat` muestra el commit con el mensaje esperado y solo los archivos previstos.
- `git status` no muestra cambios que querías incluir en el commit.
