# Qué buscar según el tipo de tarea

Listas para el paso 3 de la skill. No hay que cubrir cada ítem: elige los que aplican al contexto del paso 1. Si la tarea no calza en ninguna sección, usa los cinco ejes del paso 3 tal cual.

## Comunicaciones (correos, avisos, comunicados, mensajes a clientes)

**Antes de buscar, define:**

- El tipo de mensaje: transaccional (confirmación, aviso de servicio), comercial o marketing, interno, institucional, o respuesta a un reclamo. La regulación cambia mucho entre transaccional y comercial.
- El país del destinatario, y si es una persona o una empresa.
- La relación: cliente actual, prospecto, empleado o proveedor.

**Obligatorio:**

- Reglas de comunicación comercial y de spam en la jurisdicción del destinatario. Ejemplos: CAN-SPAM en Estados Unidos; ePrivacy, GDPR y PECR en la UE y el Reino Unido; la ley de protección del consumidor y la de datos personales en países de Latinoamérica.
- Protección del consumidor cuando el mensaje anuncia cambios de precio, de condiciones o de contrato: plazos de aviso, derecho a terminar y forma de notificación.
- Datos personales: qué se puede incluir en el mensaje y qué base legal permite enviarlo.
- Reglas del sector cuando aplican, como finanzas, salud, telecomunicaciones o educación.

**Guías y práctica:**

- La guía de tono o de marca de la propia organización. Va primero y gana ante cualquier guía externa.
- Lenguaje claro: ISO 24495-1 y las guías públicas de plain language.
- Plantillas públicas de organizaciones comparables para el mismo tipo de mensaje: avisos de incidente, de alza de precio, de cambio de términos, de despido o de cierre.
- Prácticas de comunicación de crisis o de incidentes, cuando el mensaje da una mala noticia.

**Errores comunes:**

- Esconder la información importante al final.
- Prometer lo que no está decidido.
- Faltar a un plazo legal de aviso.
- Usar un tono que contradice la marca.

## Software (implementar una feature, elegir una librería, diseñar una API)

**Antes de buscar, define:** lenguaje, framework y versiones exactas; dónde corre; restricciones de seguridad o de compliance.

**Obligatorio:**

- Especificaciones del protocolo o del formato: RFCs, W3C, WHATWG y los estándares de la industria.
- Compliance que toca el código, como PCI DSS para pagos, leyes de datos personales y accesibilidad (WCAG).

**Guías y práctica:**

- La documentación oficial y el changelog de la versión que usa el proyecto, no de la última versión.
- OWASP (Cheat Sheets y ASVS) para todo lo que toca autenticación, entrada de usuarios, secretos o permisos.
- Si existe una librería mantenida que ya resuelve el problema: actividad reciente, licencia y adopción.
- Implementaciones de referencia en proyectos conocidos.
- Lo que el propio repositorio ya hace en casos parecidos, que se busca antes que en internet.

**Errores comunes:**

- Issues abiertos y CVEs de las librerías candidatas.
- Postmortems públicos sobre el mismo tipo de sistema.
- Las razones por las que la gente abandonó un enfoque popular.

## Procesos y políticas (onboarding, vacaciones, gestión de incidentes, aprobaciones)

**Antes de buscar, define:** el país y la legislación laboral o sectorial que aplica, el tamaño de la organización y quién va a operar el proceso.

**Obligatorio:**

- La ley aplicable y la guía del regulador. Por ejemplo, el código del trabajo para políticas de personas o la regulación sectorial para procesos de compliance.
- Los contratos y las certificaciones vigentes de la organización, como ISO 27001 o SOC 2, que ya imponen controles.

**Guías y práctica:**

- Marcos reconocidos: ISO, NIST, ITIL, o el estándar del sector.
- Handbooks públicos de organizaciones comparables, como los de empresas que publican sus procesos o los manuales de servicios de gobierno.
- Las políticas, ADRs y procesos que la organización ya tiene. Un proceso nuevo debe calzar con los existentes.

**Errores comunes:**

- Procesos copiados de organizaciones mucho más grandes.
- Pasos sin responsable.
- Políticas que nadie puede cumplir y por lo tanto nadie cumple.
