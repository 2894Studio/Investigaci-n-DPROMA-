// Recorta la parte alta del panel de detalle (y la cabecera) a cada ancho: antes (maqueta) y después (prototipo).
const { chromium } = require('playwright'); const path = require('path');
const CAP = path.join(__dirname, '..', 'capturas');
const U = { original: 'http://127.0.0.1:8732/24_tickets.html', prototipo: 'http://127.0.0.1:8740/24-tickets-zona-superior.html' };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, h] of [[1440, 800], [1280, 720], [1024, 768], [390, 844]]) for (const [et, url] of Object.entries(U)) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce', colorScheme: 'light', deviceScaleFactor: 1 });
    const p = await ctx.newPage(); await require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs').preparar(p);
    await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(150);
    // cabecera + parte alta del detalle en una sola imagen: se usa la página completa del contenedor .main
    const main = await p.$('.main');
    const bb = await main.boundingBox();
    if (w >= 1280) {
      const det = await p.$('.detalle'); const d = await det.boundingBox();
      await p.screenshot({ path: path.join(CAP, `24-zona-${et}--${w}.png`), clip: { x: bb.x, y: bb.y, width: bb.width, height: Math.min(420, h - bb.y) } });
    } else {
      // apilado: se lleva el detalle a la vista
      await p.evaluate(() => { const d = document.querySelector('.detalle'); d.scrollTop = Math.max(0, d.querySelector('.dh').offsetHeight - 160); });
      await p.waitForTimeout(100);
      await p.screenshot({ path: path.join(CAP, `24-zona-${et}--${w}.png`) });
    }
    await ctx.close();
  }
  await b.close(); console.log('ok');
})();
