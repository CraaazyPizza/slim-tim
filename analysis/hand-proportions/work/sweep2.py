import numpy as np, json, sys, os
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from run_2026 import measure
from ratios import ratios

def valid(r,q):
    t=r['tips']; T2,T3,T4=[np.array(t[k]) for k in ('T2','T3','T4')]
    if not (T3[1]<T2[1] and T3[1]<T4[1]): return False
    for A,B in [(T2,T3),(T3,T4)]:
        d=np.linalg.norm(A-B)
        if not (40<d<220): return False
    ymax=max(T2[1],T3[1],T4[1])
    for k in ('C23','C34'):
        if not (ymax+70 < r[k][1] < ymax+330): return False
    if not (180<q['L3b']<420 and 120<q['L4']<380): return False
    if not (30<q['Wc']<140): return False
    return True

rows=[]
for frac in [0.5,0.7,0.85]:
    for n in range(3724,4262,2):
        try: r=measure(n,frac)
        except Exception: r=None
        if r is None: continue
        t=r['tips']; q=ratios(t['T2'],t['T3'],t['T4'],r['C23'],r['C34'])
        if not valid(r,q): continue
        q.update(frame=n,frac=frac,T2=t['T2'],T3=t['T3'],T4=t['T4'],C23=r['C23'],C34=r['C34'])
        rows.append(q)
json.dump(rows,open('work/v3_sweep2.json','w'))
for frac in [0.5,0.7,0.85]:
    sub=sorted([r for r in rows if r['frac']==frac],key=lambda r:r['frame'])
    v=np.array([r['R_shared'] for r in sub])
    print(f'frac={frac} n={len(sub)} R_shared mean={v.mean():.4f} sd={v.std(ddof=1):.4f} med={np.median(v):.4f} range=[{v.min():.3f},{v.max():.3f}]')
    print('   frames:', ' '.join(str(r['frame']) for r in sub))
