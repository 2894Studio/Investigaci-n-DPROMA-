// Estrés: (1) cabecera sticky con N instaladores; (2) vista de día con N columnas de persona.
const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const P = 'http://127.0.0.1:8764/';
const casos = [
  { id: 'A', url: 'http://127.0.0.1:8732/34_instaladores.html', tipo: 'tabla' },
  { id: 'Aprima', url: P + '34-A-prima-cambio-minimo.html', tipo: 'tabla' },
  { id: 'C', url: P + '34-C-propuesta-previa.html', tipo: 'tabla' },
  { id: 'B', url: P + '34-B-dia-proporcional-13-9.html', tipo: 'grid' },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const c of casos) {
    out[c.id] = { sticky: {}, dia: {} };
    for (const W of [1440, 1280]) {
      // ---- 1. sticky (semana)
      for (const N of [8, 20]) {
        const ctx = await b.newContext({ viewport: { width: W, height: 900 } });
        const page = await ctx.newPage(); await preparar(page);
        await page.goto(c.url); await page.waitForTimeout(250);
        const r = await page.evaluate((N) => {
          document.getElementById('ag').dataset.vista = 'semana';
          const ag = document.querySelector('.agenda'); const tb = ag.querySelector('tbody');
          const filas = [...tb.querySelectorAll('tr:not(.sin-asignar)')];
          let i = 0; while (tb.querySelectorAll('tr:not(.sin-asignar)').length < N) { tb.appendChild(filas[i % filas.length].cloneNode(true)); i++; }
          const anc = []; let e = ag; while (e) { const cs = getComputedStyle(e); if (/(auto|scroll)/.test(cs.overflowY) && e.scrollHeight > e.clientHeight + 1) anc.push(e); e = e.parentElement; }
          anc.forEach(a => a.scrollTop = 400);
          const th = ag.querySelector('thead th'); const t = th.getBoundingClientRect();
          const region = anc.length ? anc[0].getBoundingClientRect() : { top: 0 };
          return { filas: tb.querySelectorAll('tr').length, scrollAncestros: anc.map(a => a.className || a.tagName), theadTop: Math.round(t.top), topRegionQueDesplaza: Math.round(region.top), fijada: Math.abs(t.top - region.top) < 3, alturaTabla: Math.round(ag.querySelector('table').getBoundingClientRect().height), alturaCaja: Math.round(ag.getBoundingClientRect().height) };
        }, N);
        out[c.id].sticky[W + '/' + N] = r; await ctx.close();
      }
      // ---- 2. día con N columnas
      for (const N of [4, 8, 20]) {
        const ctx = await b.newContext({ viewport: { width: W, height: 900 } });
        const page = await ctx.newPage(); await preparar(page);
        await page.goto(c.url); await page.waitForTimeout(250);
        const r = await page.evaluate(([N, tipo]) => {
          document.getElementById('ag').dataset.vista = 'dia';
          if (tipo === 'tabla') {
            const cont = document.querySelector('.dia-caja'); const tb = cont.querySelector('table');
            const ths = [...tb.querySelectorAll('thead th')]; const base = 1; // columna de J. Olvera (tiene bloque)
            const actual = ths.length - 1;
            for (let k = actual; k < N; k++) {
              tb.querySelector('thead tr').appendChild(ths[base].cloneNode(true));
              tb.querySelectorAll('tbody tr').forEach(tr => tr.appendChild(tr.children[base].cloneNode(true)));
            }
            const th2 = [...tb.querySelectorAll('thead th')]; const w = th2.slice(1).map(t => t.getBoundingClientRect().width);
            const bloques = [...cont.querySelectorAll('.bloque-cita')]; const bl = bloques.map(x => x.getBoundingClientRect());
            const trunc = [...cont.querySelectorAll('.bloque-cita b')].filter(x => x.scrollWidth > x.clientWidth + 1).length;
            return { columnas: th2.length - 1, anchoColumna: Math.round(Math.min(...w)), anchoMaxBloque: Math.round(Math.max(...bl.map(r => r.width))), altoMaxBloque: Math.round(Math.max(...bl.map(r => r.height))), scrollW: cont.scrollWidth, clientW: cont.clientWidth, desborda: cont.scrollWidth > cont.clientWidth + 1 };
          } else {
            const cont = document.getElementById('diab'); const malla = cont.querySelector('.malla');
            const cols = [...malla.querySelectorAll('.col')]; const cabs = [...malla.querySelectorAll('h3.cab')];
            for (let k = cols.length; k < N; k++) { const c1 = cols[0].cloneNode(true); const h = cabs[0].cloneNode(true); h.id = 'px' + k; c1.setAttribute('aria-labelledby', h.id); malla.appendChild(h); malla.appendChild(c1); }
            malla.style.setProperty('--cols', N);
            // Los h3 y ul se alternan por orden de fuente: reordenar para el grid de N columnas
            const nuevosH = [...malla.querySelectorAll('h3.cab')]; const nuevosC = [...malla.querySelectorAll('.col')];
            const eje = malla.querySelector('.eje'); const horaCab = malla.querySelector('div.cab');
            [horaCab, ...nuevosH, eje, ...nuevosC].forEach(n => malla.appendChild(n));
            const w = nuevosC.map(c => c.getBoundingClientRect().width); const bl = [...cont.querySelectorAll('.ev')].map(x => x.getBoundingClientRect());
            return { columnas: nuevosC.length, anchoColumna: Math.round(Math.min(...w)), anchoMaxBloque: Math.round(Math.max(...bl.map(r => r.width))), altoMaxBloque: Math.round(Math.max(...bl.map(r => r.height))), scrollW: cont.scrollWidth, clientW: cont.clientWidth, desborda: cont.scrollWidth > cont.clientWidth + 1 };
          }
        }, [N, c.tipo]);
        out[c.id].dia[W + '/' + N] = r; await ctx.close();
      }
    }
  }
  require('fs').writeFileSync('stress34.json', JSON.stringify(out, null, 1));
  await b.close();
})();
