#!/usr/bin/env python3
"""Genera experimentos/benchmark-web/index.html (experimento interno: NO va en web/, que publica Vercel) con la estética de los entregables
(sistema de diseño 2894_ / AZ: DM Sans, cloud white, cobalt, ink; docs/brand/az-branding-guide.md).

Fuente de datos: datos/benchmark.json (puntuaciones y evidencia observadas) y
datos/medidas.json (métricas automáticas de cada home). Resultado de la verificación:
datos/verificacion.json (opcional).
"""
import html
import json
import pathlib
import re
import statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "experimentos/benchmark-web"
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
MISION = "Diseño aumentado, prompting consciente, IA práctica."

# ───────────────────────── medidas automáticas ─────────────────────────
def checks_seo(m):
    mm = m["m"]
    return [("Descripción", bool(mm.get("desc"))), ("Canonical", bool(mm.get("canonical"))),
            ("Open Graph (≥4)", mm.get("og", 0) >= 4), ("Un solo H1", mm.get("h1") == 1),
            ("Datos estructurados", mm.get("jsonld", 0) >= 1), ("Alt completo", mm.get("imgsNoAlt", 1) == 0)]


def checks_a11y(m):
    mm = m["m"]
    return [("Idioma declarado", bool(mm.get("lang"))), ("Viewport", bool(mm.get("viewport"))),
            ("Enlace de salto", bool(mm.get("skip"))), ("Sin desbordamiento en móvil", m.get("mobileScrollW", 9999) <= 390),
            ("Alt completo", mm.get("imgsNoAlt", 1) == 0)]


def nivel(n, tabla):
    for minimo, p in tabla:
        if n >= minimo:
            return p
    return 0


P = data["puntuaciones"]
for sid, m in med.items():
    if sid not in P or not m.get("m"):
        continue
    for cid, fn, tabla in (("seo", checks_seo, [(6, 3), (4, 2), (2, 1)]), ("a11y", checks_a11y, [(5, 3), (4, 2), (3, 1)])):
        cs = fn(m)
        n = sum(1 for _, ok in cs if ok)
        fallos = [t for t, ok in cs if not ok]
        P[sid][cid] = {"p": nivel(n, tabla), "e": f"{n} de {len(cs)} comprobaciones" + (f"; falla: {', '.join(fallos)}." if fallos else "; todas correctas."), "checks": cs}


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
    brecha.append({"id": c["id"], "d": d, "med": statistics.median(v for v, _ in vals), "best": best[0],
                   "best_site": [SITES[s]["corto"] for v, s in vals if v == best[0]], "gap": best[0] - d})
brecha.sort(key=lambda b: (-b["gap"], -(b["med"] - b["d"])))


def fmt_med(x):
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}".replace(".", ",")


def chip(p):
    """Puntuación 0–3 en rampa monocroma (la marca excluye rojo, ámbar y verde)."""
    if p is None:
        return '<span class="chip sn">—</span>'
    return f'<span class="chip s{p}">{p}</span>'


EVID = {"completa": "Evidencia completa", "parcial": "Evidencia parcial", "ninguna": "Sin evidencia"}

# ───────────────────────── secciones ─────────────────────────
def head(eyebrow, titulo, lado=""):
    lado_h = f'<p class="lado">{esc(lado)}</p>' if lado else ""
    return f'<div class="section-head"><div><div class="eyebrow">{esc(eyebrow)}</div><h2>{esc(titulo)}</h2></div>{lado_h}</div>'


def sec_hero():
    return f"""
<section class="hero" id="inicio">
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow">Benchmark web · {FECHA}</div>
      <h1>La web de DPROMA, frente a los mejores del sector.</h1>
      <p class="lede">Doce criterios, ocho sitios y la evidencia detrás de cada nota. Competidores de carga EV en México y referentes de tecnología, automotriz y energía renovable.</p>
      <div class="acciones"><a class="btn" href="#matriz">Ver la matriz</a><a class="btn btn-sec" href="#capturas">Ver las capturas</a></div>
    </div>
    <figure class="firma">
      <div class="terreno dproma" id="terreno-hero" role="img" aria-label="Ilustración decorativa: terreno de pilares que se elevan alrededor del puntero. No contiene datos."></div>
      <figcaption>Pasa el puntero por el terreno. Es ilustración; los datos están en la matriz.</figcaption>
    </figure>
  </div>
</section>"""


def sec_resumen():
    d = TOTAL["dproma"]
    n_ok = len(COMPLETOS)
    sin = [SITES[s]["corto"] for s in ORDEN if SITES[s]["evidencia"] != "completa"]
    fuertes = [CRIT_BY[b["id"]]["nombre"] for b in sorted(brecha, key=lambda b: b["gap"]) if b["gap"] <= 0]
    fuertes = [f if f.split()[0].isupper() else f[0].lower() + f[1:] for f in fuertes]
    return f"""
<section id="resumen">
  <div class="wrap">
    {head("Resumen", "Funciona por dentro. Le falta lo que convence por fuera.", "Lectura en una frase y las cifras de la evaluación.")}
    <div class="dos">
      <div class="card">
        <p class="frase">La web de DPROMA está bien hecha. Le faltan pruebas, casos reales, imagen propia y producto visible.</p>
        <ul class="puntos">
          <li><b>Ya es referente</b> en {esc(', '.join(fuertes) or 'ningún criterio')}.</li>
          <li><b>Queda detrás</b> en fotografía y video, casos, prueba social, app visible y precios.</li>
          <li><b>La oportunidad:</b> ningún competidor de carga en México combina carga EV y gestoría vehicular para empresas.</li>
        </ul>
      </div>
      <div class="stats">
        <div class="stat card-brand"><span class="num">{d}<small>/{MAXP}</small></span><span class="et">Puntaje de DPROMA</span><span class="ap">Puesto {pos_dproma} de {n_ok}</span></div>
        <div class="stat card"><span class="num">{TOTAL[mejor]-d}</span><span class="et">Brecha con el mejor</span><span class="ap">{esc(SITES[mejor]['corto'])} · {TOTAL[mejor]}/{MAXP}</span></div>
        <div class="stat card"><span class="num">{n_ok}</span><span class="et">Sitios puntuados</span><span class="ap">{len(sin)} sin puntuar</span></div>
        <div class="stat card"><span class="num">{len(CRIT)}</span><span class="et">Criterios</span><span class="ap">10 vistos · 2 medidos</span></div>
      </div>
    </div>
    <p class="nota"><b>Cómo se mide.</b> {esc(data['meta']['nota_metodo'])} Sin puntuar: {esc(', '.join(sin))}. Capturado el {FECHA}.</p>
  </div>
</section>"""


def sec_panorama():
    cards = []
    for sid in ORDEN:
        s = SITES[sid]
        n_eval = sum(1 for c in CRIT if score(sid, c["id"]) is not None)
        total = f'<span class="tag{"" if sid == "dproma" else " tag-ink"}">{TOTAL[sid]}/{MAXP}</span>' if sid in TOTAL else '<span class="tag tag-off">Sin puntuar</span>'
        apagado = " apagado" if s["evidencia"] != "completa" else ""
        mod = " dproma" if sid == "dproma" else ""
        motivo = f'<p class="motivo">{esc(s["motivo"])}</p>' if s.get("motivo") else ""
        cards.append(f"""
<article class="card emp" tabindex="0" data-site="{sid}" aria-label="{esc(s['nombre'])}: {n_eval} de {len(CRIT)} criterios evaluados">
  <div class="terreno{mod}{apagado}" data-nombre="{esc(s['nombre'])}" data-quieto="{1 if apagado else 0}" role="img" aria-label="Ilustración decorativa de {esc(s['nombre'])}. No contiene datos."></div>
  <h3>{esc(s['nombre'])}</h3>
  <p class="rol">{esc(s['rol'])}</p>
  <div class="fila">{total}<span class="tag tag-line">{EVID[s['evidencia']]}</span></div>
  <p class="meta">{n_eval} de {len(CRIT)} criterios</p>
  {motivo}
</article>""")
    return f"""
<section id="panorama">
  <div class="wrap">
    {head("Panorama", "Las ocho empresas evaluadas.", "Cada terreno reacciona al puntero y resalta su columna en la matriz. Las empresas sin evidencia suficiente aparecen atenuadas.")}
    <div class="panorama">{''.join(cards)}</div>
  </div>
</section>"""


def sec_ranking():
    filas = "".join(f'<tr><th scope="row">{esc(SITES[s]["nombre"])}</th><td>{TOTAL[s]}</td></tr>' for s in ranking)
    leyenda = "".join(f'<li>{chip(int(k))}<span>{esc(v)}</span></li>' for k, v in ESCALA.items())
    excl = [s for s in ORDEN if s not in TOTAL]
    excl_txt = "; ".join(f"{SITES[s]['corto']}: {'sitio inaccesible' if SITES[s]['evidencia']=='ninguna' else 'evidencia parcial'}" for s in excl)
    return f"""
<section id="ranking">
  <div class="wrap">
    {head("Ranking global", f"Puntaje sobre {MAXP}.")}
    <div class="dos dos-ancho">
      <div class="card">
        <figure class="viz">
          <div class="viz-lienzo"><canvas id="v-ranking" aria-label="Barras horizontales: puntaje total de cada sitio sobre {MAXP}. DPROMA {TOTAL['dproma']}."></canvas></div>
          <p class="aviso-cdn">Sin conexión con la librería de gráficos. La tabla muestra los mismos datos.</p>
          <details class="viz-tabla"><summary>Ver los datos en tabla</summary>
            <table><caption class="sr">Puntaje total por sitio sobre {MAXP}</caption>
            <thead><tr><th>Sitio</th><th>Puntaje</th></tr></thead><tbody>{filas}</tbody>
            <tfoot><tr><th scope="row">Mediana de los otros {len(OTROS)}</th><td>{fmt_med(mediana_total)}</td></tr></tfoot></table>
          </details>
        </figure>
        <p class="pie">Sin puntaje global: {esc(excl_txt)}.</p>
      </div>
      <div class="card">
        <h3 class="mini">Cómo leer la nota</h3>
        <ul class="escala">{leyenda}</ul>
        <p class="pie">Cada criterio vale de 0 a 3. Cuanto más intenso el color, mejor la nota. El número siempre acompaña al color.</p>
      </div>
    </div>
  </div>
</section>"""


def sec_matriz():
    cols = ORDEN
    grupos = [("dproma", "Sitio evaluado"), ("mx", "Competidores en México"), ("ref", "Referentes")]
    th1 = "".join(f'<th colspan="{sum(1 for s in cols if SITES[s]["grupo"] == g)}" scope="colgroup">{t}</th>' for g, t in grupos)
    th2 = "".join(f'<th scope="col" data-col="{s}" class="{"col-d" if s=="dproma" else ""}">{esc(SITES[s]["corto"])}</th>' for s in cols)
    body = ""
    for c in CRIT:
        tds = ""
        for s in cols:
            cell = P.get(s, {}).get(c["id"])
            p = None if cell is None else cell["p"]
            lbl = (f'{c["nombre"]}, {SITES[s]["nombre"]}: {p} de 3. Ver evidencia.' if p is not None else f'{c["nombre"]}, {SITES[s]["nombre"]}: sin evaluar. Ver motivo.')
            tds += f'<td data-col="{s}" class="{"col-d" if s=="dproma" else ""}"><button type="button" class="celda" data-site="{s}" data-crit="{c["id"]}" aria-label="{esc(lbl)}">{chip(p)}</button></td>'
        tipo = "medido" if c["tipo"] == "medido" else "visto"
        body += f'<tr><th scope="row">{esc(c["nombre"])}<span class="tipo">{tipo}</span></th>{tds}</tr>'
    tot = ""
    for s in cols:
        n_eval = sum(1 for c in CRIT if score(s, c["id"]) is not None)
        tot += f'<td data-col="{s}" class="{"col-d" if s=="dproma" else ""}">' + (f'<b>{TOTAL[s]}</b> / {MAXP}' if s in TOTAL else f'<span class="sin">{n_eval} de {len(CRIT)}</span>') + '</td>'
    leyenda = "".join(f'<span class="ley">{chip(int(k))}{esc(v)}</span>' for k, v in ESCALA.items()) + '<span class="ley">' + chip(None) + 'Sin evaluar</span>'
    return f"""
<section id="matriz">
  <div class="wrap">
    {head("Matriz comparativa", f"{len(CRIT)} criterios, {len(cols)} sitios.", "Toca una celda para ver qué se observó y dónde.")}
    <div class="leyenda">{leyenda}</div>
    <div class="card tabla-card">
      <div class="matriz-wrap" tabindex="0" role="region" aria-label="Matriz comparativa, desplazable en horizontal">
        <table class="matriz">
          <caption>Puntuación de 0 a 3 por criterio y sitio. Cada celda abre su evidencia.</caption>
          <thead><tr><th rowspan="2" scope="col" class="esq">Criterio</th>{th1}</tr><tr>{th2}</tr></thead>
          <tbody>{body}</tbody>
          <tfoot><tr><th scope="row">Total</th>{tot}</tr></tfoot>
        </table>
      </div>
    </div>
    <div class="card evid" id="evidencia" aria-live="polite" tabindex="-1">
      <div class="eyebrow">Evidencia</div>
      <p class="vacio">Selecciona una celda de la matriz para ver qué se observó, en qué sitio y con qué criterio.</p>
    </div>
  </div>
</section>"""


def sec_brecha():
    filas = ""
    for i, b in enumerate(brecha):
        c = CRIT_BY[b["id"]]
        ancho = round(b["gap"] / 3 * 100)
        prio = f'<span class="tag">Prioridad {i+1}</span>' if i < 3 else ""
        med_h = chip(int(b["med"])) if float(b["med"]).is_integer() else f'<span class="chip s1">{fmt_med(b["med"])}</span>'
        filas += f"""<li class="fila-b">
  <div class="et"><b>{esc(c['nombre'])}</b>{prio}</div>
  <div class="vals"><span>DPROMA {chip(b['d'])}</span><span>Mediana {med_h}</span><span>Mejor {chip(b['best'])}<small>{esc(' · '.join(b['best_site']))}</small></span></div>
  <div class="gap"><div class="barra" role="img" aria-label="Brecha de {b['gap']} puntos con el mejor"><span style="width:{ancho}%"></span></div><b>{('+' if b['gap']>0 else '')}{b['gap']}</b></div>
</li>"""
    tabla = "".join(f'<tr><th scope="row">{esc(CRIT_BY[b["id"]]["nombre"])}</th><td>{b["d"]}</td><td>{fmt_med(b["med"])}</td><td>{b["best"]}</td><td>{b["gap"]}</td></tr>' for b in brecha)
    tg = sum(b["gap"] for b in brecha)
    return f"""
<section id="brecha">
  <div class="wrap">
    {head("Brecha de DPROMA", "Dónde cerrar primero.", f"Distancia entre DPROMA y el mejor sitio en cada criterio, contra los otros {len(OTROS)} sitios puntuados.")}
    <div class="card">
      <ol class="brecha">{filas}</ol>
      <details class="viz-tabla"><summary>Ver los datos en tabla</summary>
        <table><caption class="sr">Brecha de DPROMA por criterio</caption>
        <thead><tr><th>Criterio</th><th>DPROMA</th><th>Mediana</th><th>Mejor</th><th>Brecha</th></tr></thead><tbody>{tabla}</tbody>
        <tfoot><tr><th scope="row">Brecha acumulada</th><td></td><td></td><td></td><td>{tg}</td></tr></tfoot></table>
      </details>
    </div>
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
BAR = '<div class="marco-barra"><span class="pts" aria-hidden="true"><i></i><i></i><i></i></span><span class="url">{u}</span></div>'


def sec_capturas():
    figs = []
    for sid in sorted(ORDEN, key=lambda x: (not SITES[x]["captura"], ORDEN.index(x))):
        s = SITES[sid]
        u = esc(re.sub(r'^https?://', '', s['url']))
        if s["captura"]:
            marks = "".join(f'<span class="mk" style="left:{x}%;top:{y}%" aria-hidden="true">{i+1}</span>' for i, (x, y, _) in enumerate(ANOT[sid]))
            lista = "".join(f"<li>{esc(t)}</li>" for _, _, t in ANOT[sid])
            figs.append(f"""
<figure class="marco" data-site="{sid}">{BAR.format(u=u)}
  <div class="v-esc"><div class="cap"><img src="img/{sid}-escritorio.jpg" width="1200" height="750" loading="lazy" alt="Captura de la portada de {esc(s['nombre'])} en escritorio, {FECHA}">{marks}</div><ol class="anot">{lista}</ol></div>
  <div class="v-mov"><img src="img/{sid}-movil.jpg" width="390" height="844" loading="lazy" alt="Captura de la portada de {esc(s['nombre'])} en móvil, {FECHA}"></div>
  <figcaption><b>{esc(s['nombre'])}</b> · {esc(s['rol'])} · capturado el {FECHA}</figcaption>
</figure>""")
        else:
            figs.append(f"""
<figure class="marco vacio" data-site="{sid}">{BAR.format(u=u)}
  <div class="hueco"><p><b>{esc(s['nombre'])}: sin captura</b></p><p>{esc(s['motivo'])}</p></div>
  <figcaption><b>{esc(s['nombre'])}</b> · {esc(s['rol'])}</figcaption>
</figure>""")
    ex = [("dproma.com · Pre-diagnóstico EV", "dproma-prediagnostico", "El pre-diagnóstico cambia el resultado según lo que se ingresa."),
          ("dproma.com · Soluciones por industria", "dproma-industrias", "Siete industrias con panel propio, en una sola página."),
          ("apps.apple.com · App Tesla (México)", "tesla-app", "Única evidencia de Tesla por ahora: 4.9 de 5 con 1.5 mil calificaciones.")]
    extra = "".join(f'<figure class="marco">{BAR.format(u=esc(u))}<img src="img/{f}.jpg" width="1200" height="750" loading="lazy" alt="{esc(u)}"><figcaption>{esc(t)} Capturado el {FECHA}.</figcaption></figure>' for u, f, t in ex)
    return f"""
<section id="capturas">
  <div class="wrap">
    {head("Capturas comparadas", "La portada de cada sitio.", "En escritorio, los números marcan los patrones observados. Capturas de sitios de terceros, para análisis interno.")}
    <div class="ctl"><div class="seg" role="group" aria-label="Tipo de pantalla"><button type="button" data-vista="esc" aria-pressed="true">Escritorio</button><button type="button" data-vista="mov" aria-pressed="false">Móvil</button></div></div>
    <div class="galeria" data-vista="esc">{''.join(figs)}</div>
    <h3 class="sub">Evidencia adicional</h3>
    <div class="extras">{extra}</div>
  </div>
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
ESTADO = {"si": ("est-si", "DPROMA: sí"), "parcial": ("est-par", "DPROMA: parcial"), "no": ("est-no", "DPROMA: no")}


def sec_patrones():
    cards = ""
    for i, (t, d, sitios, est, nota) in enumerate(PATRONES, 1):
        cls, txt = ESTADO[est]
        chips = "".join(f'<span class="tag tag-line">{esc(x)}</span>' for x in sitios)
        cards += f'<article class="card pat"><header><span class="n">{i:02d}</span><span class="tag {cls}">{txt}</span></header><h3>{esc(t)}</h3><p>{esc(d)}</p><div class="chips" role="group" aria-label="Lo aplican">{chips}</div><p class="pie">{esc(nota)}</p></article>'
    n_si, n_par, n_no = (sum(1 for p in PATRONES if p[3] == k) for k in ("si", "parcial", "no"))
    return f"""
<section id="patrones">
  <div class="wrap">
    {head("Patrones", "Diez patrones de la competencia.", f"DPROMA: {n_si} sí · {n_par} parcial · {n_no} no.")}
    <div class="card" style="margin-bottom:var(--gap)">
      <h3 class="mini">DPROMA frente a los patrones</h3>
      <div class="barra-pat" role="img" aria-label="{n_si} patrones cumplidos, {n_par} parciales, {n_no} no cumplidos"><span class="b-si" style="width:{n_si*10}%"></span><span class="b-par" style="width:{n_par*10}%"></span><span class="b-no" style="width:{n_no*10}%"></span></div>
      <div class="leyenda"><span class="ley"><i class="mu b-si"></i>Sí <b>{n_si}</b></span><span class="ley"><i class="mu b-par"></i>Parcial <b>{n_par}</b></span><span class="ley"><i class="mu b-no"></i>No <b>{n_no}</b></span></div>
    </div>
    <div class="patrones">{cards}</div>
  </div>
</section>"""


def sec_mercado():
    filas = ""
    for m in data["mercado"]:
        cuota = f'{m["cuota"]} %' if m["cuota"] else "—"
        cls = "tag-line" if m["nivel"] != "Cifras contradictorias" else "tag"
        filas += f'<tr><th scope="row" data-et="Empresa">{esc(m["nombre"])}</th><td data-et="Escala">{esc(m["escala"])}</td><td data-et="Cuota de uso">{cuota}</td><td data-et="Inversión">{esc(m["inversion"])}</td><td data-et="Calidad del dato"><span class="tag {cls}">{esc(m["nivel"])}</span></td></tr>'
    conocidas = sorted([m for m in data["mercado"] if m["cuota"]], key=lambda m: -m["cuota"])
    barras = "".join(f'<li><span class="et">{esc(m["nombre"])}</span><div class="barra"><span style="width:{m["cuota"]/25*100:.0f}%"></span></div><b>{m["cuota"]} %</b></li>' for m in conocidas)
    return f"""
<section id="mercado">
  <div class="wrap">
    {head("Contexto de mercado", "Escala en México, no facturación.", "Las redes de carga son empresas privadas y no publican ingresos. Cuando el cliente aporte cifras, el orden puede cambiar.")}
    <div class="card tabla-card"><div class="matriz-wrap" tabindex="0" role="region" aria-label="Operadores de carga, desplazable en horizontal"><table class="mer"><caption>Escala, cuota de uso e inversión de los operadores de carga en México</caption>
      <thead><tr><th>Empresa</th><th>Escala</th><th>Cuota de uso</th><th>Inversión</th><th>Calidad del dato</th></tr></thead><tbody>{filas}</tbody></table></div></div>
    <div class="dos" style="margin-top:var(--gap)">
      <div class="card"><h3 class="mini">Cuota de uso (tres datos conocidos)</h3><ul class="cuota">{barras}</ul><p class="pie">Fuente: Expansión, junio de 2026. Evergo no tiene porcentaje publicado; se le atribuye el mayor despliegue.</p></div>
      <div class="card"><h3 class="mini">Administración vehicular</h3><p>Competidores con oferta B2B para flotillas: <b>GEVAC</b>, <b>Red-T</b> y <b>Traslandon</b>, más gestorías locales. No hay cifras públicas ni un líder identificado.</p><p class="pie">Pendiente: confirmar con el cliente a quién ve como competidor real.</p></div>
    </div>
  </div>
</section>"""


LENTES = [
    ("Negocio", ["DPROMA es el único del grupo que une carga EV y gestoría vehicular en un mismo sitio.", "Sus cifras visibles (20,000+ trámites, 9 ciudades) son de administración vehicular; ninguna es de carga EV.", "Las redes de carga compiten por conductores; DPROMA vende a empresas."], "Posicionarse como integrador y operador para empresas, no como red pública."),
    ("Experiencia de usuario", ["Navegación, pestañas por industria y pre-diagnóstico funcionan y se entienden.", "El proceso aparece dos veces con forma distinta: cuatro pasos arriba y cinco fases más abajo.", "La experiencia digital es una maqueta; el producto no se ve real."], "Unificar el proceso, mostrar producto real y dejar que el pre-diagnóstico envíe su resumen."),
    ("Marketing", ["No hay fotografía ni video de instalaciones; FAZT, BYD y Enphase puntúan 3 en este criterio.", "El blog tiene tres artículos; los referentes tienen centros de recursos completos.", "Propósito, misión, visión y principios ya existen en «Nosotros», pero no llegan al hero."], "Sesión fotográfica, casos cortos y páginas de SEO por industria."),
    ("Comercial", ["El CTA principal es único; ChargePoint y BYD combinan experto, cotización y canal directo.", "Los «casos» son escenarios ilustrativos; no hay clientes con nombre.", "No hay rangos de inversión, aunque sí se explican los factores de costo."], "CTA doble, rangos orientativos y dos o tres casos reales con permiso del cliente."),
]


def sec_lentes():
    cards = "".join(f'<article class="card lente"><div class="eyebrow">{esc(t)}</div><ul class="puntos">{"".join(f"<li>{esc(h)}</li>" for h in hs)}</ul><div class="op"><b>Oportunidad</b><p>{esc(op)}</p></div></article>' for t, hs, op in LENTES)
    return f"""
<section id="lentes">
  <div class="wrap">
    {head("Cuatro puntos de vista", "Negocio, experiencia, marketing y comercial.", "Los cuatro llegan a la misma conclusión: hay que enseñar más de lo que DPROMA ya hace.")}
    <div class="lentes">{cards}</div>
  </div>
</section>"""


IA_CASOS = [
    ("Asesor de pre-diagnóstico (web y WhatsApp)", ["Medio", "Alto", "Medio", "Alto"], "Bajo", "Primero"),
    ("Agente de WhatsApp para cualificar y dar seguimiento", ["Medio", "Medio", "Medio", "Alto"], "Medio", "Segundo"),
    ("Asesor de trámites vehiculares", ["Alto", "Alto", "Medio", "Medio"], "Alto", "Tras validar normativa"),
    ("Agente de voz (llamadas)", ["Bajo", "Medio", "Bajo", "Medio"], "Medio", "Fase posterior"),
]
NIV = {"Bajo": "s1", "Medio": "s2", "Alto": "s3"}


def sec_ia():
    filas = ""
    for t, imp, ries, cuando in IA_CASOS:
        tds = "".join(f'<td data-et="{l}"><span class="chip {NIV[x]} ancho">{x}</span></td>' for l, x in zip(["Negocio", "UX", "Marketing", "Comercial"], imp))
        filas += f'<tr><th scope="row">{esc(t)}</th>{tds}<td data-et="Riesgo"><span class="chip {NIV[ries]} ancho">{ries}</span></td><td data-et="Cuándo">{esc(cuando)}</td></tr>'
    return f"""
<section id="ia">
  <div class="wrap">
    {head("Inteligencia artificial", "¿Conviene incluir IA? Sí, pero acotada.")}
    <div class="card card-dark veredicto"><p class="frase">Un asesor conversacional que cualifica proyectos y agenda el diagnóstico aporta valor en las cuatro lentes. «IA en todo», no.</p><p class="ap">La IA aumenta al equipo comercial; no lo reemplaza.</p></div>
    <div class="card tabla-card" style="margin-top:var(--gap)"><div class="matriz-wrap" tabindex="0" role="region" aria-label="Casos de uso de IA, desplazable en horizontal"><table class="mer"><caption>Impacto por lente, riesgo y momento de cada caso de uso de IA. Valoración del equipo evaluador. Más intenso, más alto.</caption>
      <thead><tr><th>Caso de uso</th><th>Negocio</th><th>UX</th><th>Marketing</th><th>Comercial</th><th>Riesgo</th><th>Cuándo</th></tr></thead><tbody>{filas}</tbody></table></div></div>
    <div class="dos" style="margin-top:var(--gap)">
      <div class="card"><h3 class="mini">Tecnología: a comparar en un piloto</h3><ul class="puntos">
        <li><b>ElevenLabs Agents</b>: un mismo agente en web, teléfono y WhatsApp, con voz y texto. Fuerte en voz. Por verificar: español de México, precios e integración con CRM.</li>
        <li><b>Modelo de lenguaje propio</b> (Gemini, Claude u otro) con base de conocimiento validada, para precisión técnica; puede darle voz ElevenLabs.</li>
        <li><b>Plataformas de chat y WhatsApp</b> (Botpress, Voiceflow, Cliengo, Infobip): si pesa más la rapidez de despliegue. No evaluadas.</li></ul></div>
      <div class="card"><h3 class="mini">Piloto propuesto</h3><ul class="puntos">
        <li>Caso 1, de 6 a 8 semanas, en prueba A/B contra el formulario actual.</li>
        <li>Mide: diagnósticos agendados, tiempo de respuesta, tasa de cualificación y traspaso a un humano.</li>
        <li>Antes: tono de marca para la web, base de conocimiento validada, política de escalamiento y aviso de privacidad.</li>
        <li>Metas numéricas: se fijan con el cliente. No se inventan aquí.</li></ul></div>
    </div>
  </div>
</section>"""


FASES = [
    ("Fase 0", "Fundamentos", "0–4 semanas", ["Manual de marca y fuentes", "Posicionamiento y segmento prioritario", "Casos y permisos de logos", "Sesión fotográfica", "Entrevistas a clientes externos"]),
    ("Fase 1", "Victorias rápidas", "1–3 meses", ["Unificar el proceso", "FAQ y 2–3 casos reales", "CTA doble y WhatsApp prellenado", "Analítica de eventos", "Comparación de IA y piloto del asesor"]),
    ("Fase 2", "Rediseño", "3–6 meses", ["Sistema de diseño web de marca", "Centro de recursos", "SEO por industria y ciudad", "Cotizador con rangos", "Producto digital real a la vista"]),
    ("Fase 3", "Escala", "6–12 meses", ["App descargable", "Versiones para otros países", "Pruebas A/B continuas", "Contenido de autoridad"]),
]


def sec_ruta():
    cols = "".join(f'<li class="card fase"><span class="paso" aria-hidden="true">{i}</span><h3>{esc(t)}</h3><p class="cuando">{esc(f)} · {esc(c)}</p><ul class="puntos">{"".join(f"<li>{esc(x)}</li>" for x in its)}</ul></li>' for i, (f, t, c, its) in enumerate(FASES))
    return f"""
<section id="ruta">
  <div class="wrap">
    {head("Hoja de ruta", "Cuatro fases en doce meses.")}
    <ol class="ruta">{cols}</ol>
  </div>
</section>"""


def sec_sistema():
    v = vf.get("resumen", "")
    nota_v = f'<p class="nota"><b>Comprobado en esta página.</b> {esc(v)}</p>' if v else ""
    return f"""
<section id="sistema">
  <div class="wrap">
    {head("Sistema de diseño", "Dos sistemas, dos trabajos.", "Primero se construyó este benchmark con SIO-DPROMA; esta versión usa el sistema de los entregables.")}
    <div class="tres">
      <article class="card"><div class="eyebrow">SIO-DPROMA</div><h3>Para pantallas de producto</h3><p>Tablas densas, tableros y estados de carga dentro de la herramienta. En un informe de análisis resultó pesado y escondía el mensaje.</p></article>
      <article class="card"><div class="eyebrow">Entregables (2894_)</div><h3>Para informes que se leen</h3><p>DM Sans, cloud white, un solo acento cobalt y mucho aire. Es el sistema de esta versión: sin rojos, ámbares ni verdes, y la nota va en una rampa monocroma.</p></article>
      <article class="card"><div class="eyebrow">Huecos</div><h3>Sin regla todavía</h3><p>Mapa de calor con notas discretas, captura anotada y una ilustración interactiva decorativa (el terreno), que nunca debe llevar un dato.</p></article>
    </div>
    {nota_v}
  </div>
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
    li = "".join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in FUENTES)
    sitios = "".join(f'<li><a href="{s["url"]}" rel="noopener">{esc(s["nombre"])}</a></li>' for s in data["sitios"])
    return f"""
<section id="fuentes">
  <div class="wrap">
    {head("Fuentes y créditos", "De dónde sale cada dato.")}
    <div class="tres">
      <div class="card"><h3 class="mini">Sitios evaluados</h3><ul class="puntos">{sitios}</ul></div>
      <div class="card"><h3 class="mini">Datos de mercado</h3><ul class="puntos">{li}</ul></div>
      <div class="card"><h3 class="mini">Créditos</h3><ul class="puntos"><li>Terrenos: <a href="https://github.com/lucasmarkes/hairline" rel="noopener">@lucasmarkes/hairline</a> 0.5.1, licencia MIT (<a href="vendor/hairline-LICENSE.txt">texto</a>).</li><li>Gráficas: Chart.js 4.5.0.</li><li>Capturas de sitios de terceros, solo para análisis interno.</li><li>Datos y evidencia por celda: <a href="datos/benchmark.json">datos/benchmark.json</a>.</li></ul></div>
    </div>
  </div>
</section>"""


# ───────────────────────── CSS ─────────────────────────
LIGHT = """--bg:var(--cloud-white);--surface:#FFFFFF;--surface-alt:var(--soft-gray);--text:var(--ink-black);
--text-muted:color-mix(in srgb,var(--ink-black) 72%,var(--cloud-white));--border:color-mix(in srgb,var(--ink-black) 13%,var(--cloud-white));
--accent:var(--deep-cobalt);--accent-text:var(--deep-cobalt);--on-accent:#FFFFFF;--dark-surface:var(--ink-black);--on-dark:var(--cloud-white);--sky:var(--sky-blue);
--shadow:0 1px 2px rgba(11,11,13,0.04),0 8px 24px rgba(11,11,13,0.06);
--s0-bg:transparent;--s0-fg:var(--text-muted);--s0-bd:color-mix(in srgb,var(--ink-black) 40%,var(--cloud-white));--s1-bg:var(--soft-gray);--s1-fg:var(--ink-black);--s2-bg:var(--sky-blue);--s2-fg:var(--ink-black);--s3-bg:var(--deep-cobalt);--s3-fg:#FFFFFF;
--chart-otros:color-mix(in srgb,var(--ink-black) 28%,var(--cloud-white));--brand-fill:var(--deep-cobalt);"""
DARK = """--bg:var(--ink-black);--surface:color-mix(in srgb,var(--cloud-white) 7%,var(--ink-black));--surface-alt:color-mix(in srgb,var(--cloud-white) 13%,var(--ink-black));--text:var(--cloud-white);
--text-muted:color-mix(in srgb,var(--cloud-white) 72%,var(--ink-black));--border:color-mix(in srgb,var(--cloud-white) 17%,var(--ink-black));
--accent:var(--deep-cobalt);--accent-text:var(--sky-blue);--on-accent:#FFFFFF;--dark-surface:color-mix(in srgb,var(--cloud-white) 11%,var(--ink-black));--on-dark:var(--cloud-white);--sky:var(--sky-blue);
--shadow:0 1px 2px rgba(0,0,0,0.3),0 8px 24px rgba(0,0,0,0.35);
--s0-bg:transparent;--s0-fg:var(--text-muted);--s0-bd:color-mix(in srgb,var(--cloud-white) 42%,var(--ink-black));--s1-bg:color-mix(in srgb,var(--cloud-white) 17%,var(--ink-black));--s1-fg:var(--cloud-white);--s2-bg:var(--sky-blue);--s2-fg:var(--ink-black);--s3-bg:var(--deep-cobalt);--s3-fg:#FFFFFF;
--chart-otros:color-mix(in srgb,var(--cloud-white) 32%,var(--ink-black));--brand-fill:var(--deep-cobalt);"""

CSS = f"""
:root{{--cloud-white:#F7F8FA;--soft-gray:#E6E8EC;--ink-black:#0B0B0D;--deep-cobalt:#0A46FF;--sky-blue:#7DB7FF;
--radius:16px;--gap:1.25rem;{LIGHT}}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{{DARK}}}}}
:root[data-theme="dark"]{{{DARK}}}
:root[data-theme="light"]{{{LIGHT}}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:5rem}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}*{{animation-duration:.001ms!important;transition-duration:.001ms!important}}}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:'DM Sans',system-ui,-apple-system,sans-serif;font-weight:400;line-height:1.55;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}}
a{{color:var(--accent-text)}}
a:focus-visible,button:focus-visible,[tabindex]:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}}
.skip{{position:absolute;left:-999px;top:0;background:var(--accent);color:var(--on-accent);padding:.6rem 1rem;z-index:100}}
.skip:focus{{left:1rem;top:1rem}}
.sr{{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 clamp(1.25rem,4vw,2.5rem)}}
h1,h2,h3{{font-weight:700;letter-spacing:-0.02em;text-wrap:balance;margin:0;line-height:1.1}}
p{{margin:0}}
.eyebrow{{display:inline-flex;align-items:center;gap:.5em;font-size:.75rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-text)}}
.eyebrow::before{{content:"";width:.5em;height:.5em;border-radius:999px;background:var(--accent);display:inline-block}}
.masthead{{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}}
.masthead-inner{{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding-top:1rem;padding-bottom:1rem}}
.wordmark{{font-weight:700;font-size:1.05rem;text-decoration:none;color:var(--text)}}
.wordmark span{{color:var(--text-muted);font-weight:400}}
.masthead nav{{display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap}}
.masthead nav a{{font-size:.875rem;font-weight:500;color:var(--text-muted);text-decoration:none;display:inline-flex;align-items:center;min-height:24px}}
.masthead nav a:hover{{color:var(--accent-text)}}
.tema{{appearance:none;border:1px solid var(--border);background:var(--surface);color:var(--text);border-radius:10px;min-width:44px;min-height:44px;cursor:pointer;font:500 .8125rem 'DM Sans',sans-serif}}
.btn{{display:inline-flex;align-items:center;justify-content:center;background:var(--accent);color:var(--on-accent);border-radius:12px;padding:.75rem 1.25rem;font-weight:500;text-decoration:none;border:1px solid transparent;min-height:44px;font-family:inherit;font-size:.9375rem;cursor:pointer}}
.btn:hover{{opacity:.92}}
.btn-sec{{background:transparent;color:var(--text);border-color:var(--border)}}
.hero{{padding:clamp(3rem,8vw,5.5rem) 0 clamp(2.5rem,6vw,4rem)}}
.hero-grid{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:clamp(1.5rem,4vw,3rem);align-items:center}}
@media (max-width:900px){{.hero-grid{{grid-template-columns:1fr}}}}
.hero h1{{font-size:clamp(2.25rem,5vw,3.5rem);line-height:1.06;margin-top:.75rem;max-width:18ch}}
.lede{{margin-top:1.25rem;font-size:1.0625rem;font-weight:300;color:var(--text-muted);max-width:56ch}}
.acciones{{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1.75rem}}
.firma{{margin:0;display:flex;flex-direction:column;gap:.5rem}}
.firma figcaption{{font-size:.8125rem;color:var(--text-muted);text-align:center}}
section{{padding:clamp(2.5rem,6vw,4rem) 0}}
section + section{{border-top:1px solid var(--border)}}
.section-head{{display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;flex-wrap:wrap;margin-bottom:2rem}}
.section-head h2{{font-size:clamp(1.5rem,3vw,2.125rem);margin-top:.5rem;max-width:28ch}}
.section-head .lado{{max-width:42ch;color:var(--text-muted);font-size:.9375rem;font-weight:300}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;box-shadow:var(--shadow);min-width:0}}
.card-brand{{background:var(--accent);color:#fff;border-color:transparent}}
.card-dark{{background:var(--dark-surface);color:var(--on-dark);border-color:var(--border)}}
.mini{{font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);font-weight:700;margin-bottom:1rem}}
.pie{{font-size:.8125rem;color:var(--text-muted);margin-top:1rem;line-height:1.5}}
.nota{{margin-top:1.5rem;font-size:.875rem;color:var(--text-muted);max-width:90ch;line-height:1.6}}
.nota b{{color:var(--text)}}
.dos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:var(--gap)}}
.dos-ancho{{grid-template-columns:minmax(0,1.6fr) minmax(0,1fr)}}
@media (max-width:900px){{.dos-ancho{{grid-template-columns:1fr}}}}
.tres{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:var(--gap)}}
.tres h3{{font-size:1.125rem;margin:.6rem 0 .5rem}}
.tres p{{font-size:.9375rem;color:var(--text-muted);font-weight:300}}
.frase{{font-size:clamp(1.25rem,2.4vw,1.625rem);font-weight:700;line-height:1.25;letter-spacing:-.01em}}
.puntos{{list-style:none;margin:1rem 0 0;padding:0;display:flex;flex-direction:column;gap:.7rem}}
.puntos li{{position:relative;padding-left:1.1rem;font-size:.9375rem;line-height:1.55;color:var(--text-muted);font-weight:300}}
.puntos li::before{{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;border-radius:2px;background:var(--accent)}}
.puntos li b{{color:var(--text);font-weight:700}}
.puntos a{{color:var(--accent-text)}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap)}}
.stat{{display:flex;flex-direction:column;gap:.25rem;padding:1.5rem}}
.stat .num{{font-size:clamp(2.25rem,4.5vw,3.25rem);font-weight:700;letter-spacing:-.03em;line-height:1}}
.stat .num small{{font-size:1rem;font-weight:500;margin-left:.15em;letter-spacing:0}}
.stat .et{{font-weight:500;margin-top:.5rem}}
.stat .ap{{font-size:.8125rem}}
.stat.card .ap{{color:var(--text-muted);opacity:1}}
.tag{{display:inline-flex;align-items:center;font-size:.6875rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:8px;padding:.35em .7em;background:var(--accent);color:#fff;white-space:nowrap}}
.tag-ink{{background:var(--text);color:var(--bg)}}
.tag-line{{background:transparent;color:var(--text-muted);border:1px solid var(--border)}}
.tag-off{{background:var(--surface-alt);color:var(--text-muted)}}
.est-si{{background:var(--accent);color:#fff}} .est-par{{background:var(--sky);color:#0B0B0D}} .est-no{{background:var(--surface-alt);color:var(--text);border:1px solid var(--border)}}
.chip{{display:inline-flex;align-items:center;justify-content:center;min-width:2rem;height:1.75rem;padding:0 .5rem;border-radius:8px;font-weight:700;font-size:.8125rem;border:1px solid transparent}}
.chip.ancho{{min-width:4.5rem}}
.chip.s0{{background:var(--s0-bg);color:var(--s0-fg);border-color:var(--s0-bd)}}
.chip.s1{{background:var(--s1-bg);color:var(--s1-fg)}} .chip.s2{{background:var(--s2-bg);color:var(--s2-fg)}} .chip.s3{{background:var(--s3-bg);color:var(--s3-fg)}}
.chip.sn{{background:transparent;color:var(--text-muted);border:1px dashed var(--s0-bd)}}
.leyenda{{display:flex;gap:1.25rem;flex-wrap:wrap;align-items:center;margin-bottom:1rem;font-size:.8125rem;color:var(--text-muted)}}
.ley{{display:inline-flex;align-items:center;gap:.5rem}}
.ley b{{color:var(--text)}}
.mu{{width:10px;height:10px;border-radius:3px;display:inline-block}}
.b-si{{background:var(--accent)}} .b-par{{background:var(--sky)}} .b-no{{background:var(--surface-alt);border:1px solid var(--border)}}
.escala{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.9rem}}
.escala li{{display:flex;gap:.9rem;align-items:center;font-weight:500}}
/* terreno */
.terreno{{--hairline-plate:var(--surface);--hairline-hi:var(--text);--hairline-edge:var(--text-muted);--hairline-mid:color-mix(in srgb,var(--text-muted) 50%,var(--surface));--hairline-lo:color-mix(in srgb,var(--text-muted) 24%,var(--surface));--hairline-stroke:.9;width:100%;aspect-ratio:5/4;min-height:120px}}
.terreno.dproma{{--hairline-hi:var(--accent)}}
.terreno.apagado{{opacity:.4;filter:grayscale(1)}}
.panorama{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:var(--gap)}}
.emp{{padding:1rem 1rem 1.25rem;transition:transform .2s ease,border-color .2s ease}}
.emp:hover,.emp:focus-visible,.emp.activa{{transform:translateY(-3px);border-color:var(--accent)}}
.emp h3{{font-size:1.125rem;margin-top:.5rem}}
.emp .rol{{font-size:.8125rem;color:var(--text-muted);margin:.15rem 0 .75rem}}
.emp .fila{{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center}}
.emp .meta{{font-size:.8125rem;color:var(--text-muted);margin-top:.6rem}}
.emp .motivo{{font-size:.8125rem;color:var(--text-muted);margin-top:.6rem;line-height:1.5}}
/* gráfica */
.viz-lienzo{{position:relative;width:100%;height:270px}}
.viz canvas{{display:block;width:100%!important;height:100%!important}}
.viz{{margin:0}}
.aviso-cdn{{display:none;font-size:.8125rem;color:var(--text);background:var(--surface-alt);border-radius:10px;padding:.6rem .8rem}}
.viz.sin-libreria .viz-lienzo,.viz.sin-libreria .viz-tabla>summary{{display:none}}
.viz.sin-libreria .aviso-cdn{{display:block}}
.viz-tabla{{overflow-x:auto;margin-top:1rem}}
.viz-tabla>summary{{font-size:.8125rem;color:var(--accent-text);cursor:pointer;font-weight:500}}
.viz-tabla table{{width:100%;border-collapse:collapse;font-size:.8125rem;margin-top:.6rem}}
.viz-tabla th,.viz-tabla td{{text-align:left;padding:.4rem .5rem;border-bottom:1px solid var(--border)}}
.viz-tabla thead th{{color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;font-size:.6875rem}}
.viz-tabla tfoot th,.viz-tabla tfoot td{{border-top:2px solid var(--text);border-bottom:none;font-weight:700}}
/* matriz */
.tabla-card{{padding:0;overflow:hidden}}
.matriz-wrap{{overflow-x:auto;max-width:100%}}
table.matriz,table.mer{{width:100%;border-collapse:collapse;font-size:.875rem}}
table.matriz{{min-width:860px}} table.mer{{min-width:720px}}
caption{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
.matriz thead th,.mer thead th{{font-size:.6875rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);padding:.8rem .6rem;text-align:center;border-bottom:1px solid var(--border);white-space:nowrap;background:var(--surface)}}
.matriz thead th[scope="colgroup"]{{font-size:.625rem;border-bottom:1px solid var(--border)}}
.matriz thead th.esq,.mer thead th:first-child{{text-align:left}}
.matriz thead th.esq{{position:sticky;left:0;z-index:3;min-width:230px}}
.matriz tbody th{{text-align:left;font-weight:500;padding:.55rem 1rem;position:sticky;left:0;background:var(--surface);z-index:2;min-width:230px;border-bottom:1px solid var(--border)}}
.tipo{{display:inline-block;margin-left:.5rem;font-size:.625rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted)}}
.matriz td{{text-align:center;padding:.3rem .4rem;border-bottom:1px solid var(--border)}}
.matriz tfoot th,.matriz tfoot td{{border-top:2px solid var(--text);padding:.8rem .6rem;text-align:center;font-weight:500}}
.matriz tfoot th{{text-align:left;padding-left:1rem;position:sticky;left:0;background:var(--surface)}}
.sin{{color:var(--text-muted)}}
.col-d{{background:color-mix(in srgb,var(--accent) 7%,var(--surface))}}
.matriz [data-col].resalta{{background:var(--surface-alt)}}
.matriz .col-d.resalta{{background:color-mix(in srgb,var(--accent) 12%,var(--surface))}}
.celda{{appearance:none;border:1px solid transparent;background:transparent;border-radius:10px;padding:3px;cursor:pointer;min-width:44px;min-height:40px;display:inline-flex;align-items:center;justify-content:center}}
.celda:hover{{border-color:var(--border)}}
.celda[aria-pressed="true"]{{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 25%,transparent)}}
.mer th,.mer td{{text-align:left;padding:.9rem 1rem;vertical-align:top;border-bottom:1px solid var(--border);font-weight:400}}
.mer tbody th{{font-weight:700}}
.evid{{margin-top:var(--gap)}}
.evid .vacio{{color:var(--text-muted);margin-top:.6rem;font-size:.9375rem}}
.evid .tit{{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;margin-top:.6rem}}
.evid .tit b{{font-size:1.0625rem}}
.evid .def{{color:var(--text-muted);font-size:.8125rem;margin-top:.5rem}}
.evid .txt{{font-size:1rem;line-height:1.6;margin-top:.6rem;font-weight:300}}
.evid ul.chk{{list-style:none;margin:.9rem 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.6rem 1.2rem;font-size:.8125rem;color:var(--text-muted)}}
/* brecha */
.brecha{{list-style:none;margin:0;padding:0}}
.fila-b{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1.6fr) minmax(0,1fr);gap:1rem;align-items:center;padding:1rem 0;border-bottom:1px solid var(--border)}}
.fila-b:last-child{{border-bottom:none}}
@media (max-width:900px){{.fila-b{{grid-template-columns:1fr;gap:.6rem}}}}
.fila-b .et{{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}}
.fila-b .vals{{display:flex;gap:1rem;flex-wrap:wrap;font-size:.8125rem;color:var(--text-muted)}}
.fila-b .vals span{{display:inline-flex;align-items:center;gap:.5rem}}
.fila-b .vals small{{color:var(--text-muted)}}
.fila-b .gap{{display:flex;align-items:center;gap:.8rem}}
.barra{{flex:1;height:10px;border-radius:6px;background:var(--surface-alt);overflow:hidden}}
.barra span{{display:block;height:100%;background:var(--accent);border-radius:6px}}
:root[data-theme="dark"] .barra span{{background:var(--sky-blue)}}
.gap b{{min-width:2ch;text-align:right}}
.barra-pat{{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--surface-alt);margin-bottom:1rem}}
.barra-pat span+span{{border-left:2px solid var(--surface)}}
/* capturas */
.ctl{{margin-bottom:1.25rem}}
.seg{{display:inline-flex;background:var(--surface-alt);border-radius:12px;padding:3px;gap:2px}}
.seg button{{border:0;background:transparent;color:var(--text-muted);border-radius:10px;padding:.5rem 1rem;min-height:40px;font:500 .875rem 'DM Sans',sans-serif;cursor:pointer}}
.seg button[aria-pressed="true"]{{background:var(--surface);color:var(--text);box-shadow:var(--shadow)}}
.galeria{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,500px),1fr));gap:var(--gap);align-items:start}}
.galeria[data-vista="mov"]{{grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}}
.marco{{margin:0;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;min-width:0}}
.marco-barra{{display:flex;align-items:center;gap:.75rem;padding:.5rem .8rem;background:var(--surface-alt);border-bottom:1px solid var(--border)}}
.pts{{display:inline-flex;gap:5px}} .pts i{{width:9px;height:9px;border-radius:50%;background:var(--border)}}
.url{{font-size:.75rem;color:var(--text-muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.marco img{{display:block;width:100%;height:auto}}
.marco figcaption{{padding:.8rem 1rem;font-size:.8125rem;color:var(--text-muted);line-height:1.5;border-top:1px solid var(--border)}}
.marco figcaption b{{color:var(--text)}}
.cap{{position:relative}}
.mk{{position:absolute;transform:translate(-50%,-50%);width:24px;height:24px;border-radius:50%;background:#0A46FF;color:#fff;font:700 12px/24px 'DM Sans',sans-serif;text-align:center;box-shadow:0 0 0 2px #fff,0 1px 4px rgba(0,0,0,.4)}}
.anot{{margin:0;padding:.9rem 1rem .9rem 2.4rem;display:flex;flex-direction:column;gap:.3rem;font-size:.8125rem;color:var(--text-muted);line-height:1.45;list-style:decimal}}
.v-mov{{display:none;padding:1rem;background:var(--surface-alt)}}
.v-mov img{{max-width:260px;margin:0 auto;border-radius:16px;border:1px solid var(--border)}}
.galeria[data-vista="mov"] .v-esc{{display:none}} .galeria[data-vista="mov"] .v-mov{{display:block}}
.galeria[data-vista="mov"] .marco.vacio{{display:none}}
.marco.vacio .hueco{{padding:2.5rem 1.5rem;text-align:center;color:var(--text-muted);font-size:.9375rem;line-height:1.55;background:var(--surface-alt);display:flex;flex-direction:column;gap:.5rem}}
.marco.vacio .hueco b{{color:var(--text)}}
.sub{{font-size:1.125rem;margin:2.5rem 0 1rem}}
.extras{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:var(--gap)}}
/* patrones, lentes, mercado, ia, ruta */
.patrones{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:var(--gap)}}
.pat{{display:flex;flex-direction:column;gap:.7rem}}
.pat header{{display:flex;justify-content:space-between;align-items:center}}
.pat .n{{font-size:1.75rem;font-weight:700;color:var(--text-muted);line-height:1}}
.pat h3{{font-size:1.0625rem}}
.pat p{{font-size:.875rem;color:var(--text-muted);font-weight:300}}
.pat .pie{{margin-top:auto;font-weight:400}}
.chips{{display:flex;flex-wrap:wrap;gap:.4rem}}
.lentes{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:var(--gap)}}
.lente .op{{border-top:1px solid var(--border);margin-top:1.1rem;padding-top:1rem}}
.lente .op b{{font-size:.6875rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-text)}}
.lente .op p{{font-size:.9375rem;margin-top:.3rem}}
.cuota{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.9rem}}
.cuota li{{display:grid;grid-template-columns:70px 1fr 52px;gap:.8rem;align-items:center;font-size:.875rem}}
.cuota b{{text-align:right}}
.veredicto .frase{{font-size:clamp(1.25rem,2.4vw,1.75rem)}}
.veredicto .ap{{margin-top:.8rem;opacity:.8;font-size:.9375rem;font-weight:300}}
.ruta{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,235px),1fr));gap:var(--gap)}}
.fase .paso{{width:32px;height:32px;border-radius:10px;background:var(--text);color:var(--bg);display:grid;place-items:center;font-weight:700;margin-bottom:.9rem}}
.fase h3{{font-size:1.25rem}}
.fase .cuando{{font-size:.8125rem;color:var(--text-muted);margin-top:.25rem}}
/* pie */
.cierre{{padding:clamp(3rem,7vw,5rem) 0 3rem;border-top:1px solid var(--border)}}
.cierre .mision{{font-size:clamp(1.5rem,3.4vw,2.25rem);font-weight:700;letter-spacing:-.02em;max-width:22ch;line-height:1.12}}
.cierre .marca{{margin-top:1.5rem;font-weight:700;font-size:1.5rem;color:var(--accent-text)}}
.meta-pie{{margin-top:2rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;font-size:.8125rem;color:var(--text-muted)}}
/* móvil: tablas */
@media (max-width:640px){{.stats{{grid-template-columns:1fr}} .fila-b .gap{{order:3}} .masthead{{position:static}} .masthead nav{{flex-wrap:nowrap;overflow-x:auto;max-width:100%;padding-bottom:.25rem}} .masthead nav a{{white-space:nowrap}}}}
@media print{{.masthead{{position:static}} .tema,.acciones{{display:none}} .card,.marco{{break-inside:avoid;box-shadow:none}}}}
"""

# ───────────────────────── JS ─────────────────────────
SCRIPT = r"""
<script src="vendor/hairline-terrain.iife.js"></script>
<script>
(function(){
  var raiz=document.documentElement, bt=document.getElementById('tema');
  var mq=window.matchMedia('(prefers-color-scheme: dark)');
  function oscuro(){var t=raiz.getAttribute('data-theme');return t?t==='dark':mq.matches;}
  function pinta(){var o=oscuro();bt.setAttribute('aria-pressed',String(o));bt.setAttribute('aria-label',o?'Cambiar a tema claro':'Cambiar a tema oscuro');bt.textContent=o?'Claro':'Oscuro';}
  bt.addEventListener('click',function(){raiz.setAttribute('data-theme',oscuro()?'light':'dark');pinta();});
  mq.addEventListener('change',pinta);pinta();
})();
/* Terrenos (Hairline): ilustración decorativa; si la librería falta, la tarjeta sigue diciendo lo mismo en texto. */
(function(){
  var quieto=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(typeof Hairline==='undefined'||!Hairline.terrain){document.querySelectorAll('.terreno').forEach(function(t){t.style.display='none';});return;}
  document.querySelectorAll('.terreno').forEach(function(el){
    var apagado=el.getAttribute('data-quieto')==='1';
    try{Hairline.terrain(el,{play:!quieto&&!apagado,intensity:apagado?0.15:(el.id==='terreno-hero'?0.75:0.5),theme:'auto',
      label:'Ilustración decorativa: pilares que se elevan alrededor del puntero. No contiene datos.'});}
    catch(e){el.style.display='none';}
  });
})();
/* Panorama ↔ matriz */
(function(){
  var cards=document.querySelectorAll('.emp');
  function marca(id,on){document.querySelectorAll('.matriz [data-col="'+id+'"]').forEach(function(c){c.classList.toggle('resalta',on);});
    cards.forEach(function(c){c.classList.toggle('activa',on&&c.getAttribute('data-site')===id);});}
  cards.forEach(function(c){var id=c.getAttribute('data-site');
    c.addEventListener('mouseenter',function(){marca(id,true);});c.addEventListener('mouseleave',function(){marca(id,false);});
    c.addEventListener('focus',function(){marca(id,true);});c.addEventListener('blur',function(){marca(id,false);});});
})();
/* Matriz: evidencia por celda */
(function(){
  var D=__DATOS__, panel=document.getElementById('evidencia'), prev=null;
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
  document.querySelectorAll('.celda').forEach(function(b){b.addEventListener('click',function(){
    if(prev)prev.removeAttribute('aria-pressed');b.setAttribute('aria-pressed','true');prev=b;
    var s=D.sitios[b.dataset.site],c=D.criterios[b.dataset.crit],cell=(D.p[b.dataset.site]||{})[b.dataset.crit];
    var h='<div class="eyebrow">Evidencia</div><div class="tit"><b>'+esc(c.nombre)+' · '+esc(s.nombre)+'</b>';
    if(cell){h+='<span class="chip s'+cell.p+'">'+cell.p+'</span><span class="tag tag-line">'+esc(D.escala[cell.p])+'</span><span class="tag tag-line">'+(c.tipo==='medido'?'Medido':'Observado')+'</span></div><p class="def">'+esc(c.def)+'</p><p class="txt">'+esc(cell.e)+'</p>';
      if(cell.checks){h+='<ul class="chk">'+cell.checks.map(function(k){return '<li>'+(k[1]?'✓ ':'✗ ')+esc(k[0])+(k[1]?'':' (falla)')+'</li>';}).join('')+'</ul>';}
    }else{h+='<span class="chip sn">—</span><span class="tag tag-line">Sin evaluar</span></div><p class="def">'+esc(c.def)+'</p><p class="txt">'+esc(s.motivo||'No hay evidencia observada para este criterio.')+'</p>';}
    panel.innerHTML=h;});});
})();
/* Capturas: escritorio / móvil */
(function(){
  var g=document.querySelector('.galeria');
  document.querySelectorAll('.seg [data-vista]').forEach(function(b){b.addEventListener('click',function(){
    document.querySelectorAll('.seg [data-vista]').forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
    g.setAttribute('data-vista',b.dataset.vista);});});
})();
</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.min.js"></script>
<script>
/* Gráfica: tokens en caliente, repintado al cambiar de tema, sin animación en movimiento reducido y sin cortar el resto si el CDN falla. */
(function(){
  var quieto=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var el=document.getElementById('v-ranking'),inst=null;
  if(typeof Chart==='undefined'){document.querySelectorAll('.viz').forEach(function(v){v.classList.add('sin-libreria');var d=v.querySelector('.viz-tabla');if(d)d.open=true;});return;}
  var R=__RANKING__;
  var sonda=document.createElement('span');sonda.style.display='none';document.body.appendChild(sonda);
  function tk(n){sonda.style.color='var('+n+')';return getComputedStyle(sonda).color;}
  function config(){return {type:'bar',data:{labels:R.map(function(r){return r[0];}),datasets:[{label:'Puntaje',data:R.map(function(r){return r[1];}),
      backgroundColor:R.map(function(r){return r[2]?tk('--accent'):tk('--chart-otros');}),borderRadius:6,barThickness:24}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:4},animation:quieto?false:{duration:200},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.parsed.x+' de __MAX__';}}}},
      scales:{x:{min:0,max:__MAX__,grid:{color:tk('--border')},ticks:{color:tk('--text-muted'),stepSize:6},border:{display:false}},
              y:{grid:{display:false},ticks:{color:tk('--text'),font:{weight:500}},border:{display:false}}}}};}
  function repinta(){if(inst)inst.destroy();inst=new Chart(el,config());}
  if(el)repinta();
  new MutationObserver(function(){if(el)repinta();}).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(){if(el)repinta();});
})();
</script>"""

js_datos = {
    "sitios": {s: {"nombre": SITES[s]["nombre"], "motivo": SITES[s].get("motivo", "")} for s in SITES},
    "criterios": {c["id"]: {"nombre": c["nombre"], "def": c["def"], "tipo": c["tipo"]} for c in CRIT},
    "escala": {int(k): v for k, v in ESCALA.items()},
    "p": {s: {c: {k: v for k, v in cell.items() if k in ("p", "e", "checks")} for c, cell in P.get(s, {}).items()} for s in SITES},
}
js_rank = [[SITES[s]["corto"], TOTAL[s], s == "dproma"] for s in ranking]
script = SCRIPT.replace("__DATOS__", json.dumps(js_datos, ensure_ascii=False)).replace("__RANKING__", json.dumps(js_rank, ensure_ascii=False)).replace("__MAX__", str(MAXP))

NAV = [("resumen", "Resumen"), ("matriz", "Matriz"), ("brecha", "Brecha"), ("capturas", "Capturas"), ("patrones", "Patrones"), ("lentes", "Estrategia"), ("ia", "IA"), ("ruta", "Ruta")]
nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in NAV)

page = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Benchmark web de dproma.com · 2894_ × DPROMA</title>
<meta name="description" content="Benchmark de la web de DPROMA frente a competidores de carga EV en México y referentes de tecnología, automotriz y energía renovable." />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#resumen">Saltar al contenido</a>
<header class="masthead">
  <div class="wrap masthead-inner">
    <a class="wordmark" href="#inicio">2894_ <span>× DPROMA</span></a>
    <nav aria-label="Secciones">{nav}<button type="button" class="tema" id="tema" aria-pressed="false" aria-label="Cambiar a tema oscuro">Oscuro</button></nav>
  </div>
</header>
<main>
{sec_hero()}{sec_resumen()}{sec_panorama()}{sec_ranking()}{sec_matriz()}{sec_brecha()}{sec_capturas()}{sec_patrones()}{sec_mercado()}{sec_lentes()}{sec_ia()}{sec_ruta()}{sec_sistema()}{sec_fuentes()}
</main>
<footer class="cierre">
  <div class="wrap">
    <p class="mision">{MISION}</p>
    <p class="marca">2894_</p>
    <div class="meta-pie"><span>Benchmark web de dproma.com · {FECHA} · Experimento interno</span></div>
  </div>
</footer>
{script}
</body>
</html>
"""
(OUT / "index.html").write_text(page, encoding="utf-8")
print("OK", len(page) // 1024, "KB · DPROMA", TOTAL["dproma"], "· puesto", pos_dproma, "de", len(COMPLETOS))
print({s: TOTAL[s] for s in ranking})
