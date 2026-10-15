"""Tokens usados menos declarados, y valor declarado contra el canónico (página de reglas 2.15.0).
Uso: python3 -I tokens.py <carpeta_html> <reglas.html> <salida.json>
Lee estilos en línea y hojas <link rel=stylesheet> locales. No modifica nada."""
import re, json, os, sys, glob
D, REGLAS, OUT = sys.argv[1:4]
def decls(css):
    d = {}
    for m in re.finditer(r'(--[A-Za-z0-9_-]+)\s*:\s*([^;}]+)', css): d.setdefault(m.group(1), []).append(m.group(2).strip())
    return d
reglas = open(REGLAS, encoding='utf-8').read()
root = re.search(r':root\s*\{(.*?)\n\s*\}', reglas, re.S)
canon = {k: v[0] for k, v in decls(root.group(1)).items()} if root else {}
rows = []
for f in sorted(glob.glob(D + '/*.html')):
    src = open(f, encoding='utf-8', errors='replace').read()
    styles = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', src, re.S | re.I))
    externos = []
    for h in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', src, re.I):
        p = os.path.join(D, h)
        if not h.startswith('http') and os.path.exists(p): styles += '\n' + open(p, encoding='utf-8').read(); externos.append(h)
    decl = decls(styles)
    attrs = ' '.join(re.findall(r'style="([^"]*)"', src))
    used = set(re.findall(r'var\(\s*(--[A-Za-z0-9_-]+)', styles + ' ' + attrs))
    # un token declarado con var() a otro también cuenta; los de JS/atributos data no
    dif = {k: {'declarado': v[0], 'canonico': canon[k]} for k, v in decl.items()
           if k in canon and re.sub(r'\s+', '', v[0].lower()) != re.sub(r'\s+', '', canon[k].lower())}
    rows.append({'archivo': os.path.basename(f), 'externos': externos, 'n_declarados': len(decl),
                 'usados_no_declarados': sorted(used - set(decl)), 'valores_divergentes': dif,
                 'valores': {k: v[0] for k, v in decl.items()}})
json.dump({'n_canonicos': len(canon), 'archivos': rows}, open(OUT, 'w'), ensure_ascii=False, indent=1)
roto = [r for r in rows if r['usados_no_declarados']]
print(f"archivos {len(rows)}  canónicos {len(canon)}  con usados−declarados≠∅: {len(roto)}")
for r in roto: print('  ', r['archivo'], ', '.join(r['usados_no_declarados'][:8]))
