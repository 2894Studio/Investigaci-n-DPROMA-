"""Arreglos de accesibilidad que FICHAS_TECNICAS.md (§«Defectos reales de accesibilidad encontrados y corregidos») dice haber hecho,
y si siguen en v2. Uso: SP=<scratch> python3 -I regresion-fichas.py"""
import os, json
SP = os.environ['SP']; V1 = f'{SP}/v1flat'; V2 = f'{SP}/v2zip/Actualizacion-12-10-26'; R = '/home/user/Investigaci-n-DPROMA-/audit/v2'
rd = lambda d, n: open(f'{d}/{n}.html', encoding='utf-8').read()
cnt = lambda d, n, s: rd(d, n).count(s)
out = []
for n in ('26_estados_de_pantalla', '33_cfe_detalle', '42_alta_tramite_gestoria', '43_alta_tramite_vehicular', '44_alta_tramite_cfe'):
    out.append({'pantalla': n, 'arreglo': '`<header class="p4">` duplicaba role="banner" → `<div class="p4">`', 'ocurrencias_v1': cnt(V1, n, '<header class="p4"'), 'ocurrencias_v2': cnt(V2, n, '<header class="p4"'), 'perdido': cnt(V1, n, '<header class="p4"') == 0 and cnt(V2, n, '<header class="p4"') > 0})
for n in ('24_tickets', '33_cfe_detalle', '01_login'):
    out.append({'pantalla': n, 'arreglo': '`--text-3-fuerte` en textos que no pasaban 4,5:1', 'ocurrencias_v1': cnt(V1, n, 'text-3-fuerte'), 'ocurrencias_v2': cnt(V2, n, 'text-3-fuerte'), 'perdido': cnt(V1, n, 'text-3-fuerte') > 0 and cnt(V2, n, 'text-3-fuerte') == 0})
out.append({'pantalla': '57_menu_cuenta', 'arreglo': 'sin `role="menu"` mal aplicado (aria-required-children)', 'ocurrencias_v1': cnt(V1, '57_menu_cuenta', 'role="menu"'), 'ocurrencias_v2': cnt(V2, '57_menu_cuenta', 'role="menu"'), 'perdido': cnt(V1, '57_menu_cuenta', 'role="menu"') == 0 and cnt(V2, '57_menu_cuenta', 'role="menu"') > 0})
json.dump(out, open(f'{R}/mediciones/v2/regresion-fichas.json', 'w'), ensure_ascii=False, indent=1)
print(sum(o['perdido'] for o in out), 'de', len(out), 'arreglos documentados en FICHAS se han perdido en v2')
