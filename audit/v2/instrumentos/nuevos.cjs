// Instrumentos nuevos v2 (I1–I9 + C2/C11 + efecto de --sp-5). Solo lectura.
// Entorno: MDIR, PORT, OUT, REGLAS_PORT (servidor que sirve reglas.html 2.15.0 para resolver la paleta).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const SP = process.env.SP, M = process.env.MDIR, OUT = process.env.OUT || SP;
const PORT = process.env.PORT || '8732', RP = process.env.REGLAS_PORT || '8735';
const listar = d => fs.readdirSync(d).filter(n => n.endsWith('.html') && n !== 'index.html' && !n.startsWith('studio_')).sort();

const MEDIR = (PAL) => {
  const R = (n, d = 1) => +n.toFixed(d);
  const parse = c => {
    if (!c) return null;
    const s = c.match(/color\(\s*srgb\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)(?:\s*\/\s*([\d.eE+-]+))?/i);
    if (s) return { r: +s[1] * 255, g: +s[2] * 255, b: +s[3] * 255, a: s[4] === undefined ? 1 : +s[4] };
    const m = c.match(/[\d.]+/g); if (!m || !/^rgba?\(/i.test(c)) return null;
    return { r: +m[0], g: +m[1], b: +m[2], a: m.length > 3 ? +m[3] : 1 };
  };
  const over = (f, b) => ({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 });
  const fondo = el => { const capas = []; let n = el;
    while (n && n.nodeType === 1) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0) { capas.push(c); if (c.a === 1) break; } n = n.parentElement; }
    let base = capas.length && capas[capas.length - 1].a === 1 ? capas.pop() : { r: 255, g: 255, b: 255, a: 1 };
    for (let i = capas.length - 1; i >= 0; i--) base = over(capas[i], base); return base; };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
  const nombre = el => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const rect = el => el.getBoundingClientRect();
  // visible = con caja, no oculto y no totalmente recortado por un ancestro con overflow distinto de visible
  const visible = el => { const r = rect(el), cs = getComputedStyle(el);
    if (!(r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none')) return false;
    let a = el.parentElement, l = r.left, t = r.top, rr = r.right, bb = r.bottom;
    while (a && a !== document.body) { const c = getComputedStyle(a);
      if (c.overflowX !== 'visible' || c.overflowY !== 'visible') { const q = rect(a); l = Math.max(l, q.left); t = Math.max(t, q.top); rr = Math.min(rr, q.right); bb = Math.min(bb, q.bottom); if (rr <= l || bb <= t) return false; }
      a = a.parentElement; }
    return true; };
  // caja recortada por los ancestros con overflow (lo que de verdad se ve)
  const rv = el => { const r = rect(el); let l = r.left, t = r.top, rr = r.right, bb = r.bottom, a = el.parentElement;
    while (a && a !== document.body) { const c = getComputedStyle(a); if (c.overflowX !== 'visible' || c.overflowY !== 'visible') { const q = rect(a); l = Math.max(l, q.left); t = Math.max(t, q.top); rr = Math.min(rr, q.right); bb = Math.min(bb, q.bottom); } a = a.parentElement; }
    return { left: l, top: t, right: rr, bottom: bb, width: Math.max(0, rr - l), height: Math.max(0, bb - t) }; };
  const todos = Array.from(document.querySelectorAll('body *'));
  const vis = todos.filter(visible);
  const out = {};

  // ---------- I1: icono vs relleno del botón (incluye vistas de estado ocultas: el cálculo no necesita layout)
  {
    const f = [];
    for (const b of document.querySelectorAll('.btn, button, a.btn, [role=button]')) {
      for (const ic of b.querySelectorAll('svg, .ico, .msi')) {
        const cs = getComputedStyle(ic); const col = parse(cs.color); if (!col) continue;
        const bg = fondo(b); const fg = col.a < 1 ? over(col, bg) : col; const r = ratio(fg, bg);
        const txt = parse(getComputedStyle(b).color);
        if (r < 3) f.push({ boton: nombre(b), texto: (b.textContent || '').trim().slice(0, 24), colorIcono: cs.color, colorTexto: getComputedStyle(b).color, fondo: `rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})`, ratio: R(r, 2), enEstado: !!b.closest('.state, [class*=state]'), oculto: !visible(b) });
      }
    }
    out.I1_icono_vs_boton = { fallos: f.length, detalle: f.slice(0, 12) };
  }

  // ---------- I2: holgura entre el último control de una barra y su línea inferior
  {
    const f = [];
    for (const el of vis) {
      const cs = getComputedStyle(el); const bb = parseFloat(cs.borderBottomWidth);
      if (!(bb >= 1) || cs.borderBottomStyle === 'none') continue;
      const ctr = Array.from(el.querySelectorAll('button, .btn, input, select, .seg, .chip, a[href], [role=tab]')).filter(visible);
      if (!ctr.length) continue;
      const r = rect(el); const maxB = Math.max(...ctr.map(c => rect(c).bottom));
      const gap = r.bottom - bb - maxB;
      if (gap < 8 && r.height < 200) f.push({ barra: nombre(el), gap: R(gap), altoBarra: R(r.height), controles: ctr.length });
    }
    // variante: la línea es border-top del hermano siguiente
    for (const el of vis) {
      const sib = el.nextElementSibling; if (!sib || !visible(sib)) continue;
      const bt = parseFloat(getComputedStyle(sib).borderTopWidth); if (!(bt >= 1) || getComputedStyle(sib).borderTopStyle === 'none') continue;
      const ctr = Array.from(el.querySelectorAll('button, .btn, input, select, .seg, .chip, a[href], [role=tab]')).filter(visible); if (!ctr.length) continue;
      const gap = rect(sib).top - Math.max(...ctr.map(c => rect(c).bottom));
      if (gap < 8 && rect(el).height < 200) f.push({ barra: nombre(el) + ' → línea de ' + nombre(sib), gap: R(gap), controles: ctr.length });
    }
    out.I2_holgura_inferior = { fallos: f.length, detalle: f.slice(0, 12) };
  }

  // ---------- I3: recorte (overflow) e intersección fija/sticky con controles
  {
    const rec = [];
    for (const el of vis) {
      const cs = getComputedStyle(el); const ov = cs.overflowX + cs.overflowY;
      if (!/hidden|clip/.test(ov)) continue;
      const dx = el.scrollWidth - el.clientWidth, dy = el.scrollHeight - el.clientHeight;
      if ((dx > 1 || dy > 1) && (el.textContent || '').trim().length) rec.push({ el: nombre(el), dx, dy, texto: el.textContent.trim().slice(0, 30), ellipsis: cs.textOverflow === 'ellipsis' });
    }
    const fijos = vis.filter(e => /fixed|sticky/.test(getComputedStyle(e).position));
    const inter = [];
    const inters = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    for (const F of fijos) {
      const rf = rv(F);
      for (const I of vis.filter(e => e.matches('button, .btn, a[href], input, select') && !F.contains(e) && !e.contains(F))) {
        const ri = rv(I); const a = inters(rf, ri); const area = ri.width * ri.height;
        if (area && a / area > 0.2) inter.push({ fijo: nombre(F), posicion: getComputedStyle(F).position, control: nombre(I), texto: (I.textContent || '').trim().slice(0, 24), solape: R(a / area, 2) });
      }
    }
    out.I3_recorte = { recortados: rec.length, detalleRecorte: rec.slice(0, 12), interseccionFijos: inter.length, detalleInterseccion: inter.slice(0, 12), nFijos: fijos.length };
  }

  // ---------- I4: alineación cabecera / celda
  {
    const f = []; let tablas = 0;
    for (const t of document.querySelectorAll('table')) {
      if (!visible(t)) continue; tablas++;
      const ths = Array.from(t.querySelectorAll('thead th')); const tr = t.querySelector('tbody tr'); if (!ths.length || !tr) continue;
      const tds = Array.from(tr.children);
      ths.forEach((th, i) => { const td = tds[i]; if (!td || !visible(th) || !visible(td)) return;
        const rng = el => { const r = document.createRange(); r.selectNodeContents(el); const b = r.getBoundingClientRect(); return b.width ? b : rect(el); };
        const a = getComputedStyle(th).textAlign, b = getComputedStyle(td).textAlign;
        const lt = rng(th).left, ld = rng(td).left, rt = rng(th).right, rd = rng(td).right;
        const al = x => x === 'start' ? 'left' : x === 'end' ? 'right' : x;
        const dL = Math.abs(lt - ld), dR = Math.abs(rt - rd);
        const mismatch = al(a) !== al(b) || (Math.min(dL, dR) > 6);
        if (mismatch && (th.textContent || '').trim()) f.push({ col: i, cabecera: th.textContent.trim().slice(0, 18), alinCab: a, alinCel: b, dxIzq: R(dL), dxDer: R(dR) });
      });
    }
    out.I4_alineacion = { tablas, desalineadas: f.length, detalle: f.slice(0, 12) };
  }

  // ---------- I5: ritmo vertical y espaciado fuera de la escala --sp-*
  {
    const ESC = new Set([0, 1, 2, 4, 8, 12, 16, 20, 24, 32, 48]);
    const cont = {}; const lh = new Set(); const lhr = {};
    for (const el of vis) { const cs = getComputedStyle(el);
      for (const p of ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom', 'rowGap', 'columnGap']) { const v = parseFloat(cs[p]); if (!isNaN(v) && v > 0 && !ESC.has(Math.round(v * 10) / 10)) cont[R(v)] = (cont[R(v)] || 0) + 1; }
      if ((el.childNodes && Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 1))) {
        const fs = parseFloat(cs.fontSize), l = parseFloat(cs.lineHeight); if (!isNaN(l) && fs) { const k = R(l / fs, 2); lhr[k] = (lhr[k] || 0) + 1; } } }
    const fuera = Object.entries(cont).sort((a, b) => b[1] - a[1]);
    out.I5_ritmo = { valoresFueraDeEscala: fuera.length, ocurrenciasFueraDeEscala: fuera.reduce((s, x) => s + x[1], 0), top: fuera.slice(0, 8).map(([v, n]) => `${v}px×${n}`),
                     interlineadosDistintos: Object.keys(lhr).length, interlineados: Object.entries(lhr).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([v, n]) => `${v}×${n}`) };
  }

  // ---------- I6: presupuesto de color (familias semánticas visibles)
  {
    const fam = {}; const near = (c, hex) => { const p = parse(hex); return p && Math.abs(c.r - p.r) < 3 && Math.abs(c.g - p.g) < 3 && Math.abs(c.b - p.b) < 3; };
    const marca = (c) => { for (const [k, lista] of Object.entries(PAL)) if (lista.some(h => near(c, h))) return k; return null; };
    for (const el of vis) { const cs = getComputedStyle(el);
      for (const prop of ['backgroundColor', 'color', 'borderTopColor']) { const c = parse(cs[prop]); if (!c || c.a < 0.5) continue; const k = marca(c); if (k) { fam[k] = (fam[k] || 0) + 1; } } }
    const fam2 = Object.keys(fam).filter(k => !/^(neutro)$/.test(k));
    out.I6_color = { familiasVisibles: fam2.length, familias: fam };
  }

  // ---------- I7: colisión de texto con texto (hojas de texto que se solapan)
  {
    const hojas = vis.filter(e => Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 1) && !e.querySelector('*:not(svg):not(br):not(b):not(i):not(span):not(strong):not(em)'));
    const f = []; const inters = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    for (let i = 0; i < hojas.length && f.length < 40; i++) for (let j = i + 1; j < hojas.length; j++) {
      const a = hojas[i], b = hojas[j]; if (a.contains(b) || b.contains(a)) continue;
      const ra = rv(a), rb = rv(b); const x = inters(ra, rb); if (!x) continue;
      const mn = Math.min(ra.width * ra.height, rb.width * rb.height); if (mn && x / mn > 0.3) f.push({ a: nombre(a) + '«' + a.textContent.trim().slice(0, 14) + '»', b: nombre(b) + '«' + b.textContent.trim().slice(0, 14) + '»', solape: R(x / mn, 2) });
    }
    out.I7_colision_texto = { colisiones: f.length, detalle: f.slice(0, 10) };
  }

  // ---------- I8: paridad de botones hermanos
  {
    const f = [];
    const grupos = new Map();
    for (const b of vis.filter(e => e.matches('.btn, button.btn, a.btn'))) { const p = b.parentElement; if (!grupos.has(p)) grupos.set(p, []); grupos.get(p).push(b); }
    for (const [p, bs] of grupos) { if (bs.length < 2) continue;
      const alt = bs.map(b => R(rect(b).height)); const iconoPrim = bs.map(b => { const ic = b.querySelector('svg, .ico, .msi'); if (!ic) return 'sin'; return ic === b.firstElementChild ? 'izq' : 'der'; });
      const ancho = bs.map(b => R(rect(b).width));
      const dAlt = Math.max(...alt) - Math.min(...alt), pos = new Set(iconoPrim.filter(x => x !== 'sin'));
      if (dAlt > 1 || pos.size > 1 || (iconoPrim.includes('sin') && iconoPrim.some(x => x !== 'sin'))) f.push({ grupo: nombre(p), botones: bs.map(b => (b.textContent || '').trim().slice(0, 16)), alto: alt, ancho, icono: iconoPrim });
    }
    out.I8_paridad_botones = { gruposDispares: f.length, detalle: f.slice(0, 8) };
  }

  // ---------- I9: texto largo en celdas
  {
    const f = []; let celdas = 0;
    for (const td of document.querySelectorAll('tbody td')) { if (!visible(td)) continue; celdas++;
      const t = (td.innerText || '').trim(); const lh = parseFloat(getComputedStyle(td).lineHeight) || 18; const lineas = Math.round(rect(td).height / lh);
      if (t.length > 60 || lineas > 3) f.push({ celda: nombre(td), caracteres: t.length, lineas, texto: t.slice(0, 40) }); }
    f.sort((a, b) => b.caracteres - a.caracteres);
    out.I9_celdas = { celdas, largas: f.length, detalle: f.slice(0, 6) };
  }

  // ---------- C2: 10,5 px solo en rótulos en mayúsculas
  {
    const f = [];
    for (const el of vis) { const cs = getComputedStyle(el); if (cs.fontSize !== '10.5px') continue;
      const t = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim(); if (t.length < 2) continue;
      const mayus = cs.textTransform === 'uppercase' || t === t.toUpperCase();
      if (!mayus) f.push({ el: nombre(el), texto: t.slice(0, 24) }); }
    out.C2_105_no_mayusculas = { fallos: f.length, detalle: f.slice(0, 8) };
  }

  // ---------- C11: .nota / .banda ≤ 140 caracteres
  {
    const f = []; let n = 0;
    for (const el of document.querySelectorAll('.nota, .banda, [class*="banda"]')) { n++; const t = (el.textContent || '').trim().replace(/\s+/g, ' '); if (t.length > 140) f.push({ el: nombre(el), caracteres: t.length, oculto: !visible(el), texto: t.slice(0, 50) }); }
    out.C11_texto_largo = { revisados: n, sobre140: f.length, detalle: f.slice(0, 8) };
  }

  // ---------- efecto de --sp-5 sin declarar
  {
    const decl = getComputedStyle(document.documentElement).getPropertyValue('--sp-5').trim();
    const sels = [];
    for (const sh of document.styleSheets) { let reglas; try { reglas = Array.from(sh.cssRules); } catch { continue; }
      const rec = rs => { for (const r of rs) { if (r.cssRules && !r.selectorText) { rec(Array.from(r.cssRules)); continue; } if (r.style && /var\(\s*--sp-5/.test(r.cssText) && r.selectorText) sels.push(r.selectorText); } };
      rec(reglas); }
    let afectados = 0; const ej = [];
    if (!decl) for (const s of sels) { let els = []; try { els = Array.from(document.querySelectorAll(s)); } catch { } afectados += els.length;
      if (els[0] && ej.length < 5) { const cs = getComputedStyle(els[0]); ej.push({ selector: s.slice(0, 50), padding: cs.padding, gap: cs.gap, margin: cs.margin }); } }
    out.SP5 = { declarado: decl || null, reglasQueLoUsan: sels.length, elementosAfectados: afectados, ejemplos: ej };
  }

  out.meta = { nodosVisibles: vis.length, alto: document.documentElement.scrollHeight };
  return out;
};

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage(); await require('./lib.cjs').preparar(p);
  // paleta canónica 2.15.0, resuelta desde la página de reglas (claro)
  const pr = await ctx.newPage(); await pr.goto(`http://127.0.0.1:${RP}/reglas.html`, { waitUntil: 'load' });
  const PAL = await pr.evaluate(() => { const cs = getComputedStyle(document.documentElement); const g = n => { const v = cs.getPropertyValue(n).trim(); return v; };
    const probe = document.createElement('i'); document.body.appendChild(probe);
    const rgb = n => { const v = g('--' + n); if (!v) return null; probe.style.color = ''; probe.style.color = v; return getComputedStyle(probe).color; };
    const out = {}; for (const f of ['ok', 'warn', 'err', 'block', 'pause']) out[f] = [f, f + '-bg', f + '-ink'].map(rgb).filter(Boolean);
    out.acento = ['accent', 'accent-ink'].map(rgb).filter(Boolean); out.serie = [1, 2, 3, 4].map(i => rgb('serie-' + i)).filter(Boolean); return out; });
  await pr.close();
  const res = { _paleta: PAL };
  for (const n of listar(M)) {
    try {
      await p.goto(`http://127.0.0.1:${PORT}/${n}`, { waitUntil: 'load', timeout: 30000 }); await p.waitForTimeout(400);
      res[n.replace('.html', '')] = await p.evaluate(MEDIR, PAL);
    } catch (e) { res[n.replace('.html', '')] = { error: String(e.message).slice(0, 80) }; }
    process.stdout.write('.');
  }
  await b.close();
  fs.writeFileSync(OUT + '/nuevos.json', JSON.stringify(res, null, 1));
  console.log('\nlisto');
})();
