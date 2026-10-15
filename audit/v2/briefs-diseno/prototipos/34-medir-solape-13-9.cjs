const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
(async()=>{ const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
 const ctx = await b.newContext({viewport:{width:1440,height:900}}); const page = await ctx.newPage(); await preparar(page);
 await page.goto('http://127.0.0.1:8764/34-B-dia-proporcional-13-9.html?estres=1&sinplan=1'); await page.evaluate(()=>{document.getElementById('ag').dataset.vista='dia'}); await page.waitForTimeout(300);
 const r = await page.evaluate(()=>[...document.querySelectorAll('#diab .ev')].map(e=>({dur:+e.dataset.dur, bloqueDesborda:e.scrollHeight>e.clientHeight+0.5, sh:e.scrollHeight, ch:e.clientHeight, textoSolapa:(()=>{const hs=[...e.children].map(c=>{const rg=document.createRange(); rg.selectNodeContents(c); const rc=rg.getBoundingClientRect(); return rc;}); let s=0; for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++) if(Math.min(hs[i].bottom,hs[j].bottom)-Math.max(hs[i].top,hs[j].top)>1) s++; return s;})()})).sort((a,b)=>a.dur-b.dur));
 console.log(JSON.stringify(r)); await b.close(); })();
