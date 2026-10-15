# Cómo volver a medir cuando el cliente aplique la primera ronda

Un solo comando repite los mismos medidores de la revisión sobre la carpeta de pantallas nueva y dice qué se cerró, qué persiste y qué
empeoró frente a la base (`mediciones/v2/`).

```bash
bash audit/v2/instrumentos/remedir.sh <carpeta_con_los_html_nuevos> [carpeta_de_salida]
```

Qué hace, en orden:

1. **Valida los medidores** con HTML de respuesta conocida (`verificar-fixtures.sh`). Si falla, se detiene: no se mide con instrumentos sin validar.
2. **Barrido por patrón** (`barrido.py`): busca en el código, con línea, las reglas que el informe pide cambiar (menú `.side .et{display:none}`,
   `.state .ico` descendiente, `--text-3: #66717F`, `<link>` a Google Fonts, ids repetidos, `.p4` sin relleno inferior, botón flotante) y lista los archivos
   cerrados, los que persisten y los nuevos.
3. **Medición en el navegador** (táctil, contraste, menú a 1000 px, tokens, instrumentos nuevos) con las fuentes reales.
4. **Totales frente a la base** (`comparar_medidas.py`), con las mismas 12 cuentas de la tabla «Qué se contó en las 50 pantallas» del informe.

Comprobado: ejecutado sobre el propio paquete del 12-oct reproduce la base **sin ninguna diferencia** (12 de 12 totales y 9 de 9 patrones).
La salida queda en `audit/v2/mediciones/remedicion-<fecha>/`.

Requisitos: Node 22 con Playwright (`NODE_PATH=/opt/node22/lib/node_modules`), Chromium en `/opt/pw-browsers` y Python 3. El comando solo lee la carpeta nueva.
