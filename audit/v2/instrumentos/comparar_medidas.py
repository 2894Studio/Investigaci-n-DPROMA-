"""Compara los totales de los medidores entre dos carpetas de resultados (base y nueva).
Uso: python3 -I comparar_medidas.py <carpeta_base> <carpeta_nueva>
Misma cuenta que la tabla «Qué se contó en las 50 pantallas» del informe."""
import json, sys, os

def cargar(d, f):
    p = os.path.join(d, f)
    if not os.path.exists(p): return None
    j = json.load(open(p))
    return j['v2'] if isinstance(j, dict) and 'v2' in j and isinstance(j['v2'], dict) else j

def totales(d):
    t, c, s, k, n = (cargar(d, f) for f in ('tactil.json', 'contraste.json', 'sidebar.json', 'tokens.json', 'nuevos.json'))
    o = {}
    if t: o['Destinos de pulsación menores de 24 px'] = {a: v['bajo24'] for a, v in t.items()}
    if c:
        o['Textos bajo el contraste AA, tema claro'] = {a: v['claro']['fallos'] for a, v in c.items()}
        o['Textos bajo el contraste AA, tema oscuro'] = {a: (v.get('oscuro') or {}).get('fallos', 0) for a, v in c.items()}
    if s: o['Enlaces del menú sin nombre accesible a 1000 px'] = {a: v.get('sinNombre', 0) for a, v in s.items() if v.get('hayMenu')}
    if k: o['Tokens usados sin declarar'] = {r['archivo'][:-5]: len(r['usados_no_declarados']) for r in k['archivos']}
    if n:
        for rot, (a, b) in {'Iconos casi del color del botón (I1)': ('I1_icono_vs_boton', 'fallos'), 'Barras sin holgura inferior (I2)': ('I2_holgura_inferior', 'fallos'),
                            'Parejas de botones dispares (I8)': ('I8_paridad_botones', 'gruposDispares'), 'Celdas con párrafo (I9)': ('I9_celdas', 'largas'),
                            'Textos de 10,5 px sin mayúsculas (C2)': ('C2_105_no_mayusculas', 'fallos'), 'Textos de más de 140 caracteres (C11)': ('C11_texto_largo', 'sobre140'),
                            'Elementos afectados por --sp-5 sin declarar': ('SP5', 'elementosAfectados')}.items():
            o[rot] = {p: (v.get(a, {}).get(b, 0) or 0) for p, v in n.items() if isinstance(v, dict) and 'error' not in v}
    return o

base, nueva = totales(sys.argv[1]), totales(sys.argv[2])
print(f'{"Indicador":52s} {"antes":>6s} {"ahora":>6s}  pantallas que mejoran / empeoran')
for k in base:
    if k not in nueva: continue
    b, a = base[k], nueva[k]
    mejor = sorted(p for p in a if p in b and a[p] < b[p]); peor = sorted(p for p in a if p in b and a[p] > b[p])
    print(f'{k:52s} {sum(b.values()):6d} {sum(a.values()):6d}  {len(mejor)} / {len(peor)}' + (f'   empeoran: {", ".join(peor[:6])}' if peor else ''))
