---
description: Comprueba qué skills externas del sistema de calidad están disponibles en esta sesión
---

Diagnóstico de solo lectura. **No instales nada** y no propongas instalar salvo que te lo pregunten
después.

Comprueba la disponibilidad de las siete skills del sistema con tres sondas, en este orden:

1. `ListPlugins` y `ListSkills` con los términos `ui-ux`, `impeccable`, `taste`, `slop`, `slides`,
   `diagram`, `understand`. Cubre lo sincronizado desde la cuenta de claude.ai.
2. Sistema de archivos, tolerante a fallo — si alguno no existe, no es un error:
   ```
   ls ~/.claude/plugins/marketplaces 2>/dev/null
   ls ~/.claude/plugins/repos 2>/dev/null
   ls ~/.claude/skills 2>/dev/null
   ```
   Cubre lo instalado con `/plugin` en una máquina local.
3. El listado de skills disponibles en esta sesión, que es lo único que refleja lo que de verdad se
   puede invocar. Si una skill aparece en el sistema de archivos pero no en el listado de la sesión,
   cuenta como **ausente**: está en disco pero no cargada.

Devuelve una tabla de siete filas, en español, con estas columnas:

| Skill | Fase | Presente | Fallback si no |
|---|---|---|---|

Las fases y los fallbacks están en `docs/skills-externas-routing.md` §1 y §4 — léelos, no los cites
de memoria.

Cierra con una línea que diga cuántas de las siete están disponibles y si eso limita algo de lo que
haya en marcha ahora mismo. Si no hay nada en marcha, no inventes una recomendación: basta la tabla.
