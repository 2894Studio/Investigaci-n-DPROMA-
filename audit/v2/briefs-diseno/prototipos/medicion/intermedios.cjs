// Anchos intermedios (entre los cuatro de referencia): sin recorte ni solape en la zona rediseñada.
const { chromium } = require('playwright'); const M = require('./medir-lib.cjs');
const fs = require('fs');
const ANCHOS = [[1101, 800], [1200, 800], [1100, 800], [900, 800], [861, 800], [760, 800], [560, 800]];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const [pant, url] of [['24', 'http://127.0.0.1:8740/24-tickets-zona-superior.html'], ['27a', 'http://127.0.0.1:8740/27-acordeon-sucursales.html'], ['27e', 'http://127.0.0.1:8740/27-etiquetas-de-estado.html']]) {
    out[pant] = {};
    for (const [w, h] of ANCHOS) {
      const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
      const page = await ctx.newPage(); await require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs').preparar(page);
      await page.goto(url, { waitUntil: 'load' }); await page.evaluate(M.inyectar);
      if (pant === '27a') await page.evaluate(() => document.querySelectorAll('.suc-btn[aria-controls]').forEach(bt => { const d = document.getElementById(bt.getAttribute('aria-controls')); if (d.hidden) bt.click(); }));
      await page.waitForTimeout(100);
      out[pant][w] = await page.evaluate((pant) => {
        const M = window.__M; const r = { docScrollH: document.documentElement.scrollWidth > innerWidth };
        if (pant === '24') {
          const det = document.querySelector('.detalle'); const zona = [document.querySelector('.dh'), document.querySelector('.resumen-ticket')];
          r.recorte = zona.map(z => M.recorte(z).nFuera); r.solapes = zona.map(z => M.solapes(z, ':scope > *').length);
          const rt = document.querySelector('.resumen-ticket'); r.columnas = getComputedStyle(rt).gridTemplateColumns;
          const c = document.querySelector('.campos').getBoundingClientRect(); r.campos = { x: +c.left.toFixed(0), w: +c.width.toFixed(0), h: +c.height.toFixed(0) };
          const cab = document.querySelector('.p4'); const ctrls = Array.from(cab.querySelectorAll('.seg,.btn')); const rc = cab.getBoundingClientRect();
          r.cabecera = { holguraInferior: +(rc.bottom - 1 - Math.max(...ctrls.map(e => e.getBoundingClientRect().bottom))).toFixed(1), recorte: M.recorte(cab).nFuera };
        } else if (pant === '27a') {
          const caja = document.querySelector('.tabla-caja'); const rc = caja.getBoundingClientRect();
          r.paneles = Array.from(document.querySelectorAll('tr.hijas')).filter(M.vis).map(p => ({ id: p.id, botonesFuera: Array.from(p.querySelectorAll('button')).filter(e => e.getBoundingClientRect().right > rc.right + 0.5).length, fuera: Array.from(p.querySelectorAll('li, li *')).filter(e => e.getBoundingClientRect().right > rc.right + 0.5).length }));
        } else {
          const filas = Array.from(document.querySelectorAll('tbody tr')).filter(tr => !tr.classList.contains('hijas'));
          r.celdasRecortadas = Array.from(document.querySelectorAll('td[data-et="Documentos fiscales"]')).filter(td => td.scrollWidth > td.clientWidth + 1).length;
          r.alturas = filas.map(tr => Math.round(tr.getBoundingClientRect().height));
          const caja = document.querySelector('.tabla-caja'); r.scroll = { sw: caja.scrollWidth, cw: caja.clientWidth };
        }
        return r;
      }, pant);
      await ctx.close();
    }
  }
  await b.close();
  fs.writeFileSync(__dirname + '/intermedios.json', JSON.stringify(out, null, 1)); console.log(JSON.stringify(out));
})();
