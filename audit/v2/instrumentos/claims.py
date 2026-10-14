"""Verifica el catálogo C1–C18 del PDF del cliente contra los HTML recibidos (lectura estática).
Uso: python3 -I claims.py <carpeta_html> <cambios.txt> <salida.json>
Por cada (pantalla, código) que el PDF dice aplicado: confirmado / no_confirmado / no_verificable_mecanicamente."""
import re, json, os, sys
D, TXT, OUT = sys.argv[1:4]
t = open(TXT, encoding='utf-8').read()
filas = {}
for l in t.splitlines():
    m = re.match(r'\s*(?:html_v2|sistema(?:/[\w\-]+)+)/([\w\-\.]+\.html)\s+((?:C\d+(?:\s*·\s*)?)+)\s+(\d+|—)→(\d+)\s+(\d+|—)(?:→(\d+))?\s+#(\d+)', l)
    if m:
        filas[m.group(1)] = {'codigos': re.findall(r'C\d+', m.group(2)), 'lt12': (None if m.group(3) == "—" else int(m.group(3)), int(m.group(4))),
                             'p105': (None if m.group(5) == '—' else int(m.group(5)), None if m.group(6) is None else int(m.group(6))), 'pr': m.group(7)}
def estilos(src): return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', src, re.S | re.I))
def regla(css, sel):
    return [m.group(1) for m in re.finditer(r'(?:^|[}\s,])' + sel + r'\s*\{([^}]*)\}', css)]
res, resumen = {}, {}
for n, f in sorted(filas.items()):
    p = os.path.join(D, n)
    if not os.path.exists(p): res[n] = {'estado': 'archivo_ausente_del_zip', 'codigos': f['codigos']}; continue
    src = open(p, encoding='utf-8', errors='replace').read(); css = estilos(src)
    css_nocom = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    tam = [float(x) for x in re.findall(r'font-size\s*:\s*([\d.]+)px', css_nocom)]
    lt12 = sum(1 for x in tam if x < 12 and x != 10.5); n105 = sum(1 for x in tam if x == 10.5)
    r = {}
    chk = {
      'C1': lambda: lt12 == 0,
      'C2': lambda: True,  # 10.5px solo en rótulos en mayúsculas: se verifica abajo
      'C3': lambda: bool(re.search(r'\.state\s*>\s*\.ico', css_nocom)) and not re.search(r'\.state\s+\.ico', css_nocom),
      'C4': lambda: any(re.search(r'min-height\s*:\s*36px', b) for b in regla(css_nocom, r'\.btn')),
      'C5': lambda: any(re.search(r'min-height\s*:\s*28px', b) for b in regla(css_nocom, r'\.btn\.mini')),
      'C6': lambda: any(re.search(r'padding\s*:\s*0\b', b) for b in regla(css_nocom, r'\.iconbtn')),
      'C7': lambda: len(re.findall(r'\[data-tacto', css_nocom)) > 0 and len(re.findall(r'\[data-tacto', css_nocom)) == len(re.findall(r':root\s*\[data-tacto', css_nocom)),
      'C8': lambda: '@font-face' in css_nocom,
      'C9': lambda: 'fonts.googleapis' not in src and 'fonts.gstatic' not in src,
      'C10': lambda: not any(re.search(r'(?<![-\w])color\s*:\s*var\(--(link|accent|primary|marca)', b) for b in regla(css_nocom, r'\.folio')),
      'C12': lambda: 'Ver detalle' not in src,
      'C16': lambda: bool(re.search(r':root\s*\{[^}]*--sp-5\s*:', css_nocom, re.S)),
      'C17': lambda: '<caption' in src,
    }
    for c in f['codigos']:
        if c in chk: r[c] = 'confirmado' if chk[c]() else 'NO_confirmado'
        else: r[c] = 'no_verificable_mecanicamente'
    # C2: ¿alguna regla con 10.5px sin text-transform:uppercase?
    malas = [b.strip()[:80] for b in re.findall(r'\{([^{}]*font-size\s*:\s*10\.5px[^{}]*)\}', css_nocom) if 'uppercase' not in b]
    if 'C2' in r: r['C2'] = 'se_mide_en_navegador'
    res[n] = {'codigos': r, 'lt12_pdf_despues': f['lt12'][1], 'lt12_medido': lt12, 'p105_pdf_despues': f['p105'][1], 'p105_medido': n105,
              'p105_sin_uppercase': malas[:3], 'pr': f['pr']}
tot = {}
for n, v in res.items():
    for c, e in (v.get('codigos') or {}).items() if isinstance(v.get('codigos'), dict) else []:
        tot.setdefault(c, {}).setdefault(e, []).append(n)
json.dump({'pdf_pantallas': len(filas), 'por_pantalla': res, 'por_codigo': {c: {e: len(v) for e, v in d.items()} for c, d in sorted(tot.items())},
           'incumplen': {c: d.get('NO_confirmado', []) for c, d in sorted(tot.items()) if d.get('NO_confirmado')}}, open(OUT, 'w'), ensure_ascii=False, indent=1)
print('pantallas en tabla del PDF:', len(filas), '| ausentes del zip:', sum(1 for v in res.values() if v.get('estado')))
for c, d in sorted(tot.items(), key=lambda x: int(x[0][1:])): print(c, {e: len(v) for e, v in d.items()})
