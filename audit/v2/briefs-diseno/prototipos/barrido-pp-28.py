#!/usr/bin/env python3 -I
"""Barrido de los pain_points de las 11 entrevistas por palabras de interfaz móvil/cabecera (brief de Mi día, §2.1). Solo lee."""
import json, glob, re, sys, pathlib
base = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/Investigaci-n-DPROMA-/data/insights')
pat = re.compile(r'\b(app|aplicaci[oó]n|m[oó]vil|celular|tel[eé]fono|pantalla|cabecera|agenda|instalador(es)?)\b', re.I)
n = 0
for f in sorted(base.glob('*.json')):
    for p in json.load(open(f)).get('pain_points', []):
        t = p['descripcion'] + ' ' + p.get('evidencia', '')
        if pat.search(t): n += 1; print(f.name[:34], p['id'], p['severidad'], t[:110].replace('\n', ' '))
print('coincidencias:', n)
