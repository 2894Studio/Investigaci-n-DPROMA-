const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const SP = process.env.SP, M = SP + '/maquetas/maquetas-SIO-por-funcionalidad-2026-09-30';
const listar = (d, a = []) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name);
  if (e.isDirectory()) listar(p, a); else if (e.name.endsWith('.html') && e.name !== 'index.html' && !e.name.startsWith('studio_')) a.push(path.relative(M, p)); } return a; };

const MEDIR = () => {
  const parse = c => {
    if (!c) return null;
    // color(srgb 0.9 0.88 0.93 / 0.5)  -> componentes 0..1
    const srgb = c.match(/color\(\s*srgb\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)(?:\s*\/\s*([\d.eE+-]+))?/i);
    if (srgb) return { r: +srgb[1]*255, g: +srgb[2]*255, b: +srgb[3]*255, a: srgb[4] === undefined ? 1 : +srgb[4] };
    const m = c.match(/[\d.]+/g); if (!m) return null;
    if (/^rgba?\(/i.test(c)) return { r: +m[0], g: +m[1], b: +m[2], a: m.length > 3 ? +m[3] : 1 };
    return null;   // formato no reconocido: NO adivinar
  };
  // composicion alfa real: capa sobre capa hasta llegar a opaco
  const over = (f, b) => ({ r: f.r*f.a + b.r*(1-f.a), g: f.g*f.a + b.g*(1-f.a), b: f.b*f.a + b.b*(1-f.a), a: 1 });
  const fondoReal = el => {
    const capas = [];
    let n = el;
    while (n && n.nodeType === 1) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0) { capas.push(c); if (c.a === 1) break; }
      n = n.parentElement;
    }
    let base = capas.length && capas[capas.length-1].a === 1 ? capas.pop() : { r:255, g:255, b:255, a:1 };
    for (let i = capas.length - 1; i >= 0; i--) base = over(capas[i], base);
    return base;
  };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); };
    return .2126*f(c.r) + .7152*f(c.g) + .0722*f(c.b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x+.05)/(y+.05); };

  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0'; };
  const nodos = Array.from(document.querySelectorAll('*')).filter(el =>
    vis(el) && Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 1));

  const fallos = [];
  for (const el of nodos) {
    const cs = getComputedStyle(el);
    const fg0 = parse(cs.color); if (!fg0) continue;
    const bg = fondoReal(el);
    const fg = fg0.a < 1 ? over(fg0, bg) : fg0;          // el texto tambien puede ser translucido
    const px = parseFloat(cs.fontSize), peso = parseInt(cs.fontWeight) || 400;
    const grande = px >= 24 || (px >= 18.66 && peso >= 700);
    const min = grande ? 3 : 4.5;
    const r = ratio(fg, bg);
    if (r < min - 0.005) fallos.push({
      sel: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/)[0] : ''),
      txt: el.textContent.trim().slice(0, 32), color: cs.color,
      fondo: `rgb(${Math.round(bg.r)}, ${Math.round(bg.g)}, ${Math.round(bg.b)})`,
      px, peso, ratio: +r.toFixed(2), min });
  }
  const seen = new Set(), ded = [];
  for (const f of fallos) { const k = f.sel + '|' + f.color + '|' + f.fondo + '|' + f.px;
    if (!seen.has(k)) { seen.add(k); ded.push(f); } }
  ded.sort((a, b) => a.ratio - b.ratio);
  return { nodosTexto: nodos.length, fallos: ded.length, detalle: ded.slice(0, 15) };
};

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' })).newPage();
  const out = {};
  for (const rel of listar(M).sort()) {
    const n = path.basename(rel, '.html');
    await p.goto('http://127.0.0.1:8731/' + rel, { waitUntil: 'load', timeout: 30000 });
    await p.waitForTimeout(450);
    await p.addStyleTag({ content: '[data-andamio]{display:none !important}' });
    out[n] = { claro: await p.evaluate(MEDIR) };
    const tema = await p.$('#tema');
    if (tema) { await p.evaluate(e => e.click(), tema); await p.waitForTimeout(400); out[n].oscuro = await p.evaluate(MEDIR); }
    process.stdout.write('.');
  }
  await b.close();
  fs.writeFileSync(SP + '/contraste.json', JSON.stringify(out, null, 1));
  console.log('\nlisto');
})();
