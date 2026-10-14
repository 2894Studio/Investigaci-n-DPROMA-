"""Delta v1→v2 con el MISMO arnés (fuentes inyectadas) sobre las dos versiones. Uso: python3 -I delta.py <mediciones_dir>"""
import json, sys, os
M = sys.argv[1]
L = lambda v, f: json.load(open(f'{M}/{v}/{f}.json'))
v = {k: {f: L(k, f) for f in ('tactil', 'contraste', 'sidebar', 'hover')} for k in ('v1-control', 'v2')}
tk = {k: L(k, 'tokens') for k in ('v1-control', 'v2')}
tkd = {k: {r['archivo'].replace('.html', ''): r for r in tk[k]['archivos']} for k in tk}
man = json.load(open(f'{M}/../MANIFIESTO.json'))['archivos']
nombres = sorted(set(v['v1-control']['tactil']) | set(v['v2']['tactil']))
def metr(k, n):
    d = v[k]; o = {}
    t = d['tactil'].get(n); c = d['contraste'].get(n); s = d['sidebar'].get(n); u = tkd[k].get(n)
    if t: o['bajo24'] = t['bajo24']
    if c and 'claro' in c: o['contraste_claro'] = c['claro']['fallos']; o['contraste_oscuro'] = (c.get('oscuro') or {}).get('fallos')
    if s and s.get('hayMenu'): o['menu_sin_nombre'] = s['sinNombre']
    if u: o['sin_declarar'] = len(u['usados_no_declarados'])
    return o
filas = []
for n in nombres:
    a = metr('v1-control', n) if n in v['v1-control']['tactil'] else None
    b = metr('v2', n) if n in v['v2']['tactil'] else None
    estado = 'nueva' if a is None else 'ausente_en_v2' if b is None else ('identica' if man.get(n + '.html', {}).get('igual_a_v1') else 'modificada')
    f = {'pantalla': n, 'estado': estado, 'v1': a, 'v2': b}
    if a and b:
        f['delta'] = {k: (b[k] - a[k]) for k in b if k in a and isinstance(b[k], (int, float)) and isinstance(a[k], (int, float))}
    filas.append(f)
json.dump(filas, open(f'{M}/delta-v1-v2.json', 'w'), ensure_ascii=False, indent=1)
mod = [f for f in filas if f['estado'] == 'modificada']
suma = lambda k, w: sum((f[w] or {}).get(k, 0) or 0 for f in mod)
print('comparables modificadas:', len(mod), '| identicas:', sum(f['estado'] == 'identica' for f in filas), '| nuevas:', sum(f['estado'] == 'nueva' for f in filas), '| ausentes:', sum(f['estado'] == 'ausente_en_v2' for f in filas))
for k in ('bajo24', 'contraste_claro', 'contraste_oscuro', 'menu_sin_nombre', 'sin_declarar'):
    print(f'{k:18} v1={suma(k,"v1"):4}  v2={suma(k,"v2"):4}  (solo las {len(mod)} modificadas)')
reg = [f['pantalla'] + ' ' + str({k: d for k, d in f['delta'].items() if d > 0}) for f in mod if any(d > 0 for d in f['delta'].values())]
print('REGRESIONES (algún indicador sube):', len(reg)); [print('  ', r) for r in reg]
nuevas = [(f['pantalla'], f['v2']) for f in filas if f['estado'] == 'nueva']
print('NUEVAS:'); [print('  ', n, m) for n, m in nuevas]
