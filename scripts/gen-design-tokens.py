#!/usr/bin/env python3
"""Genera web/design-tokens.json (formato DTCG) a partir de los dos bloques
:root de web/entregables/reglas-de-diseno.html — nunca a mano. Fuente de
verdad: el CSS real de la página renderizada. Re-ejecutar tras cada cambio
de token vía la skill sio-dproma-design-sync.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_HTML = REPO_ROOT / "web/entregables/reglas-de-diseno.html"
OUT_JSON = REPO_ROOT / "web/design-tokens.json"

COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$|^rgba?\(|^color-mix\(")
DIMENSION_RE = re.compile(r"^-?[\d.]+px$")
FONT_FAMILY_HINT = {"font-ui", "font-brand"}

# Grupos por prefijo de nombre de token -> ruta DTCG (grupo.subgrupo)
GROUPS = [
    ("marca-", "marca"),
    ("chrome-", "chrome"),
    ("serie-", "grafica.serie"),
    ("sp-", "espaciado"),
    ("r-", "radio"),
    ("sh-", "sombra"),
    ("fs-", "tipografia.tamano"),
    ("font-", "tipografia.familia"),
]


def classify(name: str, value: str) -> tuple[str, str]:
    """Devuelve (grupo_dtcg, $type) para un token."""
    for prefix, group in GROUPS:
        if name.startswith(prefix):
            break
    else:
        group = "color" if COLOR_RE.match(value) else "base"

    if name in FONT_FAMILY_HINT:
        return "tipografia.familia", "fontFamily"
    if DIMENSION_RE.match(value):
        return group, "dimension"
    if value.startswith(("0 ", "0px ")) or group == "sombra":
        return group, "shadow"
    if COLOR_RE.match(value):
        return group, "color"
    return group, "other"


def extract_root_block(css: str, start_idx: int) -> str:
    """Desde el índice de '{' que abre un :root, devuelve su contenido hasta el '}' que cierra."""
    depth = 0
    i = start_idx
    body_start = None
    while i < len(css):
        if css[i] == "{":
            depth += 1
            if depth == 1:
                body_start = i + 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return css[body_start:i]
        i += 1
    raise ValueError("Bloque :root sin cerrar")


COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def parse_tokens(block: str) -> dict[str, str]:
    block = COMMENT_RE.sub("", block)
    tokens = {}
    for decl in block.split(";"):
        decl = decl.strip()
        if not decl or not decl.startswith("--"):
            continue
        name, _, value = decl.partition(":")
        tokens[name.strip().lstrip("-")] = value.strip()
    return tokens


def build_dtcg(light: dict[str, str], dark: dict[str, str]) -> dict:
    root: dict = {}
    all_names = sorted(set(light) | set(dark))
    for name in all_names:
        light_val = light.get(name)
        dark_val = dark.get(name, light_val)
        if light_val is None:
            continue
        group, dtcg_type = classify(name, light_val)
        node = root
        for part in group.split("."):
            node = node.setdefault(part, {})
        entry = {"$type": dtcg_type, "$value": light_val}
        if dark_val != light_val:
            entry["$extensions"] = {
                "com.dproma.theme": {"light": light_val, "dark": dark_val}
            }
        node[name] = entry
    return root


def main() -> None:
    css = SOURCE_HTML.read_text(encoding="utf-8")

    first_root = css.index(":root")
    light_block = extract_root_block(css, css.index("{", first_root))

    dark_anchor = css.index("prefers-color-scheme: dark")
    dark_root = css.index(":root", dark_anchor)
    dark_block = extract_root_block(css, css.index("{", dark_root))

    light_tokens = parse_tokens(light_block)
    dark_tokens = parse_tokens(dark_block)

    dtcg = build_dtcg(light_tokens, dark_tokens)
    dtcg = {
        "$description": (
            "Tokens de SIO-DPROMA en formato DTCG (Design Tokens Community Group). "
            "Generado automáticamente desde web/entregables/reglas-de-diseno.html — "
            "nunca editar este archivo a mano, correr scripts/gen-design-tokens.py de nuevo."
        ),
        **dtcg,
    }

    OUT_JSON.write_text(json.dumps(dtcg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Escrito {OUT_JSON.relative_to(REPO_ROOT)} — {len(light_tokens)} tokens ({len(dark_tokens)} con variante oscura).")


if __name__ == "__main__":
    sys.exit(main())
