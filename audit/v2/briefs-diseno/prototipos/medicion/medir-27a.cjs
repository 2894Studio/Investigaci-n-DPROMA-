// Medición del acordeón de sucursales del padrón (27_padron_clientes y prototipo).
// Uso: NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node medir-27a.cjs <url> <etiqueta> [salida.json]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const M = require('./medir-lib.cjs');
const url = process.argv[2], etiqueta = process.argv[3] || 'x', salida = process.argv[4];
const VP = [[1440, 900], [1280, 800], [1024, 768], [390, 844]];
const CAPDIR = path.join(__dirname, '..', 'capturas');

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = { url, etiqueta, fecha: new Date().toISOString(), medidas: {} };
  for (const [w, h] of VP) for (const tema of ['light', 'dark']) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce', colorScheme: tema });
    const page = await ctx.newPage();
    await require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs').preparar(page);
    await page.goto(url, { waitUntil: 'load' });
    await page.evaluate(M.inyectar);
    await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), tema);

    // 1) integridad de los controles: cada aria-controls apunta a un id existente
    const integridad = await page.evaluate(() => {
      const bs = Array.from(document.querySelectorAll('.suc-btn[aria-controls]'));
      return { botones: bs.length, conDestino: bs.filter(x => document.getElementById(x.getAttribute('aria-controls'))).length,
               nombres: bs.map(x => x.getAttribute('aria-label')), expandidos: bs.map(x => x.getAttribute('aria-expanded')),
               filasHijas: document.querySelectorAll('tr.hijas').length };
    });
    // 2) comportamiento: clic alterna aria-expanded/hidden; Escape cierra y devuelve el foco
    const comportamiento = await page.evaluate(async () => {
      const bs = Array.from(document.querySelectorAll('.suc-btn[aria-controls]')); const res = [];
      for (const bt of bs) {
        const dest = document.getElementById(bt.getAttribute('aria-controls')); if (!dest) { res.push({ id: bt.getAttribute('aria-controls'), existe: false }); continue; }
        const antes = bt.getAttribute('aria-expanded'), ocultoAntes = dest.hidden || getComputedStyle(dest).display === 'none';
        bt.click();
        const despues = bt.getAttribute('aria-expanded'), ocultoDespues = dest.hidden || getComputedStyle(dest).display === 'none';
        // dejamos abierto para probar Escape sobre el botón: si el clic lo cerró, se reabre primero
        if (bt.getAttribute('aria-expanded') !== 'true') bt.click();
        bt.focus(); bt.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
        const trasEsc = bt.getAttribute('aria-expanded'), foco = document.activeElement === bt;
        // ... y Escape desde dentro del panel
        if (bt.getAttribute('aria-expanded') !== 'true') bt.click();
        const interior = dest.querySelector('button'); let escInterior = null;
        if (interior) { interior.focus(); interior.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); escInterior = bt.getAttribute('aria-expanded') === 'false' && document.activeElement === bt; }
        if (bt.getAttribute('aria-expanded') !== 'true') bt.click(); // dejarlo abierto
        res.push({ id: dest.id, existe: true, antes, despues, alterna: antes !== despues, ocultoAntes, ocultoDespues, escCierra: trasEsc === 'false', focoVuelve: foco, escDesdeDentro: escInterior, final: bt.getAttribute('aria-expanded') });
      }
      return res;
    });
    // 3) abrir todos los paneles para medir geometría
    await page.evaluate(() => { document.querySelectorAll('.suc-btn[aria-controls]').forEach(bt => { const d = document.getElementById(bt.getAttribute('aria-controls')); if (d && (bt.getAttribute('aria-expanded') !== 'true' || d.hidden)) bt.click(); }); });
    await page.evaluate(() => { if (document.activeElement) document.activeElement.blur(); document.querySelector('.tabla-caja').scrollLeft = 0; const m = document.getElementById('contenido'); if (m) m.scrollTop = 0; });
    await page.waitForTimeout(150);
    const geo = await page.evaluate(() => {
      const M = window.__M; const res = {};
      const caja = document.querySelector('.tabla-caja'); const rc = caja.getBoundingClientRect();
      res.cajaVisible = { l: +rc.left.toFixed(1), r: +rc.right.toFixed(1), scrollW: caja.scrollWidth, clientW: caja.clientWidth, scrollHorizontal: caja.scrollWidth > caja.clientWidth + 1 };
      const fab = document.querySelector('.fab').getBoundingClientRect();
      const paneles = Array.from(document.querySelectorAll('tr.hijas')).filter(M.vis);
      res.paneles = paneles.map(p => {
        const td = p.querySelector('td'); const rp = p.getBoundingClientRect();
        const lis = Array.from(p.querySelectorAll('li'));
        const filas = lis.map(li => {
          const rng = el => { const r = document.createRange(); r.selectNodeContents(el); return r.getBoundingClientRect(); };
          const nom = li.querySelector('.nom'); const btn = li.querySelector('button, .btn'); const pill = li.querySelector('.pill');
          const nombreB = li.querySelector('.nom b'); const dir = li.querySelector('.nom .dir') || li.querySelector('.nom > span:not(.l1)');
          const rb = btn.getBoundingClientRect();
          const finTexto = Math.max(nombreB ? rng(nombreB).right : 0, dir ? rng(dir).right : 0);
          const finPill = pill ? pill.getBoundingClientRect().right : null;
          return { nombre: (nombreB && nombreB.textContent) || '', pill: pill ? pill.textContent.trim() : null,
                   huecoNombreAccion: +(rb.left - (nombreB ? rng(nombreB).right : 0)).toFixed(1),
                   huecoTextoAccion: +(rb.left - finTexto).toFixed(1),
                   huecoTextoPill: pill ? +(pill.getBoundingClientRect().left - finTexto).toFixed(1) : null,
                   apilado: btn.getBoundingClientRect().top > (nombreB ? nombreB.getBoundingClientRect().bottom : 0) - 1,
                   huecoNombrePill: pill ? +(pill.getBoundingClientRect().left - rng(nombreB).right).toFixed(1) : null,
                   huecoPillAccion: pill ? +(rb.left - finPill).toFixed(1) : null,
                   btn: { x: +rb.left.toFixed(1), r: +rb.right.toFixed(1), w: +rb.width.toFixed(1), h: +rb.height.toFixed(1) },
                   alto: +li.getBoundingClientRect().height.toFixed(1) };
        });
        const hijos = Array.from(p.querySelectorAll('*')).filter(M.vis).filter(e => !/^(TD|TR)$/.test(e.tagName));
        const maxR = Math.max(...hijos.map(e => e.getBoundingClientRect().right)); const minL = Math.min(...hijos.map(e => e.getBoundingClientRect().left));
        return { id: p.id, alto: +rp.height.toFixed(1), ancho: +rp.width.toFixed(1), anchoListaUtil: (() => { const ul = p.querySelector('ul'); return ul ? +ul.getBoundingClientRect().width.toFixed(1) : null; })(),
                 maxDerecha: +maxR.toFixed(1), minIzquierda: +minL.toFixed(1),
                 fueraDeLaCajaVisible: hijos.filter(e => { const r = e.getBoundingClientRect(); return r.right > rc.right + 0.5 || r.left < rc.left - 0.5; }).length,
                 botonesFueraDeLaCajaVisible: Array.from(p.querySelectorAll('button')).filter(e => e.getBoundingClientRect().right > rc.right + 0.5).length,
                 enZonaFab: Array.from(p.querySelectorAll('button')).filter(e => { const r = e.getBoundingClientRect(); return !(r.right < fab.left - 16 || r.left > fab.right || r.bottom < fab.top - 16 || r.top > fab.bottom) && r.right > fab.left - 16; }).length,
                 chars: p.textContent.trim().replace(/\s+/g, ' ').length,
                 filas };
      });
      res.fab = { x: +fab.left.toFixed(1), w: +fab.width.toFixed(1) };
      res.docScrollH = document.documentElement.scrollWidth > innerWidth;
      return res;
    });
    // 4) calidad: contraste, fuentes, destinos dentro de los paneles y de la columna de sucursales
    const calidad = await page.evaluate(() => {
      const M = window.__M; const q = { contraste: [], fuentes: 0, fuentesMuestra: [], destinos: [], solapes: [] };
      for (const p of Array.from(document.querySelectorAll('tr.hijas')).filter(M.vis)) {
        const c = M.contraste(p); q.contraste.push({ id: p.id, nodos: c.nodos, min: c.minimo, fallos: c.fallos.map(f => `${f.txt}|${f.ratio}|${f.px}px`) });
        const f = M.fuentes(p); q.fuentes += f.bajo12; q.fuentesMuestra.push(...f.muestra);
        const d = M.destinos(p); q.destinos.push({ id: p.id, total: d.total, bajo24: d.bajo24, min: d.min });
        q.solapes.push(...M.solapes(p.querySelector('ul'), ':scope > li'));
      }
      const sb = Array.from(document.querySelectorAll('.suc-btn')).filter(M.vis).map(e => { const r = e.getBoundingClientRect(); return { w: +r.width.toFixed(1), h: +r.height.toFixed(1) }; });
      q.sucBtn = { n: sb.length, minW: Math.min(...sb.map(x => x.w)), minH: Math.min(...sb.map(x => x.h)) };
      return q;
    });
    out.medidas[`${w}x${h}-${tema}`] = { integridad, comportamiento, geo, calidad };
    if (tema === 'light') {
      // captura de la primera zona con paneles abiertos
      await page.evaluate(() => { const r = document.querySelector('tr.hijas'); r.previousElementSibling.scrollIntoView({ block: 'start' }); });
      await page.screenshot({ path: path.join(CAPDIR, `27a-${etiqueta}--${w}.png`) });
    }
    await ctx.close();
  }
  await b.close();
  const js = JSON.stringify(out, null, 1);
  if (salida) fs.writeFileSync(salida, js); else console.log(js);
})();
