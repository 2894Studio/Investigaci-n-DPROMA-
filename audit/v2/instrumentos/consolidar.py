"""Consolida la auditoría v2: lee SOLO los JSON ya validados/verificados y las mediciones; no inventa nada.
Uso: python3 -I consolidar.py   ->  audit/v2/INFORME-v2.md  +  audit/v2/consolidado-v2.json"""
import json, glob, os, re, collections
R = '/home/user/Investigaci-n-DPROMA-/audit/v2'
L = lambda p: json.load(open(p, encoding='utf-8'))
raw = {os.path.basename(f)[:-5]: L(f) for f in sorted(glob.glob(f'{R}/raw/[0-9]*.json'))}
aviso = L(f'{R}/raw/_aviso-conformidad.json')
claims = L(f'{R}/mediciones/v2/claims.json'); man = L(f'{R}/MANIFIESTO.json')['archivos']
delta = L(f'{R}/mediciones/delta-v1-v2.json')
nue = {k: L(f'{R}/mediciones/{k}/nuevos.json') for k in ('v1-control', 'v2')}
for k in nue: nue[k].pop('_paleta', None)
ver = {}
for f in glob.glob(f'{R}/verif/verif-*.json'):
    for v in L(f)['verificaciones']: ver[v['id']] = v
conc = L(f'{R}/replica/concordancia.json') if os.path.exists(f'{R}/replica/concordancia.json') else {}
out = []; P = out.append

# ---------- 1. integridad de la entrega
pdf = claims['por_pantalla']
ausentes = sorted(n[:-5] for n, v in pdf.items() if v.get('estado'))
no_alin = sorted(n[:-5] for n, v in pdf.items() if not v.get('estado') and any(e == 'NO_confirmado' for e in v['codigos'].values()))
conf = sorted(n[:-5] for n, v in pdf.items() if not v.get('estado') and not any(e == 'NO_confirmado' for e in v['codigos'].values()))
nuevas = sorted(f['pantalla'] for f in delta if f['estado'] == 'nueva'); identicas = sorted(f['pantalla'] for f in delta if f['estado'] == 'identica')
inline = sorted(n[:-5] for n, v in pdf.items() if not v.get('estado') and v.get('lt12_inline'))
htmls = [n[:-5] for n in man if n.endswith('.html')]
profundas = sorted(raw)
mecanicas = sorted(set(htmls) - set(profundas))

# ---------- 2. hallazgos críticos agrupados por tema
TEMAS = [
 ('menu', 'Menú lateral colapsado (861–1100 px) sin nombre accesible', lambda t: 'side .et' in t and ('§7.2' in t or 'nombre accesible' in t or 'aria' in t),
  '`.side .et{display:none}` deja 15 enlaces sin texto ni `aria-label`. Cambiar a ocultación visual (la técnica de `.sr`) o añadir `aria-label` a cada `.it`: §7.2 pide que la etiqueta no desaparezca.'),
 ('state_ico', 'Icono gris sobre botón verde en vistas de estado (obs. 1)', lambda t: '.state .ico' in t or '.esp .ico' in t,
  'Cambiar `.state .ico` por `.state > .ico` (y `.esp > .ico` en el catálogo). El cliente ya lo declara como C3; en estos archivos no está aplicado. Verificado con contraste: 1,03:1 → 4,89:1.'),
 ('text3', 'Valor obsoleto de `--text-3` (4,21:1 sobre `--surface-2`)', lambda t: '--text-3' in t and ('4,21' in t or '#66717f' in t.lower()),
  '`--text-3: #5C6675` (el cliente ya lo declara en su tabla de tokens; en estos archivos no está aplicado o se revirtió).'),
 ('font', 'Google Fonts por `<link>` (D116 las retira)', lambda t: 'googleapis' in t or 'fuentes autoalojadas' in t.lower(),
  'Sustituir el `<link>` por `@font-face` autoalojado. El cliente lo declara como C8/C9; en `01_login` no está aplicado.'),
 ('ids', 'Identificadores duplicados en formularios (campos sin nombre accesible)', lambda t: 'id' in t and ('únicos' in t or 'unicos' in t or 'renumerar' in t or 'ids duplicados' in t),
  'Renumerar los `id` y sus `for`/`aria-controls` (§11: todos los `id` únicos).'),
 ('target', 'Destinos de pulsación menores de 24 px (buscador, folio, migas, enlaces)', lambda t: '§7.3' in t,
  'Dar `min-height:24px` (y relleno) al `input` del buscador y a los enlaces `.folio`/`.migas`. Verificado solo en `46`: ahí WCAG 2.5.8 se cumple por la excepción de espaciado, así que es divergencia de §7.3, **no** falla crítica de accesibilidad.'),
]
def texto(h): return ((h.get('regla') or '') + ' ' + (h.get('hay_en_el_build') or '')).lower().replace('`', '`')
temas = {k: {'titulo': t, 'fix': fx, 'items': []} for k, t, _, fx in TEMAS}; otros = []
exag = {i for i, v in ver.items() if v['veredicto'] == 'exagerada'}
for n, d in raw.items():
    for h in d['f1_cumplimiento']['hallazgos']:
        if not (h.get('critico') or {}).get('es'): continue
        tx = texto(h); hit = None
        for k, _, f, _ in TEMAS:
            if f(tx): hit = k; break
        rec = {'pantalla': n, 'id': h['id'], 'estado_vs_v1': h.get('estado_vs_v1'), 'criterio': h['critico'].get('criterio'), 'severidad': h['severidad'],
               'resumen': (h.get('por_que_importa') or '')[:230], 'verificacion': ver.get(h['id'], {}).get('veredicto'), 'regla': h['regla'][:70]}
        (temas[hit]['items'] if hit else otros).append(rec)
# 46cxc-08/11: exageradas -> no críticas (excepción de espaciado WCAG 2.5.8)
for k in temas: temas[k]['items'] = [i for i in temas[k]['items'] if i['id'] not in ('v2-46cxc-08', 'v2-46cxc-11')]
otros = [o for o in otros if o['id'] not in exag] + []
regres = [(n, h) for n, d in raw.items() for h in d['f1_cumplimiento']['hallazgos'] if h.get('estado_vs_v1') == 'regresion']

# ---------- 3. observaciones
RESP = {}
for n, d in raw.items():
    for o in d['observaciones_resueltas']: RESP.setdefault(o.get('hoja'), []).append((n, o))
OBS_TXT = {1: 'Icono gris sobre botón verde en error', 2: 'Portal cliente móvil: botones no uniformes', 3: 'Padrón: estados específicos, acciones cortadas, «Acciones» alineada', 4: '«Croquis y anexos» de la alta de orden, caja cortada',
 5: 'RHL incidentes: interlineado', 6: 'Tablero: gráficas ininteligibles', 7: 'Ficha cliente: «Datos fiscales» alto', 8: 'Viáticos: textos largos en tabla', 9: 'Tickets TI: rediseño crítico (cajas amarillas)',
 10: 'Sistémico: cajas contra la línea inferior', 11: 'Consumo de material: exceso de color', 12: 'Acordeón de sucursales: rediseño crítico', 13: 'Mi día: barra superior sin espacio', 14: 'Agenda de instaladores',
 15: 'Alta de orden: sombra sobre la barra', 16: 'Cuentas por cobrar: cajas estiradas', 17: 'Asistente: rediseño crítico, ¿Chat?, dos colores', 18: 'Bitácora: «CON QUÉ FILTROS»', 19: '«Siguiente» cortado en verificación de pedido'}

# ---------- métricas de instrumentos nuevos, 42 comunes
com = [n for n in nue['v2'] if n in nue['v1-control']]
def tot(k, a, b): return sum((v.get(a, {}).get(b, 0) or 0) for n, v in nue[k].items() if n in com and 'error' not in v)
INS = [('I1_icono_vs_boton', 'fallos', 'I1 icono vs relleno del botón'), ('I2_holgura_inferior', 'fallos', 'I2 barras sin holgura inferior'), ('I6_color', 'familiasVisibles', 'I6 familias de color (suma por pantalla)'),
       ('I8_paridad_botones', 'gruposDispares', 'I8 grupos de botones dispares'), ('I9_celdas', 'largas', 'I9 celdas largas'), ('C2_105_no_mayusculas', 'fallos', 'C2 10,5 px sin mayúsculas'), ('C11_texto_largo', 'sobre140', 'C11 textos de más de 140 caracteres'), ('SP5', 'elementosAfectados', '`--sp-5` sin declarar: elementos afectados')]
mod = [f for f in delta if f['estado'] == 'modificada']
suma = lambda k, w: sum((f[w] or {}).get(k, 0) or 0 for f in mod)

# ---------- F3 y F5
f3 = collections.Counter(d['f3_boost_ui'].get('puntuacion') for d in raw.values())
f5 = collections.Counter(p.get('cobertura') for d in raw.values() for p in (d.get('f5_investigacion') or {}).get('pain_points_evaluados', []))
dec = collections.Counter(h['decision']['valor'] for d in raw.values() for h in d['f1_cumplimiento']['hallazgos'])
estv1 = collections.Counter(h.get('estado_vs_v1') for d in raw.values() for h in d['f1_cumplimiento']['hallazgos'])
cober = [(n, c['patron']) for n, d in raw.items() for c in d.get('cobertura') or []]
vc = collections.Counter(v['veredicto'] for v in ver.values())

# ================= INFORME =================
P('# Auditoría v2 · SIO-DPROMA · paquete «Actualización 12-oct-2026»\n')
P('**Estudio:** 2894 Studio · **Fecha de la auditoría:** 14-oct-2026 · **Sistema de diseño de referencia:** v2.15.0 · **Solo auditoría:** ningún archivo del cliente se modificó (SHA-256 en `MANIFIESTO.json`).\n')
P('## 1 · Resumen ejecutivo\n')
carp = collections.Counter((v['carpeta_pdf'].split('/')[0], 'ausente' if v.get('estado') else ('sin' if any(e == 'NO_confirmado' for e in v['codigos'].values()) else 'ok')) for v in pdf.values())
P(f'1. **Alcance.** Se audita lo que contiene el ZIP: {len(htmls)} pantallas. El listado de pantallas del PDF del cliente no se usa como criterio. Sí se contrastó, a modo informativo, lo que el PDF declara contra los archivos (Anexo A): {len(pdf)-len(ausentes)} de sus {len(pdf)} pantallas están en el ZIP y en {len(no_alin)} de ellas no se ven los cambios declarados.')
P(f'2. **Qué se auditó.** {len(htmls)} pantallas en el ZIP: **{len(profundas)}** a fondo (observaciones, F1, F3; F4 y F5 en las de nivel A), con instrumentos medidos y fixtures validados; las otras {len(mecanicas)} solo con regresión mecánica. {len(identicas)} son idénticas a v1.')
P(f'3. **Calidad de la propia auditoría.** {sum(vc.values())} afirmaciones altas o críticas pasaron por verificadores que intentaron refutarlas con medición propia: **{vc["confirmada"]} confirmadas, {vc["exagerada"]} exageradas, {vc.get("refutada",0)} refutadas** (precisión {100*vc["confirmada"]/sum(vc.values()):.1f} %). Una réplica ciega de 2 pantallas **no** alcanzó el umbral de concordancia que nos fijamos (§8): una sola pasada no agota lo que hay.')
P('4. **Lo que sí está medido, en una línea cada uno.**')
P('    - El icono gris sobre «Reintentar» (obs. 1) tiene causa raíz: `.state .ico` descendiente. El arreglo es `.state > .ico`; el cliente lo declara y no lo aplicó en ' + str(len(temas['state_ico']['items'])) + ' hallazgos críticos de estas pantallas.')
P('    - El menú lateral colapsado sigue sin nombre accesible en ' + str(len({i['pantalla'] for i in temas['menu']['items']})) + ' pantallas auditadas (existía en v1).')
P('    - La hipótesis de que `--sp-5` explica los problemas de espaciado se **refuta** para Mi día (obs. 13): la causa es `.p4-t` con `padding-bottom:0` (§3.1). Para Acceso (51) explica los huecos de 0 px entre bloques, no el interlineado.')
P('    - Las «cajas contra la línea inferior» (obs. 10) son sistémicas: la plantilla de cabecera `.p4` no tiene relleno inferior y se copió en decenas de archivos.')
P('    - El panel «CON QUÉ FILTROS» (obs. 18) es, según la FICHA del cliente, un **registro de auditoría**, no controles: el defecto es de color y de mezcla de conceptos, no de operabilidad.')
P('5. **Rediseños críticos** (Tickets TI, acordeón de sucursales, Asistente, Mi día): diagnóstico y brief con veredicto de viabilidad en §7.')
P('6. **Lo que se le pide al cliente** se limita a críticos y regresiones (§5); el resto se adopta y se documenta en nuestro sistema (§6).\n')

P('## 2 · Qué contiene el ZIP\n')
P(f'El ZIP trae {len(htmls)} pantallas HTML (más `_sio-tokens.css`, `FICHAS_TECNICAS.md` y el aviso del padrón). Frente a v1: **{len(identicas)} idénticas** ({", ".join(identicas)}), **{len(nuevas)} nuevas** ({", ".join(nuevas)}) y {len(htmls)-len(identicas)-len(nuevas)} modificadas. De las 52 de v1, {len([f for f in delta if f["estado"]=="ausente_en_v2"])} no están en este ZIP ({", ".join(sorted(f["pantalla"] for f in delta if f["estado"]=="ausente_en_v2"))}); sus observaciones (4 y 15, `49_alta_orden`) quedan sin datos.\n')
P(f'Auditoría a fondo: {len(profundas)} pantallas. Solo regresión mecánica: {len(mecanicas)}.\n')
P('## 3 · Regresión mecánica v1 → v2 (mismo arnés, mismas fuentes)\n')
P(f'Se midieron las {len(mod)} pantallas modificadas comunes a v1 y v2 con los instrumentos de v1 (v1 se re-midió con el mismo arnés para que la diferencia sea honesta).\n')
P('| Indicador | v1 | v2 |\n|---|---:|---:|')
for k, nm in (('bajo24', 'Destinos < 24 px'), ('contraste_claro', 'Fallos de contraste (claro)'), ('contraste_oscuro', 'Fallos de contraste (oscuro)'), ('menu_sin_nombre', 'Enlaces de menú sin nombre a 1000 px'), ('sin_declarar', 'Tokens usados sin declarar')):
    P(f'| {nm} | {suma(k,"v1")} | {suma(k,"v2")} |')
P('\nInstrumentos nuevos (42 pantallas comunes). **Son candidatos, no veredictos:** los auditores encontraron falsos positivos (I3 e I7) y errores míos que se corrigieron (I6, I9, capturas, C1 en línea).\n')
P('| Instrumento | v1 | v2 |\n|---|---:|---:|')
for a, b, nm in INS: P(f'| {nm} | {tot("v1-control",a,b)} | {tot("v2",a,b)} |')
P('')
P(f'**Regresiones confirmadas por auditor ({len(regres)}):** ' + '; '.join(f'`{n}` ({h["regla"].split(" (")[0].split(" —")[0].split(" +")[0][:48]})' for n, h in regres) + '.\n')

P('## 4 · Tus 19 observaciones, una por una\n')
P('Veredicto = lo que se **reprodujo** con evidencia en el archivo recibido. Ojo: los auditores conocían cada observación, así que esta tabla mide si se puede **verificar** lo que viste, no si lo habrían descubierto solos (§8).\n')
P('| Hoja | Pantalla | Veredicto | Causa raíz | Cambio | Crítico | Decisión |\n|---:|---|---|---|---|:-:|---|')
for h in range(1, 20):
    rs = RESP.get(h)
    if h == 14:
        P('| 14 | `34_instaladores` | respondida en el brief | La agenda del sistema no existe en 2.15.0 (no hay §6.24; §13.9 solo regula alto por dato). No cambiar la del cliente; cambio mínimo en texto, «Sin asignar» y domingo a 1280. | medio | no | adoptar_cliente (con cambio mínimo) |')
        continue
    if rs:
        for n, o in rs:
            cr = (o.get('causa_raiz') or '—').replace('|', '/').replace('\n', ' ')[:210]
            P(f'| {h} | `{n}` | {o["veredicto"]} | {cr} | {o.get("tipo_de_cambio") or "—"} | {"sí (criterio " + str(o["critico"].get("criterio")) + ")" if (o.get("critico") or {}).get("es") else "no"} | {(o.get("decision") or {}).get("valor")} |')
    elif h in (4, 15): P(f'| {h} | `49_alta_orden` | **sin datos v2** | La pantalla no viene en el ZIP (el PDF dice que se actualizó) | — | — | pedir el archivo |')
    else: P(f'| {h} | — | sin datos | — | — | — | — |')
P('\nObservaciones 0 son de la lista de «revisión exhaustiva» (Acceso, Altas como modal).\n')

P('## 5 · Lo que se le pide al cliente: solo críticos y regresiones\n')
P('Criterios de «crítico» (acordados): (1) fallo de accesibilidad medido, (2) impide la tarea u oculta la acción primaria, (3) acción irreversible o de dinero sin protección, (4) contradice una decisión de DPROMA o expone datos personales, (5) rediseño marcado y viable. Todo lo demás se adopta.\n')
P('### 5.1 Arreglos transversales (una sustitución cierra muchos)\n')
P('| Tema | Hallazgos críticos | Pantallas | Arreglo |\n|---|---:|---|---|')
for k, t in temas.items():
    its = t['items']
    if its and k != 'target': P(f'| {t["titulo"]} | {len(its)} | {", ".join(sorted({i["pantalla"] for i in its}))} | {t["fix"]} |')
t = temas['target']
P(f'\n**Divergencia sencilla, no se exige como crítica ({len(t["items"])} hallazgos que los auditores marcaron críticos):** {t["titulo"]}. Pantallas: {", ".join(sorted({i["pantalla"] for i in t["items"]}))}. {t["fix"]} Se propone arreglarla porque es un cambio de una línea (regla 2), no como fallo de accesibilidad.\n')
P('\n### 5.2 Críticos propios de una pantalla\n')
P('| Pantalla | Hallazgo | Criterio | Estado vs v1 | Verificación |\n|---|---|:-:|---|---|')
for o in otros: P(f'| `{o["pantalla"]}` | {o["regla"]} — {o["resumen"]} | {o["criterio"]} | {o["estado_vs_v1"]} | {o["verificacion"] or "—"} |')
P('\n### 5.3 Regresiones frente a v1\n')
P('| Pantalla | Hallazgo | Regla | Verificación |\n|---|---|---|---|')
for n, h in regres:
    v = ver.get(h['id'], {}); corr = (' — ' + re.sub(r'\s+', ' ', str(v.get('correccion') or ''))[:160]) if v.get('veredicto') == 'exagerada' else ''
    P(f'| `{n}` | {(h.get("por_que_importa") or "")[:200]} | {h["regla"].split(" (")[0][:60]} | {v.get("veredicto") or "no verificada (severidad no alta)"}{corr} |')
P('')

P('### 5.4 Arreglos de accesibilidad que el propio cliente documentó y que v2 deshace\n')
rf = L(f'{R}/mediciones/v2/regresion-fichas.json')
P(f'`FICHAS_TECNICAS.md` («Defectos reales de accesibilidad encontrados y corregidos», verificados con axe-core) lista arreglos ya hechos en v1. Se comprobó cada uno en el ZIP: **{sum(o["perdido"] for o in rf)} de {len(rf)} se han perdido** (el patrón de v1 ya no está). Parece que la actualización se aplicó sobre copias anteriores a esos arreglos.\n')
P('| Pantalla | Arreglo documentado | v1 | v2 | ¿Perdido? |\n|---|---|---:|---:|:-:|')
for o in rf: P(f'| `{o["pantalla"]}` | {o["arreglo"]} | {o["ocurrencias_v1"]} | {o["ocurrencias_v2"]} | {"**sí**" if o["perdido"] else "no"} |')
P('\n(Ocurrencias = veces que aparece la construcción en el archivo; para el arreglo de `header` y `role="menu"`, 0 es lo correcto; para `--text-3-fuerte`, lo correcto es >0.) Además, en `24`, `33` y `01` el `--text-3` sigue en `#66717F` (4,21:1 sobre `--surface-2`), así que esos textos quedan sin ninguno de los dos arreglos: ni `--text-3-fuerte` ni el `#5C6675` nuevo. Esto amplía las 7 regresiones de §5.3, que solo cubrían las pantallas auditadas a fondo.\n')
P('## 6 · Lo que se adopta del cliente y se documenta en nuestro sistema\n')
P(f'De los {sum(dec.values())} hallazgos de F1: **{dec["adoptar_cliente"]} se adoptan** (el cliente decide), **{dec["exigir_cambio"]} se le exigen**, **{dec["ajustar_sistema"]} piden ajustar nuestro sistema**, {dec["decidir_diseño"]} son decisiones de diseño abiertas y {dec["sin_accion"]} no requieren acción. Estado frente a v1: {estv1["persiste"]} persisten, {estv1["nuevo"]} son nuevos, {estv1["regresion"]} son regresiones.\n')
P('Patrones que el cliente usa y nuestro sistema no documenta (propuestas de regla en cada ficha, campo `cobertura`):\n')
P('| Pantalla | Patrón sin regla |\n|---|---|')
for n, c in cober: P(f'| `{n}` | {c[:260].replace("|","/")} |')
P('\nContradicciones internas de nuestro sistema que los auditores encontraron (a resolver al subir versión): §2.1 (10,5 px solo en mayúsculas) frente a §7.2 (`.grp` a 10,5 px sin mayúsculas); §6.5 (Material Symbols por `<link>`) frente a D116 (sin Google Fonts); §1.4 frente a §12.5 en la antigüedad de saldo por tramos.\n')

P('## 7 · Conformidad con el aviso del ingeniero (28-sep) y rediseños\n')
P('### 7.1 Aviso del padrón, 12 ítems\n')
P('| # | Decisión | ' + ' | '.join(f'`{p[:2]}`' for p in ('27', '21', '41', '58', '59')) + ' |\n|---:|---|:-:|:-:|:-:|:-:|:-:|')
SIM = {'cumple': '✓', 'no_cumple': '✗', 'no_aplica': '·', 'no_verificable': '?'}
for it in aviso['items']:
    cells = [SIM.get(it['por_pantalla'].get(p, {}).get('estado'), '·') for p in ('27_padron_clientes', '21_ficha_cliente', '41_alta_cliente', '58_altas_como_modal', '59_editar_cliente')]
    P(f'| {it["n"]} | {it["decision"]}: {it["texto"]} | ' + ' | '.join(cells) + ' |')
P('\nLas ✗ de `58` se refieren al diálogo «Nuevo cliente» de esa página, obsoleto para el alta de cliente según FICHAS (`58` ya no gobierna `41`, pero sigue gobernando las otras cuatro altas).')
P('\n✓ cumple · ✗ no cumple · ? no verificable · · no aplica. Desajustes extra y críticos: ' + '; '.join(c['resumen'] for c in aviso.get('hallazgos_criticos', [])) + '\n')
P('### 7.2 Briefs de diseño (Fase 4)\n')
bd = sorted(glob.glob(f'{R}/briefs-diseno/*.md'))
P('Cada brief parte de lo que dibujó el cliente, evalúa al menos dos opciones (la primera siempre «mínimo cambio sobre lo del cliente»), trae un prototipo medido a 1440/1280/1024/390 px y termina con un veredicto de viabilidad. Los archivos completos están en `audit/v2/briefs-diseno/`.\n')
P('| Brief | Observación | Veredicto de viabilidad | Recomendación |\n|---|---|---|---|')
OBSB = {'24-tickets-zona-superior.md': '9 y 10 · Tickets TI, zona superior', '27-acordeon-sucursales.md': '12 · acordeón de sucursales', '27-etiquetas-de-estado.md': '3 · etiquetas de estado del padrón', '28-mi-dia.md': '13 · Mi día',
        '34-agenda.md': '14 · agenda de instaladores', '47-asistente.md': '17 · Asistente', '54-panel-con-que-filtros.md': '18 · panel «CON QUÉ FILTROS»'}
RECB = {'24-tickets-zona-superior.md': 'Un solo bloque ámbar (el plazo) a ancho declarado junto a los datos; la regla de cierre en una banda neutra de una frase; el resto a toggletip; `padding-bottom` en la cabecera.',
 '27-acordeon-sucursales.md': 'Cinco filas hijas que abren; la fila hija ocupa el ancho visible de la tabla con «Ver órdenes» al final de cada fila (revisado tras un comentario: el brief proponía una lista de 560 px); estado solo si la sucursal está bloqueada.',
 '27-etiquetas-de-estado.md': 'Un estado por eje (Completos · Pendientes · Sin calcular; Activo · Inactivo); el documento que falta es una línea, no un estado; sin «Por vencer» hasta D7.',
 '28-mi-dia.md': '`.p4{padding-bottom:var(--sp-3)}`, declarar `--sp-5`, aire al final de la lista y resumen oculto en vacío/error. La opción C recupera los 12 px de pliegue subiendo la fecha a la cabecera, pero requiere decisión de producto.',
 '34-agenda.md': 'No cambiarla: ningún fallo crítico depende de ella. Cambio mínimo: texto ≥12 px, fila «Sin asignar», domingo visible a 1280, cabecera fija, `--text-3`. La «agenda del sistema» no existe en 2.15.0.',
 '47-asistente.md': '«Chat» no merece sección propia. La franja se conserva. Quitar `margin-top:-12px` de `.fuentes`; cuerpo y pie como zonas hermanas; 24 px a los 5 destinos pequeños. Condición: decidir si el asistente solo consulta (47) o ejecuta con confirmación (10).',
 '54-panel-con-que-filtros.md': 'Dos grupos en la misma celda; marca «Dato personal» con escudo sin color de estado; valores literales («Querétaro y Celaya», no «2 de 5»). Incluye la regla de sistema para la marca de sensibilidad.'}
for f in bd:
    t = open(f, encoding='utf-8').read(); nm = os.path.basename(f)
    i = t.find('Veredicto de viabilidad'); seg = t[i:i + 400] if i >= 0 else ''
    m = re.findall(r'no viable ahora|viable con condiciones|viable', seg.lower())
    ver_txt = ('B viable; C viable con condiciones' if nm == '28-mi-dia.md' else (m[0] if m else '(ver archivo)'))
    P(f'| [`{nm}`](briefs-diseno/{nm}) | {OBSB.get(nm, nm)} | **{ver_txt}** | {RECB.get(nm, "(ver archivo)")} |')
P('\n**Dos hechos que cambian la lectura de la observación 3:** las etiquetas «Falta documento» e «Incompleto» no existen en `27_padron_clientes` del ZIP (`grep` = 0); «Incompleto» solo aparece en `06_padron_clientes`, un prototipo anterior. Probablemente tu captura es de otra versión. Y los briefs de `24` y `27` parten de la copia que trae el ZIP (Anexo A).\n')
pc = L(f'{R}/mediciones/v2/padron-combinado.json')
P('### 7.3 Padrón de clientes con todos los ajustes a la vez\n')
P('Se combinaron sobre el archivo real de `27_padron_clientes` el acordeón de sucursales, los estados de documentos por eje, el aire bajo la cabecera, el buscador a 24 px, las acciones de fila ancladas a la derecha y la retirada del banner de duplicados (D8). Es un prototipo (`briefs-diseno/prototipos/27-padron-combinado.html`), no un cambio aplicado.\n')
P('| Medido en el navegador | Ancho | Archivo del ZIP | Con los ajustes |\n|---|---:|---:|---:|')
for w in (1440, 1280, 1024):
    o, n_ = pc[f'original-{w}'], pc[f'combinado-{w}']
    P(f'| «Ver órdenes» a la vista | {w} px | {o["verOrdenes"].replace(" dentro","")} | {n_["verOrdenes"].replace(" dentro","")} |')
    P(f'| Botones de fila completos | {w} px | {o["accionesFila"].replace(" dentro","")} | {n_["accionesFila"].replace(" dentro","")} |')
P('\n**Estado de cada parte de las observaciones del padrón tras los briefs:**\n')
P('| Observación | Parte | Estado |\n|---|---|---|')
P('| 3 | Estados demasiado específicos | Resuelta (brief de etiquetas): un estado por eje |')
P('| 3 | Acciones cortadas en todas las filas | Resuelta en el prototipo combinado anclando la columna de acciones a la derecha. **Propuesta nuestra, sin brief propio** |')
P('| 3 | «Acciones» alineada a la izquierda de su casilla | **Sin resolver**: no hay solución evaluada |')
P('| 12 | Acordeón de sucursales | Resuelto (brief del acordeón, revisado: fila a todo el ancho visible con «Ver órdenes» al final) |')
P('| — | Banner de duplicados (D8) y chip «por vencer» (D7) | Retirados en el prototipo: el aviso del ingeniero los deja pospuestos |')
P('| — | Botón flotante sobre la última fila | **Sin resolver** |\n')
P('## 8 · Qué tan fiable es esta auditoría\n')
P(f'- **Validadores deterministas** (no son agentes): {len(raw)} de {len(raw)} fichas con 0 errores (JSON, § existentes en la 2.15.0, clases y ids presentes en el HTML, citas literales en su línea, `pp-NNN` reales, hashes). Una ficha de prueba rota a propósito dispara los 8 errores inyectados.')
ci = L(f'{R}/mediciones/v2/citas.json')
P(f'- **Citas del sistema de diseño:** todo lo citado se contrastó con el md de la **v2.15.0** (`docs/sistema-diseno-sio-dproma.md`; es el último disponible: las 4 ramas que traen la 2.15.0 tienen el mismo archivo, hash `a4b43d7a3f3e`; la rama de trabajo, en 2.13.3, no se usó como fuente). De {ci["fragmentos"]} fragmentos entrecomillados, **{ci["literales_en_2_15_0"]} son literales en la 2.15.0** ({round(100*ci["literales_en_2_15_0"]/ci["fragmentos"])} %). Los {len(ci["no_literales"])} restantes son citas de `FICHAS_TECNICAS.md` ({sum(r["esta_en_FICHAS"] for r in ci["no_literales"])}) o paráfrasis; **ninguno coincide con la 2.13.3** ({sum(r["esta_en_2_13_3"] for r in ci["no_literales"])}), así que no hay arrastre de la versión anterior. Detalle en `mediciones/v2/citas.json`.')
P(f'- **Verificación adversarial:** {sum(vc.values())} afirmaciones: {vc["confirmada"]} confirmadas, {vc["exagerada"]} exageradas, {vc.get("refutada",0)} refutadas, {vc.get("no_concluyente",0)} no concluyentes. Las exageradas se corrigieron en este informe (p. ej. el recorte de acciones a 1366 px es de 11 px, no «fuera»; el hueco del acordeón mide 578–654 px). **Cero refutaciones no prueba que no haya errores:** la réplica lo muestra.')
if conc: P(f'- **Réplica ciega** (2 pantallas, sin ver el original): mismo veredicto de observación 2 de 2; coincidencia de § citados **{round(100*sum(v["jaccard_§"] for v in conc.values())/len(conc))} %**, por debajo del 80 % que nos fijamos. De los hallazgos altos del original, la réplica reprodujo 5 de 10; encontró otros que el original no tenía. Lo que ambas pasadas encuentran es sólido; la lista no es exhaustiva.')
P('- **Instrumentos validados antes de usarse** con HTML sintético de respuesta conocida (contraste con alfa y `color-mix`, táctil, menú, I1–I9, C2, C11, `--sp-5`): 15 de 15 aciertos. Aun así los auditores hallaron seis fallos de mi instrumental (capturas de 800 px, I6, I9, C1 sin estilos en línea, I3 e I7 con falsos positivos, `lib.cjs` inyecta las fuentes y no sirve para probar fuentes). Están corregidos o documentados.')
P('- **Recall frente a tus 19 observaciones:** ' + str(sum(1 for h in range(1, 20) if RESP.get(h) and any(o["veredicto"] in ("confirmada", "parcial") for _, o in RESP[h]))) + ' de 19 reproducidas con evidencia por un auditor (más la 14, respondida por el brief de agenda: 17 de 19 con respuesta); 2 (4 y 15) no se pueden probar porque `49_alta_orden` no viene en el ZIP; **No es un recall ciego:** los auditores sabían qué buscar.')
P('- **Límites.** Las otras ' + str(len(mecanicas)) + ' pantallas solo tienen medición mecánica. Los hallazgos se refieren al archivo recibido, no a lo que el cliente tenga en otra carpeta. `FICHAS_TECNICAS.md` se usó como fuente de decisiones del cliente; se contradice a sí misma en un punto (plazo de tickets, tanda 3 frente a tanda 4). F3 sale entre 2 y 4 en las pantallas auditadas: ' + ', '.join(f'{k}: {v}' for k, v in sorted(f3.items())) + ' pantallas.')
P(f'- **F5 contra investigación** (solo nivel A y 54): ' + ', '.join(f'{k} {v}' for k, v in f5.items()) + '.\n')

P('## 9 · Pendientes\n')
P('1. **Opcional:** si más adelante se consigue la carpeta `sistema/` del cliente, re-medir esas pantallas; este informe se limita al ZIP recibido.')
P('2. **Confirmar identidades inferidas**: la hoja 1 es `22` o `32` (ambas tienen el defecto); la hoja 2 es `05_app_cliente` (coincide el nombre «Laura Núñez»); la hoja 5 es `13_panel_asistencia_rhl`, no `48`.')
P('3. **Decidir** las preguntas de diseño abiertas (§7.2). Para documentar divergencias en el sistema, el contenido de la 2.15.0 es el mismo en las 4 ramas que la traen; solo falta elegir en cuál se commitea.')
P('4. **Corregir en nuestro sistema** las contradicciones de §6 antes de subir versión.\n')
P('## Anexo A · Contraste informativo con el PDF del cliente\n')
P(f'La columna «Carpeta» sale del propio PDF (`html_v2/` o `sistema/`). El análisis sale de `claims.py` (lectura estática de cada código C1–C18 del PDF contra su archivo) y de comparar hashes con v1. C11, C13, C14, C15 y C18 no se pueden verificar mecánicamente; C2 se mide en navegador.\n')
P('| Grupo | N | Pantallas |\n|---|---:|---|')
P(f'| Listadas en el PDF y **ausentes del ZIP** | {len(ausentes)} | {", ".join(ausentes)} |')
P(f'| Listadas, presentes, **sin los cambios declarados** | {len(no_alin)} | {", ".join(no_alin)} |')
P(f'| Listadas, presentes, **cambios confirmados** | {len(conf)} | {", ".join(conf)} |')
P(f'| En el ZIP y nuevas respecto a v1 | {len(nuevas)} | {", ".join(nuevas)} |')
P(f'| Idénticas byte a byte a v1 | {len(identicas)} | {", ".join(identicas)} |\n')
P(f'Nota sobre C1 (nada menor de 12 px): se midió en las hojas `<style>`. Además, {len(inline)} pantallas tienen `font-size` menor de 12 px en atributos `style=""` ({", ".join(inline)}); no es claro si el PDF contaba esos atributos, así que no se usa para clasificar.\n')
P('**Lectura.** Las observaciones 4 y 15 (`49_alta_orden`, que vive en `sistema/icev/`) no se pueden auditar sobre v2. Tickets TI, Acceso, Altas como modal, Cuentas por cobrar y Agenda de instaladores son pantallas de `sistema/`: lo que se auditó de ellas es la copia que trae el ZIP, que puede no ser la que viste en tus capturas.\n')


P('## Anexo B · Cómo reproducir\n')
P('`audit/v2/instrumentos/` (medidores, `verificar-fixtures.sh`, `validar.py`, `concordancia.py`, `consolidar.py`), `audit/v2/mediciones/` (JSON de v1 y v2), `audit/v2/raw/` (una ficha por pantalla), `audit/v2/verif/` y `audit/v2/replica/`. Todas las cifras de este documento salen de esos archivos.\n')
# ---- redacción para el ingeniero: esta es SU primera auditoría; "v1/v2" no existen para él.
txt = '\n'.join(out)
txt = txt.replace('# Auditoría v2 · SIO-DPROMA · paquete «Actualización 12-oct-2026»', '# Auditoría SIO-DPROMA · entrega «Actualización 12-oct-2026»')
txt = txt.replace('| Indicador | v1 | v2 |', '| Indicador | Entrega 30-sep | Entrega 12-oct |').replace('| Instrumento | v1 | v2 |', '| Instrumento | Entrega 30-sep | Entrega 12-oct |')
txt = txt.replace('| Pantalla | Patrón sin regla |', '| Pantalla | Patrón sin regla |')
txt = txt.replace('## 3 · Regresión mecánica v1 → v2', '## 3 · Qué cambió entre la entrega del 30-sep y la del 12-oct')
txt = txt.replace('Estado frente a v1:', 'Estado frente a la entrega del 30-sep:')
txt = txt.replace('Frente a v1:', 'Frente a la entrega del 30-sep:').replace('De las 52 de v1,', 'De las 52 de la entrega del 30-sep,')
txt = txt.replace('(v1 se re-midió con el mismo arnés para que la diferencia sea honesta)', '(la entrega del 30-sep se re-midió con el mismo arnés para que la diferencia sea honesta)')
txt = txt.replace('con los instrumentos de v1', 'con los mismos instrumentos en las dos entregas')
txt = txt.replace('Regresiones frente a v1', 'Regresiones frente a la entrega del 30-sep').replace('frente a v1', 'frente a la entrega del 30-sep')
txt = re.sub(r'(?<![\w./`-])v1(?![\w/-]|\.\w)', 'la entrega del 30-sep', txt)
txt = re.sub(r'(?<![\w./`-])v2(?![\w/-]|\.\w)', 'la entrega del 12-oct', txt)
txt = txt.replace('Este documento', 'Este documento')
nota = ('> **Cómo leer este informe.** Es la primera auditoría que se entrega al cliente: nadie le ha comunicado antes ningún hallazgo nuestro. '
        '«Persiste» significa solo que el problema ya estaba en la entrega del 30-sep; no que se haya ignorado un aviso. '
        '«Regresión» y «pérdida» se usan únicamente cuando el cliente tenía algo bien en septiembre (o lo declaró él mismo) y en octubre dejó de estarlo.\n')
txt = txt.replace('## 1 · Resumen ejecutivo', nota + '\n## 1 · Resumen ejecutivo', 1)
open(f'{R}/INFORME-v2.md', 'w', encoding='utf-8').write(txt)
print('ok', len(txt), 'caracteres')
json.dump({'entrega': {'ausentes': ausentes, 'no_alineadas': no_alin, 'confirmadas': conf, 'nuevas': nuevas, 'identicas': identicas}, 'temas': {k: {'titulo': v['titulo'], 'n': len(v['items']), 'pantallas': sorted({i['pantalla'] for i in v['items']})} for k, v in temas.items()},
           'otros_criticos': len(otros), 'regresiones': len(regres), 'verificacion': dict(vc), 'decisiones': dict(dec), 'cobertura': len(cober)}, open(f'{R}/consolidado-v2.json', 'w'), ensure_ascii=False, indent=1)

