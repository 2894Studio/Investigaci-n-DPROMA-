// Convierte las capturas de la revisión a JPEG ligeros en web/entregables/img/revision/.
// Uso: LISTA=lista.json OUT=<dir> node imagenes.cjs   (lista: {nombre: ruta_png})
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const lista = JSON.parse(fs.readFileSync(process.env.LISTA, 'utf8')); fs.mkdirSync(process.env.OUT, { recursive: true });
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }); const p = await b.newPage();
  const meta = {};
  for (const [k, f] of Object.entries(lista)) {
    const b64 = fs.readFileSync(f).toString('base64');
    const r = await p.evaluate(async b64 => { const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
      const max = 1200, s = Math.min(1, max / img.naturalWidth); const c = document.createElement('canvas'); c.width = Math.round(img.naturalWidth * s); c.height = Math.round(img.naturalHeight * s);
      const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0, c.width, c.height);
      return { u: c.toDataURL('image/jpeg', 0.88), w: c.width, h: c.height }; }, b64);
    fs.writeFileSync(path.join(process.env.OUT, k + '.jpg'), Buffer.from(r.u.split(',')[1], 'base64')); meta[k] = [r.w, r.h];
  }
  fs.writeFileSync(path.join(process.env.OUT, '_medidas.json'), JSON.stringify(meta)); await b.close(); console.log(Object.keys(meta).length, 'imágenes');
})();
