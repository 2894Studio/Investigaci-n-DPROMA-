"""Comprueba que las citas «…» del campo dice_el_sistema son literales en el md 2.15.0 (el último disponible: idéntico en las 4 ramas que lo traen).
Uso: SP=<scratch> python3 -I validar-citas.py   -> mediciones/v2/citas.json"""
import json, glob, re, unicodedata, os
SP = os.environ['SP']; R = '/home/user/Investigaci-n-DPROMA-/audit/v2'
def n(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[`*_"\'“”‘’]', '', s); s = s.replace('—', '-').replace('–', '-'); return re.sub(r'\s+', ' ', s).strip(' .,;:·')
nueva = n(open(f'{SP}/sistema2150/sistema-diseno.md', encoding='utf-8').read())
vieja = n(open('/home/user/Investigaci-n-DPROMA-/docs/sistema-diseno-sio-dproma.md', encoding='utf-8').read())  # 2.13.3 (mi rama)
fichas = n(open(f'{SP}/v2zip/Actualizacion-12-10-26/FICHAS_TECNICAS.md', encoding='utf-8').read())
tot = ok = 0; resto = []
for f in sorted(glob.glob(f'{R}/raw/[0-9]*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for h in d['f1_cumplimiento']['hallazgos']:
        for m in re.findall(r'«([^»]{20,})»', h.get('dice_el_sistema') or ''):
            ps = [n(p) for p in re.split(r'…|\.\.\.|\[[^\]]*\]', m) if len(n(p)) >= 18]
            if not ps: continue
            tot += 1
            if all(p in nueva for p in ps): ok += 1
            else: resto.append({'pantalla': d['pantalla'], 'id': h['id'], 'cita': m[:140], 'esta_en_FICHAS': all(p in fichas for p in ps), 'esta_en_2_13_3': all(p in vieja for p in ps)})
json.dump({'fragmentos': tot, 'literales_en_2_15_0': ok, 'no_literales': resto}, open(f'{R}/mediciones/v2/citas.json', 'w'), ensure_ascii=False, indent=1)
print(tot, ok, len(resto), 'en FICHAS:', sum(r['esta_en_FICHAS'] for r in resto), 'en 2.13.3:', sum(r['esta_en_2_13_3'] for r in resto))
