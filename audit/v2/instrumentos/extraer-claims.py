"""Extrae las afirmaciones altas/críticas de cada ficha para la verificación adversarial.
El verificador recibe SOLO la afirmación (lo que se dice que hay) y el archivo, nunca el razonamiento del autor."""
import json, glob, os, sys
R = '/home/user/Investigaci-n-DPROMA-/audit/v2'; out = []
for f in sorted(glob.glob(f'{R}/raw/[0-9]*.json')):
    d = json.load(open(f, encoding='utf-8')); n = d['pantalla']
    for h in d['f1_cumplimiento']['hallazgos']:
        if h.get('severidad') == 'alta' or (h.get('critico') or {}).get('es'):
            out.append({'id': h['id'], 'pantalla': n, 'tipo': 'f1', 'afirmacion': h.get('hay_en_el_build'), 'regla': h.get('regla'), 'selector': h.get('selector'), 'linea': h.get('linea')})
    for o in d.get('observaciones_resueltas') or []:
        if (o.get('critico') or {}).get('es') or o.get('veredicto') == 'confirmada':
            out.append({'id': f"{n}-obs{o['hoja']}", 'pantalla': n, 'tipo': 'obs', 'afirmacion': ' | '.join(e.get('dato', '') for e in o.get('evidencia', [])), 'regla': None, 'selector': None, 'causa_raiz': o.get('causa_raiz')})
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else f'{R}/claims-a-verificar.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'afirmaciones;', len({c['pantalla'] for c in out}), 'pantallas')
