# Entradas de Tesla (pendientes)

tesla.com devuelve «Access Denied» (403) al navegador automatizado, así que Tesla entra al
benchmark solo con evidencia parcial (ficha pública de su app).

Para completarlo, desde un navegador normal:

1. Abrir `https://www.tesla.com/es_mx/charging`, la página de Supercharger y la de
   Supercharger for Business.
2. Guardar captura de página completa (escritorio) y, si se puede, una en móvil; o «Guardar como PDF».
3. Dejar los archivos en esta carpeta.

Con eso se puntúan los criterios hoy «sin evaluar» de Tesla (solo lo que se vea en las capturas),
se añade su captura a la galería y se actualiza `datos/benchmark.json`. Después:
`python3 scripts/gen-benchmark-web.py`.
