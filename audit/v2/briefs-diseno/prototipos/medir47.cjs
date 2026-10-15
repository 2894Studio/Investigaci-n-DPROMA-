// Medición del Asistente (47): original del cliente vs prototipos. Solo lee; no modifica ningún HTML.
// Uso:  cd <scratchpad> && NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node <ruta>/medir47.cjs
// Entorno: ORIG (url del original, def. http://127.0.0.1:8732/47_asistente.html), PROTO (base de prototipos, def. http://127.0.0.1:8777),
//          OUT (carpeta de salida de capturas y json, def. la carpeta de este script)
const { chromium } = require('playwright');
const lib = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const path = require('path');
const ORIG = process.env.ORIG || 'http://127.0.0.1:8732/47_asistente.html';
const PROTO = process.env.PROTO || 'http://127.0.0.1:8777';
const OUT = process.env.OUT || __dirname;
const VARIANTES = [
  ['original', ORIG],
  ['A-minimo', PROTO + '/47-asistente-A-minimo.html'],
  ['B-recomendado', PROTO + '/47-asistente-B-recomendado.html'],
  ['C-historial', PROTO + '/47-asistente-C-historial-compacto.html'],
  ['D-estados', PROTO + '/47-asistente-D-estados-respuesta.html'],
];
const ANCHOS = [[1440, 900], [1280, 800], [1024, 768], [390, 844], [820, 1180]];

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
  const out = {};
  const tx = [...document.querySelectorAll('.msg.ia .tx')];
  // 1. Solape entre la última línea de texto y la franja
  out.respuestas = tx.filter(t => t.querySelector('.fuentes') && t.querySelector('p')).map((t, i) => {
    const fu = t.querySelector('.fuentes'); const ps = [...t.querySelectorAll('p')].filter(p => !fu.contains(p)); const last = ps[ps.length - 1];
    const rg = document.createRange(); rg.selectNodeContents(last); const rs = [...rg.getClientRects()]; const ll = rs[rs.length - 1];
    const fr = R(fu), tr = R(t);
    const cs = getComputedStyle(fu);
    // la caja de línea de texto (line-height) es la que "toca"; el glifo ocupa ~el cuerpo de la fuente
    return { i, aireUltimaLineaFranja: f1(fr.t - ll.bottom), aireGlifo: f1(fr.t - (ll.bottom - (ll.height - 14) / 2)),
      franjaMarginTop: cs.marginTop, franjaFondo: cs.backgroundColor, tarjetaFondo: getComputedStyle(t).backgroundColor,
      franjaAlto: f1(fr.h), tarjetaAlto: f1(tr.h),
      aireInferiorFranjaBordeTarjeta: f1(tr.b - 1 - fr.b),
      enlaces: [...fu.querySelectorAll('a')].map(a => { const ar = R(a); return { txt: a.textContent.trim().slice(0, 28), w: f1(ar.w), h: f1(ar.h) }; }) };
  });
  // 2. Destinos pulsables (región que acepta la pulsación: la <label> si existe)
  const dest = [...document.querySelectorAll('.hist a,.hist input,.mensajes a,.mensajes button,.compositor button,.compositor textarea,.p4 button,.p4 a')]
    .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; })
    .map(e => { const lab = e.closest('label'); const r = R(lab || e); return { sel: e.tagName.toLowerCase() + (e.id ? '#' + e.id : e.className ? '.' + String(e.className).split(' ')[0] : ''), txt: (e.textContent || e.placeholder || '').trim().slice(0, 26), w: f1(r.w), h: f1(r.h), region: lab ? 'label' : 'propio' }; });
  out.destinos = { total: dest.length, bajo24: dest.filter(d => Math.min(d.w, d.h) < 24), bajo44: dest.filter(d => d.h < 44).length, minAlto: Math.min(...dest.map(d => d.h)) };
  // 3. Recorte y solape
  const dentro = [];
  tx.forEach((t, i) => { const tr = R(t); t.querySelectorAll('*').forEach(e => { const r = R(e); if (r.w === 0 || r.h === 0) return;
    if (r.l < tr.l - .5 || r.r > tr.r + .5 || r.t < tr.t - .5 || r.b > tr.b + .5) dentro.push({ i, el: e.tagName + '.' + e.className, l: f1(r.l - tr.l), r: f1(tr.r - r.r), t: f1(r.t - tr.t), b: f1(tr.b - r.b) }); }); });
  out.fueraDeTarjeta = dentro.slice(0, 6);
  const desborde = [...document.querySelectorAll('.msg *,.mensajes,.compositor *')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'visible' && e.clientWidth > 0).map(e => e.tagName + '.' + e.className);
  out.recorteHorizontalInterno = desborde.slice(0, 6);
  out.scrollHorizontalPagina = document.documentElement.scrollWidth > innerWidth + 1;
  const inter = (a, b) => !(a.r <= b.l + .5 || b.r <= a.l + .5 || a.b <= b.t + .5 || b.b <= a.t + .5);
  const sol = [];
  tx.filter(t => t.querySelector('.fuentes')).forEach((t, i) => { const hijos = [...t.children].map(c => [c, R(c)]);
    for (let a = 0; a < hijos.length; a++) for (let b = a + 1; b < hijos.length; b++) if (inter(hijos[a][1], hijos[b][1])) sol.push({ i, a: hijos[a][0].className || hijos[a][0].tagName, b: hijos[b][0].className || hijos[b][0].tagName });
    const fu = t.querySelector('.fuentes'); const hs = [...fu.children].map(c => R(c));
    for (let a = 0; a < hs.length; a++) for (let b = a + 1; b < hs.length; b++) if (inter(hs[a], hs[b])) sol.push({ i, a: 'hijo-franja-' + a, b: 'hijo-franja-' + b }); });
  out.solapes = sol;
  // 4. Contraste (texto de la franja y de sus controles)
  const c = {};
  const fu = tx[0].querySelector('.fuentes'); c.rotuloFranja = contr(fu.querySelector('.et')); c.enlaceFranja = contr(fu.querySelector('a'));
  const tx2 = tx[1].querySelector('.fuentes'); c.rotuloFranja2 = contr(tx2.querySelector('.et')); c.enlaceFranja2 = contr(tx2.querySelector('a'));
  c.cuerpo = contr(tx[0].querySelector('p')); c.aviso = contr(document.querySelector('.aviso-ia')); c.qn = contr(document.querySelector('.msg .qn'));
  const bp = document.querySelector('.fuentes--paso .btn'); if (bp) c.botonPaso = contr(bp);
  out.contrasteClaro = c;
  document.documentElement.setAttribute('data-theme', 'dark');
  const d = {}; d.rotuloFranja = contr(fu.querySelector('.et')); d.enlaceFranja = contr(fu.querySelector('a')); d.enlaceFranja2 = contr(tx2.querySelector('a')); d.cuerpo = contr(tx[0].querySelector('p')); d.qn = contr(document.querySelector('.msg .qn'));
  out.contrasteOscuro = d;
  if (bp) d.botonPaso = contr(bp);
  document.documentElement.setAttribute('data-theme', 'light');
  // 5. Reparto de la altura (hilo vs historial vs compositor) y cabecera
  const H = innerHeight; out.altura = { vp: H, hilo: f1(R(document.querySelector('.mensajes')).h), hist: f1(R(document.querySelector('.hist')).h), compositor: f1(R(document.querySelector('.compositor')).h), cabecera: f1(R(document.querySelector('.p4')).h) };
  out.altura.hiloPct = Math.round(100 * out.altura.hilo / H);
  const p4 = document.querySelector('.p4'); const btn = p4.querySelector('.btn'); out.cabecera = { paddingBottom: getComputedStyle(p4).paddingBottom, aireBotonBorde: f1(R(p4).b - 1 - R(btn).b) };
  // 6. Isotipo del avatar
  const av = document.querySelector('.msg.ia .av svg'); const u = av.querySelector('use'); out.isotipoAvatar = { svg: f1(R(av).w) + 'x' + f1(R(av).h), dx: f1(R(u).l - R(av).l), tieneViewBox: av.hasAttribute('viewBox') };
  const lg = document.querySelector('.side .logo svg'); const ul = lg.querySelector('use'); out.isotipoLogo = { dx: f1(R(ul).l - R(lg).l), tieneViewBox: lg.hasAttribute('viewBox') };
  // foco: el contorno (2px + 2px de separación) de cada enlace/botón de la franja cabe dentro de la tarjeta (no lo recorta overflow:hidden)
  out.foco = tx.flatMap(t => [...t.querySelectorAll('.fuentes a')].map(a => { a.focus({ focusVisible: true }); const cs = getComputedStyle(a); const r = R(a), tr = R(t);
    const ow = parseFloat(cs.outlineWidth) || 0, off = parseFloat(cs.outlineOffset) || 0; const ext = ow + off;
    return { txt: a.textContent.trim().slice(0, 24), outline: cs.outlineStyle + ' ' + cs.outlineWidth, cabe: r.l - ext >= tr.l && r.r + ext <= tr.r && r.t - ext >= tr.t && r.b + ext <= tr.b }; }));
  document.activeElement && document.activeElement.blur();
  const pend = document.querySelector('.msg.ia[aria-busy]'); const ref = document.querySelector('.ref-err');
  out.estadosRespuesta = pend ? { pendienteStatus: !!pend.querySelector('[role=status][aria-label]'), skelSinTexto: [...pend.querySelectorAll('.skel')].every(e => e.textContent.trim() === ''), qnPendiente: contr(pend.querySelector('.qn')),
    refError: ref ? contr(ref) : null, botonError: contr(document.querySelector('.msg.ia:last-child .btn.mini')), botonErrorAlto: f1(R(document.querySelector('.msg.ia:last-child .btn.mini')).h), textoErrorChars: document.querySelector('.msg.ia:last-child .tx-cuerpo p').textContent.length } : null;
  out.ariaLive = !!document.querySelector('.mensajes[role="log"],.mensajes[aria-live],[role="log"]');
  out.buscarEsLabel = !!document.querySelector('label.search');
  return out;
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const todo = {};
  for (const [nombre, url] of VARIANTES) {
    todo[nombre] = {};
    for (const [W, H] of ANCHOS) {
      const page = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: W === 390 ? 2 : 1 });
      await lib.preparar(page);
      await page.goto(url);
      try { todo[nombre][W] = await page.evaluate(medir); } catch (e) { console.log("ERR", nombre, W, String(e).slice(0, 300)); await page.close(); continue; }
      if (nombre !== 'original' && (W === 1440 || W === 390)) {
        await page.screenshot({ path: path.join(OUT, `47-${nombre}-${W}.png`) });
      }
      if (W === 1440 && nombre === 'D-estados') {
        await page.evaluate(() => { const m = document.querySelector('.mensajes'); m.scrollTop = m.scrollHeight; });
        const bb = await (await page.$('.mensajes')).boundingBox(); await page.screenshot({ path: path.join(OUT, `47-D-estados-1440-hilo.png`), clip: bb });
      }
      if (W === 1440 && nombre === 'B-recomendado') {
        await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
        const e2 = await page.$$('.msg.ia'); await e2[1].screenshot({ path: path.join(OUT, `47-${nombre}-respuesta2-oscuro.png`) });
        await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'light'));
      }
      if (W === 1440) {
        const els = await page.$$('.msg.ia');
        for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(OUT, `47-${nombre}-respuesta${i + 1}.png`) });
      }
      await page.close();
    }
  }
  require('fs').writeFileSync(path.join(OUT, 'medidas-47.json'), JSON.stringify(todo, null, 1));
  await b.close();
  for (const n of Object.keys(todo)) for (const W of Object.keys(todo[n])) {
    const m = todo[n][W];
    console.log(n.padEnd(14), W, 'aire', m.respuestas.map(r => r.aireUltimaLineaFranja).join('/'), '| bajo24', m.destinos.bajo24.length, '| solapes', m.solapes.length, '| fuera', m.fueraDeTarjeta.length, '| scrollH', m.scrollHorizontalPagina,
      '| hilo', m.altura.hilo + 'px(' + m.altura.hiloPct + '%)', '| cab pb', m.cabecera.paddingBottom, 'aireBtn', m.cabecera.aireBotonBorde, '| rot/enl', m.contrasteClaro.rotuloFranja, m.contrasteClaro.enlaceFranja, 'osc', m.contrasteOscuro.rotuloFranja, m.contrasteOscuro.enlaceFranja, '| foco', m.foco.every(f => f.cabe), '| est', m.estadosRespuesta ? JSON.stringify(m.estadosRespuesta) : '-', '| live', m.ariaLive, '| dxAv', m.isotipoAvatar.dx);
  }
})();
