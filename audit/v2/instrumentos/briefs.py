"""Ensambla el brief de cada pantalla que audita a fondo (todo lo ya medido, para que el auditor no re-mida ni invente).
Uso: SP=<scratch> python3 -I briefs.py   -> $SP/briefs2/<pantalla>.json"""
import json, os, re, glob
SP = os.environ['SP']; R = '/home/user/Investigaci-n-DPROMA-/audit'
M = f'{R}/v2/mediciones'; V2 = f'{SP}/v2zip/Actualizacion-12-10-26'
L = lambda *p: json.load(open(os.path.join(*p)))
tact, cont, side, tok = L(M, 'v2/tactil.json'), L(M, 'v2/contraste.json'), L(M, 'v2/sidebar.json'), L(M, 'v2/tokens.json')
nue, anc, cla, man = L(M, 'v2/nuevos.json'), L(M, 'v2/anchos.json'), L(M, 'v2/claims.json'), L(R, 'v2/MANIFIESTO.json')
dlt = {f['pantalla']: f for f in L(M, 'delta-v1-v2.json')}
tokd = {r['archivo'].replace('.html', ''): r for r in tok['archivos']}
fich = open(f'{V2}/FICHAS_TECNICAS.md', encoding='utf-8').read()
OBS = {  # hoja, texto de la observación (palabras de la persona, resumidas sin añadir nada)
 '24_tickets': [(9, 'Rediseño crítico, parte superior: las dos cajas amarillas no se distribuyen bien.'), (10, 'Sistémico, visto aquí: las cajas (Abiertos/Míos/Todos + Nuevo ticket) chocan con la línea inferior; debe haber siempre margen. En múltiples páginas.')],
 '27_padron_clientes': [(3, 'Estados demasiado específicos («Falta documento», «Incompleto»); recuadro de acciones cortado en todas las filas; «Acciones» debe alinearse a la izquierda de su casilla.'), (12, 'Rediseño crítico del acordeón de sucursales: no es usable ni estético; diseñarlo y documentarlo.')],
 '21_ficha_cliente': [(7, 'Caja «Datos fiscales» innecesariamente alta; «Editar datos fiscales» al final de la línea.')],
 '41_alta_cliente': [], '59_editar_cliente': [],
 '28_instalador_mi_dia': [(13, 'Barra superior sin espacio bajo «Mi día»; contrastar con el flujo de la investigación.')],
 '47_asistente': [(17, 'Rediseño crítico; ¿sección «Chat»?; ¿por qué dos colores, blanco y gris? (captura: la última línea sigue tocando la franja).')],
 '51_acceso': [(0, 'Lista de revisión exhaustiva: «Acceso: no respeta espaciado e interlineado».')],
 '58_altas_como_modal': [(0, 'Lista de revisión exhaustiva: «Altas como modal: información sobrepuesta».')],
 '26_estados_de_pantalla': [(1, 'Icono gris sobre botón verde «Reintentar» en estados de error; debe ser blanco (componente «Patrón de error», transversal).')],
 '22_gestoria': [(1, 'Estado de error de gestoría (22 ó 32, por confirmar): icono gris sobre el botón verde «Reintentar».')],
 '32_cfe_bandeja': [(1, 'Posible pantalla de la observación 1 (22 ó 32, por confirmar).')],
 '05_app_cliente': [(2, 'Portal del cliente móvil («Laura Núñez», identificado por contenido, por confirmar): «Contactar a DPROMA» no uniforme con «Reagendar cita»; icono junto al texto en uno y apartado en otro; reducir texto.')],
 '48_asistencia_rhl': [(5, 'RHL incidentes: el interlineado da sensación de desorden.')],
 '20_tablero': [(6, '«Volumen de las últimas 12 semanas»: gráficas ininteligibles; texto amontonado sobre las barras; dar orden.')],
 '23_viaticos': [(8, '«Monto y excedente»: textos largos en tabla. «Habíamos creado una versión limpia» (probable propuestas/viaticos.html).')],
 '25_consumo_de_material': [(11, '¿Cumple el sistema? Exceso de color. Evaluar soluciones.')],
 '34_instaladores': [(14, 'Agenda: ¿vale cambiarla por la del sistema? ¿Combinables? ¿Cuál es más efectiva?')],
 '46_cuentas_por_cobrar': [(16, 'Las cajas se habían ajustado; existe una vista optimizada con reglas para que no se repitiera (propuestas/cuentas-por-cobrar.html, §13.2–§13.4).')],
 '54_bitacora_descargas': [(18, 'Panel «CON QUÉ FILTROS»: ¿estos filtros tienen sentido para el flujo?')],
 '55_verificacion_pedido': [(19, '«Siguiente» cortado en el borde superior de la tarjeta; debe ir por fuera.')],
 '01_login': [],
 '13_panel_asistencia_rhl': [(5, 'RHL incidentes: el interlineado da sensación de desorden. (El auditor del 48 halló que la «bandeja de incidencias» está en ESTE archivo, no en 48.)')],
}
def ficha(n):
    out = []; blocks = re.split(r'(?m)^(?=#{1,2} )', fich)
    for b in blocks:
        head = b.split('\n', 1)[0]
        if re.search(r'`' + re.escape(n) + r'(\.html)?`', head) or (n.split('_')[0] + '_') in head and n in head: out.append(b.strip())
    return ('\n\n'.join(out))[:6000] or None
ALIAS_V1 = {'48_asistencia_rhl': '13_panel_asistencia_rhl'}  # por contenido; el 13 sigue en el ZIP idéntico a v1
def v1resumen(n):
    p = f'{R}/raw/{ALIAS_V1.get(n, n)}.json'
    if not os.path.exists(p): return None
    d = L(p); h = d['f1_cumplimiento']['hallazgos']
    return {'archivo': f'audit/raw/{n}.json', 'veredicto': d['f1_cumplimiento']['veredicto'], 'n_hallazgos': len(h),
            'hallazgos': [{'id': x['id'], 'sev': x['severidad'], 'regla': x['regla'], 'selector': x.get('selector')} for x in h],
            'f3': d['f3_boost_ui']['puntuacion']}
os.makedirs(f'{SP}/briefs2', exist_ok=True)
for n in OBS:
    c = cla['por_pantalla'].get(n + '.html', {})
    b = {'pantalla': n, 'archivo': f'{V2}/{n}.html', 'sha256': man['archivos'][n + '.html']['sha256'], 'url': f'http://127.0.0.1:8732/{n}.html',
         'observaciones_del_usuario': [{'hoja': h, 'texto': t} for h, t in OBS[n]],
         'estado_vs_pdf_del_cliente': {'codigos_declarados': c.get('codigos'), 'lt12_medido': c.get('lt12_medido'), 'lt12_pdf_despues': c.get('lt12_pdf_despues'),
             'lectura': 'NO_ALINEADO: el archivo recibido no muestra los cambios que el PDF declara' if any(e == 'NO_confirmado' for e in (c.get('codigos') or {}).values()) else ('alineado' if c else 'no_listado_en_pdf')},
         'estado_entrega': dlt.get(n, {}).get('estado'),
         'mediciones_v2': {'tactil_bajo24': tact.get(n), 'contraste': cont.get(n), 'menu_1000px': side.get(n),
             'tokens_usados_no_declarados': tokd.get(n, {}).get('usados_no_declarados'), 'tokens_valores_divergentes': tokd.get(n, {}).get('valores_divergentes'),
             'instrumentos_nuevos': nue.get(n), 'anchos_1440_1280_1024': anc.get(n)},
         'delta_vs_v1': dlt.get(n, {}).get('delta'), 'v1': v1resumen(n), 'nota_v1': ('v1 = 13_panel_asistencia_rhl (misma pantalla renombrada, INFERIDO por contenido)' if n in ALIAS_V1 else None), 'ficha_tecnica_del_cliente': ficha(n),
         'capturas': sorted(os.path.basename(x) for x in glob.glob(f'{SP}/shots2/{n}--*.png'))}
    json.dump(b, open(f'{SP}/briefs2/{n}.json', 'w'), ensure_ascii=False, indent=1)
print(len(OBS), 'briefs en', f'{SP}/briefs2')
