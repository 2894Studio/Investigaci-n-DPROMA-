#!/usr/bin/env bash
# Valida los instrumentos contra HTML sintético de respuesta conocida. Si falla, no se mide con ellos.
# Uso: SP=<scratch> bash verificar-fixtures.sh
set -e
cd "$(dirname "$0")"; export NODE_PATH=${NODE_PATH:-/opt/node22/lib/node_modules}
export MDIR="$PWD/fixtures" PORT=8734 OUT="$(mktemp -d)" SP="${SP:-$OUT}"
(cd fixtures && python3 -m http.server 8734 --bind 127.0.0.1 >/dev/null 2>&1 & echo $! > "$OUT/pid"); sleep 1
for i in contraste tactil sidebar; do node $i.cjs >/dev/null; done
(mkdir -p "$OUT/web" && cd "$OUT/web" && echo "<style>:root{--ok:#2F8F6F;--ok-bg:#DCF0E7;--ok-ink:#1D5A46}</style>" > reglas.html && python3 -m http.server 8735 --bind 127.0.0.1 >/dev/null 2>&1 & echo $! > "$OUT/pid2"); sleep 1
REGLAS_PORT=8735 node nuevos.cjs >/dev/null; kill "$(cat "$OUT/pid2")" 2>/dev/null || true
kill "$(cat "$OUT/pid")" 2>/dev/null || true
python3 -I - "$OUT" <<'PY'
import json,sys
o=sys.argv[1]; e=json.load(open('fixtures/ESPERADO.json'))
c=json.load(open(o+'/contraste.json'))['contraste-fx']['claro']
txt=' | '.join(d['txt'] for d in c['detalle'])
assert c['fallos']==len(e['contraste-fx']['fallos_esperados']), c
assert all(any(x in d['txt'] for d in c['detalle']) for x in e['contraste-fx']['fallos_esperados'])
assert not any(x in txt for x in e['contraste-fx']['no_deben_aparecer']), txt
t=json.load(open(o+'/tactil.json'))['tactil-fx']; assert (t['total'],t['bajo24'])==(3,2), t
s=json.load(open(o+'/sidebar.json'))['sidebar-fx']; assert (s['total'],s['sinNombre'])==(3,1), s
n=json.load(open(o+'/nuevos.json'))['nuevos-fx']
for k,v in e['nuevos-fx'].items():
    a,b=k.split('.'); assert n[a][b]==v, (k,n[a][b],v)
print('FIXTURES OK: contraste 3/3 fallos exactos, tactil 2/3, menu lateral 1/3, instrumentos nuevos 12/12')
PY
