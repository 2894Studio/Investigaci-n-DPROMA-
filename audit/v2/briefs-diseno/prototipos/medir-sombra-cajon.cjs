// Mide cuánto se cuela la sombra del cajón de menú cerrado en el borde izquierdo a 390 px (28 y 47). Compara píxeles con y sin sombra. Solo lee.
const { chromium } = require('playwright');
const lib = require('/home/user/Investigaci-n-DPROMA-/audit/v2/instrumentos/lib.cjs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
for (const u of ['http://127.0.0.1:8732/28_instalador_mi_dia.html','http://127.0.0.1:8732/47_asistente.html']){
const p=await b.newPage({viewport:{width:390,height:844}});await lib.preparar(p);await p.goto(u);
await p.addStyleTag({content:'*{transition:none !important}'});
const info=await p.evaluate(()=>{const s=document.querySelector('.side');const r=s.getBoundingClientRect();return {right:r.right,sombra:getComputedStyle(s).boxShadow,abierto:document.documentElement.getAttribute('data-menu')}});
async function fila(){const buf=await p.screenshot({clip:{x:0,y:400,width:70,height:1}});const b64=buf.toString('base64');
 return p.evaluate(async b64=>{const img=new Image();img.src='data:image/png;base64,'+b64;await img.decode();const c=document.createElement('canvas');c.width=img.width;c.height=1;const x=c.getContext('2d');x.drawImage(img,0,0);return [0,10,20,30,40,50,69].map(i=>Array.from(x.getImageData(i,0,1,1).data).slice(0,3).join(','));},b64);}
const con=await fila();
await p.addStyleTag({content:'.side{box-shadow:none !important}'});
const sin=await fila();
console.log(u.split('/').pop(),JSON.stringify(info));console.log('x=0,10,20,30,40,50,69 con sombra:',con.join(' | '));console.log('sin sombra:',sin.join(' | '));await p.close();}
await b.close();})();
