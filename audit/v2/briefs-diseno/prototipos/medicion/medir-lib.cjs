// Funciones de medición compartidas por los tres prototipos.
// Solo lectura: se evalúan dentro de la página, no modifican nada.
// Uso: const M = require('./medir-lib.cjs'); await page.evaluate(M.inyectar);  // deja window.__M
//
// Contraste: mismo criterio que audit/v2/instrumentos/contraste.cjs (composición alfa real,
// fondo efectivo del ancestro, 4,5:1 texto normal, 3:1 grande o gráfico).

const inyectar = () => {
  const parse = c => {
    if (!c) return null;
    const srgb = c.match(/color\(\s*srgb\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)(?:\s*\/\s*([\d.eE+-]+))?/i);
    if (srgb) return { r: +srgb[1] * 255, g: +srgb[2] * 255, b: +srgb[3] * 255, a: srgb[4] === undefined ? 1 : +srgb[4] };
    const m = c.match(/[\d.]+/g); if (!m) return null;
    if (/^rgba?\(/i.test(c)) return { r: +m[0], g: +m[1], b: +m[2], a: m.length > 3 ? +m[3] : 1 };
    return null;
  };
  const over = (f, b) => ({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 });
  const fondoReal = el => {
    const capas = []; let n = el;
    while (n && n.nodeType === 1) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0) { capas.push(c); if (c.a === 1) break; }
      n = n.parentElement;
    }
    let base = capas.length && capas[capas.length - 1].a === 1 ? capas.pop() : { r: 255, g: 255, b: 255, a: 1 };
    for (let i = capas.length - 1; i >= 0; i--) base = over(capas[i], base);
    return base;
  };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'; };
  const caja = el => { const r = el.getBoundingClientRect(); return { x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), r: +r.right.toFixed(1), b: +r.bottom.toFixed(1) }; };

  // Contraste de todos los textos visibles dentro de `raiz` (o del documento).
  const contraste = (raiz) => {
    raiz = raiz || document.body;
    const nodos = [raiz, ...Array.from(raiz.querySelectorAll('*'))].filter(el => vis(el) && Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 0));
    const filas = [];
    for (const el of nodos) {
      const cs = getComputedStyle(el); const fg0 = parse(cs.color); if (!fg0) continue;
      const bg = fondoReal(el); const fg = fg0.a < 1 ? over(fg0, bg) : fg0;
      const px = parseFloat(cs.fontSize), peso = parseInt(cs.fontWeight) || 400;
      const grande = px >= 24 || (px >= 18.66 && peso >= 700);
      filas.push({ txt: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 40), px, peso, ratio: +ratio(fg, bg).toFixed(2), min: grande ? 3 : 4.5 });
    }
    const fallos = filas.filter(f => f.ratio < f.min - 0.005);
    return { nodos: filas.length, minimo: filas.length ? Math.min(...filas.map(f => f.ratio)) : null, fallos };
  };

  // Contraste de un icono/borde (gráfico, 3:1): color de `el` contra su fondo real.
  const contrasteGrafico = (el, prop) => {
    const cs = getComputedStyle(el); const fg0 = parse(prop === 'borde' ? cs.borderTopColor : cs.color);
    const bg = fondoReal(el.parentElement || el); const fg = fg0.a < 1 ? over(fg0, bg) : fg0;
    return +ratio(fg, bg).toFixed(2);
  };

  // Tamaño mínimo de fuente del texto visible dentro de `raiz` (§2.1: suelo 12 px).
  const fuentes = (raiz) => {
    raiz = raiz || document.body;
    const bajo = []; let n = 0;
    for (const el of [raiz, ...raiz.querySelectorAll('*')]) {
      if (!vis(el)) continue;
      if (!Array.from(el.childNodes).some(t => t.nodeType === 3 && t.textContent.trim().length > 0)) continue;
      n++; const px = parseFloat(getComputedStyle(el).fontSize);
      if (px < 12) bajo.push({ txt: el.textContent.trim().slice(0, 30), px, cls: (typeof el.className === 'string' ? el.className : '').split(/\s+/)[0] });
    }
    return { nodos: n, bajo12: bajo.length, muestra: bajo.slice(0, 8) };
  };

  // Destinos interactivos < 24×24 (WCAG 2.5.8 / §7.3). Una casilla/campo dentro de <label> cuenta por la etiqueta.
  const destinos = (raiz) => {
    raiz = raiz || document.body;
    const it = Array.from(raiz.querySelectorAll('button, a[href], input, select, textarea, [role="button"], [role="menuitem"], summary')).filter(vis);
    const filas = it.map(el => {
      let r = el.getBoundingClientRect();
      const lab = el.closest('label');
      if (lab) { const rl = lab.getBoundingClientRect(); r = rl; }
      return { tag: el.tagName.toLowerCase(), nombre: (el.getAttribute('aria-label') || el.textContent || el.type || '').trim().replace(/\s+/g, ' ').slice(0, 36), w: +r.width.toFixed(1), h: +r.height.toFixed(1) };
    });
    const bajo = filas.filter(f => f.w < 24 || f.h < 24);
    return { total: filas.length, bajo24: bajo.length, detalle: bajo.slice(0, 8), min: filas.length ? { w: Math.min(...filas.map(f => f.w)), h: Math.min(...filas.map(f => f.h)) } : null };
  };

  // Solapes entre cajas hermanas visibles dentro de `raiz` (intersección de área > 1 px²).
  const solapes = (raiz, sel) => {
    const els = Array.from((raiz || document.body).querySelectorAll(sel || ':scope > *')).filter(vis);
    const out = [];
    for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
      const a = els[i].getBoundingClientRect(), b = els[j].getBoundingClientRect();
      const w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (w > 0.5 && h > 0.5 && w * h > 1) out.push({ a: els[i].className || els[i].tagName, b: els[j].className || els[j].tagName, area: +(w * h).toFixed(1) });
    }
    return out;
  };

  // Recorte: hijos cuyo borde derecho excede al de `cont` (o cuyo scrollWidth > clientWidth).
  const recorte = (cont, margen) => {
    margen = margen === undefined ? 0.5 : margen;
    const rc = cont.getBoundingClientRect(); const fuera = [];
    for (const el of cont.querySelectorAll('*')) {
      if (!vis(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.right > rc.right + margen || r.left < rc.left - margen) fuera.push({ el: (el.className && typeof el.className === 'string' ? el.className.split(/\s+/)[0] : el.tagName), l: +r.left.toFixed(1), r: +r.right.toFixed(1) });
    }
    return { cont: { l: +rc.left.toFixed(1), r: +rc.right.toFixed(1), scrollW: cont.scrollWidth, clientW: cont.clientWidth }, fuera: fuera.slice(0, 8), nFuera: fuera.length };
  };

  window.__M = { parse, over, fondoReal, ratio, vis, caja, contraste, contrasteGrafico, fuentes, destinos, solapes, recorte };
};

module.exports = { inyectar };
