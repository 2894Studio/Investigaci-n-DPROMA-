// Orden de tabulación y foco visible en el prototipo B del Asistente (47). Solo lee.
const { chromium } = require('playwright');
const lib = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const URL = process.env.URL || 'http://127.0.0.1:8777/47-asistente-B-recomendado.html';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } }); await lib.preparar(p); await p.goto(URL);
  const paradas = [];
  for (let i = 0; i < 34; i++) {
    await p.keyboard.press('Tab');
    paradas.push(await p.evaluate(() => { const e = document.activeElement; const cs = getComputedStyle(e.closest('.search') && e.matches('input') ? e.closest('.search') : e);
      return { tag: e.tagName.toLowerCase() + (e.getAttribute('role') ? '[role=' + e.getAttribute('role') + ']' : ''), nombre: (e.getAttribute('aria-label') || e.textContent || e.placeholder || '').trim().slice(0, 34), contorno: (e.closest('.search') && e.matches('input') ? '(en .search) ' : '') + cs.outlineStyle + ' ' + cs.outlineWidth }; }));
  }
  paradas.forEach((s, i) => console.log(String(i + 1).padStart(2), s.tag.padEnd(16), s.contorno.padEnd(10), s.nombre));
  const sinContorno = paradas.filter(s => /none|\s0px$/.test(s.contorno.replace('(en .search) ','')));
  console.log('paradas sin contorno visible:', sinContorno.length, sinContorno.map(s => s.nombre));
  await b.close();
})();
