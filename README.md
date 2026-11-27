# BipBop Skills

Marketplace público de skills mantenidas por [BipBop Labs](https://bipbop.cl) para Claude Code, Codex y ChatGPT. El marketplace `bipbop` publica un plugin, `bipbop-skills`, con todas las skills del árbol `skills/`. Ese árbol es la fuente canónica para todos los clientes.

## Skills disponibles

Incluidas en el plugin `bipbop-skills`.

| Skill | Uso |
| --- | --- |
| [`adr`](skills/adr/) | Reglas para leer Architecture Decision Records, políticas y procedimientos, y para decidir qué tipo de documento necesita una regla. El modelo la carga solo. Ver el [README de adr](skills/adr/README.md). |
| [`adr-init`](skills/adr-init/) | Crear o adoptar la carpeta de ADRs, su template, su índice, `known-debt.md` y el puntero en CLAUDE.md o AGENTS.md. |
| [`adr-distill`](skills/adr-distill/) | Recuperar decisiones implícitas del código y la historia de git, y decidir con la persona cuáles se registran. |
| [`adr-new`](skills/adr-new/) | Registrar un ADR, una política o un procedimiento desde la conversación o el diff. |
| [`adr-review`](skills/adr-review/) | Revisar un diff o una rama contra los ADRs, políticas y procedimientos aceptados. Solo reporta. |
| [`best-prompting`](skills/best-prompting/) | Escribir y revisar prompts, descripciones de tools y briefs para agentes, con prácticas agnósticas al modelo y la evidencia detrás de cada una. |
| [`commit`](skills/commit/) | Crear commits atómicos: revisar el diff real, elegir qué stagear, seguir el estilo del repositorio y respetar los hooks. |
| [`create-skills`](skills/create-skills/) | Crear, revisar, validar y empaquetar skills portables siguiendo las mejores prácticas de Claude, Codex y ChatGPT. |
| [`microcopy`](skills/microcopy/) | Escribir botones, errores, vacíos, confirmaciones y otros textos breves de interfaz. |
| [`code-principles`](skills/code-principles/) | Nueve principios para todo el código que diseñas, escribes, arreglas o revisas, con una prueba por principio. |
| [`fix`](skills/fix/) | Arreglar un bug en su causa: reproducirlo, encontrar la causa con evidencia, test que falla primero, refactor de la sección si su diseño causó el bug, y verificar donde se reprodujo. |
| [`pr`](skills/pr/) | Abrir un pull request con resumen técnico, plan de pruebas y resumen para el cliente. Apunta a `stg` cuando el repositorio la tiene. |
| [`research-first`](skills/research-first/) | Investigar cómo resuelve la industria una tarea (estándares, regulaciones, guías y errores conocidos), destilarlo en un brief con fuentes y hacer la tarea apoyada en él. |
| [`simple-writing`](skills/simple-writing/) | Reescribir textos para que se entiendan a la primera, en lenguaje simple o lectura fácil. |
| [`test-audit`](skills/test-audit/) | Filtrar tests nuevos al escribirlos y auditar tests de bajo valor, acoplados a la implementación o duplicados. Adaptada de [OpenClaw](https://github.com/openclaw/openclaw) (MIT). |
| [`writing`](skills/writing/) | Escribir todo texto para una persona o un agente (respuestas, informes, PRs, commits, mensajes, prompts) con las reglas de ASD-STE100, para que no se pueda malinterpretar, en inglés y en español. Adaptada de la skill homónima del [plugin de PostHog](https://github.com/PostHog/ai-plugin) (MIT). |

## Instalar y mantener al día

El marketplace se llama `bipbop` y se agrega una sola vez. Después instalas el plugin `bipbop-skills`. Las skills se invocan con su namespace, por ejemplo `/bipbop-skills:microcopy` o `/bipbop-skills:adr-init`.

### Claude Code

Instalar, dentro de Claude Code:

```text
/plugin marketplace add BipBop-Labs/bipbop-skills
/plugin install bipbop-skills@bipbop
```

Actualizar:

```text
/plugin marketplace update bipbop
/plugin update bipbop-skills@bipbop
/reload-plugins
```

El primer comando descarga el catálogo nuevo, el segundo actualiza el plugin, y `/reload-plugins` aplica los cambios sin reiniciar la sesión. Un plugin solo se actualiza cuando sube su versión, así que revisa el [CHANGELOG](CHANGELOG.md) para saber qué cambió.

Para no hacerlo a mano, activa la actualización automática: `/plugin` > **Marketplaces** > `bipbop` > **Enable auto-update**. Claude Code revisa el marketplace al iniciar y actualiza los plugins instalados. En marketplaces de terceros como este viene desactivada por defecto.

Revisar lo instalado o quitar un plugin:

```text
/plugin list
/plugin uninstall bipbop-skills@bipbop
```

Los plugins `adr` y `bipflow` ya no existen. Sus skills ahora viven en `bipbop-skills`. Si los tenías instalados, desinstálalos con `/plugin uninstall adr@bipbop` y `/plugin uninstall bipflow@bipbop`. Los nombres nuevos son:

| Antes | Ahora |
| --- | --- |
| `/adr:init` | `/bipbop-skills:adr-init` |
| `/adr:distill` | `/bipbop-skills:adr-distill` |
| `/adr:new` | `/bipbop-skills:adr-new` |
| `/adr:review` | `/bipbop-skills:adr-review` |
| `adr:adr` | `bipbop-skills:adr` |
| `/bipflow:commit` | `/bipbop-skills:commit` |
| `/bipflow:pr` | `/bipbop-skills:pr` |

### Codex CLI

Instalar:

```bash
codex plugin marketplace add BipBop-Labs/bipbop-skills --ref main
codex plugin add bipbop-skills@bipbop
```

Actualizar. Codex conserva un snapshot local del marketplace, así que hay que pedir los cambios nuevos:

```bash
codex plugin marketplace upgrade bipbop
codex plugin marketplace list
codex plugin list
```

Para fijar una versión reproducible, usa un tag en vez de `main`:

```bash
codex plugin marketplace add BipBop-Labs/bipbop-skills --ref v0.2.0
```

### ChatGPT administrado

Un administrador puede importar `https://github.com/BipBop-Labs/bipbop-skills` desde **Admin > Plugins > Add > Import marketplace**. Deja vacío el subdirectorio para usar la raíz del repositorio. Los marketplaces nuevos se sincronizan automáticamente cada día; **Sync now** solicita una actualización inmediata.

## Estructura

```text
.
├── plugin.json                         # Manifest portable Agent Plugins
├── .agents/plugins/marketplace.json   # Marketplace de Codex y ChatGPT
├── .claude-plugin/
│   ├── marketplace.json               # Marketplace de Claude Code
│   └── plugin.json                    # Manifest de compatibilidad de Claude
├── skills/<nombre>/
│   ├── SKILL.md
│   ├── references/                    # Material detallado opcional
│   ├── scripts/                       # Automatización determinista opcional
│   └── assets/                        # Recursos opcionales
└── scripts/validate.py
```

El marketplace y el plugin `bipbop-skills` viven en la raíz. Así Claude y Codex resuelven el mismo árbol sin copias ni enlaces simbólicos que puedan divergir.

## Buenas prácticas para escribir skills

Estas reglas combinan el subconjunto común de las guías oficiales de [skills de OpenAI](https://developers.openai.com/plugins/build/skills), [paquetes de plugins de OpenAI](https://developers.openai.com/plugins/build/plugins), [plugins de Claude Code](https://code.claude.com/docs/en/plugins) y [marketplaces de Claude Code](https://code.claude.com/docs/en/plugin-marketplaces).

1. **Una meta reconocible por skill.** Divide workflows con disparadores, entradas o criterios de éxito distintos.
2. **`name` y `description` en el frontmatter.** El nombre usa `kebab-case` y coincide con su carpeta. La descripción explica qué hace la skill y cuándo debe activarse. Los pasos, formatos y reglas de seguridad van en el cuerpo.
3. **Instrucciones accionables.** Declara precondiciones, entradas, decisiones, efectos laterales, manejo de fallos y una verificación observable. Una skill debe decir cómo saber que terminó bien.
4. **Divulgación progresiva.** Mantén `SKILL.md` enfocado. Mueve material extenso a `references/`, scripts repetibles a `scripts/` y recursos estáticos a `assets/`. Enlaza cada archivo y explica cuándo cargarlo.
5. **Código solo cuando aporta determinismo.** No agregues un script si las instrucciones y herramientas existentes resuelven el trabajo de forma fiable. Documenta entradas, salidas, red y efectos laterales de todo ejecutable.
6. **Prioridad clara.** Las instrucciones explícitas de la persona y las reglas del sistema tienen prioridad sobre la guía de una skill. Evita reglas ambiguas o contradictorias.
7. **Sin datos privados.** No publiques nombres de clientes, correos, teléfonos, RUT, IDs de Notion, URLs internas, tokens, webhooks, código propietario ni ejemplos reconocibles. Revisa toda la historia que vas a empujar, no solo el estado final.
8. **Portabilidad real.** Usa rutas relativas dentro de la carpeta de la skill. No dependas de rutas locales, archivos fuera del plugin ni symlinks que escapen del repositorio.
9. **Prueba activación y resultado.** Verifica solicitudes que deben activar la skill, solicitudes que no deben activarla, casos ambiguos, errores de herramientas y calidad del resultado final.
10. **Cambios mínimos y revisables.** Una PR por tema. Cualquier cambio en scripts, hooks, MCP, permisos o dependencias recibe revisión de seguridad explícita.

Plantilla mínima:

```markdown
---
name: example-skill
description: Hace X. Usar cuando la persona pide Y o necesita Z.
---

# Example skill

## When to use
- Disparadores claros.
- Casos que quedan fuera.

## Procedure
1. Acción con un criterio de término observable.

## Pitfalls
- Fallos específicos y cómo evitarlos.

## Verification
- Evidencia que demuestra que la tarea terminó bien.
```

## Validar

```bash
python3 scripts/validate.py
claude plugin validate .
```

El validador local revisa JSON, coherencia entre manifests, frontmatter, nombres únicos, enlaces relativos, symlinks e identificadores sensibles. Claude agrega su validación oficial. Codex no expone un comando `plugin validate`; por eso el chequeo final usa una instalación aislada desde el marketplace.

Antes de abrir una PR, prueba ambos clientes en directorios aislados:

```bash
CODEX_TEST_HOME="$(mktemp -d)"
CODEX_HOME="$CODEX_TEST_HOME" codex plugin marketplace add ./ --json
CODEX_HOME="$CODEX_TEST_HOME" codex plugin add bipbop-skills@bipbop --json
CODEX_HOME="$CODEX_TEST_HOME" codex plugin list --json
rm -rf "$CODEX_TEST_HOME"

CLAUDE_TEST_HOME="$(mktemp -d)"
CLAUDE_CONFIG_DIR="$CLAUDE_TEST_HOME" claude plugin marketplace add ./
CLAUDE_CONFIG_DIR="$CLAUDE_TEST_HOME" claude plugin install bipbop-skills@bipbop
CLAUDE_CONFIG_DIR="$CLAUDE_TEST_HOME" claude plugin list --json
rm -rf "$CLAUDE_TEST_HOME"
```

Para validar la distribución Git, repite la prueba con `BipBop-Labs/bipbop-skills --ref <rama-o-tag>` después de publicar la referencia que quieres probar.

## Versiones y actualizaciones

El plugin `bipbop-skills` usa SemVer y mantiene la misma versión en `plugin.json` y `.claude-plugin/plugin.json`. Cada plugin adicional en `plugins/<nombre>/` tiene su propia versión, sincronizada entre sus dos manifests. Los catálogos no repiten la versión para evitar drift.

- **PATCH:** correcciones y ajustes compatibles.
- **MINOR:** una skill nueva o una capacidad compatible.
- **MAJOR:** renombrar o eliminar skills, cambiar comportamiento de forma incompatible, o exigir permisos/herramientas nuevas.

Cada release lleva tag `vMAJOR.MINOR.PATCH` y una entrada en [CHANGELOG.md](CHANGELOG.md). Los clientes detectan una actualización por el cambio de versión: si cambias un plugin sin subir su versión, quienes ya lo instalaron no reciben el cambio.

## Seguridad, privacidad y licencias

Lee [SECURITY.md](SECURITY.md) antes de reportar una vulnerabilidad. Todo aporte original de este repositorio se publica bajo [MIT](LICENSE). Marcas, libros y otros materiales de terceros pertenecen a sus respectivos titulares.

## Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md), agrega o actualiza las pruebas necesarias y abre una PR con el resultado de `python3 scripts/validate.py`.
