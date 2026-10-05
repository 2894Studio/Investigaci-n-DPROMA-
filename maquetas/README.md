# Maquetas de SIO-DPROMA

Maquetas HTML de pantallas de SIO-DPROMA, organizadas por funcionalidad. Material de
referencia recibido del equipo de DPROMA: **no es código de este repositorio y no se
publica** con la web de hallazgos (`web/`). Vive aquí para que el análisis de research y
las auditorías de diseño puedan leerlo sin depender de un archivo subido en cada sesión.

## Paquetes

| Paquete | Fecha | Pantallas |
|---|---|---|
| `SIO-por-funcionalidad-2026-09-30/` | 30 de septiembre de 2026 | 59 maquetas + índice |

## `SIO-por-funcionalidad-2026-09-30/`

Punto de entrada: abre `SIO-por-funcionalidad-2026-09-30/index.html` en el navegador. Es un
índice con el nombre legible de cada pantalla y su enlace; no requiere servidor ni build.

| Carpeta | Área | Archivos |
|---|---|---|
| `01-principal/` | Tablero (resumen ejecutivo) | 2 |
| `02-padron-de-clientes/` | Padrón de clientes: listado, ficha, alta, edición | 9 |
| `03-icev-instalacion-de-cargadores/` | ICEV: órdenes, instaladores, material, app de campo | 14 |
| `04-tramites-vehiculares-y-cfe/` | Gestoría, Administración Vehicular, CFE | 12 |
| `05-direccion-y-administracion/` | Viáticos, compras, cobranza, facturación, asistencia | 14 |
| `06-soporte/` | Tickets y asistente D-PRIMI | 3 |
| `07-transversales/` | Login, acceso, error, estados de pantalla, menú de cuenta | 5 |

Siete de los archivos llevan prefijo `studio_`: son la versión del 8 de septiembre de la
misma pantalla, conservada para poder comparar la iteración. El índice las etiqueta como
*"Versión Studio (8-sep)"*.

## Notas técnicas

- Cada archivo es HTML autocontenido: los design tokens van en un bloque `:root` al inicio
  y el CSS es inline. No hay hoja de estilos compartida que haya que servir aparte.
- Únicas dependencias externas: Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`)
  y Chart.js desde `cdn.jsdelivr.net` en las pantallas con gráficas. Sin estas, la maqueta
  sigue siendo legible pero pierde la tipografía y las gráficas.
- Para renderizar con Playwright, sírvelas por HTTP local
  (`python3 -m http.server --bind 127.0.0.1`) en vez de `file://` — ver el apartado de
  troubleshooting de la skill `sio-dproma-design-audit`.
- Varias maquetas incluyen bandas de aviso que declaran su propio estado (p. ej.
  *"Propuesta — sin backend"*). Son parte del material original: indican qué pantallas
  todavía no tienen servicio detrás, no un error de la maqueta.

## Relación con la auditoría de diseño

La skill `sio-dproma-design-audit` parte de que *no existe un catálogo canónico de qué
pantallas debería tener SIO-DPROMA* y que el material auditado no vive en el repo. Este
paquete cambia las dos cosas en parte: es el inventario de pantallas más completo que
tenemos y ya está aquí. Aun así **no es un catálogo canónico**: son maquetas de propuesta,
no el build de producción (`sio-qa.dproma.com`), así que no sirve como referencia de "qué
hay implementado hoy" ni como base para reportar pantallas faltantes. Para auditar
conformidad sigue haciendo falta el export real de producción.
