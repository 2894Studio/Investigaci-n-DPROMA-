const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
const casos = [['A','http://127.0.0.1:8732/54_bitacora_descargas.html'],['propuesta','http://127.0.0.1:8764/54-panel-con-que-filtros.html']];
function medir() {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return [0,0,0,0]; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0],p[1],p[2], p.length>3?p[3]:1]; };
  const over = (f,b) => { const a=f[3]; return [f[0]*a+b[0]*(1-a), f[1]*a+b[1]*(1-a), f[2]*a+b[2]*(1-a), 1]; };
  const bgDe = el => { const ch=[]; let e=el; while(e){ ch.push(parse(getComputedStyle(e).backgroundColor)); e=e.parentElement; } let b=[255,255,255,1]; for(let i=ch.length-1;i>=0;i--) b=over(ch[i],b); return b; };
  const lum = c => { const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)}; return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); };
  const cr = (a,b) => { const l1=lum(a), l2=lum(b); return Math.round((Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05)*100)/100; };
  const r = {};
  const celdas = [...document.querySelectorAll('td[data-et="Con qué filtros"]')];
  r.celdasAlto = celdas.map(c => Math.round(c.closest('tr').getBoundingClientRect().height));
  r.columnaAncho = Math.round(celdas[0].getBoundingClientRect().width);
  const cont = document.querySelector('.tabla-caja');
  r.tabla = { clientW: cont.clientWidth, scrollW: cont.scrollWidth, ocultos: Math.max(0, cont.scrollWidth - cont.clientWidth), pagina: document.documentElement.scrollWidth };
  // textos de las celdas de filtros
  const items = []; 
  celdas.forEach(c => { const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) { const t=n.textContent.trim(); if(!t) continue; const el=n.parentElement; const st=getComputedStyle(el); const bg=bgDe(el); const fg=over(parse(st.color),bg); items.push({t, fs: parseFloat(st.fontSize), ratio: cr(fg,bg)}); } });
  r.textoFiltros = { nodos: items.length, tamanoMin: Math.min(...items.map(i=>i.fs)), contrasteMin: Math.min(...items.map(i=>i.ratio)), peor: items.sort((a,b)=>a.ratio-b.ratio)[0] };
  // marca de dato personal: borde e icono
  const marcas = [...document.querySelectorAll('.f-chip.pers, .sens')];
  r.marcas = marcas.map(m => { const st=getComputedStyle(m); const bg=bgDe(m.parentElement); const bf=over(parse(st.borderTopColor), bg); const fondo=bgDe(m); const ico=m.querySelector('svg'); const ic = ico? over(parse(getComputedStyle(ico).color), fondo):null;
    const txt=[...m.querySelectorAll('b,span')][0]; const tc=over(parse(st.color), fondo);
    return { clase: m.className, texto: m.textContent.trim().slice(0,40), texto_contraste: cr(tc, fondo), borde_contra_entorno: cr(bf, bg), icono_contraste: ic? cr(ic, fondo): null, bordeColor: st.borderTopColor, bg: st.backgroundColor }; });
  // elementos con color de semáforo ámbar en la zona de contenido
  const warn = getComputedStyle(document.documentElement);
  const tok = n => warn.getPropertyValue(n).trim();
  const objetivos = [tok('--warn'), tok('--warn-bg'), tok('--warn-ink')].map(h => { const d=document.createElement('i'); d.style.color=h; document.body.appendChild(d); const c=getComputedStyle(d).color; d.remove(); return c; });
  let usos = 0; const lista=[];
  document.querySelectorAll('main *').forEach(e => { const st=getComputedStyle(e); [st.color, st.backgroundColor, st.borderTopColor].forEach(c => { if (objetivos.includes(c)) { usos++; lista.push(e.className||e.tagName); } }); });
  r.usosAmbarEnMain = { total: usos, elementos: [...new Set(lista)] };
  r.tabbablesEnCeldas = celdas.reduce((n,c)=>n+c.querySelectorAll('a,button,[tabindex]:not([tabindex="-1"]),input').length,0);
  r.nota = (document.querySelector('.nota')||{}).textContent?.trim();
  r.notaLen = r.nota ? r.nota.length : 0;
  return r;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const [id,url] of casos) {
    out[id] = {};
    for (const W of [1440,1280,1024,390]) {
      for (const tema of ['light','dark']) {
        if (W!==1440 && tema==='dark') continue;
        const ctx = await b.newContext({ viewport:{width:W,height:900}, colorScheme: tema });
        const page = await ctx.newPage(); await preparar(page);
        await page.goto(url); await page.evaluate(t=>document.documentElement.setAttribute('data-theme',t),tema); await page.waitForTimeout(250);
        out[id][W+'/'+tema] = await page.evaluate(medir);
        if (W===1440 && tema==='light') {
          out[id].aria = await page.locator('td[data-et="Con qué filtros"]').first().ariaSnapshot();
          out[id].ariaFila = await page.locator('tbody tr').first().ariaSnapshot();
        }
        await ctx.close();
      }
    }
  }
  require('fs').writeFileSync('med54.json', JSON.stringify(out,null,1));
  await b.close();
})();
