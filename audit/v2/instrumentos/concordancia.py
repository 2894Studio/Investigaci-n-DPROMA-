"""Concordancia de la réplica ciega: coincidencia de §, de veredicto de observación y de hallazgos críticos entre el original y la réplica."""
import json, re, sys
R = '/home/user/Investigaci-n-DPROMA-/audit/v2'
def secs(d):
    t = json.dumps({k: v for k, v in d.items() if k in ('f1_cumplimiento',)}, ensure_ascii=False)
    return set(re.findall(r'§\s?(\d+(?:\.\d+)*)', t))
def crit(d): return {(h.get('selector') or '')[:25] for h in d['f1_cumplimiento']['hallazgos'] if h.get('severidad') == 'alta' or (h.get('critico') or {}).get('es')}
res = {}
for n in sys.argv[1:]:
    a = json.load(open(f'{R}/raw/{n}.json')); b = json.load(open(f'{R}/replica/{n}.json'))
    sa, sb = secs(a), secs(b); j = len(sa & sb) / len(sa | sb) if sa | sb else 1
    va = [o['veredicto'] for o in a['observaciones_resueltas']]; vb = [o['veredicto'] for o in b['observaciones_resueltas']]  # una observación por pantalla en la réplica
    res[n] = {'§_original': sorted(sa), '§_replica': sorted(sb), 'jaccard_§': round(j, 2), 'solo_original': sorted(sa - sb), 'solo_replica': sorted(sb - sa),
              'veredictos_obs': list(zip(va, vb)), 'obs_coinciden': va[:len(vb)] == vb[:len(va)],
              'n_hallazgos': (len(a['f1_cumplimiento']['hallazgos']), len(b['f1_cumplimiento']['hallazgos']))}
    print(n, 'obs coinciden:', res[n]['obs_coinciden'], '| Jaccard §:', res[n]['jaccard_§'], '| obs:', res[n]['veredictos_obs'], '| solo orig', res[n]['solo_original'], '| solo réplica', res[n]['solo_replica'])
json.dump(res, open(f'{R}/replica/concordancia.json', 'w'), ensure_ascii=False, indent=1)
if res: print('MEDIA Jaccard §:', round(sum(v['jaccard_§'] for v in res.values()) / len(res), 2))
