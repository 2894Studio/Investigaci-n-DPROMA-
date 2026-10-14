// Renderiza el HTML de impresión del informe a PDF A4 (Chromium vía Playwright).
// Uso: node pdf.cjs <url> <salida.pdf>
const { chromium } = require('playwright');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: out, format: 'A4', printBackground: true,
    margin: { top: '18mm', bottom: '20mm', left: '18mm', right: '18mm' },
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font:7.5pt Helvetica,Arial,sans-serif;color:#16181D;padding:0 18mm;display:flex;justify-content:space-between"><span>Qué corregir en las 50 pantallas · DPROMA × 2894 Studio</span><span class="pageNumber"></span></div>' });
  await b.close(); console.log('pdf listo:', out);
})();
