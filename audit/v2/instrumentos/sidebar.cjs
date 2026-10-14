const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const SP = process.env.SP, M = process.env.MDIR;
const listar = (d,a=[])=>{for(const e of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,e.name);
  if(e.isDirectory())listar(p,a);else if(e.name.endsWith('.html')&&e.name!=='index.html'&&!e.name.startsWith('studio_'))a.push(path.relative(M,p));}return a;};
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport:{width:1000,height:800} });
  await require('./lib.cjs').preparar(p);
  const out = {};
  for (const rel of listar(M).sort()) {
    const n = path.basename(rel,'.html');
    try {
      await p.goto('http://127.0.0.1:'+(process.env.PORT||'8732')+'/'+rel,{waitUntil:'load',timeout:25000}); await p.waitForTimeout(350);
      out[n] = await p.evaluate(() => {
        const its = Array.from(document.querySelectorAll('.side .it, nav .it, aside .it'));
        if (!its.length) return { hayMenu:false };
        const vis = its.filter(e => e.getBoundingClientRect().width>0);
        const sinNombre = vis.filter(e => {
          const t=(e.innerText||'').trim(), al=e.getAttribute('aria-label'), ti=e.getAttribute('title');
          return !t && !al && !ti; });
        return { hayMenu:true, total:vis.length, sinNombre:sinNombre.length,
                 anchoSide: document.querySelector('.side')?.getBoundingClientRect().width|0 };
      });
    } catch(e){ out[n]={error:e.message.slice(0,50)}; }
    process.stdout.write('.');
  }
  await b.close();
  fs.writeFileSync((process.env.OUT||SP) + '/sidebar.json', JSON.stringify(out,null,1));
  const con = Object.entries(out).filter(([k,v])=>v.hayMenu);
  const rotas = con.filter(([k,v])=>v.sinNombre>0);
  console.log(`\n\n=== §7.2 a 1000px de ancho ===`);
  console.log(`  maquetas con menu lateral: ${con.length}/52`);
  console.log(`  con enlaces SIN nombre accesible: ${rotas.length}`);
  console.log(`  enlaces anonimos en total: ${rotas.reduce((s,[k,v])=>s+v.sinNombre,0)}`);
  if (rotas.length) console.log(`  ejemplo: ${rotas[0][0]} -> ${rotas[0][1].sinNombre}/${rotas[0][1].total} sin nombre, .side de ${rotas[0][1].anchoSide}px`);
  const ok = con.filter(([k,v])=>v.sinNombre===0);
  if (ok.length) console.log(`  CORRECTAS (${ok.length}): ${ok.slice(0,6).map(([k])=>k).join(', ')}`);
})();
