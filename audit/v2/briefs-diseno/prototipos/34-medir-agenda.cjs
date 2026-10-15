// Medición comparativa de la agenda (34). Solo lee. Uso: node med34.cjs <etiqueta> <url> <selectorSemana|-> <selectorDia|-> <salida.json>
const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const [,, etiqueta, url, selSem, selDia, salida] = process.argv;

// función que corre dentro de la página
function medir(args) {
  const { sel, vista } = args;
  const ag = document.getElementById('ag');
  if (ag) ag.dataset.vista = vista;
  const cont = document.querySelector(sel);
  if (!cont) return { error: 'sin contenedor ' + sel };
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return [0,0,0,0]; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0],p[1],p[2], p.length>3?p[3]:1]; };
  const over = (f,b) => { const a=f[3]; return [f[0]*a+b[0]*(1-a), f[1]*a+b[1]*(1-a), f[2]*a+b[2]*(1-a), 1]; };
  const bgDe = el => { const cadena=[]; let e=el; while(e){ cadena.push(parse(getComputedStyle(e).backgroundColor)); e=e.parentElement; } let b=[255,255,255,1]; for(let i=cadena.length-1;i>=0;i--) b=over(cadena[i],b); return b; };
  const lum = c => { const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)}; return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); };
  const cr = (a,b) => { const l1=lum(a), l2=lum(b); return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); };
  const r = {};
  const box = cont.getBoundingClientRect();
  const tb = cont.querySelector('table');
  r.contenedor = { clientWidth: cont.clientWidth, scrollWidth: cont.scrollWidth, ocultosPx: Math.max(0, cont.scrollWidth - cont.clientWidth), tag: cont.tagName.toLowerCase() };
  r.pagina = { scrollW: document.documentElement.scrollWidth, innerW: innerWidth };
  // texto
  let total=0, menor12=0, minFs=99; const tamanos={}; const contr=[]; const trunc=[];
  const w = document.createTreeWalker(cont, NodeFilter.SHOW_TEXT); let n;
  while (n = w.nextNode()) {
    const t = n.textContent.trim(); if (!t) continue; const el = n.parentElement; const st = getComputedStyle(el);
    if (st.display==='none' || st.visibility==='hidden') continue;
    const rc = el.getBoundingClientRect(); if (rc.width===0 && rc.height===0) continue;
    if (el.closest('.sr')) continue; // texto solo para lector
    total++; const fs = parseFloat(st.fontSize); tamanos[fs]=(tamanos[fs]||0)+1; if (fs<12) menor12++; if (fs<minFs) minFs=fs;
    const fg = over(parse(st.color), bgDe(el)); const bg = bgDe(el); const ratio = cr(fg,bg);
    contr.push({ t: t.slice(0,28), fs, ratio: Math.round(ratio*100)/100 });
    if (st.textOverflow==='ellipsis' && el.scrollWidth > el.clientWidth+1) trunc.push(t);
  }
  r.texto = { nodos: total, menoresDe12: menor12, tamanoMinimo: minFs, tamanos };
  r.contraste = { minimo: Math.min(...contr.map(c=>c.ratio)), bajo45: contr.filter(c=>c.ratio<4.5).map(c=>c.t+' '+c.fs+'px '+c.ratio+':1') };
  r.truncados = trunc;
  // destinos
  const tiles = [...cont.querySelectorAll('a.vt, a.cita, .bloque-cita, a.ev')].map(a => { const b=a.getBoundingClientRect(); return { w: Math.round(b.width), h: Math.round(b.height), cls: a.className, tag: a.tagName }; });
  r.citas = { n: tiles.length, minW: Math.min(...tiles.map(t=>t.w)), minH: Math.min(...tiles.map(t=>t.h)), enlaces: tiles.filter(t=>t.tag==='A').length };
  if (tb) {
    const ths = [...tb.querySelectorAll('thead th')].map(t => ({ t: t.textContent.trim().slice(0,14), w: Math.round(t.getBoundingClientRect().width) }));
    r.columnas = ths;
    r.filasH = [...tb.querySelectorAll('tbody tr')].map(t => Math.round(t.getBoundingClientRect().height));
    r.tablaW = Math.round(tb.getBoundingClientRect().width);
    r.alturaCaja = Math.round(box.height);
    const dom = tb.querySelector('th.dom-col');
    if (dom) { const d = dom.getBoundingClientRect(); const visible = Math.max(0, Math.min(d.right, box.right) - Math.max(d.left, box.left)); r.domingo = { ancho: Math.round(d.width), visiblePx: Math.round(visible), recortadoPx: Math.round(d.width - visible) };
      const vd = tb.querySelector('td.dom-col a'); if (vd) { const v = vd.getBoundingClientRect(); r.visitaDomingo = { ancho: Math.round(v.width), visiblePx: Math.round(Math.max(0, Math.min(v.right, box.right) - v.left)) }; } }
  }
  // lector: cuántos huecos con nombre accesible
  const libres = [...cont.querySelectorAll('.libre')]; r.libres = { n: libres.length, conTextoParaLector: libres.filter(l => l.querySelector('.sr') || l.getAttribute('aria-label')).length };
  return r;
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = { etiqueta, url, anchos: {} };
  for (const W of [1440, 1280, 1024, 390]) {
    const ctx = await b.newContext({ viewport: { width: W, height: 900 } });
    const page = await ctx.newPage(); await preparar(page);
    await page.goto(url); await page.waitForTimeout(300);
    const res = {};
    if (selSem !== '-') res.semana = await page.evaluate(medir, { sel: selSem, vista: 'semana' });
    if (selDia !== '-') res.dia = await page.evaluate(medir, { sel: selDia, vista: 'dia' });
    // contraste con el cursor sobre la primera fila (semana)
    if (selSem !== '-') {
      await page.evaluate(() => { const a=document.getElementById('ag'); if (a) a.dataset.vista='semana'; });
      const fila = page.locator(selSem + ' tbody tr').first();
      await fila.hover({ force: true }).catch(()=>{});
      res.semanaHover = await page.evaluate(medir, { sel: selSem, vista: 'semana' });
      res.semanaHover = { contraste: res.semanaHover.contraste };
    }
    out.anchos[W] = res;
    await ctx.close();
  }
  require('fs').writeFileSync(salida, JSON.stringify(out, null, 1));
  await b.close();
})();
