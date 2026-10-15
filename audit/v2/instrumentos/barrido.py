"""Barrido por patrón sobre una carpeta de pantallas HTML.

Busca en el código, con número de línea, las reglas que el informe pide cambiar, para dar la lista
completa de archivos de cada sustitución y para volver a medir cuando el cliente aplique los cambios.

Uso:
  python3 -I barrido.py <carpeta_html> <salida.json>
  python3 -I barrido.py <carpeta_html> <salida.json> --comparar <base.json>   # qué se cerró y qué persiste

Solo lee. Cada patrón devuelve {archivo: [líneas]}; un archivo sin coincidencias no aparece.
"""
import json, os, re, sys, collections

def lineas(txt):
    return txt.split('\n')

def linea_de(txt, pos):
    return txt.count('\n', 0, pos) + 1

def reglas(txt):
    """(selector, cuerpo, posición) de cada regla CSS plana, incluidas las de dentro de @media.
    Solo mira los bloques <style>; recorrido lineal para no enredarse con archivos grandes."""
    out = []
    for st in re.finditer(r'<style[^>]*>(.*?)</style>', txt, re.S):
        css, base = st.group(1), st.start(1)
        css = re.sub(r'/\*.*?\*/', lambda m: ' ' * len(m.group(0)), css, flags=re.S)   # comentarios fuera, misma longitud
        i, n, ini = 0, len(css), 0   # ini = inicio del selector actual
        while i < n:
            c = css[i]
            if c == '{':
                sel = css[ini:i]
                j = css.find('}', i + 1)
                k = css.find('{', i + 1)
                if k != -1 and (j == -1 or k < j):       # bloque anidado (@media): seguir dentro
                    ini = i + 1; i += 1; continue
                if j == -1: break
                out.append((sel.strip(), css[i + 1:j], base + ini + (len(sel) - len(sel.lstrip()))))
                ini = j + 1; i = j + 1; continue
            if c == '}':
                ini = i + 1
            i += 1
    return out

def barrer(txt):
    r = {}
    rs = reglas(txt)
    # 1 · menú lateral: texto oculto con display:none sin alternativa para lector de pantalla
    r['menu_et_display_none'] = [linea_de(txt, p) for s, b, p in rs
                                 if re.search(r'\.side\s+\.et\b', s) and re.search(r'display\s*:\s*none', b)]
    # 1b · enlaces del menú sin nombre accesible propio (aria-label o title)
    its = re.findall(r'<a\b[^>]*class="[^"]*\bit\b[^"]*"[^>]*>', txt)
    sin = [t for t in its if 'aria-label=' not in t and ' title=' not in t]
    r['menu_enlaces_it'] = len(its)
    r['menu_enlaces_sin_nombre_propio'] = len(sin)
    # 2 · icono: regla descendiente en vez de hijo directo
    r['state_ico_descendiente'] = [linea_de(txt, p) for s, b, p in rs if re.search(r'\.(state|esp)\s+\.ico\b', s)]
    r['state_ico_hijo_directo'] = [linea_de(txt, p) for s, b, p in rs if re.search(r'\.(state|esp)\s*>\s*\.ico\b', s)]
    # 3 · --text-3 en tema claro
    m = re.search(r'--text-3\s*:\s*(#[0-9A-Fa-f]{6})', txt)
    r['text3_valor_claro'] = m.group(1).upper() if m else None
    r['text3_linea'] = linea_de(txt, m.start()) if m else None
    # 4 · fuentes pedidas a Google por <link>
    r['google_fonts_link'] = [linea_de(txt, g.start()) for g in re.finditer(r'<link[^>]+fonts\.googleapis\.com[^>]*>', txt)]
    r['font_face'] = len(re.findall(r'@font-face', txt))
    # 5 · identificadores repetidos
    ids = re.findall(r'<[a-zA-Z][^<>]*?\sid="([^"]+)"', re.sub(r'<style[^>]*>.*?</style>|<script[^>]*>.*?</script>', '', txt, flags=re.S))
    c = collections.Counter(ids)
    r['ids_repetidos'] = {k: v for k, v in c.items() if v > 1}
    # 6 · cabecera .p4 sin relleno inferior declarado en su regla
    p4 = [(b, linea_de(txt, p)) for s, b, p in rs if re.fullmatch(r'\.p4', s)]
    r['p4_sin_padding_bottom'] = [ln for b, ln in p4 if not re.search(r'padding(-bottom)?\s*:', b)]
    r['p4_regla'] = [ln for b, ln in p4]
    # 7 · botón flotante
    r['fab'] = bool(re.search(r'class="fab\b', txt))
    return r

def resumen(res):
    """Cuenta de archivos por patrón (ficha para el informe)."""
    s = collections.OrderedDict()
    def n(f):
        return sorted(a for a, v in res.items() if f(v))
    s['menu_et_display_none'] = n(lambda v: v['menu_et_display_none'])
    s['menu_enlaces_sin_nombre_propio'] = n(lambda v: v['menu_enlaces_sin_nombre_propio'] > 0 and v['menu_et_display_none'])
    s['state_ico_descendiente'] = n(lambda v: v['state_ico_descendiente'])
    s['state_ico_descendiente_sin_hijo_directo'] = n(lambda v: v['state_ico_descendiente'] and not v['state_ico_hijo_directo'])
    s['text3_66717F'] = n(lambda v: v['text3_valor_claro'] == '#66717F')
    s['google_fonts_link'] = n(lambda v: v['google_fonts_link'])
    s['ids_repetidos'] = n(lambda v: v['ids_repetidos'])
    s['p4_sin_padding_bottom'] = n(lambda v: v['p4_sin_padding_bottom'])
    s['fab'] = n(lambda v: v['fab'])
    return s

def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    carpeta, salida = a[0], a[1]
    res = {}
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith('.html'): continue
        txt = open(os.path.join(carpeta, f), encoding='utf-8', errors='replace').read()
        res[f[:-5]] = barrer(txt)
    out = {'archivos': len(res), 'por_archivo': res, 'resumen': resumen(res)}
    if '--comparar' in sys.argv:
        base = json.load(open(sys.argv[sys.argv.index('--comparar') + 1]))['resumen']
        cmp = {}
        for k, ahora in out['resumen'].items():
            antes = set(base.get(k, []))
            ahora = set(ahora)
            cmp[k] = {'antes': len(antes), 'ahora': len(ahora), 'cerrados': sorted(antes - ahora),
                      'persisten': sorted(antes & ahora), 'nuevos': sorted(ahora - antes)}
        out['comparacion'] = cmp
    json.dump(out, open(salida, 'w'), ensure_ascii=False, indent=1)
    for k, v in out['resumen'].items():
        print(f'{k:42s} {len(v):3d} de {len(res)}')
    if 'comparacion' in out:
        print('--- frente a la base ---')
        for k, c in out['comparacion'].items():
            print(f'{k:42s} antes {c["antes"]:3d} → ahora {c["ahora"]:3d}  (cerrados {len(c["cerrados"])}, nuevos {len(c["nuevos"])})')

if __name__ == '__main__':
    main()
