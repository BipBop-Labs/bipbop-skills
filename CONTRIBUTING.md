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

## Revisión

Una PR debe explicar:

- el objetivo de la skill o cambio;
- qué solicitudes deben y no deben activarla;
- qué efectos laterales o permisos requiere;
- qué validaciones y pruebas se ejecutaron;
- el origen y licencia de cualquier material de terceros.

Los cambios en scripts, hooks, MCP, dependencias, red o permisos requieren revisión de seguridad explícita. No incluyas secretos ni datos de clientes en commits, ramas, issues o ejemplos.

## Releases

La versión canónica debe coincidir en `plugin.json` y `.claude-plugin/plugin.json`. No agregues una versión a las entradas de marketplace. Usa SemVer y tags `vMAJOR.MINOR.PATCH`.
