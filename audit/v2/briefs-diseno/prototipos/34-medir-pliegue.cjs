const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
(async()=>{
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [id,url] of [['A','http://127.0.0.1:8732/34_instaladores.html'],['Aprima','http://127.0.0.1:8764/34-A-prima-cambio-minimo.html'],['C','http://127.0.0.1:8764/34-C-propuesta-previa.html']]) {
    for (const [W,H] of [[1280,800],[1440,900]]) {
      const ctx = await b.newContext({viewport:{width:W,height:H}}); const page = await ctx.newPage(); await preparar(page);
      await page.goto(url); await page.waitForTimeout(250);
      const r = await page.evaluate((H)=>{ const ag=document.querySelector('.agenda'); const top=Math.round(ag.getBoundingClientRect().top);
        const trs=[...ag.querySelectorAll('tbody tr')]; const enteras=trs.filter(t=>t.getBoundingClientRect().bottom<=H).length;
        const parc=trs.filter(t=>{const r=t.getBoundingClientRect(); return r.top<H && r.bottom>H}).length;
        return {agendaTop:top, filasTotal:trs.length, filasEnterasEnPliegue:enteras, parciales:parc}; }, H);
      console.log(id,W+'x'+H,JSON.stringify(r)); await ctx.close();
    }
  }
  await b.close();
})();
