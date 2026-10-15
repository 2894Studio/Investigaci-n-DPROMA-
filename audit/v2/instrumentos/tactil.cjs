const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const SP = process.env.SP, M = process.env.MDIR;
const listar = (d, a = []) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name);
  if (e.isDirectory()) listar(p, a); else if (e.name.endsWith('.html') && e.name !== 'index.html' && !e.name.startsWith('studio_')) a.push(path.relative(M, p)); } return a; };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' })).newPage();
  await require('./lib.cjs').preparar(p);
  const out = {};
  for (const rel of listar(M).sort()) {
    const n = path.basename(rel, '.html');
    await p.goto('http://127.0.0.1:'+(process.env.PORT||'8732')+'/' + rel, { waitUntil: 'load', timeout: 30000 });
    await p.waitForTimeout(500);
    await p.addStyleTag({ content: '[data-andamio]{display:none !important}' });
    out[n] = await p.evaluate(() => {
      const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const it = Array.from(document.querySelectorAll('button, a[href], input, select, textarea, [role="button"], [tabindex]:not([tabindex="-1"])')).filter(vis);
      const bajo24 = it.map(el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return { tag: el.tagName.toLowerCase(), cls: (typeof el.className === 'string' ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''),
                 txt: (el.textContent || el.getAttribute('aria-label') || el.type || '').trim().slice(0,24),
                 w: +r.width.toFixed(1), h: +r.height.toFixed(1), tipo: el.type || '' }; })
        .filter(o => o.h < 24 || o.w < 24);
      return { total: it.length, bajo24: bajo24.length,
               checkbox: bajo24.filter(o => o.tipo === 'checkbox' || o.tipo === 'radio').length,
               muestra: bajo24.slice(0, 10),
               dataTacto: document.documentElement.getAttribute('data-tacto') || null,
               reglaTactoSinRoot: Array.from(document.styleSheets).flatMap(s => { try { return Array.from(s.cssRules) } catch { return [] } })
                 .filter(r => r.selectorText && /data-tacto/.test(r.selectorText) && !/^:root/.test(r.selectorText.trim())).length };
    });
    process.stdout.write('.');
  }
  await b.close();
  fs.writeFileSync((process.env.OUT||SP) + '/tactil.json', JSON.stringify(out, null, 1));
  console.log('\nlisto');
})();
