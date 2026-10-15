# Instrucciones para revisar a fondo una pantalla del paquete del 12-oct-2026 (segunda vuelta, 27 pantallas)

Revisas **pantallas de un equipo externo (DPROMA)** contra **nuestro** sistema de diseño **v2.15.0**. Estas 27 solo tuvieron
medición automática; ahora tienen revisión a fondo. Es la primera revisión de estas pantallas: **no comparas con entregas anteriores**.
**Solo revisas.** No modificas ninguna pantalla ni documento del cliente ni del repo. Lo único que escribes es
`/home/user/Investigaci-n-DPROMA-/audit/v2/raw/<pantalla>.json`.

Antes de empezar, lee también `audit/CRITERIOS-DE-REVISION.md`: lo que la persona que dirige el proyecto mira primero y cómo quiere la entrega.

## 0 · Las dos reglas de trabajo (decididas por la persona que dirige el proyecto)

**Regla 1 — Prioridad al cliente, salvo que sea crítico.** Lo que el cliente hizo se adopta y se documenta en el sistema; **no se le
pide cambiar**. Un hallazgo es **crítico** solo si cumple al menos uno de:

1. Falla de accesibilidad **medida**: contraste < 4,5:1 en texto o < 3:1 en controles; destino táctil < 24 px; control sin nombre
   accesible; contenido invisible bajo una preferencia del usuario.
2. Impide completar la tarea u oculta la acción primaria.
3. Acción irreversible o de dinero sin protección.
4. Contradice una decisión de producto de DPROMA (aviso del 28-sep, `FICHAS_TECNICAS.md`) o expone datos personales.

(El criterio de «rediseño marcado como crítico» no aplica a estas 27 pantallas.)

**Regla 2 — Lo no crítico no se descarta.** «No crítico» solo significa que no se le **exige** al cliente. Un cambio sencillo que (i) mejora
la estética de forma global o (ii) delata una causa raíz en el sistema de diseño o en otra parte, **se evalúa con una solución concreta**.

`decision.valor` ∈ `adoptar_cliente` · `exigir_cambio` (solo críticos) · `ajustar_sistema` (el sistema debe documentar lo que el cliente
hizo o corregirse él) · `decidir_diseño` (pregunta de diseño abierta) · `sin_accion`.

## 1 · Qué hay en tu dossier (ya medido: NO lo vuelvas a medir; cítalo)

`/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/briefs2/<pantalla>.json`

- `modo`: `cumplimiento` o `cobertura`. En `cobertura` (app de campo móvil) el sistema solo regula §7.3 y el contraste: lo que no esté
  regulado va a `cobertura` como patrón sin regla, **no** como «no cumple».
- `estado_vs_pdf_del_cliente`: el PDF del cliente declara cambios (C1–C18). Si dice `NO_ALINEADO`, el archivo **no contiene** lo que el
  PDF declara. Audita **lo que hay** y explica en `por_que_importa` que «no está aplicado».
- `mediciones_v2`: táctil, contraste (con ratio), menú a 1000 px, tokens usados−declarados, instrumentos nuevos (I1 icono vs botón ·
  I2 holgura inferior · I3 recorte e intersección de fijos · I4 alineación cabecera/celda · I5 ritmo vertical · I6 presupuesto de color ·
  I7 colisión de texto · I8 paridad de botones · I9 longitud de celdas · C2 10,5 px · C11 textos > 140 · efecto de `--sp-5`) y recortes
  horizontales a 1440/1280/1024. **Los instrumentos dan candidatos, no veredictos.** Falsos positivos conocidos: `main` con `overflow`
  (scroll del shell), `.sr`/`caption` (texto solo para lector de pantalla), tablas con scroll horizontal intencional. Un candidato solo es
  hallazgo cuando lo has visto en la captura o en el código.
- `barrido_por_patron`: resultado de buscar en el código del archivo, con línea, las reglas que el informe ya pide cambiar (menú
  `.side .et{display:none}`, `.state .ico` descendiente, `--text-3`, Google Fonts, ids repetidos, `.p4` sin relleno inferior, botón flotante).
  Úsalo como punto de partida: si el patrón está, cítalo con su línea.
- `ficha_tecnica_del_cliente`: la sección de `FICHAS_TECNICAS.md` de esa pantalla, **de dónde sale cada decisión según el cliente**. Una
  decisión documentada ahí no es «defecto» por ser distinta de nuestro gusto: solo lo es si rompe una regla medible del sistema. `null` =
  no hay ficha.
- `capturas`: en `/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/shots2/`
  (`--1440.png` página completa, `--1280-fold.png` primer pliegue). **Ábrelas con Read antes de afirmar nada visual.**
- Código fuente: el `archivo` del dossier. Obtén números de línea reales con `grep -n`. Nunca de memoria.

## 2 · Qué leer del sistema (v2.15.0)

1. `/tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad/sistema2150/sistema-diseno.md`
   — **fuente de verdad de los §**. Todo § que cites debe existir ahí.
2. Valores que cambiaron en 2.15.0: `--text-3` ahora `#5C6675`; `--serie-1..4`; `--surface-hover`; `--border-ctrl`; `--on-state`; `--chrome-*`;
   `--marca-*`; fuentes autoalojadas (D116: **sin** `<link>` a Google Fonts). `.state > .ico` (hijo directo) es el arreglo del icono de un
   botón dentro de una vista de estado.
3. Aviso del ingeniero del 28-sep (`AVISO_A_STUDIO_PADRON_2026-09-28.md`, en `.../scratchpad/v2zip/Actualizacion-12-10-26/`): solo para las
   pantallas del padrón (aquí: `06_padron_clientes`); señala desajustes evidentes (D6 «Reenviar liga» no se construye; D7 vigencia y D8
   duplicados pospuestos; D1 el alta es una página).

## 3 · Evidencia: lo que impide inventar (no negociable)

Cada hallazgo lleva:

- **`certeza`**: `medido` (un instrumento o una medición tuya reproducible) · `leido_en_codigo` (cita literal con línea) · `inferido`
  (deducido sin ver ni medir). **Un hallazgo `inferido` no puede ser severidad alta ni crítico.**
- **`reproduce`** (uno de):
  - `{"tipo":"medicion","instrumento":"I2_holgura_inferior","detalle":"gap 0 en header.p4"}` — debe existir en tu dossier o en un script
    tuyo que describas;
  - `{"tipo":"codigo","linea":412,"cita":"texto literal de esa línea"}` — **la cita debe ser subcadena literal de esa línea** (se validará
    por máquina);
  - `{"tipo":"captura","archivo":"36_recetas_despacho--1280-fold.png","region":"descripción de lo que se ve"}`.
- Un hallazgo sin § verificable del sistema o sin decisión documentada del cliente (D-n, FICHA) **no es hallazgo**: va a `sin_datos`.
- Nunca inventes un hex, selector, línea, ratio ni cifra. Si no puedes evaluar algo: `"no_evaluado"` y el motivo.
- **Atribución a DPROMA**: solo con cita literal e ID (D-n del aviso, `FICHAS`, o §). Si no, es nuestro sistema el que no lo dice.
- Si dudas entre dos lecturas, di las dos. No elijas la más dramática.
- **Antes de dar por cierta una afirmación sobre el archivo, compruébala en el archivo** (grep, medición o captura). En la primera vuelta
  una afirmación de este tipo («el archivo no declara `--border-ctrl`») resultó falsa y llegó hasta el informe.

Las fuentes reales (Inter, Michroma) se inyectaron al renderizar (no vienen en el paquete). Si una pantalla parece distinta a la del cliente
por la fuente, dilo; no lo cuentes como defecto de ellos.

## 4 · Severidades y alcance

- **F1 cumplimiento** — `alta`: riesgo real de accesibilidad o afecta al componente más repetido/visible. `media`: inconsistencia visible pero
  contenida. `baja`: diverge de nomenclatura, funciona.
- **F3 boost UI** 1–5 (1 reescritura, 5 excelente) con 5 dimensiones 0–4 (accesibilidad, rendimiento `no_evaluado`, theming, responsive, integridad).
- **Sin F4 ni F5** en esta vuelta: escribe `"f4_nielsen": []` y `"f5_investigacion": {"pain_points_evaluados": [], "usabilidad_para_el_area": "no evaluado"}`.
- Si dos pantallas comparten un defecto del mismo bloque copiado, repórtalo en cada una pero dilo en `por_que_importa` («mismo bloque que en …»).

## 5 · Esquema del JSON (`/home/user/Investigaci-n-DPROMA-/audit/v2/raw/<pantalla>.json`)

```json
{
  "pantalla": "36_recetas_despacho", "tier": "B", "modo": "cumplimiento | cobertura", "sha256": "(del dossier)",
  "estado_vs_pdf": "alineado | NO_ALINEADO | no_listado_en_pdf",
  "estados_auditados": ["lista"], "capturas": ["36_recetas_despacho--1440.png"],
  "observaciones_resueltas": [],
  "f1_cumplimiento": {"veredicto": "cumple | cumple_parcialmente | no_cumple", "hallazgos": [{
      "id": "v2-36recetas-01", "severidad": "alta", "regla": "§6.4 Vistas de estado",
      "dice_el_sistema": "cita literal corta del sistema", "hay_en_el_build": "literal o medición",
      "selector": ".state .btn", "linea": 412, "certeza": "medido", "reproduce": {},
      "critico": {"es": false, "criterio": null}, "decision": {"valor": "adoptar_cliente", "motivo": "..."},
      "por_que_importa": "consecuencia real para quien usa la pantalla"}]},
  "cerrados_desde_v1": [],
  "f3_boost_ui": {"puntuacion": 3, "dimensiones": {}, "justificacion": "...", "evidencia": ["..."]},
  "f4_nielsen": [], "f5_investigacion": {"pain_points_evaluados": [], "usabilidad_para_el_area": "no evaluado"},
  "cobertura": [{"patron": "...", "propuesta_de_regla": "redactada en el tono del sistema"}],
  "sin_datos": ["..."]
}
```

**No escribas `f2_tokens`**: lo inyecta el orquestador. Valida que parsea: `python3 -m json.tool <archivo>`.
Tu id de hallazgo: `v2-<numero+nombre corto>-NN` (p. ej. `v2-36recetas-01`).

## 6 · Cómo medir algo que no está en tu dossier

Servidor ya levantado: `http://127.0.0.1:8732/<pantalla>.html`. Playwright (CommonJS; **no ESM**):
```
cd /tmp/claude-0/-home-user-Investigaci-n-DPROMA-/914082f4-4ca1-5668-92da-6e6b458c949e/scratchpad && \
NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node tu-script.cjs
```
con `chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'})`. Para tener las mismas fuentes que el orquestador:
`await require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs').preparar(page)` justo después de crear la página. Oculta el
andamio `[data-andamio]` (ya lo hace `preparar`): no es UI de producto. **Nunca `file://`.** No uses `pkill`.
Guarda tus scripts en el scratchpad, nunca en el repo; descríbelos en `reproduce`.
