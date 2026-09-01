#!/usr/bin/env python3
"""Recalcula la tabla de métricas de la §2 desde los archivos y la compara con
el documento de entrega. Si divergen, sale con código 1.

Uso:
    python3 docs/entrega/metricas.py                 # imprime la tabla
    python3 docs/entrega/metricas.py --verifica      # además la contrasta con el HTML

Los originales entregados por DPROMA no están en el repositorio. Se le indica
dónde están con --originales; por omisión busca ./originales junto a este script.
"""
import argparse, json, os, re, sys
from collections import Counter
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PROPUESTAS = os.path.join(RAIZ, "web", "entregables", "propuestas")
DOC = os.path.join(AQUI, "entrega-padron-desarrollo.html")

PANTALLAS = [
    ("Padrón", "27_padron_clientes.html", "padron-clientes.html"),
    ("Ficha",  "21_ficha_cliente.html",   "ficha-cliente.html"),
    ("Alta",   "41_alta_cliente.html",    "alta-cliente.html"),
    ("Editar", "59_editar_cliente.html",  "editar-cliente.html"),
]

FILAS = [
    # (clave, etiqueta para la consola, texto exacto de la primera celda en el HTML)
    ("lineas",          "Líneas de archivo",         "Líneas de archivo"),
    ("simbolos_svg",    "Símbolos SVG de trazo",     "Símbolos SVG de trazo"),
    ("iconos_material", "Iconos Material",           "Iconos Material"),
    ("aria_live",       "Regiones aria-live",        "Regiones aria-live"),
    ("ids_repetidos",   "id repetidos",              "id repetidos"),
    ("input_file",      "Campos type=file",          'Campos type="file"'),
    ("required",        "Campos obligatorios reales","Campos obligatorios reales"),
    ("bajo12",          "Declaraciones bajo 12px",   "Declaraciones bajo 12 px"),
    ("manejadores",     "Manejadores de evento",     "Manejadores de evento"),
]


class Ids(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.append(d["id"])

    # Sin esto, un <use …/> o un <img …/> no pasa por handle_starttag.
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def medir(ruta):
    with open(ruta, encoding="utf-8") as f:
        s = f.read()
    p = Ids()
    p.feed(s)
    repetidos = sum(1 for _, n in Counter(p.ids).items() if n > 1)
    bajo12 = sum(1 for m in re.finditer(r"font-size\s*:\s*([0-9.]+)px", s)
                 if float(m.group(1)) < 12)
    return {
        "lineas": s.count("\n"),
        "simbolos_svg": len(re.findall(r"<symbol\b", s)),
        # Cuenta las apariciones en el fuente, incluida la de dentro de una
        # plantilla de JS: son iconos que la pantalla acaba pintando.
        "iconos_material": len(re.findall(r"""class=["']msi[ "']""", s)),
        "aria_live": len(re.findall(r"aria-live=", s)),
        "ids_repetidos": repetidos,
        "input_file": len(re.findall(r'type="file"', s)),
        "required": len(re.findall(r"\brequired\b(?![-\w])", s)),
        "bajo12": bajo12,
        "manejadores": len(re.findall(r"addEventListener\(", s)),
    }


def tabla_del_documento():
    """Extrae de la §2 del HTML los pares «antes → después» de cada fila."""
    with open(DOC, encoding="utf-8") as f:
        html = f.read()
    cuerpo = re.search(r"El diff medido.*?</table>", html, re.S)
    if not cuerpo:
        sys.exit("No encuentro la tabla de métricas en el documento.")
    filas = {}
    for tr in re.findall(r"<tr>(.*?)</tr>", cuerpo.group(0), re.S):
        celdas = [re.sub(r"<[^>]+>", "", c).replace("&nbsp;", " ")
                  .replace("\u00a0", " ").replace("&amp;", "&")
                  for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if len(celdas) == 5 and not celdas[0].startswith("Medida"):
            filas[celdas[0].strip()] = [c.strip() for c in celdas[1:]]
    return filas


def texto(antes, despues):
    if antes == despues:
        return f"{antes:,}".replace(",", ".") if antes else "0"
    return f"{antes:,} → {despues:,}".replace(",", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--originales", default=os.path.join(AQUI, "originales"),
                    help="carpeta con los HTML originales entregados por DPROMA")
    ap.add_argument("--verifica", action="store_true",
                    help="contrasta las cifras con las del documento y falla si divergen")
    a = ap.parse_args()

    datos = {}
    for nombre, orig, prop in PANTALLAS:
        ro = os.path.join(a.originales, orig)
        rp = os.path.join(PROPUESTAS, prop)
        if not os.path.exists(ro):
            sys.exit(f"Falta el original {ro}\n"
                     f"Indica su carpeta con --originales.")
        datos[nombre] = {"antes": medir(ro), "despues": medir(rp)}

    anchos = max(len(e) for _, e, _ in FILAS)
    print(f"{'':{anchos}}  " + "  ".join(f"{n:>18}" for n, _, _ in PANTALLAS))
    for clave, etiqueta, _ in FILAS:
        cel = [texto(datos[n]['antes'][clave], datos[n]['despues'][clave])
               for n, _, _ in PANTALLAS]
        print(f"{etiqueta:{anchos}}  " + "  ".join(f"{c:>18}" for c in cel))

    if not a.verifica:
        return 0

    doc = tabla_del_documento()
    fallos = []
    for clave, etiqueta, en_doc in FILAS:
        # La fila se localiza por el texto exacto de su primera celda, ya sin
        # etiquetas: dos filas empiezan por «Campos» y buscar por prefijo las
        # confundiría.
        fila = doc.get(en_doc)
        if fila is None:
            fallos.append(f"{etiqueta}: no encuentro la fila «{en_doc}» en el documento")
            continue
        for i, (n, _, _) in enumerate(PANTALLAS):
            esperado = fila[i].replace(" ", " ").strip()
            if esperado in ("—", "-"):
                continue
            real = texto(datos[n]['antes'][clave], datos[n]['despues'][clave])
            if real.replace(".", "") != esperado.replace(".", ""):
                fallos.append(f"{etiqueta} · {n}: el documento dice «{esperado}», "
                              f"los archivos dicen «{real}»")

    if fallos:
        print("\nDIVERGENCIAS:")
        for f in fallos:
            print("  -", f)
        return 1
    print("\nLas cifras del documento coinciden con los archivos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
