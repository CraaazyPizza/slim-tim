import numpy as np, json, sys, os
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from run_2026 import measure
from ratios import ratios

frames = list(range(3830,3879,3)) + list(range(3886,3936,3)) + list(range(3730,3826,6))
rows=[]
for frac in [0.5,0.7,0.85]:
    for n in frames:
        try: r=measure(n,frac)
        except Exception as e: r=None
        if r is None: continue
        t=r['tips']
        q=ratios(t['T2'],t['T3'],t['T4'],r['C23'],r['C34'])
        q.update(frame=n,frac=frac,
                 T2=t['T2'],T3=t['T3'],T4=t['T4'],C23=r['C23'],C34=r['C34'],d=r['d'])
        rows.append(q)
json.dump(rows,open('work/v3_sweep.json','w'))
import collections
for frac in [0.5,0.7,0.85]:
    sub=[r for r in rows if r['frac']==frac]
    print(f'--- frac={frac}  n={len(sub)}')
    for k in ['R_shared','R_own','R_L4Wc','R_L3Wc','R_tip','splay34','L3b','L4']:
        v=np.array([r[k] for r in sub])
        print(f'   {k:9s} mean={v.mean():7.3f} sd={v.std(ddof=1):6.3f}  med={np.median(v):7.3f}  min={v.min():7.3f} max={v.max():7.3f}')
