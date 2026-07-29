import numpy as np, json, os, sys
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from ratios import ratios

# ---- 2011 ----
tips=json.load(open('work/xju_tips.json'))
res2011={}
for tk in ['t55','t64']:
    T=[t[:2] for t in tips[tk]['tips']]
    for fr in [70,85]:
        d=json.load(open(f'work/xju_land_{tk}_f{fr}.json'))
        res2011[(tk,fr)]=ratios(T[1],T[2],T[3],d['C23'],d['C34'])
keys=['R_shared','R_own','R_L4Wc','R_L3Wc','R_tip','L4','L3b','L3','Wc','splay34']
print('=== 2011 print (Xju_CY5ZESA, 97-frame median stack) ===')
for k in keys:
    v=np.array([res2011[c][k] for c in res2011])
    print(f'  {k:9s} {v.mean():8.3f}  spread {v.min():.3f}..{v.max():.3f}')

# ---- 2026 ----
rows=json.load(open('work/v3_sweep2.json'))
shots={'B(3724-3830)':(3724,3830),'A(3831-3878)':(3831,3878),'C(3879-3935)':(3879,3935),
       'D(3936-4100)':(3936,4100),'E(4101-4260)':(4101,4260)}
print('\n=== 2026 video 3, per shot (frac=0.7) ===')
shotmeans={k:[] for k in keys}
for lab,(a,b) in shots.items():
    s=[r for r in rows if r['frac']==0.7 and a<=r['frame']<=b]
    if not s: continue
    line=f'  {lab:14s} n={len(s):3d} '
    for k in ['R_shared','R_L4Wc','R_L3Wc','L4','L3b','Wc','splay34']:
        v=np.array([r[k] for r in s]); line+=f'{k}={v.mean():7.3f}±{(v.std(ddof=1) if len(v)>1 else 0):.3f} '
        if k in shotmeans: shotmeans[k].append(v.mean())
    print(line)
print('\n  pooled over shot means:')
for k in ['R_shared','R_L4Wc','R_L3Wc']:
    v=np.array(shotmeans[k]); print(f'    {k:9s} {v.mean():.3f} ± {v.std(ddof=1):.3f}  (n_shots={len(v)})')
allv=np.array([r['R_shared'] for r in rows if r['frac']==0.7])
print(f'    all valid frames: n={len(allv)} mean={allv.mean():.3f} sd={allv.std(ddof=1):.3f} min={allv.min():.3f} max={allv.max():.3f}')
for f in [0.5,0.85]:
    a=np.array([r['R_shared'] for r in rows if r['frac']==f])
    print(f'    frac={f}: n={len(a)} mean={a.mean():.3f} sd={a.std(ddof=1):.3f}')

# ---- systematic: how far must the cleft move to null the difference? ----
print('\n=== cleft-position sensitivity (the palmar-print vs dorsal-photo systematic) ===')
r11=res2011[('t64',70)]; L4a,L3a=r11['L4'],r11['L3b']
s26=[r for r in rows if r['frac']==0.7 and 3831<=r['frame']<=3935]
L4b=np.mean([r['L4'] for r in s26]); L3bb=np.mean([r['L3b'] for r in s26])
print(f'  2011: L4={L4a:.0f} L3b={L3a:.0f} R={L4a/L3a:.3f}')
print(f'  2026: L4={L4b:.0f} L3b={L3bb:.0f} R={L4b/L3bb:.3f}')
print('  moving the 2026 cleft DISTALLY by d (px and % of L3b):')
for pct in [0,5,10,15,20,25,30,40,50,58]:
    d=pct/100*L3bb
    print(f'     d={d:6.1f} ({pct:2d}%)  R_2026={(L4b-d)/(L3bb-d):.3f}')
print('  moving the 2011 cleft PROXIMALLY by d (px and % of L3b):')
for pct in [0,5,10,15,20,25,30,40,50]:
    d=pct/100*L3a
    print(f'     d={d:6.1f} ({pct:2d}%)  R_2011={(L4a+d)/(L3a+d):.3f}')
