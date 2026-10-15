#!/usr/bin/env python3
# §10 «Una regla copiada puede traerse un token que aquí no existe»: usados − declarados debe ser vacío.
# También cuenta los colores hex literales fuera de :root (la regla de fondo del sistema: ningún hex en un componente).
import re, sys, pathlib
for f in sys.argv[1:]:
    s = pathlib.Path(f).read_text(encoding='utf-8')
    css = ''.join(re.findall(r'<style>(.*?)</style>', s, flags=re.S))
    body = re.sub(r'<svg width="0".*?</svg>', '', s, flags=re.S)    # el sprite lleva el degradado del isotipo
    usados = set(re.findall(r'var\((--[\w-]+)', css + body))
    declarados = set(re.findall(r'(--[\w-]+)\s*:', css))
    # hex fuera de los bloques :root
    sin_root = re.sub(r':root[^{]*\{[^}]*\}', '', css)
    sin_root = re.sub(r'@media \(prefers-color-scheme:dark\)\{.*?\n\}\n', '', sin_root, flags=re.S)
    hex_ = re.findall(r'#[0-9A-Fa-f]{3,8}\b', sin_root)
    print(pathlib.Path(f).name, '| tokens usados:', len(usados), '| sin declarar:', sorted(usados - declarados), '| hex fuera de :root:', hex_[:6], len(hex_))
