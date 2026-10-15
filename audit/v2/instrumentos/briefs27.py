"""Dossier medido de las 27 pantallas que solo tuvieron medición automática.
Uso: SP=<scratch> python3 -I briefs27.py  -> $SP/briefs2/<pantalla>.json  (mismo formato que briefs.py, sin observaciones ni v1)"""
import json, os, re, glob
SP = os.environ['SP']; R = '/home/user/Investigaci-n-DPROMA-/audit'
M = f'{R}/v2/mediciones/v2'; V2 = f'{SP}/v2zip/Actualizacion-12-10-26'
L = lambda p: json.load(open(p))
tact, cont, side, tok, nue, anc, cla, bar = (L(f'{M}/{f}.json') for f in ('tactil', 'contraste', 'sidebar', 'tokens', 'nuevos', 'anchos', 'claims', 'barrido'))
nue = nue['v2'] if 'v2' in nue and isinstance(nue['v2'], dict) else nue
man = L(f'{R}/v2/MANIFIESTO.json')
tokd = {r['archivo'].replace('.html', ''): r for r in tok['archivos']}
fich = open(f'{V2}/FICHAS_TECNICAS.md', encoding='utf-8').read()
MOVIL = {'04_app_personal', '09_app_checklist_instalacion', '11_app_login_2fa_offline', '12_app_checado_asistencia', '14_app_checado_oficina', '29_instalador_orden'}
N27 = open(f'{SP}/n27.txt').read().strip().split(',')
def ficha(n):
    out = []
    for b in re.split(r'(?m)^(?=#{1,3} )', fich):
        head = b.split('\n', 1)[0]
        if re.search(r'`' + re.escape(n) + r'(\.html)?`', head): out.append(b.strip())
    return ('\n\n'.join(out))[:6000] or None
os.makedirs(f'{SP}/briefs2', exist_ok=True)
for n in N27:
    c = cla['por_pantalla'].get(n + '.html', {})
    b = {'pantalla': n, 'archivo': f'{V2}/{n}.html', 'sha256': man['archivos'][n + '.html']['sha256'], 'url': f'http://127.0.0.1:8732/{n}.html',
         'modo': 'cobertura' if n in MOVIL else 'cumplimiento', 'observaciones_del_usuario': [],
         'estado_vs_pdf_del_cliente': {'codigos_declarados': c.get('codigos'), 'lt12_medido': c.get('lt12_medido'), 'lt12_pdf_despues': c.get('lt12_pdf_despues'),
             'lectura': 'NO_ALINEADO: el archivo recibido no muestra los cambios que el PDF declara' if any(e == 'NO_confirmado' for e in (c.get('codigos') or {}).values()) else ('alineado' if c else 'no_listado_en_pdf')},
         'mediciones_v2': {'tactil_bajo24': tact.get(n), 'contraste': cont.get(n), 'menu_1000px': side.get(n),
             'tokens_usados_no_declarados': tokd.get(n, {}).get('usados_no_declarados'), 'tokens_valores_divergentes': tokd.get(n, {}).get('valores_divergentes'),
             'instrumentos_nuevos': nue.get(n), 'anchos_1440_1280_1024': anc.get(n)},
         'barrido_por_patron': bar['por_archivo'].get(n), 'ficha_tecnica_del_cliente': ficha(n),
         'capturas': sorted(os.path.basename(x) for x in glob.glob(f'{SP}/shots2/{n}--*.png'))}
    json.dump(b, open(f'{SP}/briefs2/{n}.json', 'w'), ensure_ascii=False, indent=1)
print(len(N27), 'dossiers en', f'{SP}/briefs2')
