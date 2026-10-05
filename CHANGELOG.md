# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) y las versiones siguen [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Plugin `adr` (0.1.0) en `plugins/adr/`: Architecture Decision Records para cualquier repositorio, con `/adr:init`, `/adr:distill`, `/adr:new`, `/adr:review`, validador `validate-adrs.py` sin dependencias y hook Stop opcional desactivado por defecto. El marketplace ahora admite plugins adicionales en `plugins/<nombre>/`.
- Plugin `adr` (0.2.0): `validate-adrs.py` acepta `--fail-on-proposed`, que marca como error los ADRs que siguen en `proposed`. Está pensado para CI, para que no se integre un ADR que nadie aceptó ni rechazó; los snippets de CI de `--print-setup` ahora usan `--strict --fail-on-proposed`.
- Plugin `bipflow` (0.1.0) en `plugins/bipflow/` con las skills `commit` y `pr`, para que un agente cree commits atómicos y abra pull requests con secciones para quien revisa y para el cliente. Se invocan como `/bipflow:commit` y `/bipflow:pr`.
- Skill `krug-usability-testing`, basada en "Rocket Surgery Made Easy" de Steve Krug, para planear, ejecutar y revisar tests de usabilidad y validación temprana de conceptos.

### Changed

- `ousterhout-software-design`: en review, reportar solo red flags con acción; sin elogios ni ítems sin recomendación.

### Fixed

- Plugin `adr` (0.2.0): `validate-adrs.py` ya no reporta como obsoletas las rutas de `paths` que empiezan con punto, como `.github/workflows/ci.yml`. Antes les quitaba el punto inicial y avisaba que no coincidían con nada en el repositorio.

## [0.2.0] - 2026-09-10

### Added

- Skill `create-skills` para crear, revisar, validar y distribuir skills portables.
- Skill `simple-writing`, migrada desde el repositorio de skills de Revi.

## [0.1.0] - 2026-09-10

### Added

- Marketplace público compatible con Claude Code, Codex y ChatGPT.
- Skills `best-prompting`, `microcopy` y `ousterhout-software-design`.
- Validación local, política de seguridad y guía de contribución.
