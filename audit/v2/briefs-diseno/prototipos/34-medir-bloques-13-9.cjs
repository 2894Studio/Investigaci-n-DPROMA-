const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const BASE = 'http://127.0.0.1:8764/34-B-dia-proporcional-13-9.html';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const [nombre, q] of [['con_plan', '?estres=1'], ['sin_plan', '?estres=1&sinplan=1'], ['datos_reales', '']]) {
    for (const W of [1440, 1024]) {
      const ctx = await b.newContext({ viewport: { width: W, height: 900 } });
      const page = await ctx.newPage(); await preparar(page);
      await page.goto(BASE + q); await page.waitForTimeout(300);
      await page.evaluate(() => { document.getElementById('ag').dataset.vista = 'dia'; });
      await page.waitForTimeout(200);
      const r = await page.evaluate(() => {
        const res = [];
        document.querySelectorAll('#diab .ev').forEach(ev => {
          const eb = ev.getBoundingClientRect();
          const hijos = [...ev.children].filter(c => !c.hidden && getComputedStyle(c).display !== 'none');
          const info = hijos.map(c => { const r = c.getBoundingClientRect(); const lh = parseFloat(getComputedStyle(c).lineHeight);
            return { cls: c.className, top: r.top, bottom: r.bottom, h: r.height, lh, comprimida: r.height < lh - 0.5, desbordaPropio: c.scrollHeight > c.clientHeight + 1 }; });
          let solapes = 0, cortadas = 0;
          for (let i = 0; i < info.length; i++) {
            if (info[i].bottom > eb.bottom + 0.5 || info[i].top < eb.top - 0.5) cortadas++;
            for (let j = i + 1; j < info.length; j++) if (Math.min(info[i].bottom, info[j].bottom) - Math.max(info[i].top, info[j].top) > 1) solapes++;
          }
          res.push({ dur: +ev.dataset.dur, alto: Math.round(eb.height * 10) / 10, lineas: info.map(i => i.cls), comprimidas: info.filter(i => i.comprimida).length, desbordan: info.filter(i => i.desbordaPropio).length, solapes, cortadas,
                     aria: ev.getAttribute('aria-label') });
        });
        return res.sort((a, b) => a.dur - b.dur);
      });
      out[nombre + '@' + W] = r;
      await ctx.close();
    }
  }
  require('fs').writeFileSync('bloques139.json', JSON.stringify(out, null, 1));
  await b.close();
})();
