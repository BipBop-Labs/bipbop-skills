# Contribuir

## Agregar o cambiar una skill

1. Crea `skills/<nombre-kebab-case>/SKILL.md`.
2. Incluye `name` y `description` en frontmatter. El nombre debe coincidir con la carpeta y la descripción debe explicar capacidad y disparadores.
3. Mantén una sola meta reconocible. Separa workflows con disparadores, entradas o criterios de éxito distintos.
4. Mueve el detalle opcional a `references/`, la automatización determinista a `scripts/` y recursos estáticos a `assets/`.
5. Usa rutas relativas y verifica que cada enlace exista.
6. Inventa ejemplos desde cero. No adaptes casos reales ni publiques identificadores, URLs o datos internos.
7. Ejecuta `python3 scripts/validate.py`.
8. Prueba solicitudes positivas, negativas, ambiguas y fallidas en al menos uno de los hosts soportados.
9. Actualiza la tabla del README y el CHANGELOG cuando corresponda.

## Agregar o cambiar un plugin

Los plugins adicionales viven en `plugins/<nombre>/` y se instalan por separado (`adr`, `bipflow`).

1. Crea `plugins/<nombre>/plugin.json` y `plugins/<nombre>/.claude-plugin/plugin.json` con el mismo `name` y `version`. El segundo declara `"skills": "./skills/"`.
2. Agrega las skills en `plugins/<nombre>/skills/<skill>/SKILL.md`, con las mismas reglas de arriba.
3. Registra el plugin en `.claude-plugin/marketplace.json` y `.agents/plugins/marketplace.json` con source `./plugins/<nombre>`.
4. Agrega un `README.md` al plugin y una fila en la tabla "Plugins adicionales" y en la sección de instalación del README raíz.
5. Ejecuta `python3 scripts/validate.py`.

## Revisión

Una PR debe explicar:

- el objetivo de la skill o cambio;
- qué solicitudes deben y no deben activarla;
- qué efectos laterales o permisos requiere;
- qué validaciones y pruebas se ejecutaron;
- el origen y licencia de cualquier material de terceros.

Los cambios en scripts, hooks, MCP, dependencias, red o permisos requieren revisión de seguridad explícita. No incluyas secretos ni datos de clientes en commits, ramas, issues o ejemplos.

## Releases

La versión canónica debe coincidir en `plugin.json` y `.claude-plugin/plugin.json`. Cada plugin en `plugins/<nombre>/` lleva su propia versión, sincronizada entre sus dos manifests. Sube la versión del plugin que cambiaste: sin ese cambio, quienes ya lo instalaron no reciben la actualización. No agregues una versión a las entradas de marketplace. Usa SemVer y tags `vMAJOR.MINOR.PATCH`.
