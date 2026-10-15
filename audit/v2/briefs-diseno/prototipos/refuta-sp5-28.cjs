// Refutación reproducible de la hipótesis «--sp-5 causa la cabecera sin aire» (28 Mi día). Solo lee.
const { chromium } = require('playwright');
const lib = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [nombre, css] of [['original', ''], ['+ :root{--sp-5:20px}', ':root{--sp-5:20px}'], ['+ .p4{padding-bottom:var(--sp-3)}', '.p4{padding-bottom:var(--sp-3)}']]) {
    const r = {};
    for (const W of [390, 1440]) {
      const p = await b.newPage({ viewport: { width: W, height: 844 } }); await lib.preparar(p);
      await p.goto(process.env.ORIG || 'http://127.0.0.1:8732/28_instalador_mi_dia.html'); if (css) await p.addStyleTag({ content: css });
      r[W] = await p.evaluate(() => { const e = document.querySelector('.p4'); return { alto: +e.getBoundingClientRect().height.toFixed(1), pb: getComputedStyle(e).paddingBottom, gordoPadL: getComputedStyle(document.querySelector('.gordo')).paddingLeft }; });
      await p.close();
    }
    console.log(nombre.padEnd(34), JSON.stringify(r));
  }
  await b.close();
})();
