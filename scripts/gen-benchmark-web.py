#!/usr/bin/env python3
"""Genera web/entregables/benchmark-web/index.html.

Fuente de datos: web/entregables/benchmark-web/datos/benchmark.json (puntuaciones y
evidencia observadas) y datos/medidas.json (métricas automáticas de cada home).
Hereda el cromo, los tokens y la envoltura de Chart.js del tablero de Administración
Vehicular de SIO-DPROMA (web/entregables/propuestas/administracion-vehicular-tablero.html).
"""
import html
import json
import pathlib
import re
import statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "web/entregables/propuestas/administracion-vehicular-tablero.html"
OUT = ROOT / "web/entregables/benchmark-web"
data = json.loads((OUT / "datos/benchmark.json").read_text(encoding="utf-8"))
med = json.loads((OUT / "datos/medidas.json").read_text(encoding="utf-8"))
vf_path = OUT / "datos/verificacion.json"
vf = json.loads(vf_path.read_text(encoding="utf-8")) if vf_path.exists() else {}

esc = html.escape
SITES = {s["id"]: s for s in data["sitios"]}
CRIT = data["criterios"]
CRIT_BY = {c["id"]: c for c in CRIT}
ESCALA = data["meta"]["escala"]
ORDEN = ["dproma", "evergo", "fazt", "vemo", "tesla", "chargepoint", "byd", "enphase"]
FECHA = "15 oct 2026"

# ───────────────────────── medidas automáticas ─────────────────────────
def checks_seo(m):
    mm = m["m"]
    return [
        ("Descripción", bool(mm.get("desc"))),
        ("Canonical", bool(mm.get("canonical"))),
        ("Open Graph (≥4)", mm.get("og", 0) >= 4),
        ("Un solo H1", mm.get("h1") == 1),
        ("Datos estructurados", mm.get("jsonld", 0) >= 1),
        ("Alt completo", mm.get("imgsNoAlt", 1) == 0),
    ]

def checks_a11y(m):
    mm = m["m"]
    return [
        ("Idioma declarado", bool(mm.get("lang"))),
        ("Viewport", bool(mm.get("viewport"))),
        ("Enlace de salto", bool(mm.get("skip"))),
        ("Sin desbordamiento en móvil", m.get("mobileScrollW", 9999) <= 390),
        ("Alt completo", mm.get("imgsNoAlt", 1) == 0),
    ]

def nivel(n, tabla):
    for minimo, p in tabla:
        if n >= minimo:
            return p
    return 0

P = data["puntuaciones"]
for sid, m in med.items():
    if sid not in P or not m.get("m"):
        continue
    cs = checks_seo(m)
    n = sum(1 for _, ok in cs if ok)
    fallos = [t for t, ok in cs if not ok]
    P[sid]["seo"] = {
        "p": nivel(n, [(6, 3), (4, 2), (2, 1)]),
        "e": f"{n} de 6 comprobaciones" + (f"; falla: {', '.join(fallos)}." if fallos else "; todas correctas."),
        "checks": cs,
    }
    ca = checks_a11y(m)
    n = sum(1 for _, ok in ca if ok)
    fallos = [t for t, ok in ca if not ok]
    P[sid]["a11y"] = {
        "p": nivel(n, [(5, 3), (4, 2), (3, 1)]),
        "e": f"{n} de 5 comprobaciones" + (f"; falla: {', '.join(fallos)}." if fallos else "; todas correctas."),
        "checks": ca,
    }

def score(sid, cid):
    c = P.get(sid, {}).get(cid)
    return None if c is None else c["p"]

COMPLETOS = [s for s in ORDEN if SITES[s]["evidencia"] == "completa"]
TOTAL = {s: sum(score(s, c["id"]) for c in CRIT) for s in COMPLETOS}
MAXP = 3 * len(CRIT)
OTROS = [s for s in COMPLETOS if s != "dproma"]
ranking = sorted(COMPLETOS, key=lambda s: -TOTAL[s])
pos_dproma = ranking.index("dproma") + 1
mejor = ranking[0]
mediana_total = statistics.median(TOTAL[s] for s in OTROS)

brecha = []
for c in CRIT:
    d = score("dproma", c["id"])
    vals = [(score(s, c["id"]), s) for s in OTROS]
    best = max(vals, key=lambda t: t[0])
    med_c = statistics.median(v for v, _ in vals)
    brecha.append({"id": c["id"], "d": d, "med": med_c, "best": best[0], "best_site": [SITES[s]["corto"] for v, s in vals if v == best[0]], "gap": best[0] - d})
brecha.sort(key=lambda b: (-b["gap"], -(b["med"] - b["d"])))

# ───────────────────────── utilidades HTML ─────────────────────────
PILL = {0: "p-err", 1: "p-warn", 2: "p-neutro", 3: "p-ok"}
def pill(p, extra=""):
    if p is None:
        return f'<span class="pill p-pause" {extra}>—</span>'
    return f'<span class="pill {PILL[p]}" {extra}>{p}</span>'

def ico(name, cls="ico ico-sm"):
    return f'<svg class="{cls}" aria-hidden="true" translate="no"><use href="#{name}"/></svg>'

def fmt_med(x):
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}".replace(".", ",")

EVID = {"completa": ("p-ok", "Evidencia completa"), "parcial": ("p-warn", "Evidencia parcial"), "ninguna": ("p-pause", "Sin evidencia")}

# ───────────────────────── secciones ─────────────────────────
def sec_resumen():
    d = TOTAL["dproma"]
    n_ok = len(COMPLETOS)
    sin = [SITES[s]["corto"] for s in ORDEN if SITES[s]["evidencia"] != "completa"]
    fuertes = [CRIT_BY[b["id"]]["nombre"] for b in sorted(brecha, key=lambda b: b["gap"]) if b["gap"] <= 0]
    fuertes = [f if f.split()[0].isupper() else f[0].lower() + f[1:] for f in fuertes]
    return f"""
<section id="resumen" aria-labelledby="h-resumen">
<div class="rot"><h2 id="h-resumen">Resumen</h2><span class="alcance">{ico('m-visibility','ico ico-xs')}home, navegación y páginas de primer nivel</span></div>
<div class="bw-hero">
  <div class="widget bw-mensaje">
    <header><h3>Lectura en una frase</h3></header>
    <p class="bw-frase">La web de DPROMA funciona y está bien hecha por dentro. <span>Le falta lo que convence por fuera: pruebas, casos reales, imagen propia y producto visible.</span></p>
    <ul class="bw-puntos">
      <li>{ico('m-check_circle')}<span><b>Ya está a nivel de referente</b> en {esc(', '.join(fuertes) or 'ningún criterio')}.</span></li>
      <li>{ico('m-error')}<span><b>Queda detrás</b> en fotografía y video, casos, prueba social, app visible y precios.</span></li>
      <li>{ico('m-trending_up')}<span><b>La oportunidad:</b> ningún competidor de carga en México combina carga EV y gestoría vehicular para empresas.</span></li>
    </ul>
  </div>
  <figure class="bw-firma">
    <div class="terreno dproma" id="terreno-hero" data-nombre="DPROMA" role="img" aria-label="Ilustración decorativa: terreno de pilares que se elevan alrededor del puntero. No contiene datos."></div>
    <figcaption>Mueve el puntero sobre el terreno. Es solo ilustración; los datos están en la matriz.</figcaption>
  </figure>
</div>
<div class="widget" style="margin-top:var(--sp-4)">
  <header><h3>Cifras de la evaluación</h3></header>
  <div class="cifras">
    <div class="kpi"><span class="cifra tnum">{n_ok}</span><div class="etq"><span class="rotulo">Sitios puntuados</span><span class="apoyo">{len(sin)} sin puntuar</span></div></div>
    <div class="kpi"><span class="cifra tnum">{len(CRIT)}</span><div class="etq"><span class="rotulo">Criterios</span><span class="apoyo">10 vistos · 2 medidos</span></div></div>
    <div class="kpi"><span class="cifra tnum">{d}<span class="unidad">/ {MAXP}</span></span><div class="etq"><span class="rotulo">Puntaje de DPROMA</span><span class="apoyo">puesto {pos_dproma} de {n_ok}</span></div></div>
    <div class="kpi"><span class="cifra tnum">{TOTAL[mejor]-d}</span><div class="etq"><span class="rotulo">Brecha con el mejor</span><span class="apoyo">{esc(SITES[mejor]['corto'])} · {TOTAL[mejor]}/{MAXP}</span></div></div>
  </div>
</div>
<p class="nota-reloj nota">{ico('m-info')}<span><b>Cómo se mide.</b> {esc(data['meta']['nota_metodo'])} Sin puntuar: {esc(', '.join(sin))}. Capturado el {FECHA}.</span></p>
</section>"""


def sec_panorama():
    cards = []
    for sid in ORDEN:
        s = SITES[sid]
        ev_cls, ev_txt = EVID[s["evidencia"]]
        n_eval = sum(1 for c in CRIT if score(sid, c["id"]) is not None)
        total = (f'<span class="pill p-neutro">{TOTAL[sid]}<span class="de">/{MAXP}</span></span>' if sid in TOTAL
                 else '<span class="pill p-pause">Sin puntuar</span>')
        apagado = " apagado" if s["evidencia"] != "completa" else ""
        mod = " dproma" if sid == "dproma" else ""
        motivo = f'<p class="motivo">{esc(s["motivo"])}</p>' if s.get("motivo") else ""
        cards.append(f"""
<article class="widget bw-emp" tabindex="0" data-site="{sid}" aria-label="{esc(s['nombre'])}: {n_eval} de {len(CRIT)} criterios evaluados">
  <div class="terreno{mod}{apagado}" data-nombre="{esc(s['nombre'])}" data-quieto="{1 if apagado else 0}" role="img" aria-label="Ilustración decorativa de {esc(s['nombre'])}. No contiene datos."></div>
  <div class="bw-emp-datos">
    <h3>{esc(s['nombre'])}</h3>
    <p class="rol">{esc(s['rol'])}</p>
    <div class="fila">{total}<span class="pill {ev_cls}">{ev_txt}</span></div>
    <p class="meta tnum">{n_eval} de {len(CRIT)} criterios</p>
    {motivo}
  </div>
</article>""")
    return f"""
<section id="panorama" aria-labelledby="h-panorama">
<div class="rot"><h2 id="h-panorama">Panorama de las empresas evaluadas</h2><span class="alcance">{ico('m-group','ico ico-xs')}{len(ORDEN)} sitios</span></div>
<p class="bw-sub">Cada terreno reacciona al puntero. Al pasar sobre una empresa se resalta su columna en la matriz. Las empresas sin evidencia suficiente aparecen atenuadas y quietas.</p>
<div class="panorama">{''.join(cards)}</div>
</section>"""


def sec_ranking():
    filas = "".join(
        f'<tr><th scope="row">{esc(SITES[s]["nombre"])}</th><td class="tnum">{TOTAL[s]}</td></tr>' for s in ranking)
    leyenda = "".join(
        f'<li>{pill(k)}<span><b>{esc(v)}</b></span></li>' for k, v in ((int(a), b) for a, b in ESCALA.items()))
    excl = [s for s in ORDEN if s not in TOTAL]
    excl_txt = "; ".join(f"{SITES[s]['corto']}: {'sitio inaccesible' if SITES[s]['evidencia']=='ninguna' else 'evidencia parcial'}" for s in excl)
    return f"""
<section id="ranking" aria-labelledby="h-ranking">
<div class="rot"><h2 id="h-ranking">Ranking global</h2><span class="alcance">{ico('m-bar_chart','ico ico-xs')}puntaje sobre {MAXP}</span></div>
<div class="dash">
  <div class="widget" style="grid-column:span 12" data-w="7">
    <header><h3>Puntaje total por sitio</h3></header>
    <figure class="viz">
      <div class="viz-lienzo" style="height:260px"><canvas id="v-ranking" aria-label="Barras horizontales: puntaje total de cada sitio sobre {MAXP}. DPROMA {TOTAL['dproma']}."></canvas></div>
      <p class="aviso-cdn">Sin conexión con la librería de gráficos.</p>
      <details class="viz-tabla"><summary>Ver los datos en tabla</summary>
        <table><caption class="sr">Puntaje total por sitio sobre {MAXP}</caption>
        <thead><tr><th>Sitio</th><th>Puntaje</th></tr></thead><tbody>{filas}</tbody>
        <tfoot><tr><th scope="row">Mediana de los otros {len(OTROS)}</th><td class="tnum">{fmt_med(mediana_total)}</td></tr></tfoot></table>
      </details>
    </figure>
    <p class="pie">Sin puntaje global: {esc(excl_txt)}.</p>
  </div>
  <div class="widget" style="grid-column:span 12" data-w="5">
    <header><h3>Cómo leer la nota</h3></header>
    <ul class="bw-escala">{leyenda}</ul>
    <p class="pie">Cada criterio vale de 0 a 3. El total suma los {len(CRIT)} criterios.</p>
  </div>
</div>
</section>"""


def sec_matriz():
    cols = ORDEN
    grupos = [("dproma", "Sitio evaluado"), ("mx", "Competidores en México"), ("ref", "Referentes")]
    th1 = ""
    for g, t in grupos:
        n = sum(1 for s in cols if SITES[s]["grupo"] == g)
        th1 += f'<th colspan="{n}" scope="colgroup" class="grp-{g}">{t}</th>'
    th2 = "".join(f'<th scope="col" data-col="{s}" class="{"col-dproma" if s=="dproma" else ""}">{esc(SITES[s]["corto"])}</th>' for s in cols)
    body = ""
    for c in CRIT:
        tds = ""
        for s in cols:
            cell = P.get(s, {}).get(c["id"])
            p = None if cell is None else cell["p"]
            lbl = (f'{c["nombre"]}, {SITES[s]["nombre"]}: {p} de 3. Ver evidencia.' if p is not None
                   else f'{c["nombre"]}, {SITES[s]["nombre"]}: sin evaluar. Ver motivo.')
            tds += (f'<td data-col="{s}" data-et="{esc(SITES[s]["corto"])}" class="{"col-dproma" if s=="dproma" else ""}"><button type="button" class="celda" data-site="{s}" data-crit="{c["id"]}" '
                    f'aria-label="{esc(lbl)}">{pill(p)}</button></td>')
        tipo = "medido" if c["tipo"] == "medido" else "visto"
        body += f'<tr><th scope="row">{esc(c["nombre"])}<span class="tipo">{tipo}</span></th>{tds}</tr>'
    tot = ""
    for s in cols:
        n_eval = sum(1 for c in CRIT if score(s, c["id"]) is not None)
        tot += (f'<td data-col="{s}" data-et="{esc(SITES[s]["corto"])}" class="tnum {"col-dproma" if s=="dproma" else ""}">' +
                (f'<b>{TOTAL[s]}</b> / {MAXP}' if s in TOTAL else f'<span class="sin">{n_eval} de {len(CRIT)}</span>') + '</td>')
    leyenda = "".join(f'<span class="ley-it">{pill(int(k))}{esc(v)}</span>' for k, v in ESCALA.items()) + f'<span class="ley-it">{pill(None)}Sin evaluar</span>'
    return f"""
<section id="matriz" aria-labelledby="h-matriz">
<div class="rot"><h2 id="h-matriz">Matriz comparativa</h2><span class="alcance">{ico('m-table_chart','ico ico-xs')}{len(CRIT)} criterios · {len(cols)} sitios</span></div>
<div class="ley" style="margin-bottom:var(--sp-3)">{leyenda}</div>
<div class="tarjeta">
  <div class="tabla-caja bw-matriz">
    <table>
      <caption>Puntuación de 0 a 3 por criterio y sitio. Cada celda abre su evidencia.</caption>
      <thead><tr><th rowspan="2" scope="col" class="esq">Criterio</th>{th1}</tr><tr>{th2}</tr></thead>
      <tbody>{body}</tbody>
      <tfoot><tr><th scope="row">Total</th>{tot}</tr></tfoot>
    </table>
  </div>
</div>
<div class="widget bw-evid" id="evidencia" aria-live="polite" tabindex="-1">
  <header><h3>Evidencia</h3></header>
  <p class="vacio">Selecciona una celda de la matriz para ver qué se observó, en qué sitio y con qué criterio.</p>
</div>
</section>"""


def sec_brecha():
    filas = ""
    for i, b in enumerate(brecha):
        c = CRIT_BY[b["id"]]
        cls = "s-err" if b["gap"] >= 2 else ("s-warn" if b["gap"] == 1 else "s-ok")
        ancho = round(b["gap"] / 3 * 100)
        prio = f'<span class="pill p-err">Prioridad {i+1}</span>' if i < 3 else ""
        mejores = " · ".join(b["best_site"])
        med_html = pill(int(b['med'])) if float(b['med']).is_integer() else '<span class="pill p-neutro">' + fmt_med(b['med']) + '</span>'
        filas += f"""<li class="bw-fila">
  <div class="et"><b>{esc(c['nombre'])}</b>{prio}</div>
  <div class="vals"><span>DPROMA {pill(b['d'])}</span><span>Mediana {med_html}</span><span>Mejor {pill(b['best'])}<small>{esc(mejores)}</small></span></div>
  <div class="gap"><div class="barra" role="img" aria-label="Brecha de {b['gap']} puntos con el mejor"><span class="{cls}" style="width:{max(ancho,0)}%"></span></div><b class="tnum">{('+' if b['gap']>0 else '')}{b['gap']}</b></div>
</li>"""
    tabla = "".join(
        f'<tr><th scope="row">{esc(CRIT_BY[b["id"]]["nombre"])}</th><td class="tnum">{b["d"]}</td><td class="tnum">{fmt_med(b["med"])}</td><td class="tnum">{b["best"]}</td><td class="tnum">{b["gap"]}</td></tr>' for b in brecha)
    tg = sum(b["gap"] for b in brecha)
    return f"""
<section id="brecha" aria-labelledby="h-brecha">
<div class="rot"><h2 id="h-brecha">Brecha de DPROMA por criterio</h2><span class="alcance">{ico('m-trending_up','ico ico-xs')}contra los otros {len(OTROS)} sitios puntuados</span></div>
<p class="bw-sub">La brecha es la distancia entre DPROMA y el mejor sitio en cada criterio. Rojo: 2 puntos o más. Ámbar: 1. Verde: DPROMA ya alcanza al mejor.</p>
<div class="widget">
  <ol class="bw-brecha">{filas}</ol>
  <details class="viz-tabla"><summary>Ver los datos en tabla</summary>
    <table><caption class="sr">Brecha de DPROMA por criterio</caption>
    <thead><tr><th>Criterio</th><th>DPROMA</th><th>Mediana</th><th>Mejor</th><th>Brecha</th></tr></thead><tbody>{tabla}</tbody>
    <tfoot><tr><th scope="row">Brecha acumulada</th><td></td><td></td><td></td><td class="tnum">{tg}</td></tr></tfoot></table>
  </details>
</div>
</section>"""


ANOT = {
    "dproma": [(50, 4, "Menú de siete ítems y un único CTA."), (30, 36, "H1 claro: para quién y qué ofrece."), (76, 56, "Niveles de potencia en el hero: diferenciador concreto."), (30, 98, "Sellos NOM-001-SEDE y trámites CFE."), (96, 93, "Botón flotante de WhatsApp.")],
    "evergo": [(60, 12, "Menú con Mapa y acceso Evergo Fleet."), (40, 48, "El hero es una campaña de evento, no la propuesta de valor."), (50, 94, "Tres entradas con foto: público, residencial y empresas."), (88, 4, "Búsqueda y cambio de idioma.")],
    "fazt": [(50, 3, "Promoción de cashback en una franja superior."), (72, 16, "Rutas B2B (profesionales, hosts, anunciantes) solo en el menú."), (50, 62, "Video y claim de «líder» sin una cifra que lo respalde.")],
    "chargepoint": [(24, 7, "Menú por industria, productos, socios y conductores."), (92, 8, "CTA fijo «Connect With an Expert»."), (28, 46, "Propuesta: «all-in-one partner»."), (30, 96, "Se declara «no operador»: posicionamiento explícito.")],
    "byd": [(30, 8, "Menú por intención: prueba de manejo y flotillas."), (80, 8, "App y localizador de distribuidor siempre visibles."), (50, 94, "Precio y costo por kilómetro en el hero."), (95, 92, "WhatsApp flotante.")],
    "enphase": [(40, 3, "Cuatro audiencias en el primer nivel del menú."), (67, 3, "CTA «Get started» fijo."), (50, 74, "Mensaje de una línea y dos CTAs: aprender o ver el video.")],
}


def sec_capturas():
    figs = []
    for sid in sorted(ORDEN, key=lambda x: (not SITES[x]["captura"], ORDEN.index(x))):
        s = SITES[sid]
        if s["captura"]:
            marks = "".join(f'<span class="mk" style="left:{x}%;top:{y}%" aria-hidden="true">{i+1}</span>' for i, (x, y, _) in enumerate(ANOT[sid]))
            lista = "".join(f"<li>{esc(t)}</li>" for _, _, t in ANOT[sid])
            figs.append(f"""
<figure class="marco" data-site="{sid}">
  <div class="marco-barra"><span class="pts" aria-hidden="true"><i></i><i></i><i></i></span><span class="url tnum">{esc(re.sub(r'^https?://','',s['url']))}</span></div>
  <div class="marco-vista">
    <div class="v-esc"><div class="cap"><img src="img/{sid}-escritorio.jpg" width="1200" height="750" loading="lazy" alt="Captura de la portada de {esc(s['nombre'])} en escritorio, {FECHA}">{marks}</div><ol class="anot">{lista}</ol></div>
    <div class="v-mov"><img src="img/{sid}-movil.jpg" width="390" height="844" loading="lazy" alt="Captura de la portada de {esc(s['nombre'])} en móvil, {FECHA}"></div>
  </div>
  <figcaption><b>{esc(s['nombre'])}</b> · {esc(s['rol'])} · capturado el {FECHA}</figcaption>
</figure>""")
        else:
            figs.append(f"""
<figure class="marco vacio" data-site="{sid}">
  <div class="marco-barra"><span class="pts" aria-hidden="true"><i></i><i></i><i></i></span><span class="url tnum">{esc(re.sub(r'^https?://','',s['url']))}</span></div>
  <div class="hueco-cap">{ico('m-lock','ico')}<p><b>{esc(s['nombre'])}: sin captura</b></p><p>{esc(s['motivo'])}</p></div>
  <figcaption><b>{esc(s['nombre'])}</b> · {esc(s['rol'])}</figcaption>
</figure>""")
    extra = f"""
<div class="extras">
  <figure class="marco"><div class="marco-barra"><span class="pts" aria-hidden="true"><i></i><i></i><i></i></span><span class="url tnum">dproma.com · Pre-diagnóstico EV</span></div><img src="img/dproma-prediagnostico.jpg" width="1200" height="750" loading="lazy" alt="Pre-diagnóstico EV de DPROMA con resultado calculado"><figcaption>El pre-diagnóstico cambia el resultado según lo que se ingresa. Capturado el {FECHA}.</figcaption></figure>
  <figure class="marco"><div class="marco-barra"><span class="pts" aria-hidden="true"><i></i><i></i><i></i></span><span class="url tnum">dproma.com · Soluciones por industria</span></div><img src="img/dproma-industrias.jpg" width="1200" height="750" loading="lazy" alt="Pestañas de soluciones por industria de DPROMA"><figcaption>Siete industrias con panel propio, en una sola página. Capturado el {FECHA}.</figcaption></figure>
  <figure class="marco"><div class="marco-barra"><span class="pts" aria-hidden="true"><i></i><i></i><i></i></span><span class="url tnum">apps.apple.com · App Tesla (México)</span></div><img src="img/tesla-app.jpg" width="1200" height="750" loading="lazy" alt="Ficha de la app de Tesla en App Store México con 4.9 de 5"><figcaption>Única evidencia de Tesla por ahora: 4.9 de 5 con 1.5 mil calificaciones. Capturado el {FECHA}.</figcaption></figure>
</div>"""
    return f"""
<section id="capturas" aria-labelledby="h-capturas">
<div class="rot"><h2 id="h-capturas">Capturas comparadas</h2><span class="alcance">{ico('m-image','ico ico-xs')}portada de cada sitio</span></div>
<div class="bw-vista-ctl"><div class="seg" role="group" aria-label="Tipo de pantalla">
  <button type="button" data-vista="esc" aria-pressed="true">Escritorio</button><button type="button" data-vista="mov" aria-pressed="false">Móvil</button></div>
  <span class="bw-sub" style="margin:0">En escritorio, los números marcan los patrones observados. Capturas de sitios de terceros, para análisis interno.</span></div>
<div class="galeria" data-vista="esc">{''.join(figs)}</div>
<h3 class="bw-h3">Evidencia adicional</h3>
{extra}
</section>"""


PATRONES = [
    ("Menú por audiencia desde el primer nivel", "El visitante elige su ruta (empresa, conductor, instalador) sin buscar.", ["ChargePoint", "BYD", "Enphase"], "parcial", "«Soluciones» enruta por industria; flotillas y desarrolladores no tienen ruta propia."),
    ("Una página por industria", "Cada sector tiene su mensaje, su caso y su CTA.", ["ChargePoint", "Enphase"], "parcial", "Siete industrias, pero en pestañas dentro de una sola página."),
    ("CTA doble y canal directo", "Hablar con un experto, pedir cotización y escribir por WhatsApp.", ["ChargePoint", "BYD", "Enphase"], "parcial", "Un CTA principal repetido, más WhatsApp flotante."),
    ("Herramienta que cualifica", "Estimador, configurador o mapa que entrega valor antes del contacto.", ["BYD", "Enphase", "Evergo"], "si", "Pre-diagnóstico EV funcional."),
    ("Prueba social por capas", "Logos, cifras de escala, testimonios con nombre y respaldo externo.", ["ChargePoint"], "parcial", "Cifras y logos de marcas; sin clientes ni testimonios."),
    ("Casos reales con resultado", "Contexto, solución y números de un cliente identificable.", ["ChargePoint", "Enphase"], "no", "/casos son escenarios ilustrativos."),
    ("Producto digital visible", "Capturas reales de la app y botones de descarga.", ["Evergo", "FAZT"], "parcial", "Maqueta sin descarga."),
    ("Centro de recursos y ayuda", "Guías, FAQ, formación y soporte por audiencia.", ["ChargePoint", "Enphase", "Evergo"], "parcial", "Blog de 3 artículos y secciones de costos y requisitos."),
    ("Un diferenciador concreto en el hero", "Una cifra, un precio o un beneficio que se entiende en cinco segundos.", ["FAZT", "BYD", "Enphase"], "si", "Tres niveles de potencia y sellos NOM-001-SEDE y CFE."),
    ("Precio o rango a la vista", "El visitante sabe el orden de magnitud antes de contactar.", ["BYD", "FAZT"], "parcial", "Explica los factores de costo, sin rangos."),
]
ESTADO = {"si": ("p-ok", "DPROMA: sí"), "parcial": ("p-warn", "DPROMA: parcial"), "no": ("p-err", "DPROMA: no")}


def sec_patrones():
    cards = ""
    for i, (t, d, sitios, est, nota) in enumerate(PATRONES, 1):
        cls, txt = ESTADO[est]
        chips = "".join(f'<span class="pill p-neutro">{esc(x)}</span>' for x in sitios)
        cards += f"""<article class="widget bw-pat"><header><span class="num tnum">{i:02d}</span><span class="pill {cls}">{txt}</span></header>
<h3>{esc(t)}</h3><p>{esc(d)}</p><div class="chips" role="group" aria-label="Lo aplican">{chips}</div><p class="pie">{esc(nota)}</p></article>"""
    n_si = sum(1 for p in PATRONES if p[3] == "si")
    n_par = sum(1 for p in PATRONES if p[3] == "parcial")
    n_no = sum(1 for p in PATRONES if p[3] == "no")
    return f"""
<section id="patrones" aria-labelledby="h-patrones">
<div class="rot"><h2 id="h-patrones">Diez patrones de la competencia</h2><span class="alcance">{ico('m-checklist','ico ico-xs')}{n_si} sí · {n_par} parcial · {n_no} no</span></div>
<div class="widget" style="margin-bottom:var(--sp-4)"><header><h3>DPROMA frente a los patrones</h3></header>
<div class="barra" role="img" aria-label="{n_si} patrones cumplidos, {n_par} parciales, {n_no} no cumplidos"><span class="s-ok" style="width:{n_si*10}%"></span><span class="s-warn" style="width:{n_par*10}%"></span><span class="s-err" style="width:{n_no*10}%"></span></div>
<div class="leyenda"><span><i class="mu" style="background:var(--ok)"></i>Sí <b>{n_si}</b></span><span><i class="mu" style="background:var(--warn)"></i>Parcial <b>{n_par}</b></span><span><i class="mu" style="background:var(--err)"></i>No <b>{n_no}</b></span></div></div>
<div class="patrones">{cards}</div>
</section>"""


def sec_mercado():
    filas = ""
    for m in data["mercado"]:
        nivel_cls = {"Cifras de la empresa": "p-neutro", "Dato de terceros": "p-neutro", "Cifras contradictorias": "p-warn"}[m["nivel"]]
        cuota = f'{m["cuota"]} %' if m["cuota"] else "—"
        filas += f'<tr><th scope="row">{esc(m["nombre"])}</th><td data-et="Escala">{esc(m["escala"])}</td><td class="tnum" data-et="Cuota de uso">{cuota}</td><td data-et="Inversión">{esc(m["inversion"])}</td><td data-et="Calidad del dato"><span class="pill {nivel_cls}">{esc(m["nivel"])}</span></td></tr>'
    conocidas = [m for m in data["mercado"] if m["cuota"]]
    barras = "".join(f'<li><span class="et">{esc(m["nombre"])}</span><div class="barra"><span class="s-pausa" style="width:{m["cuota"]/25*100:.0f}%"></span></div><b class="tnum">{m["cuota"]} %</b></li>' for m in sorted(conocidas, key=lambda m: -m["cuota"]))
    return f"""
<section id="mercado" aria-labelledby="h-mercado">
<div class="rot"><h2 id="h-mercado">Contexto de mercado en México</h2><span class="alcance">{ico('m-map','ico ico-xs')}escala, no facturación</span></div>
<p class="banda" style="margin-bottom:var(--sp-4)">{ico('m-info')}<span><b>No es facturación.</b> Las redes de carga son empresas privadas y no publican ingresos. Esta tabla muestra escala e inversión anunciadas. Cuando el cliente aporte cifras de facturación, el orden puede cambiar.</span></p>
<div class="dash">
  <div class="widget" style="grid-column:span 12"><header><h3>Operadores de carga</h3></header>
    <div class="tabla-caja"><table class="mer"><caption class="sr">Escala, cuota de uso e inversión de los operadores de carga en México</caption>
    <thead><tr><th>Empresa</th><th>Escala</th><th>Cuota de uso</th><th>Inversión</th><th>Calidad del dato</th></tr></thead><tbody>{filas}</tbody></table></div>
  </div>
  <div class="widget" style="grid-column:span 12" data-w="6"><header><h3>Cuota de uso (tres datos conocidos)</h3></header>
    <ul class="bw-cuota">{barras}</ul>
    <p class="pie">Fuente: Expansión, junio de 2026. Evergo no tiene porcentaje publicado; se le atribuye el mayor despliegue.</p>
  </div>
  <div class="widget" style="grid-column:span 12" data-w="6"><header><h3>Administración vehicular</h3></header>
    <p>Competidores identificados con oferta B2B para flotillas: <b>GEVAC</b>, <b>Red-T</b> y <b>Traslandon</b>, más gestorías locales. No hay cifras públicas ni un líder identificado.</p>
    <p class="pie">Pendiente: confirmar con el cliente a quién ve como competidor real.</p>
  </div>
</div>
</section>"""


LENTES = [
    ("Negocio", "m-work", "Alta", [
        "DPROMA es el único del grupo que une carga EV y gestoría vehicular en un mismo sitio.",
        "Sus cifras visibles (20,000+ trámites, 9 ciudades) son de administración vehicular; ninguna es de carga EV.",
        "Las redes de carga compiten por conductores; DPROMA vende a empresas.",
    ], "Posicionarse como integrador y operador para empresas, no como red pública."),
    ("Experiencia de usuario", "m-person", "Alta", [
        "Navegación, pestañas por industria y pre-diagnóstico funcionan y se entienden.",
        "El proceso aparece dos veces con forma distinta: cuatro pasos arriba y cinco fases más abajo.",
        "La experiencia digital es una maqueta; el producto no se ve real.",
    ], "Unificar el proceso, mostrar producto real y dejar que el pre-diagnóstico envíe su resumen."),
    ("Marketing", "m-article", "Alta", [
        "No hay fotografía ni video de instalaciones; FAZT, BYD y Enphase puntúan 3 en este criterio.",
        "El blog tiene tres artículos; los referentes tienen centros de recursos completos.",
        "Propósito, misión, visión y principios ya existen en «Nosotros», pero no llegan al hero.",
    ], "Sesión fotográfica, casos cortos y páginas de SEO por industria."),
    ("Comercial", "m-trending_up", "Alta", [
        "El CTA principal es único; ChargePoint y BYD combinan experto, cotización y canal directo.",
        "Los «casos» son escenarios ilustrativos; no hay clientes con nombre.",
        "No hay rangos de inversión, aunque sí se explican los factores de costo.",
    ], "CTA doble, rangos orientativos y dos o tres casos reales con permiso del cliente."),
]


def sec_lentes():
    cards = ""
    for t, ic, pr, hs, op in LENTES:
        li = "".join(f"<li>{esc(h)}</li>" for h in hs)
        cards += f"""<article class="widget bw-lente"><header><h3>{ico(ic,'ico')} {esc(t)}</h3><span class="pill p-err">Prioridad {pr.lower()}</span></header>
<ul class="hall">{li}</ul><div class="op"><b>Oportunidad</b><p>{esc(op)}</p></div></article>"""
    return f"""
<section id="lentes" aria-labelledby="h-lentes">
<div class="rot"><h2 id="h-lentes">Cuatro puntos de vista</h2><span class="alcance">{ico('m-visibility','ico ico-xs')}negocio · UX · marketing · comercial</span></div>
<div class="lentes">{cards}</div>
</section>"""


IA_CASOS = [
    ("Asesor de pre-diagnóstico (web y WhatsApp)", ["Medio", "Alto", "Medio", "Alto"], "Bajo", "Primero"),
    ("Agente de WhatsApp para cualificar y dar seguimiento", ["Medio", "Medio", "Medio", "Alto"], "Medio", "Segundo"),
    ("Asesor de trámites vehiculares", ["Alto", "Alto", "Medio", "Medio"], "Alto", "Tras validar normativa"),
    ("Agente de voz (llamadas)", ["Bajo", "Medio", "Bajo", "Medio"], "Medio", "Fase posterior"),
]
NV = {"Alto": "p-ok", "Medio": "p-neutro", "Bajo": "p-warn"}
RV = {"Bajo": "p-ok", "Medio": "p-warn", "Alto": "p-err"}


def sec_ia():
    filas = ""
    for t, imp, ries, cuando in IA_CASOS:
        tds = "".join(f'<td data-et="{l}"><span class="pill {NV[x]}">{x}</span></td>' for l, x in zip(["Negocio", "UX", "Marketing", "Comercial"], imp))
        filas += f'<tr><th scope="row">{esc(t)}</th>{tds}<td data-et="Riesgo"><span class="pill {RV[ries]}">{ries}</span></td><td data-et="Cuándo">{esc(cuando)}</td></tr>'
    return f"""
<section id="ia" aria-labelledby="h-ia">
<div class="rot"><h2 id="h-ia">¿Conviene incluir IA?</h2><span class="alcance">{ico('m-support_agent','ico ico-xs')}capa transversal, acotada</span></div>
<div class="widget bw-veredicto"><header><h3>Veredicto</h3></header>
<p class="bw-frase" style="font-size:var(--fs-sub)"><b>Sí, pero acotada.</b> <span>Un asesor conversacional que cualifica proyectos y agenda el diagnóstico aporta valor en las cuatro lentes. «IA en todo» no.</span></p></div>
<div class="widget" style="margin-top:var(--sp-4)"><header><h3>Casos de uso frente a las cuatro lentes</h3><span class="n">Valoración del equipo evaluador</span></header>
<div class="tabla-caja"><table><caption class="sr">Impacto por lente, riesgo y momento de cada caso de uso de IA</caption>
<thead><tr><th>Caso de uso</th><th>Negocio</th><th>UX</th><th>Marketing</th><th>Comercial</th><th>Riesgo</th><th>Cuándo</th></tr></thead><tbody>{filas}</tbody></table></div></div>
<div class="dash" style="margin-top:var(--sp-4)">
  <div class="widget" style="grid-column:span 12" data-w="6"><header><h3>Tecnología: a comparar en un piloto</h3></header>
    <ul class="hall">
      <li><b>ElevenLabs Agents</b>: un mismo agente en web, teléfono y WhatsApp, con voz y texto. Fuerte en voz. Por verificar: español de México, precios e integración con CRM.</li>
      <li><b>Modelo de lenguaje propio</b> (Gemini, Claude u otro) con base de conocimiento validada, para precisión técnica; puede darle voz ElevenLabs.</li>
      <li><b>Plataformas de chat y WhatsApp</b> (Botpress, Voiceflow, Cliengo, Infobip): si pesa más la rapidez de despliegue. No evaluadas.</li>
    </ul></div>
  <div class="widget" style="grid-column:span 12" data-w="6"><header><h3>Piloto propuesto</h3></header>
    <ul class="hall">
      <li>Caso 1, de 6 a 8 semanas, en prueba A/B contra el formulario actual.</li>
      <li>Mide: diagnósticos agendados, tiempo de respuesta, tasa de cualificación y traspaso a un humano.</li>
      <li>Condiciones previas: tono de marca para la web, base de conocimiento validada, política de escalamiento y aviso de privacidad.</li>
      <li>Metas numéricas: se fijan con el cliente. No se inventan aquí.</li>
    </ul></div>
</div>
</section>"""


FASES = [
    ("Fase 0", "Fundamentos", "0–4 semanas", ["Manual de marca y fuentes", "Posicionamiento y segmento prioritario", "Casos y permisos de logos", "Sesión fotográfica", "Entrevistas a clientes externos"]),
    ("Fase 1", "Victorias rápidas", "1–3 meses", ["Unificar el proceso", "FAQ y 2–3 casos reales", "CTA doble y WhatsApp prellenado", "Analítica de eventos", "Comparación de IA y piloto del asesor"]),
    ("Fase 2", "Rediseño", "3–6 meses", ["Sistema de diseño web de marca", "Centro de recursos", "SEO por industria y ciudad", "Cotizador con rangos", "Producto digital real a la vista"]),
    ("Fase 3", "Escala", "6–12 meses", ["App descargable", "Versiones para otros países", "Pruebas A/B continuas", "Contenido de autoridad"]),
]


def sec_ruta():
    cols = ""
    for i, (f, t, cuando, its) in enumerate(FASES):
        li = "".join(f"<li>{esc(x)}</li>" for x in its)
        cols += f'<li class="widget bw-fase"><span class="paso tnum" aria-hidden="true">{i}</span><h3>{esc(t)}</h3><p class="cuando">{esc(f)} · {esc(cuando)}</p><ul class="hall">{li}</ul></li>'
    return f"""
<section id="ruta" aria-labelledby="h-ruta">
<div class="rot"><h2 id="h-ruta">Hoja de ruta</h2><span class="alcance">{ico('m-schedule','ico ico-xs')}12 meses</span></div>
<ol class="ruta">{cols}</ol>
</section>"""


def sec_sistema():
    v = vf.get("resumen", "")
    nota_v = f'<p class="nota-reloj nota">{ico("m-info")}<span><b>Comprobado en esta página.</b> {esc(v)}</span></p>' if v else ""
    return f"""
<section id="sistema" aria-labelledby="h-sistema">
<div class="rot"><h2 id="h-sistema">¿Es aplicable el sistema de diseño de SIO-DPROMA?</h2><span class="alcance">{ico('m-verified_user','ico ico-xs')}esta página es la prueba</span></div>
<div class="widget bw-veredicto"><header><h3>Veredicto</h3></header>
<p class="bw-frase" style="font-size:var(--fs-sub)"><b>Sí, con cuatro huecos documentados.</b> <span>Cromo, tokens, rejilla, tablas, semáforo y capa de dashboard sirvieron tal cual. Las piezas de análisis se resolvieron componiendo; no hay regla para ellas.</span></p></div>
<div class="tres">
  <div class="widget"><header><h3>{ico('m-check_circle','ico ico-sm')} Sirvió tal cual</h3></header>
  <ul class="hall"><li>Cromo de aplicación, menú lateral, tema claro y oscuro.</li><li>Rejilla de doce columnas, <code>.widget</code> y <code>.cifras</code>.</li><li>Barra apilada, leyenda y ranking con tabla equivalente (§12).</li><li>Pastillas del semáforo para la nota de 0 a 3.</li><li>Tabla densa, nota de método y banda.</li></ul></div>
  <div class="widget"><header><h3>{ico('m-build','ico ico-sm')} Se resolvió componiendo</h3></header>
  <ul class="hall"><li>Matriz de 12 × 8: tabla + pastilla + botón por celda.</li><li>Marco de captura: tarjeta con barra de URL.</li><li>Brecha por criterio: barra de CSS con el semáforo.</li><li>Hoja de ruta: lista ordenada de widgets.</li></ul></div>
  <div class="widget"><header><h3>{ico('m-error','ico ico-sm')} Huecos: reglas por proponer</h3></header>
  <ul class="hall"><li><b>Mapa de calor</b> con puntuaciones discretas.</li><li><b>Captura anotada</b> con marcadores numerados y lista.</li><li><b>Ilustración interactiva decorativa</b> (terreno de Hairline): nunca debe llevar un dato.</li><li><b>Escala de cuatro niveles</b> (0–3) frente a los cinco estados del semáforo.</li></ul></div>
</div>
{nota_v}
</section>"""


FUENTES = [
    ("Expansión · cuota de uso de cargadores (jun-2026)", "https://expansion.mx/empresas/2026/06/03/mexicanos-ya-no-prefieren-tesla-cargan-auto-electrico-red"),
    ("El Financiero · VEMO recauda fondos (sep-2025)", "https://www.elfinanciero.com.mx/empresas/2025/09/02/mas-autos-chinos-para-uber-mexico-vemo-recauda-fondos-para-expandir-su-flota-en-cdmx-y-monterrey/"),
    ("Clúster Industrial · VEMO suma 1,950 conectores", "https://clusterindustrial.com.mx/vemo-suma-1-950-conectores-para-facilitar-la-recarga-de-vehiculos-electricos-en-mexico/"),
    ("Evergo · más de 15,000 estaciones planeadas", "https://evergo.com/en/evergo-to-revolutionize-electric-mobility-in-mexico-with-more-than-15000-charging-stations-planned/"),
    ("Valencia Plaza · Factorenergia lanza FAZT en México", "https://valenciaplaza.com/nr-economia/factorenergia-lanza-fazt-en-mexico-con-el-objetivo-de-instalar-1.000-puntos-de-carga-electrica-hasta-2030"),
    ("ElevenLabs · Agents con WhatsApp", "https://elevenlabs.io/es/blog/elevenlabs-agents-whatsapp-support"),
]


def sec_fuentes():
    li = "".join(f'<li><a class="lnk" href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in FUENTES)
    sitios = "".join(f'<li><a class="lnk" href="{s["url"]}" rel="noopener">{esc(s["nombre"])}</a></li>' for s in data["sitios"])
    return f"""
<section id="fuentes" aria-labelledby="h-fuentes">
<div class="rot"><h2 id="h-fuentes">Fuentes y créditos</h2></div>
<div class="tres">
  <div class="widget"><header><h3>Sitios evaluados</h3></header><ul class="hall">{sitios}</ul></div>
  <div class="widget"><header><h3>Datos de mercado</h3></header><ul class="hall">{li}</ul></div>
  <div class="widget"><header><h3>Créditos</h3></header><ul class="hall"><li>Terrenos: <a class="lnk" href="https://github.com/lucasmarkes/hairline" rel="noopener">@lucasmarkes/hairline</a> 0.5.1, licencia MIT (<a class="lnk" href="vendor/hairline-LICENSE.txt">texto</a>).</li><li>Gráficas: Chart.js 4.5.0.</li><li>Capturas de sitios de terceros, solo para análisis interno.</li><li>Datos y evidencia por celda: <a class="lnk" href="datos/benchmark.json">datos/benchmark.json</a>.</li></ul></div>
</div>
</section>"""


# ───────────────────────── CSS propio ─────────────────────────
CSS = r"""
/* ═══ Benchmark web — estilos propios de esta pantalla (sobre los tokens de SIO-DPROMA) ═══ */
.cifras{ display:grid; gap:var(--sp-3); align-items:start; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); grid-template-rows:auto auto }
.cifras > .kpi{ grid-row:span 2; display:grid; grid-template-rows:subgrid; gap:var(--sp-1); background:var(--surface-2); border:1px solid transparent; border-radius:var(--r-card); padding:var(--sp-4) }
@media (forced-colors:active){ .cifras > .kpi{ border-color:CanvasText } }
.cifras .etq{ display:flex; flex-direction:column; overflow-wrap:anywhere }
.cifras .rotulo{ font-size:var(--fs-base); font-weight:500; color:var(--text) }
.cifras .apoyo{ font-size:var(--fs-meta); line-height:1.4; color:var(--text-3-fuerte) } /* §12.4.1 dice --text-3 (4,93:1); medido sobre --surface-2 da 4,2:1. --text-3-fuerte cumple. */
@supports not (grid-template-rows:subgrid){ .cifras > .kpi{ grid-row:auto; grid-template-rows:none } }
.tnum{ font-variant-numeric:tabular-nums }
.nota-reloj{ margin-top:var(--sp-4) }
.bw-sub{ color:var(--text-2); font-size:var(--fs-dense); line-height:1.6; margin:0 0 var(--sp-4); max-width:78ch }
.bw-h3{ font:700 var(--fs-base) var(--font-ui); margin:var(--sp-6) 0 var(--sp-3) }
main[id="contenido"] section[id]{ scroll-margin-top:var(--sp-4) }
.tab > section + section{ margin-top:var(--sp-2) }
.widget .pie{ margin:0 }
.widget > header h3{ display:inline-flex; align-items:center; gap:var(--sp-2) }
.widget p{ margin:0 }
.hall{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:var(--sp-2) }
.hall li{ position:relative; padding-left:var(--sp-4); font-size:var(--fs-dense); line-height:1.55; color:var(--text-2) }
.hall li::before{ content:""; position:absolute; left:2px; top:.62em; width:6px; height:6px; border-radius:2px; background:var(--accent) }
.hall li b{ color:var(--text) }
code{ font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.92em; background:var(--surface-2); padding:1px 5px; border-radius:4px }

/* Resumen */
.bw-hero{ display:grid; grid-template-columns:minmax(0,1.15fr) minmax(0,1fr); gap:var(--sp-4); align-items:stretch }
@media (max-width:980px){ .bw-hero{ grid-template-columns:1fr } }
.bw-frase{ font:700 var(--fs-title)/1.3 var(--font-ui); letter-spacing:-.01em; color:var(--text) }
.bw-frase span{ color:var(--text-2); font-weight:500 }
.bw-puntos{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:var(--sp-3) }
.bw-puntos li{ display:flex; gap:var(--sp-3); align-items:flex-start; font-size:var(--fs-base); line-height:1.5; color:var(--text-2) }
.bw-puntos li .ico{ margin-top:2px; flex:none; color:var(--accent) }
.bw-puntos li b{ color:var(--text) }
.bw-firma{ margin:0; background:var(--surface); border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--sh-rest); padding:var(--sp-4); display:flex; flex-direction:column; gap:var(--sp-2); justify-content:center; min-width:0 }
.bw-firma figcaption{ font-size:var(--fs-meta); color:var(--text-3); line-height:1.5; text-align:center }

/* Terrenos (Hairline). El terreno es ilustración: nunca lleva un dato. */
.terreno{ --hairline-plate:var(--surface); --hairline-hi:var(--text); --hairline-edge:var(--text-3);
  --hairline-mid:color-mix(in srgb,var(--text-3) 55%,var(--surface)); --hairline-lo:color-mix(in srgb,var(--text-3) 26%,var(--surface)); --hairline-stroke:.9;
  width:100%; aspect-ratio:5/4; min-height:120px }
.terreno.dproma{ --hairline-hi:var(--accent) }
.terreno.apagado{ opacity:.42; filter:grayscale(1) }
.panorama{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:var(--sp-4) }
.bw-emp{ padding:var(--sp-3); gap:var(--sp-2); transition:border-color var(--dur-base) var(--ease-out), box-shadow var(--dur-base) var(--ease-out) }
.bw-emp:hover,.bw-emp:focus-visible,.bw-emp.activa{ border-color:var(--accent) }
.bw-emp-datos h3{ font:700 var(--fs-base) var(--font-ui); text-transform:none; letter-spacing:0; color:var(--text); margin:0 }
.bw-emp-datos .rol{ font-size:var(--fs-meta); color:var(--text-3); margin:2px 0 var(--sp-2) }
.bw-emp-datos .fila{ display:flex; gap:var(--sp-2); flex-wrap:wrap; align-items:center }
.bw-emp-datos .meta{ font-size:var(--fs-meta); color:var(--text-3); margin-top:var(--sp-2) }
.bw-emp-datos .motivo{ font-size:var(--fs-meta); color:var(--text-2); margin-top:var(--sp-2); line-height:1.5 }
.pill .de{ opacity:.7; font-weight:600 }

/* Ranking, escala */
.dash > [data-w="7"]{ grid-column:span 12 }
.dash > [data-w="5"]{ grid-column:span 12 }
@media (min-width:1100px){ .dash > [data-w="7"]{ grid-column:span 7 } .dash > [data-w="5"]{ grid-column:span 5 } .dash > [data-w="6"]{ grid-column:span 6 } }
.dash > [data-w="6"]{ grid-column:span 12 }
.bw-escala{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:var(--sp-3) }
.bw-escala li{ display:flex; gap:var(--sp-3); align-items:center; font-size:var(--fs-base) }

/* Matriz */
.tabla-caja.bw-matriz{ overflow-x:auto; max-width:100% }
.bw-matriz table{ min-width:860px }
.bw-matriz thead th{ text-align:center }
.bw-matriz thead th.esq{ text-align:left; min-width:230px; position:sticky; left:0; z-index:8 }
.bw-matriz thead th[scope="colgroup"]{ border-bottom:1px solid var(--border); color:var(--text-3); font-size:11px }
.bw-matriz tbody th{ white-space:normal; font-weight:500; position:sticky; left:0; background:var(--surface); z-index:4; min-width:230px }
.bw-matriz tbody th .tipo{ display:inline-block; margin-left:var(--sp-2); font-size:11px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; color:var(--text-3) }
.bw-matriz td{ text-align:center; padding:var(--sp-1) var(--sp-2) }
.bw-matriz tfoot th,.bw-matriz tfoot td{ border-top:2px solid var(--border-2); border-bottom:none; font-weight:600; text-align:center; height:var(--row-comfy) }
.bw-matriz tfoot th{ text-align:left; position:sticky; left:0; background:var(--surface) }
.bw-matriz tfoot .sin{ color:var(--text-3); font-weight:500 }
.bw-matriz .col-dproma{ background:var(--accent-soft) }
.bw-matriz [data-col].resalta{ background:var(--surface-2) }
.bw-matriz .col-dproma.resalta{ background:var(--accent-soft) }
.celda{ appearance:none; border:1px solid transparent; background:transparent; border-radius:var(--r-ctrl); padding:3px; cursor:pointer; min-width:44px; min-height:34px; display:inline-flex; align-items:center; justify-content:center }
.celda:hover{ border-color:var(--border-2) }
.celda[aria-pressed="true"]{ border-color:var(--accent); box-shadow:0 0 0 2px var(--accent-soft) }
.celda .pill{ min-width:32px; justify-content:center }
.bw-evid{ margin-top:var(--sp-4) }
.bw-evid .vacio{ color:var(--text-3); font-size:var(--fs-dense) }
.bw-evid .tit{ display:flex; gap:var(--sp-3); align-items:center; flex-wrap:wrap }
.bw-evid .tit b{ font-size:var(--fs-base) }
.bw-evid .def{ color:var(--text-3); font-size:var(--fs-meta) }
.bw-evid .txt{ font-size:var(--fs-base); line-height:1.6; color:var(--text) }
.bw-evid ul.chk{ list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:var(--sp-2) }

/* Brecha */
.bw-brecha{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column }
.bw-fila{ display:grid; grid-template-columns:minmax(0,1.2fr) minmax(0,1.6fr) minmax(0,1fr); gap:var(--sp-4); align-items:center; padding:var(--sp-3) 0; border-bottom:1px solid var(--border) }
.bw-fila:last-child{ border-bottom:none }
@media (max-width:900px){ .bw-fila{ grid-template-columns:1fr; gap:var(--sp-2) } }
.bw-fila .et{ display:flex; gap:var(--sp-2); align-items:center; flex-wrap:wrap; font-size:var(--fs-base) }
.bw-fila .vals{ display:flex; gap:var(--sp-4); flex-wrap:wrap; font-size:var(--fs-meta); color:var(--text-3) }
.bw-fila .vals span{ display:inline-flex; align-items:center; gap:var(--sp-2) }
.bw-fila .vals small{ color:var(--text-3) }
.bw-fila .gap{ display:flex; align-items:center; gap:var(--sp-3) }
.bw-fila .gap .barra{ flex:1 }
.bw-fila .gap b{ min-width:2ch; text-align:right }
.barra .s-pausa{ background:var(--pause) }

/* Capturas */
.bw-vista-ctl{ display:flex; gap:var(--sp-4); align-items:center; flex-wrap:wrap; margin-bottom:var(--sp-4) }
.galeria{ display:grid; grid-template-columns:repeat(auto-fill,minmax(min(100%,520px),1fr)); gap:var(--sp-4); align-items:start }
.galeria[data-vista="mov"]{ grid-template-columns:repeat(auto-fill,minmax(230px,1fr)) }
.marco{ margin:0; background:var(--surface); border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--sh-rest); overflow:hidden; min-width:0; display:flex; flex-direction:column }
.marco-barra{ display:flex; align-items:center; gap:var(--sp-3); padding:6px var(--sp-3); background:var(--surface-2); border-bottom:1px solid var(--border) }
.marco-barra .pts{ display:inline-flex; gap:5px }
.marco-barra .pts i{ width:9px; height:9px; border-radius:50%; background:var(--border-2) }
.marco-barra .url{ font-size:var(--fs-meta); color:var(--text-3); overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
.marco img{ display:block; width:100%; height:auto }
.marco figcaption{ padding:var(--sp-3); font-size:var(--fs-meta); color:var(--text-3); line-height:1.5; border-top:1px solid var(--border) }
.marco figcaption b{ color:var(--text) }
.cap{ position:relative }
.mk{ position:absolute; transform:translate(-50%,-50%); width:22px; height:22px; border-radius:50%; background:var(--accent); color:var(--accent-ink); font:800 12px/22px var(--font-ui); text-align:center; box-shadow:0 0 0 2px #fff, 0 1px 4px rgba(0,0,0,.45) }
.anot{ margin:0; padding:var(--sp-3) var(--sp-4) var(--sp-3) calc(var(--sp-4) + 22px); display:flex; flex-direction:column; gap:4px; font-size:var(--fs-meta); color:var(--text-2); line-height:1.45; list-style:decimal }
.v-mov{ display:none; padding:var(--sp-3); background:var(--surface-2) }
.v-mov img{ max-width:260px; margin:0 auto; border-radius:14px; border:1px solid var(--border-2) }
.galeria[data-vista="mov"] .v-esc{ display:none }
.galeria[data-vista="mov"] .v-mov{ display:block }
.marco.vacio .hueco-cap{ padding:var(--sp-8) var(--sp-4); display:flex; flex-direction:column; align-items:center; text-align:center; gap:var(--sp-2); color:var(--text-2); font-size:var(--fs-dense); line-height:1.5; background:repeating-linear-gradient(135deg,transparent 0 10px,var(--surface-2) 10px 11px) }
.marco.vacio .hueco-cap .ico{ width:26px; height:26px; color:var(--text-3) }
.extras{ display:grid; grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr)); gap:var(--sp-4) }

/* Patrones, lentes, mercado, ruta */
.patrones{ display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:var(--sp-4) }
.bw-pat header{ justify-content:space-between }
.bw-pat .num{ font:800 var(--fs-title)/1 var(--font-ui); color:var(--text-3) }
.bw-pat h3{ font:700 var(--fs-base) var(--font-ui); margin:0; text-transform:none; letter-spacing:0; color:var(--text) }
.bw-pat p{ font-size:var(--fs-dense); color:var(--text-2); line-height:1.5 }
.bw-pat .chips{ display:flex; flex-wrap:wrap; gap:var(--sp-1) }
.lentes{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr)); gap:var(--sp-4) }
.bw-lente > header{ align-items:center }
.bw-lente > header h3{ display:inline-flex; align-items:center; gap:var(--sp-2) }
.bw-lente .op{ border-top:1px solid var(--border); padding-top:var(--sp-3); display:flex; flex-direction:column; gap:var(--sp-1) }
.bw-lente .op p{ font-size:var(--fs-dense); color:var(--text); line-height:1.5 }
.bw-lente .op b{ font-size:var(--fs-meta); text-transform:uppercase; letter-spacing:.06em; color:var(--accent) }
.mer td,.mer th{ white-space:normal; height:auto; padding:var(--sp-3) var(--sp-4); vertical-align:top }
.bw-cuota{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:var(--sp-3) }
.bw-cuota li{ display:grid; grid-template-columns:80px 1fr 52px; gap:var(--sp-3); align-items:center; font-size:var(--fs-dense) }
.bw-cuota b{ text-align:right }
.tres{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr)); gap:var(--sp-4); margin-top:var(--sp-4) }
.bw-veredicto{ border-left:4px solid var(--accent) }
.ruta{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr)); gap:var(--sp-4); counter-reset:f }
.bw-fase{ position:relative }
.bw-fase .paso{ width:30px; height:30px; border-radius:50%; background:var(--accent); color:var(--accent-ink); display:grid; place-items:center; font-weight:800 }
.bw-fase h3{ font:700 var(--fs-sub) var(--font-ui); text-transform:none; letter-spacing:0; color:var(--text); margin:0 }
.bw-fase .cuando{ font-size:var(--fs-meta); color:var(--text-3) }
.side .it[aria-current="location"]{ background:var(--chrome-activo); color:var(--chrome-ink); font-weight:600; border-left-color:var(--ok) }
.viz-tabla{ overflow-x:auto }
.viz-tabla td,.viz-tabla th{ white-space:normal }
@media print{ .side,.cromo-top,.fab,.demo{ display:none !important } main[id="contenido"]{ overflow:visible } .hoja,.app,.area,.main{ overflow:visible; height:auto } }
@media (prefers-reduced-motion:reduce){ .bw-emp{ transition:none } }
"""

# ───────────────────────── armado ─────────────────────────
src = BASE.read_text(encoding="utf-8")
lines = src.split("\n")
head = "\n".join(lines[:817])  # hasta antes de </style> (línea 818)
assert lines[817].strip() == "</style>", lines[817]
sprite = lines[821]
assert sprite.startswith('<svg width="0" height="0"'), sprite[:60]
head = head.replace("<title>SIO-DPROMA — Tablero de Administración Vehicular</title>", "<title>SIO-DPROMA — Benchmark web de dproma.com</title>")
head = re.sub(r'<meta name="description"[^>]*>', "", head)
head = head.replace("</head>", "")

NAV = [
    ("Principal", [("resumen", "m-dashboard", "Resumen"), ("panorama", "m-group", "Panorama")]),
    ("Benchmark", [("ranking", "m-bar_chart", "Ranking global"), ("matriz", "m-table_chart", "Matriz comparativa"), ("brecha", "m-trending_up", "Brecha de DPROMA")]),
    ("Evidencia", [("capturas", "m-image", "Capturas comparadas"), ("patrones", "m-checklist", "Diez patrones"), ("mercado", "m-map", "Contexto de mercado")]),
    ("Estrategia", [("lentes", "m-visibility", "Cuatro puntos de vista"), ("ia", "m-support_agent", "IA"), ("ruta", "m-schedule", "Hoja de ruta")]),
    ("Sistema", [("sistema", "m-verified_user", "¿Aplica SIO-DPROMA?"), ("fuentes", "m-description", "Fuentes y créditos")]),
]
def cur(i):
    return ' aria-current="location"' if i == 'resumen' else ''


side = ""
for g, items in NAV:
    gid = "g-" + g.lower()
    lis = "".join(f'<li><a class="it" href="#{i}"{cur(i)}><svg class="ico" aria-hidden="true" translate="no"><use href="#{ic}"/></svg><span class="et">{esc(t)}</span></a></li>' for i, ic, t in items)
    side += f'<div class="bloque"><p class="grp" id="{gid}">{g}</p><ul aria-labelledby="{gid}">{lis}</ul></div>'

SCRIPT_BASE = r"""
<script>
(function(){
var raiz=document.documentElement;
var bt=document.getElementById('tema');
var ico=document.getElementById('tema-ico');
var mq=window.matchMedia('(prefers-color-scheme: dark)');
function oscuro(){var t=raiz.getAttribute('data-theme');return t?t==='dark':mq.matches;}
function pinta(){
  var o=oscuro();
  bt.setAttribute('aria-pressed',String(o));
  bt.setAttribute('aria-label',o?'Cambiar a tema claro':'Cambiar a tema oscuro');
  ico.setAttribute('href',o?'#i-sun':'#i-moon');
  var m=document.querySelector('meta[name="theme-color"]');
  if(m)m.setAttribute('content',getComputedStyle(document.body).backgroundColor);
}
bt.addEventListener('click',function(){raiz.setAttribute('data-theme',oscuro()?'light':'dark');pinta();});
mq.addEventListener('change',pinta);
pinta();
var mb=document.getElementById('menu-btn');
var velo=document.querySelector('.velo-menu');
function menu(abierto){
  if(abierto)raiz.setAttribute('data-menu','abierto');else raiz.removeAttribute('data-menu');
  mb.setAttribute('aria-expanded',String(abierto));
  mb.setAttribute('aria-label',abierto?'Cerrar el menú':'Abrir el menú');
  if(velo)velo.tabIndex=abierto?0:-1;
}
if(mb)mb.addEventListener('click',function(){menu(raiz.getAttribute('data-menu')!=='abierto');});
if(velo)velo.addEventListener('click',function(){menu(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape')menu(false);});
/* Menú lateral: marca la sección visible */
var links=[].slice.call(document.querySelectorAll('.side a.it'));
links.forEach(function(a){a.addEventListener('click',function(){menu(false);links.forEach(function(x){x.removeAttribute('aria-current');});a.setAttribute('aria-current','location');});});
var cont=document.getElementById('contenido');
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
    links.forEach(function(x){if(x.getAttribute('href')==='#'+e.target.id)x.setAttribute('aria-current','location');else x.removeAttribute('aria-current');});}});},
    {root:cont,rootMargin:'-10% 0px -80% 0px'});
  document.querySelectorAll('main section[id]').forEach(function(s){io.observe(s);});
}
})();
</script>"""

SCRIPT_PAGE = r"""
<script src="vendor/hairline-terrain.iife.js"></script>
<script>
/* Terrenos (Hairline). Ilustración decorativa: si la librería falta, la tarjeta sigue diciendo lo mismo en texto. */
(function(){
  var quieto=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(typeof Hairline==='undefined'||!Hairline.terrain){document.querySelectorAll('.terreno').forEach(function(t){t.style.display='none';});return;}
  document.querySelectorAll('.terreno').forEach(function(el){
    var apagado=el.getAttribute('data-quieto')==='1';
    try{ Hairline.terrain(el,{play:!quieto&&!apagado,intensity:apagado?0.15:(el.id==='terreno-hero'?0.75:0.5),theme:'auto',
      label:'Ilustración decorativa de '+el.getAttribute('data-nombre')+': pilares que se elevan alrededor del puntero. No contiene datos.'}); }
    catch(e){ el.style.display='none'; }
  });
})();
/* Panorama ↔ matriz: resalta la columna de la empresa */
(function(){
  var cards=document.querySelectorAll('.bw-emp');
  function marca(id,on){
    document.querySelectorAll('.bw-matriz [data-col="'+id+'"]').forEach(function(c){c.classList.toggle('resalta',on);});
    cards.forEach(function(c){c.classList.toggle('activa',on&&c.getAttribute('data-site')===id);});
  }
  cards.forEach(function(c){var id=c.getAttribute('data-site');
    c.addEventListener('mouseenter',function(){marca(id,true);});c.addEventListener('mouseleave',function(){marca(id,false);});
    c.addEventListener('focus',function(){marca(id,true);});c.addEventListener('blur',function(){marca(id,false);});});
})();
/* Matriz: evidencia por celda */
(function(){
  var D=__DATOS__;
  var panel=document.getElementById('evidencia'); var prev=null;
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
  document.querySelectorAll('.celda').forEach(function(b){
    b.addEventListener('click',function(){
      if(prev)prev.removeAttribute('aria-pressed'); b.setAttribute('aria-pressed','true'); prev=b;
      var s=D.sitios[b.dataset.site], c=D.criterios[b.dataset.crit], cell=(D.p[b.dataset.site]||{})[b.dataset.crit];
      var h='<header><h3>Evidencia</h3></header><div class="tit"><b>'+esc(c.nombre)+' · '+esc(s.nombre)+'</b>';
      if(cell){h+='<span class="pill '+['p-err','p-warn','p-neutro','p-ok'][cell.p]+'">'+cell.p+' · '+esc(D.escala[cell.p])+'</span><span class="pill p-neutro">'+(c.tipo==='medido'?'Medido':'Observado')+'</span></div>';
        h+='<p class="def">'+esc(c.def)+'</p><p class="txt">'+esc(cell.e)+'</p>';
        if(cell.checks){h+='<ul class="chk">'+cell.checks.map(function(k){return '<li><span class="pill '+(k[1]?'p-ok':'p-err')+'">'+(k[1]?'Sí':'No')+'</span> '+esc(k[0])+'</li>';}).join('')+'</ul>';}
      } else {h+='<span class="pill p-pause">Sin evaluar</span></div><p class="def">'+esc(c.def)+'</p><p class="txt">'+esc(s.motivo||'No hay evidencia observada para este criterio.')+'</p>';}
      panel.innerHTML=h;
    });
  });
})();
/* Capturas: escritorio / móvil */
(function(){
  var g=document.querySelector('.galeria'); var bs=document.querySelectorAll('[data-vista]');
  document.querySelectorAll('.seg [data-vista]').forEach(function(b){b.addEventListener('click',function(){
    document.querySelectorAll('.seg [data-vista]').forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
    g.setAttribute('data-vista',b.dataset.vista);});});
})();
</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.min.js"></script>
<script>
/* Envoltura de Chart.js — §12.2 del sistema de diseño: tokens en caliente, repintado solo al cambiar de tema,
   sin animación en movimiento reducido y sin cortar el resto si el CDN falla. */
(function(){
  var quieto=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hay=typeof Chart!=='undefined';
  var el=document.getElementById('v-ranking'); var inst=null;
  if(!hay){document.querySelectorAll('.viz').forEach(function(v){v.classList.add('sin-libreria');var d=v.querySelector('.viz-tabla');if(d)d.open=true;});return;}
  var R=__RANKING__;
  function tk(n){return getComputedStyle(document.body).getPropertyValue(n).trim();}
  function config(){
    return {type:'bar',data:{labels:R.map(function(r){return r[0];}),datasets:[{label:'Puntaje',data:R.map(function(r){return r[1];}),
        backgroundColor:R.map(function(r){return r[2]?tk('--accent'):tk('--pause');}),borderRadius:4,barThickness:22}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:4},animation:quieto?false:{duration:200},
        plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.parsed.x+' de __MAX__';}}}},
        scales:{x:{min:0,max:__MAX__,grid:{color:tk('--grid-viz')},ticks:{color:tk('--text-3'),stepSize:6},border:{display:false}},
                y:{grid:{display:false},ticks:{color:tk('--text-2')},border:{display:false}}}}};
  }
  function pinta(){if(inst)inst.destroy();inst=new Chart(el,config());}
  if(el)pinta();
  new MutationObserver(function(){if(el)pinta();}).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(){if(el)pinta();});
})();
</script>"""

js_datos = {
    "sitios": {s: {"nombre": SITES[s]["nombre"], "motivo": SITES[s].get("motivo", "")} for s in SITES},
    "criterios": {c["id"]: {"nombre": c["nombre"], "def": c["def"], "tipo": c["tipo"]} for c in CRIT},
    "escala": {int(k): v for k, v in ESCALA.items()},
    "p": {s: {c: {k: v for k, v in cell.items() if k in ("p", "e", "checks")} for c, cell in P.get(s, {}).items()} for s in SITES},
}
js_rank = [[SITES[s]["corto"], TOTAL[s], s == "dproma"] for s in ranking]
script_page = (SCRIPT_PAGE
               .replace("__DATOS__", json.dumps(js_datos, ensure_ascii=False))
               .replace("__RANKING__", json.dumps(js_rank, ensure_ascii=False))
               .replace("__MAX__", str(MAXP)))

HEADER = f"""<div class="area"><header class="cromo-top" data-cromo>
<button class="iconbtn hamburguesa" type="button" id="menu-btn" aria-label="Abrir el menú" aria-expanded="false" aria-controls="menu-lateral"><svg class="ico" aria-hidden="true" translate="no"><use href="#m-menu"/></svg></button>
<div class="hueco" aria-hidden="true"></div>
<div class="derecha">
<button class="iconbtn" type="button" id="tema" aria-label="Cambiar a tema claro" aria-pressed="false"><svg class="ico" aria-hidden="true" translate="no"><use href="#m-dark_mode" id="tema-ico"/></svg></button>
<span class="cromo-prof" role="group" aria-label="Elaborado por 2894 Studio"><span class="cromo-av" aria-hidden="true">2S</span><span class="cromo-quien"><b>2894 Studio</b><small>Análisis para DPROMA</small></span></span>
</div>
</header><div class="main">
<div class="p4">
<div class="p4-t"><h1>Benchmark web de dproma.com</h1><span class="resumen"><b>{len(COMPLETOS)}</b> sitios puntuados · <b>{len(CRIT)}</b> criterios · {FECHA}</span><div class="acc"><a class="btn p" href="#matriz">{ico('m-table_chart')}Ir a la matriz</a><button class="btn" type="button" onclick="window.print()">{ico('m-print')}Imprimir</button></div></div>
</div><main id="contenido" tabindex="-1"><div class="tab">"""

body = (
    '<body>\n<a class="skip" href="#contenido">Saltar al contenido</a>\n' + sprite + '\n<div class="hoja">\n'
    '<div class="app"><button class="velo-menu" data-cromo type="button" aria-label="Cerrar el menú" tabindex="-1"></button>'
    '<nav class="side" data-cromo id="menu-lateral" aria-label="Navegación principal"><div class="logo"><svg width="44" height="42" viewBox="740 0 970 932" aria-hidden="true"><use href="#dproma-mark"/></svg><span class="wordmark" translate="no">SIO-DPROMA</span></div>'
    '<div class="side-scroll">' + side + '</div></nav>' + HEADER +
    sec_resumen() + sec_panorama() + sec_ranking() + sec_matriz() + sec_brecha() + sec_capturas() + sec_patrones() + sec_mercado() + sec_lentes() + sec_ia() + sec_ruta() + sec_sistema() + sec_fuentes() +
    '</div></main></div></div></div></div>\n' + SCRIPT_BASE + script_page + '\n</body>\n</html>\n'
)

desc = '<meta name="description" content="Benchmark de la web de DPROMA frente a competidores de carga EV en México y referentes de tecnología, automotriz y energía renovable.">'
out = head.replace("<style>", desc + "\n<style>", 1) + "\n" + CSS + "\n</style>\n</head>\n" + body
(OUT / "index.html").write_text(out, encoding="utf-8")
print("OK", len(out) // 1024, "KB · DPROMA", TOTAL["dproma"], "· puesto", pos_dproma, "de", len(COMPLETOS))
print({s: TOTAL[s] for s in ranking})
print([(b["id"], b["gap"]) for b in brecha])
