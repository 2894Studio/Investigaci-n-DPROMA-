// Arnés común de medición v2. Solo lee: no toca los HTML del cliente.
// Entorno: MDIR (carpeta de HTML), PORT (servidor local), OUT (carpeta de salida).
// Fuentes: los .woff2 de D116 no vienen en el paquete (ruta ../../apps/web/public/fuentes/).
// Se inyectan AL RENDERIZAR (interceptando la petición) para no medir recortes que son de fuente.
const fs = require('fs'), path = require('path');
const FUENTES = { inter: path.join(__dirname, 'inter-latin-wght-normal.woff2'),
                  michroma: path.join(__dirname, 'michroma-latin-400-normal.woff2') };
const PORT = process.env.PORT || '8732';

async function preparar(page) {
  await page.route('**/*', route => {
    const u = route.request().url();
    if (/inter-variable\.woff2|__fonts\/inter/.test(u)) return route.fulfill({ body: fs.readFileSync(FUENTES.inter), contentType: 'font/woff2' });
    if (/michroma\.woff2|__fonts\/michroma/.test(u)) return route.fulfill({ body: fs.readFileSync(FUENTES.michroma), contentType: 'font/woff2' });
    if (/fonts\.googleapis\.com|fonts\.gstatic\.com/.test(u)) return route.fulfill({ body: '', contentType: 'text/css' });
    return route.continue();
  });
  const css = `@font-face{font-family:'Inter';font-weight:400 700;src:url('http://127.0.0.1:${PORT}/__fonts/inter.woff2') format('woff2')}
@font-face{font-family:'Michroma';font-weight:400;src:url('http://127.0.0.1:${PORT}/__fonts/michroma.woff2') format('woff2')}
[data-andamio]{display:none !important}`;
  const goto = page.goto.bind(page);
  page.goto = async (...a) => { const r = await goto(...a); await page.addStyleTag({ content: css }); await page.evaluate(() => document.fonts.ready); return r; };
  return page;
}
module.exports = { preparar };
