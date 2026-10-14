"""Validadores deterministas de la auditoría v2 (no son agentes).
Uso: SP=<scratch> python3 -I validar.py [pantalla ...]   -> audit/v2/validacion.json y resumen en stdout.
Comprueba, por cada audit/v2/raw/<pantalla>.json:
  V1 JSON parsea y trae las claves del esquema
  V2 todo § citado existe en sistema-diseno.md 2.15.0
  V3 todo selector: sus clases (.x) e ids (#x) aparecen en el HTML
  V4 reproduce.tipo=codigo: la 'cita' es subcadena literal de esa línea
  V5 reproduce.tipo=captura: el archivo existe
  V6 reproduce.tipo=medicion: el instrumento existe en las mediciones
  V7 todo pp-NNN existe en data/insights/ y pertenece al documento citado
  V8 certeza válida; un hallazgo 'inferido' no puede ser severidad alta ni crítico
  V9 sha256 igual al manifiesto
  V10 cada observación del brief tiene respuesta en observaciones_resueltas
"""
import json, os, re, sys, glob
SP = os.environ['SP']; REPO = '/home/user/Investigaci-n-DPROMA-'; R = f'{REPO}/audit/v2'
V2 = f'{SP}/v2zip/Actualizacion-12-10-26'; RAW = os.environ.get('RAW', f'{R}/raw')
sis = open(f'{SP}/sistema2150/sistema-diseno.md', encoding='utf-8').read()
SECC = set(re.findall(r'(?m)^#{2,5}\s+(\d+(?:\.\d+)*)\.?\s', sis))
man = json.load(open(f'{R}/MANIFIESTO.json'))['archivos']
nue = json.load(open(f'{R}/mediciones/v2/nuevos.json'))
INSTR = {'contraste', 'tactil', 'sidebar', 'hover', 'tokens', 'anchos', 'claims', 'delta', 'lib', 'propio'} | {k for v in nue.values() if isinstance(v, dict) for k in v}
PP = {}
for f in glob.glob(f'{REPO}/data/insights/*.json'):
    t = open(f, encoding='utf-8').read(); PP[os.path.basename(f)] = set(re.findall(r'pp-\d{3}', t))
CERT = {'medido', 'leido_en_codigo', 'inferido'}; DEC = {'adoptar_cliente', 'exigir_cambio', 'ajustar_sistema', 'decidir_diseño', 'sin_accion'}
norm = lambda s: re.sub(r'\s+', ' ', s).strip()

def hallazgos(d):
    for h in (d.get('f1_cumplimiento') or {}).get('hallazgos', []): yield 'f1', h
    for h in d.get('f4_nielsen') or []: yield 'f4', h
    for o in d.get('observaciones_resueltas') or []:
        for e in o.get('evidencia', []): yield 'obs', e

def validar(n):
    err = []; adv = []
    p = f'{RAW}/{n}.json'
    try: d = json.load(open(p, encoding='utf-8'))
    except Exception as e: return [f'V1 JSON no parsea: {e}'], []
    for k in ('pantalla', 'f1_cumplimiento', 'f3_boost_ui', 'sin_datos', 'observaciones_resueltas'):
        if k not in d: err.append(f'V1 falta la clave {k}')
    html = open(f'{V2}/{n}.html', encoding='utf-8', errors='replace').read(); lines = html.split('\n')
    if d.get('sha256') and d['sha256'] != man[n + '.html']['sha256']: err.append('V9 sha256 distinto al manifiesto')
    # V2 §
    textos = json.dumps({k: v for k, v in d.items() if k != 'cobertura'}, ensure_ascii=False)  # cobertura = propuestas de regla NUEVAS: su § aún no existe
    for s in set(re.findall(r'§\s?(\d+(?:\.\d+)*)', textos)):
        if s not in SECC: err.append(f'V2 §{s} no existe en el sistema 2.15.0')
    brief = json.load(open(f'{SP}/briefs2/{n}.json'))
    caps = set(brief['capturas'])
    for ambito, h in hallazgos(d):
        hid = h.get('id') or h.get('n') or ambito
        cert = h.get('certeza'); rep = h.get('reproduce') or {}
        if cert is not None and cert not in CERT: err.append(f'V8 {hid}: certeza «{cert}» inválida')
        sev = h.get('severidad'); crit = (h.get('critico') or {}).get('es')
        if ambito in ('f1',) and cert == 'inferido' and (sev == 'alta' or crit): err.append(f'V8 {hid}: inferido no puede ser alta/crítico')
        if ambito in ('f1',) and not rep: err.append(f'V4 {hid}: sin reproduce')
        if ambito == 'f1' and (h.get('decision') or {}).get('valor') not in DEC: err.append(f'V8 {hid}: decision.valor inválido')
        # V3 selector
        sel = h.get('selector') or ''
        for c in set(re.findall(r'\.([A-Za-z_][\w-]*)', sel)):
            if c not in html: err.append(f'V3 {hid}: la clase .{c} no aparece en el HTML')
        for c in set(re.findall(r'#([A-Za-z_][\w-]*)', sel)):
            if not re.search(r'id=["\']' + re.escape(c) + r'["\']', html): err.append(f'V3 {hid}: el id #{c} no aparece en el HTML')
        # V4/V5/V6
        t = rep.get('tipo')
        if t == 'codigo':
            ln = rep.get('linea'); cita = rep.get('cita') or ''
            if not isinstance(ln, int) or not (1 <= ln <= len(lines)): err.append(f'V4 {hid}: línea {ln} fuera de rango')
            elif norm(cita) not in norm(lines[ln - 1]):
                near = ' '.join(lines[max(0, ln - 2):ln + 1])
                (adv if norm(cita) in norm(near) else err).append(f'V4 {hid}: la cita no es literal en la línea {ln}' + (' (sí en ±1 línea)' if norm(cita) in norm(near) else ''))
        elif t == 'captura':
            fa = os.path.basename(str(rep.get('archivo') or '').split(' ')[0])
            if fa not in caps and not os.path.exists(f'{R}/img/{fa}') and not glob.glob(f'{SP}/**/{fa}', recursive=True): err.append(f'V5 {hid}: la captura {rep.get("archivo")} no existe')
        elif t == 'medicion':
            ins = (rep.get('instrumento') or '').split('.')[0]
            raw_i = (rep.get('instrumento') or '')
            propio = re.match(r'^(script|grep|diff|lectura|ficha|propio|brief|[a-z]\d+[a-z]?$)', raw_i.strip()) or '.cjs' in raw_i or raw_i.startswith('anchos') or '(brief)' in raw_i or 'brief' in raw_i.split()[:1]
            base = re.split(r'[\s(]', ins)[0]
            if base in INSTR or ins in INSTR or propio: pass
            else: err.append(f'V6 {hid}: instrumento «{raw_i[:40]}» no reconocido (ni del brief ni script/grep propio)')
        elif rep and ambito == 'f1': err.append(f'V4 {hid}: reproduce.tipo «{t}» desconocido')
    # V7 pp
    for pp in (d.get('f5_investigacion') or {}).get('pain_points_evaluados', []):
        doc = os.path.basename(pp.get('documento') or '')
        if doc not in PP: err.append(f'V7 {pp.get("pp")}: documento {doc} no existe')
        elif pp.get('pp') not in PP[doc]: err.append(f'V7 {pp.get("pp")} no está en {doc}')
    # V10 observaciones
    hojas = {o['hoja'] for o in brief['observaciones_del_usuario']}; resp = {o.get('hoja') for o in d.get('observaciones_resueltas') or []}
    for h in hojas - resp: err.append(f'V10 observación hoja {h} sin respuesta')
    for o in d.get('observaciones_resueltas') or []:
        if o.get('veredicto') not in ('confirmada', 'parcial', 'no_confirmada', 'sin_datos'): err.append(f'V10 hoja {o.get("hoja")}: veredicto inválido')
    return err, adv

if __name__ == '__main__':
    nombres = sys.argv[1:] or sorted(os.path.basename(f)[:-5] for f in glob.glob(f'{RAW}/*.json'))
    out = {}; tot = 0
    for n in nombres:
        e, a = validar(n); out[n] = {'errores': e, 'avisos': a}; tot += len(e)
        print(f'{n:28} errores={len(e):3} avisos={len(a)}')
        for x in e[:12]: print('    ✗', x[:170])
    json.dump(out, open(f'{R}/validacion.json', 'w'), ensure_ascii=False, indent=1)
    print('TOTAL errores:', tot)
