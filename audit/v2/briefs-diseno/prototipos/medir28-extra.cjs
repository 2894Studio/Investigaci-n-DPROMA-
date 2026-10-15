// Medidas auxiliares citadas en el brief de Mi día (28): alturas de bloques a 390/1440 y holgura de las .gordo a 320/360. Solo lee.
const { chromium } = require('playwright');
const lib = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const ORIG = process.env.ORIG || 'http://127.0.0.1:8732/28_instalador_mi_dia.html';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const W of [390, 1440]) {
    const p = await b.newPage({ viewport: { width: W, height: W == 390 ? 844 : 900 } }); await lib.preparar(p); await p.goto(ORIG);
    console.log('bloques', W, JSON.stringify(await p.evaluate(() => { const h = e => +e.getBoundingClientRect().height.toFixed(1); const t = [...document.querySelectorAll('.tel > article')];
      return { senal: h(document.querySelector('.senal')), fechaCard: h(t[0]), cita1: h(t[1]), cita2: h(t[2]), llevas: h(t[3]), pie: h(document.querySelector('.pie-accion')), cromoTop: h(document.querySelector('.cromo-top')), p4: h(document.querySelector('.p4')),
        citasTexto: [...document.querySelectorAll('.p4 .resumen, .tarjeta-tel .n')].map(e => e.textContent.trim().slice(0, 40)) }; })));
    await p.close();
  }
  for (const W of [320, 360]) {
    const p = await b.newPage({ viewport: { width: W, height: 640 } }); await lib.preparar(p); await p.goto(ORIG);
    console.log('gordo', W, JSON.stringify(await p.evaluate(() => { const out = []; document.querySelectorAll('.gordo').forEach(g => { const rg = document.createRange(); rg.selectNodeContents(g); const t = rg.getBoundingClientRect(), gr = g.getBoundingClientRect();
      out.push({ holguraL: +(t.left - gr.left).toFixed(1), holguraR: +(gr.right - t.right).toFixed(1), recorta: g.scrollWidth > g.clientWidth + 1 }); });
      return { n: out.length, minHolgura: Math.min(...out.map(o => Math.min(o.holguraL, o.holguraR))), recortes: out.filter(o => o.recorta).length, scrollH: document.documentElement.scrollWidth > innerWidth + 1 }; })));
    await p.close();
  }
  await b.close();
})();
