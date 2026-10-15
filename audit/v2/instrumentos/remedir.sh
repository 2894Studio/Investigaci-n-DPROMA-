#!/usr/bin/env bash
# Vuelve a medir una carpeta de pantallas con los mismos medidores de la revisión y la compara con la base.
# Uso: bash remedir.sh <carpeta_con_los_html_nuevos> [carpeta_de_salida]
# 1) valida los medidores con HTML de respuesta conocida; 2) repite barrido, táctil, contraste, menú, tokens e instrumentos nuevos;
# 3) imprime qué se cerró, qué persiste y qué empeoró frente a audit/v2/mediciones/v2/.
set -e
AQUI="$(cd "$(dirname "$0")" && pwd)"; V2="$AQUI/.."; REPO="$V2/../.."
NUEVA="$(cd "$1" && pwd)"; SALIDA="${2:-$V2/mediciones/remedicion-$(date +%F)}"; mkdir -p "$SALIDA"
export NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}" MDIR="$NUEVA" OUT="$SALIDA" SP="$SALIDA" PORT=8741 REGLAS_PORT=8742
echo "== Validando los medidores con HTML de respuesta conocida"; bash "$AQUI/verificar-fixtures.sh" | tail -1
RG="$(mktemp -d)"; cp "$REPO/web/entregables/reglas-de-diseno.html" "$RG/reglas.html"
(cd "$NUEVA" && python3 -m http.server $PORT --bind 127.0.0.1 >/dev/null 2>&1 & echo $! > "$SALIDA/.pid1")
(cd "$RG" && python3 -m http.server $REGLAS_PORT --bind 127.0.0.1 >/dev/null 2>&1 & echo $! > "$SALIDA/.pid2")
trap 'kill $(cat "$SALIDA/.pid1" "$SALIDA/.pid2") 2>/dev/null; rm -f "$SALIDA"/.pid*' EXIT; sleep 1
cd "$AQUI"
echo "== Barrido por patrón"; python3 -I barrido.py "$NUEVA" "$SALIDA/barrido.json" --comparar "$V2/mediciones/v2/barrido.json"
echo "== Midiendo (táctil, contraste, menú, instrumentos nuevos)"
for i in tactil contraste sidebar nuevos; do node $i.cjs >/dev/null; done
python3 -I tokens.py "$NUEVA" "$RG/reglas.html" "$SALIDA/tokens.json" >/dev/null
echo "== Totales frente a la base"; python3 -I comparar_medidas.py "$V2/mediciones/v2" "$SALIDA"
