// I3b: recorte horizontal a distintos anchos de ventana (tablas con scroll oculto, columnas finales cortadas, desborde de página).
const { chromium } = require('playwright'); const fs = require('fs');
const M = process.env.MDIR, PORT = process.env.PORT || '8732', OUT = process.env.OUT;
const names = fs.readdirSync(M).filter(n => n.endsWith('.html') && !n.startsWith('studio_')).sort();
const MED = () => {
  const nom = el => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const f = []; const W = document.documentElement.clientWidth;
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); if (!r.width || !r.height || /^(sr|visually)/.test(el.className || '')) continue;
    if (/auto|scroll|hidden|clip/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 120 && !['MAIN', 'BODY', 'HTML'].includes(el.tagName) && el.tagName !== 'CAPTION')
      f.push({ tipo: 'scroll-x', el: nom(el), oculto: !/auto|scroll/.test(cs.overflowX), dx: el.scrollWidth - el.clientWidth, ancho: el.clientWidth, tabla: !!el.querySelector('table') });
  }
  const desborde = Array.from(document.querySelectorAll('body *')).filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > W + 2 && getComputedStyle(e).position !== 'fixed' && !e.closest('[style*="overflow"],.scroll,.tabla-scroll'); }).length;
  return { W, scrollsHorizontales: f.slice(0, 8), n: f.length, scrollPagina: document.documentElement.scrollWidth - W, nodosFueraDelBorde: desborde };
};
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const w of [1440, 1280, 1024]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await require('./lib.cjs').preparar(p);
    for (const n of names) { try { await p.goto(`http://127.0.0.1:${PORT}/${n}`, { waitUntil: 'load', timeout: 30000 }); await p.waitForTimeout(250); (out[n.replace('.html', '')] ||= {})[w] = await p.evaluate(MED); } catch (e) { (out[n.replace('.html', '')] ||= {})[w] = { error: 1 }; } }
    await ctx.close(); process.stdout.write('|');
  }
  await b.close(); fs.writeFileSync(OUT + '/anchos.json', JSON.stringify(out, null, 1)); console.log('listo');
})();
