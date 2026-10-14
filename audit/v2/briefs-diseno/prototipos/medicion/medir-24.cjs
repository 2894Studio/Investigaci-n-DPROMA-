// Medición de la zona superior de Tickets TI (cabecera .p4 + parte alta del detalle).
// Uso (desde el scratchpad, con el servidor de la maqueta en 8732 y/o el de prototipos en 8740):
//   NODE_PATH=/opt/node22/lib/node_modules /opt/node22/bin/node medir-24.cjs <url> <etiqueta> [salida.json] [capturas=1]
// Mide a 1440×800, 1280×720, 1024×768 y 390×844, en tema claro y oscuro, y (si existe) en modo «antigüedad».
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const M = require('./medir-lib.cjs');
const url = process.argv[2], etiqueta = process.argv[3] || 'x', salida = process.argv[4], capt = process.argv[5] === '1';
const VP = [[1440, 800], [1280, 720], [1024, 768], [390, 844]];
const CAPDIR = path.join(__dirname, '..', 'capturas');

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = { url, etiqueta, fecha: new Date().toISOString(), medidas: {} };
  for (const [w, h] of VP) for (const tema of ['light', 'dark']) for (const modo of ['plazo', 'antiguedad']) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce', colorScheme: tema });
    const page = await ctx.newPage();
    await require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs').preparar(page);
    await page.goto(url, { waitUntil: 'load' });
    await page.evaluate(M.inyectar);
    await page.evaluate((t) => document.documentElement.setAttribute('data-theme', t), tema);
    const tieneModo = await page.evaluate(() => !!document.querySelector('.plazo-ind'));
    if (modo === 'antiguedad' && !tieneModo) { await ctx.close(); continue; }
    if (modo === 'antiguedad') await page.evaluate(() => document.documentElement.setAttribute('data-plazo', 'no'));
    await page.waitForTimeout(150);
    const r = await page.evaluate(() => {
      const $ = s => document.querySelector(s), M = window.__M;
      const res = {};
      // --- cabecera .p4
      const p4 = $('.p4'), p4t = $('.p4-t');
      const ctrls = Array.from(p4t.querySelectorAll('h1, .resumen, .seg, .btn')).filter(M.vis);
      const rp = p4.getBoundingClientRect();
      const abajo = Math.max(...ctrls.map(e => e.getBoundingClientRect().bottom));
      const arriba = Math.min(...ctrls.map(e => e.getBoundingClientRect().top));
      const cs = getComputedStyle(p4);
      res.cabecera = {
        alto: +rp.height.toFixed(1), paddingBottom: cs.paddingBottom, bordeInferior: cs.borderBottomWidth,
        holguraInferior: +(rp.bottom - parseFloat(cs.borderBottomWidth) - abajo).toFixed(1),   // control más bajo → borde (sin contar la línea)
        holguraSuperior: +(arriba - rp.top).toFixed(1),
        controles: ctrls.map(e => ({ c: (e.className || e.tagName).toString().split(/\s+/)[0], ...M.caja(e) })),
        scrollHorizontal: p4t.scrollWidth > p4t.clientWidth
      };
      // --- detalle: cajas de arriba
      const det = $('.detalle'), cuerpo = $('.det-cuerpo'), dh = $('.dh');
      const caja = $('.caja-plazo') || Array.from(document.querySelectorAll('.plazo-ind')).find(M.vis);
      const bandas = Array.from(det.querySelectorAll('.banda')).filter(M.vis);
      const campos = $('.campos');
      const rd = det.getBoundingClientRect();
      res.detalle = { caja: M.caja(det), dh: M.caja(dh), cuerpo: M.caja(cuerpo), scrollW: det.scrollWidth, clientW: det.clientWidth };
      res.plazo = caja ? { clase: caja.className, ...M.caja(caja), izqRelPanel: +(caja.getBoundingClientRect().left - rd.left).toFixed(1), derRelPanel: +(rd.right - caja.getBoundingClientRect().right).toFixed(1) } : null;
      res.bandas = bandas.map(bn => ({ clase: bn.className, ...M.caja(bn), izqRelPanel: +(bn.getBoundingClientRect().left - rd.left).toFixed(1), derRelPanel: +(rd.right - bn.getBoundingClientRect().right).toFixed(1), chars: bn.textContent.trim().replace(/\s+/g, ' ').length }));
      res.campos = campos ? M.caja(campos) : null;
      // bordes compartidos y separación entre las cajas apiladas
      const bloques = [caja, ...bandas].filter(Boolean).sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
      if (bloques.length >= 2) {
        const a = bloques[0].getBoundingClientRect(), c = bloques[1].getBoundingClientRect();
        res.entreCajas = { difIzq: +(c.left - a.left).toFixed(1), difDer: +(a.right - c.right).toFixed(1), separacionVertical: +(c.top - a.bottom).toFixed(1) };
      }
      // alineación: bordes izquierdo y derecho de los bloques apilados del panel (dispersión = máx − mín)
      const apilados = [dh.querySelector('.meta-l'), dh.querySelector('h2'), dh.querySelector('.acciones'), ...bandas, document.querySelector('.resumen-ticket') || caja, document.querySelector('.descrip')].filter(Boolean).filter(M.vis);
      const izqs = apilados.map(e => e.getBoundingClientRect().left), ders = apilados.map(e => e.getBoundingClientRect().right);
      res.alineacion = { bloques: apilados.length, dispersionIzq: +(Math.max(...izqs) - Math.min(...izqs)).toFixed(1), dispersionDerBandaYDescrip: (() => { const a = [...bandas, document.querySelector('.descrip')].filter(Boolean).map(e => e.getBoundingClientRect().right); return +(Math.max(...a) - Math.min(...a)).toFixed(1); })() };
      // texto visible antes del primer campo de datos (Reporta/Atiende/Abierto)
      const walker = []; let chars = 0;
      const antes = Array.from(cuerpo.children).filter(e => !e.contains(campos) && e !== campos);
      const primerCampo = campos ? campos.getBoundingClientRect().top : null;
      const zonaEls = [caja, ...bandas].filter(Boolean);
      chars = zonaEls.reduce((s, e) => s + e.textContent.trim().replace(/\s+/g, ' ').length, 0);
      res.caracteresEnCajas = chars;
      res.primerCampoY = primerCampo === null ? null : +(primerCampo - rd.top).toFixed(1);
      // cuántos elementos de la zona alta llevan el fondo ámbar (--warn-bg)
      const probe = document.createElement('i'); probe.style.background = 'var(--warn-bg)'; document.body.appendChild(probe);
      const warn = getComputedStyle(probe).backgroundColor; probe.remove();
      const zona = [dh, ...Array.from(cuerpo.children).slice(0, 3)];
      let n = 0; const quienes = [];
      for (const z of zona) for (const e of [z, ...z.querySelectorAll('*')]) if (M.vis(e) && getComputedStyle(e).backgroundColor === warn) { n++; quienes.push((e.className || e.tagName).toString().split(/\s+/)[0]); }
      res.ambarEnZonaAlta = { n, quienes };
      // repetición del plazo dentro del panel de detalle
      const t = det.textContent;   // textContent: no depende de text-transform ni de lo visible
      res.repeticiones = { vence24ago: (t.match(/24 ago/gi) || []).length, venceHoy: (t.match(/Vence hoy/gi) || []).length, unDiaHabil: (t.match(/1 día hábil/gi) || []).length };
      // calidad: contraste, fuentes, destinos, solapes, recorte
      const zonaRaiz = document.createElement('div'); // medimos sobre dh + cajas + campos, no sobre toda la bitácora
      res.contraste = { dh: M.contraste(dh), cajas: zonaEls.map(e => ({ el: (e.className || '').toString().split(/\s+/)[0], ...(() => { const c = M.contraste(e); return { nodos: c.nodos, min: c.minimo, fallos: c.fallos.length }; })() })) };
      res.contrasteCabecera = M.contraste(p4);
      res.fuentes = { cabecera: M.fuentes(p4), dh: M.fuentes(dh), cajas: zonaEls.map(e => M.fuentes(e).bajo12).reduce((a, b2) => a + b2, 0) };
      res.destinos = { cabecera: M.destinos(p4), dh: M.destinos(dh), cajas: zonaEls.map(e => M.destinos(e).bajo24).reduce((a, b2) => a + b2, 0), infob: Array.from(document.querySelectorAll('.infob')).filter(M.vis).map(M.caja) };
      res.solapes = M.solapes(cuerpo, ':scope > *').concat(M.solapes(det, ':scope > *'));
      res.recorte = { detalle: M.recorte(det), docScrollH: document.documentElement.scrollWidth > innerWidth };
      res.ajustes = { vw: innerWidth, vh: innerHeight };
      return res;
    });
    // --- toggletip: apertura por teclado, Escape devuelve el foco, el globo cabe en el viewport y su contraste
    r.toggletips = await page.evaluate(async () => {
      const M = window.__M; const res = [];
      const botones = Array.from(document.querySelectorAll('.infob')).filter(M.vis);
      for (const b of botones) {
        b.scrollIntoView({ block: 'center' }); b.focus();
        b.click();                                   // Enter/Espacio sobre un <button> dispara click
        const t = document.getElementById(b.getAttribute('aria-controls'));
        const abierto = b.getAttribute('aria-expanded') === 'true' && !t.hidden;
        const rt = t.getBoundingClientRect();
        const c = abierto ? M.contraste(t) : null;
        const icono = M.contrasteGrafico(b);
        const fila = { nombre: b.getAttribute('aria-label'), caja: M.caja(b), abierto, describedby: b.getAttribute('aria-describedby') === t.id, chars: t.textContent.length,
          globo: abierto ? M.caja(t) : null, dentroViewport: abierto ? (rt.left >= 0 && rt.right <= innerWidth && rt.top >= 0 && rt.bottom <= innerHeight) : null, dentroHorizontal: abierto ? (rt.left >= 0 && rt.right <= innerWidth) : null,
          contrasteGlobo: c ? c.minimo : null, contrasteIcono: icono };
        b.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
        fila.cierraConEscape = b.getAttribute('aria-expanded') === 'false' && t.hidden;
        fila.focoVuelve = document.activeElement === b;
        res.push(fila);
      }
      return res;
    });
    out.medidas[`${w}x${h}-${tema}-${modo}`] = r;
    if (capt && tema === 'light' && modo === 'plazo') await page.screenshot({ path: path.join(CAPDIR, `24-${etiqueta}--${w}.png`), fullPage: false });
    await ctx.close();
  }
  await b.close();
  const js = JSON.stringify(out, null, 1);
  if (salida) fs.writeFileSync(salida, js); else console.log(js);
})();
