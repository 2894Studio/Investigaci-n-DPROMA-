import markdown, sys, os, html
src, dst, titulo = sys.argv[1], sys.argv[2], sys.argv[3]
cuerpo = markdown.markdown(open(src, encoding='utf-8').read(),
    extensions=['tables', 'fenced_code', 'toc', 'attr_list'])
CSS = """
:root{--tinta:#1B2430;--tinta2:#4C5A6B;--tinta3:#5C6675;--linea:#D7DEE6;--fondo:#FFF;
 --sup:#F7F9FB;--acento:#1E4E79;--alta:#7A2A23;--altabg:#F6DAD7;--media:#6E5210;
 --mediabg:#F5E7C6;--baja:#1D5A46;--bajabg:#DCF0E7}
*{box-sizing:border-box}
body{font:11pt/1.55 -apple-system,"Segoe UI",Inter,system-ui,sans-serif;color:var(--tinta);
 background:var(--fondo);margin:0;padding:0}
.hoja{max-width:184mm;margin:0 auto;padding:0 2mm}
h1{font-size:21pt;line-height:1.2;margin:0 0 4pt;letter-spacing:-.01em}
h2{font-size:15pt;margin:20pt 0 6pt;padding-bottom:4pt;border-bottom:2px solid var(--acento);
 page-break-after:avoid}
h3{font-size:12.5pt;margin:14pt 0 4pt;color:var(--acento);page-break-after:avoid}
h4{font-size:11pt;margin:10pt 0 3pt;color:var(--tinta2);page-break-after:avoid}
p{margin:0 0 7pt;orphans:3;widows:3}
ul,ol{margin:0 0 8pt;padding-left:16pt}li{margin:0 0 3pt}
table{width:100%;border-collapse:collapse;margin:8pt 0 12pt;font-size:8.6pt;
 page-break-inside:avoid}
th{background:var(--sup);text-align:left;font-weight:650;padding:5pt 6pt;
 border:1px solid var(--linea);vertical-align:bottom}
td{padding:4.5pt 6pt;border:1px solid var(--linea);vertical-align:top}
tr:nth-child(even) td{background:#FCFDFE}
code{font:9pt ui-monospace,"SF Mono",Menlo,Consolas,monospace;background:var(--sup);
 padding:1px 4px;border-radius:3px;border:1px solid var(--linea);white-space:nowrap}
pre{background:var(--sup);border:1px solid var(--linea);border-radius:5px;padding:8pt;
 overflow:hidden;page-break-inside:avoid}
pre code{background:none;border:0;padding:0;white-space:pre-wrap;word-break:break-word;font-size:8.2pt}
blockquote{margin:8pt 0;padding:6pt 10pt;border-left:3px solid var(--acento);
 background:var(--sup);color:var(--tinta2)}
blockquote p{margin:0}
img{max-width:100%;max-height:118mm;object-fit:contain;object-position:top;display:block;
 margin:8pt auto;border:1px solid var(--linea);border-radius:4px;page-break-inside:avoid}
hr{border:0;border-top:1px solid var(--linea);margin:16pt 0}
strong{font-weight:650}
a{color:var(--acento);text-decoration:none}
@page{size:A4;margin:16mm 13mm 18mm}
@media print{h1,h2,h3{page-break-after:avoid}}
"""
open(dst, 'w', encoding='utf-8').write(
 f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
 f'<title>{html.escape(titulo)}</title><style>{CSS}</style></head>'
 f'<body><div class="hoja">{cuerpo}</div></body></html>')
print(f"html: {dst} ({os.path.getsize(dst)} bytes)")
