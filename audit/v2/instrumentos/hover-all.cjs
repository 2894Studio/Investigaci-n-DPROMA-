const { chromium } = require('playwright');
const fs=require('fs'), path=require('path');
const SP=process.env.SP, M=SP+'/maquetas/maquetas-SIO-por-funcionalidad-2026-09-30';
const listar=(d,a=[])=>{for(const e of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,e.name);
 if(e.isDirectory())listar(p,a);else if(e.name.endsWith('.html')&&e.name!=='index.html'&&!e.name.startsWith('studio_'))a.push(path.relative(M,p));}return a;};
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const p=await b.newPage({viewport:{width:1440,height:900}});
  await require('./lib.cjs').preparar(p);
 const out={};
 for(const rel of listar(M).sort()){
  const n=path.basename(rel,'.html');
  try{
   await p.goto('http://127.0.0.1:'+(process.env.PORT||'8732')+'/'+rel,{waitUntil:'load',timeout:25000}); await p.waitForTimeout(300);
   out[n]=await p.evaluate(()=>{
    const reglas=Array.from(document.styleSheets).flatMap(s=>{try{return Array.from(s.cssRules)}catch{return[]}});
    const hover=reglas.filter(r=>r.selectorText&&/tr:hover/.test(r.selectorText)&&/surface-2/.test(r.style.cssText||'')).length;
    const filas=Array.from(document.querySelectorAll('tbody tr'));
    let nodos=0;
    for(const f of filas) nodos+=Array.from(f.querySelectorAll('*')).filter(e=>getComputedStyle(e).color==='rgb(102, 113, 127)').length;
    return {reglaHoverSurface2:hover>0, filas:filas.length, nodosText3:nodos};
   });
  }catch(e){out[n]={error:1}}
  process.stdout.write('.');
 }
 await b.close();
 fs.writeFileSync((process.env.OUT||SP) + '/hover.json',JSON.stringify(out,null,1));
 const afect=Object.entries(out).filter(([k,v])=>v.reglaHoverSurface2&&v.nodosText3>0);
 console.log(`\n\n=== --text-3 sobre --surface-2 AL SOBREVOLAR UNA FILA (4,21:1) ===`);
 console.log(`  maquetas con tabla y regla de hover a --surface-2: ${Object.values(out).filter(v=>v.reglaHoverSurface2).length}`);
 console.log(`  de esas, con texto en --text-3 dentro de las filas: ${afect.length}`);
 console.log(`  nodos afectados en total: ${afect.reduce((s,[k,v])=>s+v.nodosText3,0)}`);
 afect.sort((a,b)=>b[1].nodosText3-a[1].nodosText3).slice(0,8).forEach(([k,v])=>console.log(`    ${v.nodosText3} nodos en ${v.filas} filas  ${k}`));
})();
