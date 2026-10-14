// Medición de Mi día (28): original del cliente vs prototipos. Solo lee; no modifica ningún HTML.
// Uso:  cd <scratchpad> && NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node <ruta>/medir28.cjs
// Entorno: ORIG, PROTO (def. http://127.0.0.1:8777), OUT (def. carpeta de este script)
const { chromium } = require('playwright');
const lib = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const path = require('path');
const ORIG = process.env.ORIG || 'http://127.0.0.1:8732/28_instalador_mi_dia.html';
const PROTO = process.env.PROTO || 'http://127.0.0.1:8777';
const OUT = process.env.OUT || __dirname;
const VARIANTES = [
  ['original', ORIG],
  ['A-minimo', PROTO + '/28-mi-dia-A-minimo.html'],
  ['B-recomendado', PROTO + '/28-mi-dia-B-recomendado.html'],
  ['C-primer-pliegue', PROTO + '/28-mi-dia-C-primer-pliegue.html'],
];
const ANCHOS = [[390, 844], [1440, 900], [1280, 800], [1024, 768]];

function medir() {
  const R = e => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height }; };
  const f1 = n => +n.toFixed(1);
  const parse = c => { const m = c && c.match(/[\d.]+/g); if (!m) return null; return { r: +m[0], g: +m[1], b: +m[2], a: m.length > 3 ? +m[3] : 1 }; };
  const over = (f, b) => ({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 });
  const fondo = el => { const capas = []; let n = el;
    while (n && n.nodeType === 1) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0) { capas.push(c); if (c.a === 1) break; } n = n.parentElement; }
    let base = capas.length && capas[capas.length - 1].a === 1 ? capas.pop() : { r: 255, g: 255, b: 255, a: 1 };
    for (let i = capas.length - 1; i >= 0; i--) base = over(capas[i], base); return base; };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
  const contr = el => { const cs = getComputedStyle(el); const bg = fondo(el); let fg = parse(cs.color); if (fg.a < 1) fg = over(fg, bg); return +ratio(fg, bg).toFixed(2); };
  const st = document.createElement('style'); st.textContent = '*,*::before,*::after{transition:none !important;animation:none !important}'; document.head.appendChild(st);
  const inter = (a, b) => !(a.r <= b.l + .5 || b.r <= a.l + .5 || a.b <= b.t + .5 || b.b <= a.t + .5);
  const out = {};
  const main = document.getElementById('contenido');
  const p4 = document.querySelector('.p4'); const p4r = R(p4);
  // 1. Cabecera: aire arriba y abajo medido hasta la CAJA DE TEXTO (no la caja de línea)
  const cajasTexto = [...p4.querySelectorAll('h1,.resumen')].filter(e => e.getBoundingClientRect().height > 0).map(e => { const rg = document.createRange(); rg.selectNodeContents(e); const rs = [...rg.getClientRects()].filter(r => r.width > 0); return { t: Math.min(...rs.map(r => r.top)), b: Math.max(...rs.map(r => r.bottom)), el: e.tagName + '.' + e.className }; });
  const hijosVis = [...p4.querySelectorAll('h1,.resumen,.resumen .pill')].filter(e => e.getBoundingClientRect().height > 0).map(e => R(e));
  const topC = Math.min(...hijosVis.map(r => r.t)), botC = Math.max(...hijosVis.map(r => r.b));
  out.cabecera = { alto: f1(p4r.h), paddingBottom: getComputedStyle(p4).paddingBottom, airArriba: f1(topC - p4r.t), airAbajo: f1(p4r.b - 1 - botC),
    airAbajoTexto: f1(p4r.b - 1 - Math.max(...cajasTexto.map(c => c.b))), filas: new Set(hijosVis.filter(r => r.h > 0).map(r => Math.round(r.t / 8))).size };
  const hs = [...p4.querySelectorAll('h1,.resumen,.pill')].filter(e => e.getBoundingClientRect().height > 0).map(e => [e, R(e)]);
  out.cabecera.solapes = []; for (let a = 0; a < hs.length; a++) for (let b = a + 1; b < hs.length; b++) { if (hs[a][0].contains(hs[b][0]) || hs[b][0].contains(hs[a][0])) continue; if (inter(hs[a][1], hs[b][1])) out.cabecera.solapes.push(hs[a][0].className + '/' + hs[b][0].className); }
  out.cabecera.recorte = p4.scrollWidth > p4.clientWidth + 1 || [...p4.querySelectorAll('*')].some(e => R(e).r > p4r.r + .5);
  out.cabecera.resumenTexto = (p4.querySelector('.resumen') || {}).textContent || null;
  // 2. Primer pliegue: qué hay antes de la primera cita; ¿se ven sus acciones sin desplazar?
  const m0 = R(main); const pie = document.querySelector('.pie-accion'); const pieR = pie ? R(pie) : null;
  const c1 = document.querySelector('.cita-tel'); const c1r = R(c1);
  const acc = [...c1.querySelectorAll('.gordo')].map(b => R(b)); const visibleHasta = pieR ? pieR.t : innerHeight;
  out.primerPliegue = { vp: innerHeight, inicioMain: f1(m0.t), primeraCitaTop: f1(c1r.t), antesDeLaPrimeraCita: f1(c1r.t - m0.t), pctVPantesCita: Math.round(100 * (c1r.t - m0.t) / innerHeight),
    avisoMaterialBottom: (() => { const a = document.querySelector('.aviso-fila'); return a ? f1(R(a).b) : null; })(), avisoMaterialVisible: (() => { const a = document.querySelector('.aviso-fila'); return a && pieR ? R(a).b <= pieR.t + .5 : null; })(),
    comoLlegarBottom: f1(acc[0].b), abrirOrdenBottom: f1(acc[acc.length - 1].b), zonaVisibleHasta: f1(visibleHasta), accionesDeLaPrimeraCitaVisibles: acc[acc.length - 1].b <= visibleHasta + .5 };
  // 3. Cola de la lista: aire entre la última tarjeta y la barra fija, al final del desplazamiento
  main.scrollTop = main.scrollHeight; const tarj = [...document.querySelectorAll('.tel > article')]; const ult = R(tarj[tarj.length - 1]);
  out.cola = { airUltimaTarjetaBarra: pieR ? f1(R(pie).t - ult.b) : null, paddingBottomTel: getComputedStyle(document.querySelector('.tel')).paddingBottom };
  main.scrollTop = 0;
  // 4. Destinos pulsables
  const dest = [...document.querySelectorAll('.p4 button,.p4 a,.cromo-top button,main button,main a,.pie-accion button')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; }).map(e => { const r = R(e); return { sel: e.className.split(' ')[0] || e.tagName, w: f1(r.w), h: f1(r.h), t: (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 22) }; });
  out.destinos = { total: dest.length, bajo24: dest.filter(d => Math.min(d.w, d.h) < 24), bajo44: dest.filter(d => d.h < 44).map(d => d.sel + ':' + d.h), min: Math.min(...dest.map(d => d.h)), gordosMin: Math.min(...dest.filter(d => d.sel === 'gordo').map(d => d.h)) };
  // 5. Relleno lateral de .gordo (--sp-5)
  const g = document.querySelector('.gordo'); out.gordo = { paddingLeft: getComputedStyle(g).paddingLeft, sp5: getComputedStyle(document.documentElement).getPropertyValue('--sp-5').trim() || null };
  // 6. Desborde horizontal y elementos fuera del ancho
  out.scrollHorizontalPagina = document.documentElement.scrollWidth > innerWidth + 1;
  out.fueraDelAncho = [...document.querySelectorAll('main *,.p4 *,.pie-accion *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > innerWidth + .5 || r.left < -.5); }).slice(0, 5).map(e => e.className || e.tagName);
  // solape entre la última tarjeta y la barra fija (al final) ya cubierto en cola; solape cabecera / contenido:
  out.solapeCabeceraContenido = inter(p4r, m0);
  // 7. Contraste (claro y oscuro)
  const cc = {}; const rs = p4.querySelector('.resumen'); if (rs && rs.getBoundingClientRect().height) { cc.resumen = contr(rs); const pl = rs.querySelector('.pill'); if (pl) cc.pillCabecera = contr(pl); const rb = rs.querySelector('b'); if (rb) cc.resumenB = contr(rb); }
  cc.h1 = contr(p4.querySelector('h1')); cc.dura = contr(document.querySelector('.cita-tel .dura')); cc.avisoFila = contr(document.querySelector('.aviso-fila')); cc.senal = contr(document.querySelector('.senal'));
  out.contrasteClaro = cc;
  document.documentElement.setAttribute('data-theme', 'dark');
  const cd = {}; if (rs && rs.getBoundingClientRect().height) { cd.resumen = contr(rs); const pl = rs.querySelector('.pill'); if (pl) cd.pillCabecera = contr(pl); const rb = rs.querySelector('b'); if (rb) cd.resumenB = contr(rb); }
  cd.h1 = contr(p4.querySelector('h1')); cd.dura = contr(document.querySelector('.cita-tel .dura')); cd.avisoFila = contr(document.querySelector('.aviso-fila')); cd.senal = contr(document.querySelector('.senal'));
  out.contrasteOscuro = cd; document.documentElement.setAttribute('data-theme', 'light');
  // 8. Coherencia cabecera / estado
  out.resumenPorEstado = {};
  for (const s of ['ok', 'loading', 'empty', 'error']) { main.setAttribute('data-state', s); const r = p4.querySelector('.resumen'); out.resumenPorEstado[s] = r && getComputedStyle(r).display !== 'none' && r.getBoundingClientRect().height > 0 ? r.textContent.trim().slice(0, 60) : '(oculto)'; }
  main.setAttribute('data-state', 'ok');
  return out;
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const todo = {};
  for (const [nombre, url] of VARIANTES) {
    todo[nombre] = {};
    for (const [W, H] of ANCHOS) {
      const page = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: W === 390 ? 2 : 1 });
      await lib.preparar(page); await page.goto(url);
      try { todo[nombre][W] = await page.evaluate(medir); } catch (e) { console.log('ERR', nombre, W, String(e).slice(0, 300)); await page.close(); continue; }
      if (W === 390 || W === 1440) {
        await page.evaluate(() => { document.getElementById('contenido').scrollTop = 0; });
        await page.screenshot({ path: path.join(OUT, `28-${nombre}-${W}.png`) });
      }
      if (W === 390) {
        await page.evaluate(() => { const m = document.getElementById('contenido'); m.scrollTop = m.scrollHeight; });
        await page.screenshot({ path: path.join(OUT, `28-${nombre}-${W}-final.png`) });
        if (nombre === 'B-recomendado' || nombre === 'original') {
          for (const s of ['empty', 'error']) { await page.evaluate(s => { document.getElementById('contenido').setAttribute('data-state', s); }, s); await page.screenshot({ path: path.join(OUT, `28-${nombre}-${W}-${s}.png`) }); }
        }
      }
      await page.close();
    }
  }
  require('fs').writeFileSync(path.join(OUT, 'medidas-28.json'), JSON.stringify(todo, null, 1));
  await b.close();
  for (const n of Object.keys(todo)) for (const W of Object.keys(todo[n])) { const m = todo[n][W]; if (!m) continue;
    console.log(n.padEnd(16), W, 'cab', m.cabecera.alto + 'px pb' + m.cabecera.paddingBottom, 'arr/abj', m.cabecera.airArriba + '/' + m.cabecera.airAbajo, '(txt ' + m.cabecera.airAbajoTexto + ')', 'filas', m.cabecera.filas, 'sol', m.cabecera.solapes.length, 'rec', m.cabecera.recorte,
      '| antesCita', m.primerPliegue.antesDeLaPrimeraCita + 'px(' + m.primerPliegue.pctVPantesCita + '%)', 'accVis', m.primerPliegue.accionesDeLaPrimeraCitaVisibles, 'avisoMat', m.primerPliegue.avisoMaterialBottom, m.primerPliegue.avisoMaterialVisible, 'finCab+antes', Math.round(m.cabecera.alto + m.primerPliegue.antesDeLaPrimeraCita), '| cola', m.cola.airUltimaTarjetaBarra, '| <24', m.destinos.bajo24.length, 'gordoMin', m.destinos.gordosMin, '| sp5', m.gordo.sp5, 'padL', m.gordo.paddingLeft, '| scrollH', m.scrollHorizontalPagina, 'fuera', m.fueraDelAncho.length,
      '| res empty/error', m.resumenPorEstado.empty.slice(0, 12), '/', m.resumenPorEstado.error.slice(0, 12)); }
})();
