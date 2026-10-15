// Imprime la página del informe a PDF A4 (Chromium vía Playwright). Uso: node pdf.cjs <url> <salida.pdf>
const { chromium } = require('playwright');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.goto(url, { waitUntil: 'load', timeout: 60000 });
  await p.evaluate(async () => { const im = [...document.images]; im.forEach(i => { i.loading = 'eager'; }); await Promise.all(im.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: out, format: 'A4', preferCSSPageSize: true, printBackground: true,
    margin: { top: '16mm', bottom: '19mm', left: '15mm', right: '15mm' },
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font:7.5pt Helvetica,Arial,sans-serif;color:#8591A3;padding:0 15mm;display:flex;justify-content:space-between"><span>SIO-DPROMA · 2894 Studio</span><span class="pageNumber"></span></div>' });
  await b.close(); console.log('pdf listo:', out);
})();
