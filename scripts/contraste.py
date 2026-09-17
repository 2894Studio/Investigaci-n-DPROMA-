#!/usr/bin/env python3
"""Medición de contraste y separación de color para SIO-DPROMA.

§1.7 pide contraste medido, no estimado, y contra todos los fondos donde el color
puede caer. §1.4 pide además separación entre series medida una contra otra, en
visión normal y bajo protanopia. No había forma de reproducir ninguna de las dos
cifras dentro del repositorio; esto la da.

Sin dependencias. Uso:
    python3 scripts/contraste.py ratio  <fg> <bg>
    python3 scripts/contraste.py mix    <color> <pct> <base>   # equivale a color-mix srgb
    python3 scripts/contraste.py delta  <c1> <c2>              # OKLab x100, normal y protanopia
"""
import sys

def hex2rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

def rgb2hex(c):
    return '#' + ''.join(f'{max(0,min(255,round(v*255))):02X}' for v in c)

def _lin(c):  # sRGB -> lineal
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4

def luminancia(rgb):
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126*r + 0.7152*g + 0.0722*b

def ratio(fg, bg):
    l1, l2 = luminancia(hex2rgb(fg)), luminancia(hex2rgb(bg))
    lo, hi = sorted((l1, l2))
    return (hi + 0.05) / (lo + 0.05)

def mezcla(color, pct, base):
    """color-mix(in srgb, <color> <pct>%, <base>) — interpola en sRGB, como el navegador."""
    a, b, t = hex2rgb(color), hex2rgb(base), pct/100
    return rgb2hex(tuple(a[i]*t + b[i]*(1-t) for i in range(3)))

def oklab(rgb):
    r, g, b = (_lin(c) for c in rgb)
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b) ** (1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b) ** (1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b) ** (1/3)
    return (0.2104542553*l + 0.7936177850*m - 0.0040720468*s,
            1.9779984951*l - 2.4285922050*m + 0.4505937099*s,
            0.0259040371*l + 0.7827717662*m - 0.8086757660*s)

def protanopia(rgb):
    """Brettel/Viénot simplificado sobre LMS, para comparar series entre sí."""
    r, g, b = (_lin(c) for c in rgb)
    L = 17.8824*r + 43.5161*g + 4.11935*b
    M = 3.45565*r + 27.1554*g + 3.86714*b
    S = 0.0299566*r + 0.184309*g + 1.46709*b
    L = 2.02344*M - 2.52581*S              # el cono L se reconstruye desde M y S
    r2 = 0.0809444479*L - 0.130504409*M + 0.116721066*S
    g2 = -0.0102485335*L + 0.0540193266*M - 0.113614708*S
    b2 = -0.000365296938*L - 0.00412161469*M + 0.693511405*S
    def gam(c):
        c = max(0.0, min(1.0, c))
        return 12.92*c if c <= 0.0031308 else 1.055*c**(1/2.4) - 0.055
    return tuple(gam(c) for c in (r2, g2, b2))

def delta(c1, c2):
    a, b = hex2rgb(c1), hex2rgb(c2)
    def d(x, y):
        p, q = oklab(x), oklab(y)
        return 100 * sum((p[i]-q[i])**2 for i in range(3)) ** 0.5
    return d(a, b), d(protanopia(a), protanopia(b))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'ratio':
        fg, bg = sys.argv[2], sys.argv[3]
        r = ratio(fg, bg)
        print(f'{fg} sobre {bg}: {r:.2f}:1  '
              f'[texto {"OK" if r>=4.5 else "FALLA"} · gráfico {"OK" if r>=3 else "FALLA"}]')
    elif cmd == 'mix':
        print(mezcla(sys.argv[2], float(sys.argv[3]), sys.argv[4]))
    elif cmd == 'delta':
        n, p = delta(sys.argv[2], sys.argv[3])
        print(f'{sys.argv[2]} vs {sys.argv[3]}: ΔE normal {n:.1f} · protanopia {p:.1f}  '
              f'[suelo 15 → {"OK" if min(n,p)>=15 else "FALLA"}]')
    else:
        print(__doc__); sys.exit(1)
