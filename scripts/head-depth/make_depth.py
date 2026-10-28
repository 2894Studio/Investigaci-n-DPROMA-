"""Genera el mapa de profundidad de la cabeza de marca 2894 para el parallax web.

Uso (con torch, transformers, scipy y pillow instalados):
    python scripts/head-depth/make_depth.py web/2894-head/assets/head.png web/2894-head/assets/head-depth.png

1. Estima profundidad con Depth Anything V2 sobre el PNG compuesto en blanco.
2. La normaliza solo dentro de la silueta opaca.
3. Fuera de la silueta (borde blanco, sombra, transparencia) extiende el valor
   del borde más cercano, para que la silueta y la sombra se muevan juntas y
   nunca se desgarren.
4. Suaviza para que la pincelada y las nubes no generen relieve propio.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage
from transformers import pipeline

MODEL = "depth-anything/Depth-Anything-V2-Small-hf"


def harmonic_fill(d, known, scale=4, iters=300):
    """Rellena lo desconocido con una superficie suave que continúa el borde."""
    h, w = d.shape
    small = lambda a: np.asarray(Image.fromarray(a).resize((w // scale, h // scale), Image.BILINEAR))
    ds, ks = small(d.astype(np.float32)), small(known.astype(np.float32)) > 0.99
    # Arranca desde el valor del borde más cercano y lo relaja hasta quitar las costuras.
    _, (iy, ix) = ndimage.distance_transform_edt(~ks, return_indices=True)
    f = ds[iy, ix]
    for _ in range(iters):
        f = np.where(ks, ds, ndimage.uniform_filter(f, size=3, mode="nearest"))
    return np.asarray(Image.fromarray(f).resize((w, h), Image.BICUBIC))


def main(src, dst):
    im = Image.open(src).convert("RGBA")
    flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat.alpha_composite(im)

    depth = pipeline("depth-estimation", model=MODEL)(flat.convert("RGB"))["depth"]
    d = np.asarray(depth.resize(im.size, Image.BICUBIC), dtype=np.float32)

    alpha = np.asarray(im)[..., 3]
    # Interior de la cabeza: opaco y alejado del borde blanco del sticker.
    inside = ndimage.binary_erosion(alpha >= 250, iterations=4)

    lo, hi = np.percentile(d[inside], [1, 99.7])
    d = np.clip((d - lo) / (hi - lo), 0, 1)

    d = ndimage.gaussian_filter(d, sigma=2.5)
    d = np.where(inside, d, harmonic_fill(d, inside))
    # Transición suave en el borde, sin tocar el interior de la cara.
    edge = ndimage.gaussian_filter(inside.astype(np.float32), sigma=3)
    d = edge * d + (1 - edge) * ndimage.gaussian_filter(d, sigma=4)
    Image.fromarray((d * 255).round().astype(np.uint8), "L").save(dst, optimize=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
