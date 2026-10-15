const { chromium } = require('playwright');
const { preparar } = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
(async()=>{
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [id,url,idx] of [['A','http://127.0.0.1:8732/34_instaladores.html',2],['Aprima','http://127.0.0.1:8764/34-A-prima-cambio-minimo.html',0]]) {
    const ctx = await b.newContext({viewport:{width:1440,height:900}}); const page = await ctx.newPage(); await preparar(page);
    await page.goto(url); await page.waitForTimeout(200);
    const s = await page.locator('.agenda tbody tr').nth(idx).ariaSnapshot();
    console.log('=== '+id+' fila '+idx+'\n'+s);
    const d = await page.evaluate(()=>{document.getElementById('ag').dataset.vista='dia';}); 
    const sd = await page.locator('.dia-caja tbody tr').nth(2).ariaSnapshot(); console.log('--- día 09:00\n'+sd);
    await ctx.close();
  }
  await b.close();
})();
