#!/usr/bin/env python3 -I
"""Contraste entre las superficies del :root de la maqueta (47/28) y de pares de texto citados en los briefs. Solo cálculo."""
def L(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda v: v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def C(a, b):
    x, y = sorted([L(a), L(b)], reverse=True); return round((x + .05) / (y + .05), 2)
PARES = {
 'claro  surface / surface-2 (cuerpo / franja)': ('#FAFCFD', '#E7EDF3'),
 'claro  surface / bg (tarjeta / lienzo)': ('#FAFCFD', '#F2F5F7'),
 'claro  bg / surface-2': ('#F2F5F7', '#E7EDF3'),
 'oscuro surface / surface-2': ('#171F2C', '#1D2735'),
 'oscuro surface / bg': ('#171F2C', '#10161F'),
 'oscuro bg / surface-2': ('#10161F', '#1D2735'),
 'claro  text-3 sobre surface-2 (rótulo de franja)': ('#5C6675', '#E7EDF3'),
 'claro  link sobre surface-2 (enlace de franja)': ('#2F6B3C', '#E7EDF3'),
 'claro  block-ink sobre block-bg (pill de cabecera)': ('#6D4FA3', '#EDEBF7'),
 'claro  surface-hover / surface-2 (hover del botón de paso)': ('#DCE7E1', '#E7EDF3'),
}
for k, (a, b) in PARES.items(): print(f'{C(a, b):>5}  {k}')
