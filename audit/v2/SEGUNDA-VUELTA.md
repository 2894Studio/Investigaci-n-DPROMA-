# Segunda vuelta · 27 pantallas con revisión a fondo

Estado: fichas en `raw/` (27), verificación adversarial en `verif/verif-4..7.json`. Nada de esto ha llegado al informe del ingeniero.

## Resultado de la verificación

101 hallazgos altos o críticos revisados por otras personas con medición propia: **91 confirmados, 10 exagerados, 0 refutados**.
De los 65 marcados críticos: 59 confirmados y 6 exagerados (`33cfe-03`, `36recetas-02`, `39viatico-01`, `45autcomp-01`, `42altages-04`, `10dprimi-02`).

## Los 65 críticos por patrón

| Patrón | Pantallas | Ids |
|---|---:|---|
| Menú lateral sin nombre accesible (861–1100 px) | 16 | 29-01, 30-01, 33-02, 35-01, 36-01, 37-01, 38-02, 39-02, 40-02, 42-03, 43-02, 44-03, 45-02, 50-03, 56-02, 57-02 |
| Destino táctil < 24 px | 22 hallazgos | 03-02, 06-03, 06-04, 08-01, 11-01, 30-04, 35-02, 35-03, 37-02, 38-01, 40-01, 42-01, 42-02, 43-01, 44-01, 44-02, 50-01, 50-02 + exagerados 33-03, 36-02, 39-01, 45-01 |
| Borde de campo < 3:1 (`--border-ctrl` declarado y sin usar) | 9 | 07-01, 35-04, 36-03, 37-03, 38-03, 42-05, 43-04, 44-05, 45-03 |
| Icono del botón sobre verde a 1,03:1 (`.state .ico`) | 6 | 02-01, 03-01, 06-02, 30-02, 56-01, 57-01 |
| Texto < 4,5:1 | 6 | 02-02 y 30-03 y 36-04 (solo con el cursor encima), 04-01, 29-02, 33-01 |
| Botón flotante sobre «Crear expediente» | 3 | 43-03, 44-04, 42-04 (exagerado: tapa el 33–38 % del rótulo, el botón sigue pulsable) |
| Contra una decisión de DPROMA o contenido invisible | 3 | 06-01 (Reenviar liga, D6), 10-01 (`prefers-reduced-motion` deja las burbujas en opacity 0), 10-02 (exagerado: S-19 es un supuesto de quien hizo 47, no decisión de DPROMA) |

## Correcciones de cifras que deben entrar antes de citarlas

- Bordes de campo: 1,41:1 claro y 1,24:1 oscuro (no 1,31/1,40). Buscador de 37: 1,38 y 1,22.
- `03-kanban-02`: 16 destinos, no 17. `03-kanban-04`: 40 nodos < 12 px, no 42.
- `40-usuarios-03`: «Acciones» mide 168,5 px y 21 nodos fuera del borde, no 62 px ni 39.
- `11-login-01`: «Reenviarlo» (22 px) vive dentro de una frase; existe la vía de la app Authenticator, así que «impide entrar» es excesivo.
- `57-menucuenta-01`: «Cerrar sesión» está en la vista vacía, no en la de error.

## Decisiones de criterio pendientes de la persona que dirige

1. **Destino < 24 px.** WCAG 2.5.8 se cumple por espaciado en al menos 4 casos (33-03, 36-02, 39-01, 45-01). §7.3 y el criterio 1 literal sí los incumplen.
2. **Borde de campo < 3:1** (9 pantallas) e **icono sin contraste** (6): el criterio 1 los cubre literalmente; el arreglo es un token ya declarado / `.state > .ico`.
3. **Botón flotante** (criterio 2): ¿basta con tapar un tercio del rótulo para exigirlo?
