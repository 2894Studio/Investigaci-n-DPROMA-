# Instrucciones para auditar a fondo una pantalla del paquete 12-oct-2026 (auditoría v2)

Auditas **pantallas de un equipo externo (DPROMA)** contra **nuestro** sistema de diseño **v2.15.0**.
**Solo auditas.** No modificas ninguna pantalla ni documento del cliente ni del repo. Lo único que escribes es
`/home/user/Investigaci-n-DPROMA-/audit/v2/raw/<pantalla>.json`.

## 0 · Las dos reglas de trabajo (decididas por la persona que dirige el proyecto)

**Regla 1 — Prioridad al cliente, salvo que sea crítico.** Lo que el cliente hizo se adopta y se documenta en el
sistema; **no se le pide cambiar**. Un hallazgo es **crítico** solo si cumple al menos uno de:

1. Falla de accesibilidad **medida**: contraste < 4,5:1 en texto o < 3:1 en controles; destino táctil < 24 px; control sin
   nombre accesible; contenido invisible bajo una preferencia del usuario.
2. Impide completar la tarea u oculta la acción primaria.
3. Acción irreversible o de dinero sin protección.
4. Contradice una decisión de producto de DPROMA (aviso del 28-sep, `FICHAS_TECNICAS.md`) o expone datos personales.
5. La persona lo marcó «rediseño crítico» **y es viable** (solo en las 4 pantallas: Tickets TI, acordeón de sucursales,
   Asistente, Mi día). La viabilidad la decide la Fase 4; tú solo diagnosticas.

**Regla 2 — Lo no crítico no se descarta.** «No crítico» solo significa que no se le **exige** al cliente. Un cambio
sencillo que (i) mejora la estética de forma global o (ii) delata una causa raíz en el sistema de diseño o en otra
parte, **se evalúa con una solución concreta**. Lo demás se resuelve a favor del cliente.

`decision.valor` ∈ `adoptar_cliente` · `exigir_cambio` (solo críticos y regresiones) · `ajustar_sistema` (el sistema debe
documentar lo que el cliente hizo o corregirse él) · `decidir_diseño` (pregunta de diseño abierta) · `sin_accion`.

## 1 · Qué hay en tu brief (ya medido: NO lo vuelvas a medir; cítalo)

`/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/briefs2/<pantalla>.json`

- `observaciones_del_usuario` — lo que la persona vio en sus capturas (hoja + texto). **Cada una exige una respuesta
  explícita** en `observaciones_resueltas`. Algunas pantallas no tienen ninguna; entonces audítalas igual.
- `estado_vs_pdf_del_cliente` — **IMPORTANTE.** El PDF del cliente declara cambios (C1–C18). El orquestador los verificó
  contra el archivo. Si dice `NO_ALINEADO`, el archivo recibido **no contiene** lo que el PDF declara (p. ej. `24_tickets`
  conserva `--text-3:#66717F` y 19 declaraciones < 12 px, el PDF dice 0). Audita **lo que hay**; marca los defectos que el
  PDF decía haber arreglado como `estado_vs_v1: "persiste"` y explícalo en `por_que_importa` como «no aplicado», **no como
  regresión** (regresión = algo que v1 no tenía y v2 sí).
- `mediciones_v2` — táctil, contraste (con ratio), menú a 1000 px, tokens usados−declarados, **instrumentos nuevos**
  (I1 icono vs botón · I2 holgura inferior · I3 recorte e intersección de fijos · I4 alineación cabecera/celda ·
  I5 ritmo vertical · I6 presupuesto de color · I7 colisión de texto · I8 paridad de botones · I9 longitud de celdas ·
  C2 10,5 px · C11 textos > 140 · efecto de `--sp-5`) y recortes horizontales a 1440/1280/1024.
  **Los instrumentos dan candidatos, no veredictos.** Ejemplos de falsos positivos conocidos: `main` con `overflow`
  (es el scroll del shell), `.sr`/`caption` (texto solo para lectores de pantalla), tablas con scroll horizontal
  intencional. Un candidato solo es hallazgo cuando lo has visto en la captura o en el código.
- `delta_vs_v1` y `v1` — qué hallazgos tenía v1 (ids y reglas en `audit/raw/<pantalla>.json`). Para cada uno de los de
  severidad alta de v1 di si **persiste / cerrado / regresión**, con evidencia.
- `ficha_tecnica_del_cliente` — la sección de `FICHAS_TECNICAS.md`: **de dónde sale cada decisión según el cliente**.
  Es la fuente para entender qué es deliberado. Una decisión documentada ahí no es «defecto» por ser distinta de
  nuestro gusto: solo lo es si rompe una regla medible del sistema. `null` = no hay ficha (las `01_`–`14_` no la tienen).
- `capturas` — en `/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/shots2/`
  (`--1440.png` página completa, `--1280-fold.png` primer pliegue). **Ábrelas con Read antes de afirmar nada visual.**
- Código fuente: el `archivo` del brief. Obtén números de línea reales con `grep -n`. Nunca de memoria.

## 2 · Qué leer del sistema (v2.15.0, no 2.13.3)

1. `/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/sistema2150/sistema-diseno.md`
   — **fuente de verdad de los §**. Todo § que cites debe existir ahí.
2. `scratchpad/CHECKLIST-SISTEMA.md` — destilado de la 2.13.3 con los § más usados (atajo; en caso de duda manda el anterior).
3. Lo nuevo de 2.15.0: §13.9 (bloque cuyo alto lo fija un dato externo); valores de tokens que cambiaron: `--text-3` ahora
   `#5C6675`; `--serie-1..4`; `--surface-hover`; `--border-ctrl`; `--on-state`; `--chrome-*`; `--marca-*`; fuentes autoalojadas
   (D116: **sin** `<link>` a Google Fonts). `.state > .ico` (hijo directo) es el arreglo del defecto 2.13.4: **el icono de un
   botón dentro de una vista de estado heredaba el gris de `.state .ico`**.
4. F5: `scratchpad/PAIN-POINTS-POR-AREA.md` y `data/insights/*.json` del repo. Cita `pp-NNN` + documento.
5. Aviso del ingeniero del 28-sep (`AVISO_A_STUDIO_PADRON_2026-09-28.md`, en `.../v2zip/Actualizacion-12-10-26/`) solo para las
   pantallas del padrón (21, 27, 41, 58, 59): lo evalúa además la Fase 3; tú señala desajustes evidentes.

## 3 · Evidencia: lo que impide inventar (no negociable)

Cada hallazgo y cada respuesta a una observación lleva:

- **`certeza`**: `medido` (un instrumento o una medición tuya reproducible) · `leido_en_codigo` (cita literal con línea) ·
  `inferido` (deducido sin ver ni medir). **Un hallazgo `inferido` no puede ser severidad alta ni crítico.**
- **`reproduce`** (uno de):
  - `{"tipo":"medicion","instrumento":"I2_holgura_inferior","detalle":"gap 0 en header.p4"}` — debe existir en tu brief
    o en un script tuyo que describas;
  - `{"tipo":"codigo","linea":412,"cita":"texto literal de esa línea"}` — **la cita debe ser subcadena literal de esa línea**
    (se validará por máquina);
  - `{"tipo":"captura","archivo":"24_tickets--1280-fold.png","region":"descripción de lo que se ve"}`.
- Un hallazgo sin § verificable del sistema o sin decisión documentada del cliente (D-n, FICHA) **no es hallazgo**: va a `sin_datos`.
- Un F5 sin `pp-NNN` + documento va a `sin_datos`.
- Nunca inventes un hex, selector, línea, ratio ni cifra. Si no puedes evaluar algo: `"no_evaluado"` y el motivo.
- **Atribución a DPROMA**: solo con cita literal e ID (D-n del aviso, `FICHAS`, o §). Si no, es nuestro sistema el que no lo dice.
- Si dudas entre dos lecturas, di las dos. No elijas la más dramática.

Las fuentes reales (Inter, Michroma) se inyectaron al renderizar (no vienen en el paquete). Si una pantalla parece distinta a
la del cliente por la fuente, dilo; no lo cuentes como defecto de ellos.

## 4 · Severidades y fases

- **F1 cumplimiento** — `alta`: riesgo real de accesibilidad o afecta al componente más repetido/visible. `media`:
  inconsistencia visible pero contenida. `baja`: diverge de nomenclatura, funciona.
- **F3 boost UI** 1–5 (1 reescritura, 5 excelente) con 5 dimensiones 0–4 (accesibilidad, rendimiento `no_evaluado`, theming, responsive, integridad).
- **F4 Nielsen** (10 heurísticas, 0–4; `n/a` si no aplica) y **F5 investigación**: **solo Tier A** (y F5 de `54`).
  En Tier B escribe `"f4_nielsen": []` y `"f5_investigacion": {"pain_points_evaluados": [], "usabilidad_para_el_area": "no evaluado — Tier B"}`.
- **Tier A**: F1–F5 completas + respuesta a cada observación + causa raíz. **Tier B**: F1, F3 + observaciones.

## 5 · Respuesta a cada observación del usuario (obligatoria)

Para cada entrada de `observaciones_del_usuario` escribe un objeto en `observaciones_resueltas`:

```json
{"hoja": 3, "texto_usuario": "...",
 "veredicto": "confirmada | parcial | no_confirmada | sin_datos",
 "evidencia": [{"certeza": "medido", "reproduce": {...}, "dato": "lo que se ve/mide, concreto"}],
 "causa_raiz": "qué la produce (token, regla, componente) o «no determinada»",
 "solucion_propuesta": "cambio concreto, en el lenguaje del sistema (tokens/§), o null",
 "tipo_de_cambio": "sencillo | medio | rediseño",
 "critico": {"es": true, "criterio": 2},
 "decision": {"valor": "exigir_cambio", "motivo": "..."}}
```

Si la observación es de una pantalla que ya no se parece a lo que la persona vio (porque el archivo recibido es otro), dilo en `veredicto: "sin_datos"`.
No fuerces una confirmación: si no lo ves, **«no_confirmada»** es una respuesta válida.

## 6 · Esquema del JSON (`/home/user/Investigaci-n-DPROMA-/audit/v2/raw/<pantalla>.json`)

```json
{
  "pantalla": "27_padron_clientes", "tier": "A", "sha256": "(del brief)",
  "estado_entrega": "(del brief)", "estado_vs_pdf": "alineado | NO_ALINEADO | no_listado_en_pdf",
  "estados_auditados": ["lista"], "capturas": ["27_padron_clientes--1440.png"],
  "observaciones_resueltas": [ ... ],
  "f1_cumplimiento": {"veredicto": "cumple | cumple_parcialmente | no_cumple", "hallazgos": [{
      "id": "v2-27padron-01", "severidad": "alta", "regla": "§6.4 Vistas de estado",
      "dice_el_sistema": "cita literal corta del sistema", "hay_en_el_build": "literal o medición",
      "selector": ".state .btn", "linea": 412, "certeza": "medido", "reproduce": {...},
      "estado_vs_v1": "persiste | cerrado | regresion | nuevo",
      "critico": {"es": false, "criterio": null}, "decision": {"valor": "adoptar_cliente", "motivo": "..."},
      "por_que_importa": "consecuencia real para quien usa la pantalla"}]},
  "cerrados_desde_v1": [{"id_v1": "f1-27padron-03", "evidencia": "..."}],
  "f3_boost_ui": {"puntuacion": 3, "dimensiones": {...}, "justificacion": "...", "evidencia": ["..."]},
  "f4_nielsen": [{"n": 1, "heuristica": "...", "severidad": 3, "hallazgo": "...", "selector": "...", "certeza": "...", "reproduce": {...}}],
  "f5_investigacion": {"pain_points_evaluados": [{"pp": "pp-081", "documento": "data/insights/....json", "cobertura": "cubre | ignora | contradice", "evidencia": "..."}], "usabilidad_para_el_area": "2–4 frases"},
  "cobertura": [{"patron": "...", "propuesta_de_regla": "redactada en el tono del sistema"}],
  "sin_datos": ["..."]
}
```

**No escribas `f2_tokens`**: lo inyecta el orquestador. Valida que parsea: `python3 -m json.tool <archivo>`.

## 7 · Modo cobertura

Las pantallas de app de campo móvil se auditan con `modo: "cobertura"` (sus hallazgos van a `cobertura`; aplican §7.3 y contraste).
`05_app_cliente` es del cliente móvil: trátala así.

## 8 · Cómo medir algo que no está en tu brief

Servidor ya levantado: `http://127.0.0.1:8732/<pantalla>.html`. Playwright (CommonJS; **no ESM**):
```
cd /tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad && \
NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node tu-script.cjs
```
con `chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'})`. Para tener las mismas fuentes que el
orquestador: `await require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs').preparar(page)` justo después de crear la
página. Oculta el andamio `[data-andamio]` (ya lo hace `preparar`): no es UI de producto. **Nunca `file://`.** No uses `pkill`.
Guarda tus scripts en el scratchpad, nunca en el repo; descríbelos en `reproduce`.
