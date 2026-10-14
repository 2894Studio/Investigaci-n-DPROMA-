// Medición de las etiquetas de estado de la tabla del padrón (27_padron_clientes y prototipo).
// Uso: NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node medir-27e.cjs <url> <etiqueta> [salida.json]
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
    await page.waitForTimeout(120);
    const r = await page.evaluate(() => {
      const M = window.__M; const res = {};
      const filas = Array.from(document.querySelectorAll('tbody tr')).filter(tr => !tr.classList.contains('hijas'));
      res.alturaFilas = filas.map(tr => +tr.getBoundingClientRect().height.toFixed(1));
      res.alturaTabla = +document.querySelector('table').getBoundingClientRect().height.toFixed(1);
      // celda de documentos y de comercial
      const celdas = filas.map(tr => tr.querySelector('td[data-et="Documentos fiscales"]'));
      res.documentos = celdas.map(td => ({ pill: (td.querySelector('.pill') || {}).textContent || '', chars: td.textContent.trim().replace(/\s+/g, ' ').length,
                                          lineas: Math.round(td.getBoundingClientRect().height / 17), alto: +td.getBoundingClientRect().height.toFixed(1),
                                          recortada: td.scrollWidth > td.clientWidth + 1 }));
      res.comercial = filas.map(tr => ((tr.querySelector('td[data-et="Comercial"] .pill') || {}).textContent || '').trim());
      res.sucursalesPill = filas.map(tr => ((tr.querySelector('td[data-et="Sucursales"] .pill') || {}).textContent || '').trim()).filter(Boolean);
      // vocabulario de estados que ve una persona al recorrer la tabla (etiquetas de pill distintas)
      const set = new Set(); document.querySelectorAll('tbody td .pill').forEach(p => { if (!p.closest('.hijas')) set.add(p.textContent.trim()); });
      res.etiquetasDistintas = Array.from(set);
      // chips de resumen
      res.chips = Array.from(document.querySelectorAll('.schip')).map(c => ({ txt: c.textContent.trim().replace(/\s+/g, ' '), cls: c.className.split(/\s+/).filter(x => /^c-/.test(x))[0] }));
      res.notasAlPie = Array.from(document.querySelectorAll('.pad > p.nota, .state-ok .pad > p.nota')).map(n => n.textContent.trim().replace(/\s+/g, ' ').length);
      // calidad sobre las celdas de estado (tbody) y los chips
      const tb = document.querySelector('tbody');
      const pills = Array.from(tb.querySelectorAll('.pill')).filter(p => M.vis(p) && !p.closest('.hijas'));
      res.pills = pills.map(p => { const c = M.contraste(p); return { txt: p.textContent.trim(), clase: p.className.split(/\s+/).filter(x => /^p-/.test(x))[0], ratio: c.minimo, px: parseFloat(getComputedStyle(p).fontSize), alto: +p.getBoundingClientRect().height.toFixed(1) }; });
      const filasEstado = Array.from(document.querySelectorAll('td[data-et="Documentos fiscales"], td[data-et="Comercial"]')).filter(M.vis);
      res.contrasteCeldas = filasEstado.map(td => { const c = M.contraste(td); return { min: c.minimo, fallos: c.fallos.length }; });
      res.contrasteChips = Array.from(document.querySelectorAll('.schip')).map(c => M.contraste(c).minimo);
      res.fuentesTabla = M.fuentes(document.querySelector('table'));
      res.fuentesChips = M.fuentes(document.querySelector('.p4-f'));
      res.destinosTabla = (() => { const d = M.destinos(document.querySelector('table')); return { total: d.total, bajo24: d.bajo24, detalle: d.detalle }; })();
      res.cabeceraDocs = (() => { const th = Array.from(document.querySelectorAll('thead th')).find(x => /Documentos fiscales/i.test(x.textContent)); const r = th.getBoundingClientRect(); return { alto: +r.height.toFixed(1), ancho: +r.width.toFixed(1), tieneInfob: !!th.querySelector('.infob') }; })();
      const caja = document.querySelector('.tabla-caja');
      res.scroll = { scrollW: caja.scrollWidth, clientW: caja.clientWidth, horizontal: caja.scrollWidth > caja.clientWidth + 1, docScrollH: document.documentElement.scrollWidth > innerWidth };
      return res;
    });
    // toggletip de la cabecera: abre, mide, Escape devuelve el foco
    r.toggletips = await page.evaluate(() => {
      const M = window.__M; const res = [];
      for (const bt of Array.from(document.querySelectorAll('.infob')).filter(M.vis)) {
        bt.scrollIntoView({ block: 'center', inline: 'center' }); bt.focus(); bt.click();
        const t = document.getElementById(bt.getAttribute('aria-controls')); const rt = t.getBoundingClientRect();
        const c = M.contraste(t);
        const f = { nombre: bt.getAttribute('aria-label'), caja: M.caja(bt), chars: t.textContent.length, abierto: bt.getAttribute('aria-expanded') === 'true' && !t.hidden,
                    describedby: bt.getAttribute('aria-describedby') === t.id, globo: M.caja(t), dentroHorizontal: rt.left >= 0 && rt.right <= innerWidth, contrasteGlobo: c.minimo, contrasteIcono: M.contrasteGrafico(bt) };
        bt.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
        f.cierraConEscape = bt.getAttribute('aria-expanded') === 'false' && t.hidden; f.focoVuelve = document.activeElement === bt;
        res.push(f);
      }
      return res;
    });
    out.medidas[`${w}x${h}-${tema}`] = r;
    if (tema === 'light') {
      await page.evaluate(() => { const m = document.getElementById('contenido'); m.scrollTop = 0; });
      const caja = await page.$('.tabla-caja');
      if (w >= 1024) await caja.screenshot({ path: path.join(CAPDIR, `27e-tabla-${etiqueta}--${w}.png`) });
      else { await page.evaluate(() => { document.querySelector('tbody tr').scrollIntoView({ block: 'start' }); }); await page.screenshot({ path: path.join(CAPDIR, `27e-tabla-${etiqueta}--${w}.png`) }); }
    }
    await ctx.close();
  }
  await b.close();
  const js = JSON.stringify(out, null, 1);
  if (salida) fs.writeFileSync(salida, js); else console.log(js);
})();
