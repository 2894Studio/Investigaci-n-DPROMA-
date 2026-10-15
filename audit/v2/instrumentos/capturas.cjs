// Capturas de las pantallas auditadas a fondo (fuentes reales inyectadas, andamiaje oculto). Uso: MDIR PORT OUT NOMBRES="a,b,c"
const { chromium } = require('playwright'); const fs = require('fs');
const M = process.env.MDIR, PORT = process.env.PORT, OUT = process.env.OUT; fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, sufijo, full] of [[1440, '1440', true], [1280, '1280-fold', false]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await require('./lib.cjs').preparar(p);
    for (const n of process.env.NOMBRES.split(',')) { await p.goto(`http://127.0.0.1:${PORT}/${n}.html`, { waitUntil: 'load' }); await p.waitForTimeout(500);
      if (full) { const H = await p.evaluate(() => Math.max(...Array.from(document.querySelectorAll('*')).map(e => e.scrollHeight), document.documentElement.scrollHeight)); await p.setViewportSize({ width: w, height: Math.min(Math.max(H, 800), 5000) }); await p.waitForTimeout(250); }
      await p.screenshot({ path: `${OUT}/${n}--${sufijo}.png` }); if (full) await p.setViewportSize({ width: w, height: 800 }); }
    await ctx.close();
  }
  await b.close(); console.log('capturas ok');
})();
