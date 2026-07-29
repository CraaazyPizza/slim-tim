import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
R1 = sl(L1_ROWS, L1_X)
Pf = np.array([pp(RES[i]) for i in range(len(FR))]); INK = -Pf
ci = [FR.index(f) for f in CAP]

def par1(v):  # 3-point parabolic vertex
    d = v[0]-2*v[1]+v[2]
    return 0.0 if abs(d)<1e-15 else 0.5*(v[0]-v[2])/d

def align1d(a,b,rad=6):
    a=a-a.mean(); b=b-b.mean()
    n=len(a); best=None
    for s in range(-rad,rad+1):
        aa=a[rad:n-rad]; bb=np.roll(b,s)[rad:n-rad]
        r=float((aa*bb).sum()/np.sqrt((aa*aa).sum()*(bb*bb).sum()))
        if best is None or r>best[1]: best=(s,r)
    s=best[0]; vs=[]
    for k in (s-1,s,s+1):
        aa=a[rad:n-rad]; bb=np.roll(b,k)[rad:n-rad]
        vs.append(float((aa*bb).sum()/np.sqrt((aa*aa).sum()*(bb*bb).sum())))
    return s+par1(vs), best[1]

print('=== 1D drift of the caption layer within f970-989 (vs leave-one-out mean) ===')
print('   dx from column-profile of ink; dy from row-profile of ink; line-1 band')
dxs=[];dys=[]
for i in ci:
    loo = INK[[j for j in ci if j!=i]][:, R1[0], R1[1]].mean(0)
    cur = INK[i][R1[0], R1[1]]
    dx,rx = align1d(cur.sum(0), loo.sum(0), 6)
    dy,ry = align1d(cur.sum(1), loo.sum(1), 6)
    dxs.append(dx); dys.append(dy)
    print('  f%d  dx=%+.3f (r=%.3f)   dy=%+.3f (r=%.3f)'%(FR[i],dx,rx,dy,ry))
dxs=np.array(dxs); dys=np.array(dys)
print('  dx: mean %+.3f  sd %.3f  ptp %.3f'%(dxs.mean(),dxs.std(),dxs.ptp()))
print('  dy: mean %+.3f  sd %.3f  ptp %.3f'%(dys.mean(),dys.std(),dys.ptp()))

# control: what drift does pure noise produce? use caption-free frames
print('\n=== null: same measurement on caption-free frames 1010-1029 vs their own LOO mean ===')
ni=[FR.index(f) for f in range(1010,1030)]
dxn=[];dyn=[]
for i in ni:
    loo = INK[[j for j in ni if j!=i]][:, R1[0], R1[1]].mean(0)
    cur = INK[i][R1[0], R1[1]]
    dx,_=align1d(cur.sum(0),loo.sum(0),6); dy,_=align1d(cur.sum(1),loo.sum(1),6)
    dxn.append(dx); dyn.append(dy)
print('  dx: sd %.3f ptp %.3f | dy: sd %.3f ptp %.3f'%(np.std(dxn),np.ptp(dxn),np.std(dyn),np.ptp(dyn)))

# does averaging help or hurt? measure NCC of (stack of k frames) against an
# INDEPENDENT held-out half, i.e. split-half agreement as a function of k.
print('\n=== split-half: information content of best-1 vs best-k averages (line 1 band) ===')
order=[983,973,974,984,981,982,971,972,980,985,989,988,986,977,970,978,979,987,975,976]
A=[FR.index(f) for f in order[0::2]]; B=[FR.index(f) for f in order[1::2]]
for k in [1,2,3,5,7,10]:
    a=INK[A[:k]][:,R1[0],R1[1]].mean(0); b=INK[B[:k]][:,R1[0],R1[1]].mean(0)
    print('  k=%2d per half:  split-half NCC = %.4f'%(k, ncc(a,b)))
