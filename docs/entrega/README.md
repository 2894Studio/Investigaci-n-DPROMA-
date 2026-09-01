# Entrega a desarrollo — módulo de clientes

Qué hay aquí y cómo se regenera.

| Archivo | Qué es |
|---|---|
| `entrega-padron-desarrollo.html` | El documento. Se escribe aquí, con CSS de impresión (`@page`, control de saltos). |
| `img/` | Las capturas embebidas, generadas con el navegador. |
| `originales/` | Las cuatro maquetas que entregó DPROMA, tal cual llegaron. Son la referencia del «antes» y las necesita el script de métricas. |
| `metricas.py` | Recalcula la tabla de la §2 desde los archivos y la contrasta con el documento. |

La salida —`web/entregables/entrega-padron-desarrollo.pdf`— se publica en el sitio y se
descarga desde el entregable del padrón.

## Comprobar que las cifras del documento siguen siendo ciertas

```sh
python3 docs/entrega/metricas.py --verifica
```

Sale con código 1 y nombra la divergencia si alguna cifra de la §2 ya no coincide con los
archivos. Conviene ejecutarlo cada vez que se toque una de las cuatro pantallas.

## Regenerar el PDF

No hay pandoc ni weasyprint en este entorno; sí Chromium. El documento se imprime con
`page.pdf()` de Playwright sobre el HTML servido por HTTP:

1. Servir la carpeta `docs/` (`npx http-server docs -p 8897`).
2. Abrir `http://localhost:8897/entrega/entrega-padron-desarrollo.html` en Chromium.
3. Imprimir con `printBackground:true` y `preferCSSPageSize:true` a
   `web/entregables/entrega-padron-desarrollo.pdf`.

## Cómo se generaron las capturas

Con Chromium a 1440×780, tema claro, y el panel `[data-andamio]` oculto.

Las del **«después»** sirven los subconjuntos de fuente reales, descargados desde las mismas
URLs de Google Fonts que enlazan las maquetas: la salida del navegador a Google está bloqueada
en este entorno, pero los archivos publicados siguen apuntando a Google Fonts, que es lo
correcto en producción.

Las del **«antes»** se renderizan **sin inyectar ninguna fuente**, a propósito. Las cuatro
maquetas originales declaran `Inter` sin cargarla nunca —cero hojas de estilo enlazadas,
`document.fonts.size === 0`—, así que en un navegador real se veían en la fuente del sistema.
Inyectarles Inter mostraría un «antes» mejor que el real.
