import numpy as np, json
from PIL import Image
from scipy import ndimage
F="frames/OpSTlDJWFFI"
def disk(r):
    y,x=np.ogrid[-r:r+1,-r:r+1]; return (x*x+y*y)<=r*r

def candidates(n):
    """All dark blobs fully enclosed in the window's bright sky, with descriptors."""
    a=np.asarray(Image.open(f"{F}/f{n:05d}.png").convert("L")).astype(float)[0:1063,280:1636]
    hi=np.percentile(a,85)
    if hi<110: return a,None
    sky=ndimage.binary_opening(a>hi*0.72, np.ones((5,5)))
    lab,k=ndimage.label(sky)
    if k==0: return a,None
    s=ndimage.sum(sky,lab,range(1,k+1))
    if s.max()<150_000: return a,None
    sky=(lab==int(np.argmax(s))+1)
    holes=ndimage.binary_opening(ndimage.binary_fill_holes(sky)&~sky, disk(5))
    lab2,k2=ndimage.label(holes)
    cands=[]
    for i in range(1,k2+1):
        blob=ndimage.binary_fill_holes(lab2==i)
        ar=int(blob.sum())
        if ar<1200: continue
        ys,xs=np.nonzero(blob)
        W=xs.max()-xs.min()+1; H=ys.max()-ys.min()+1
        # reject blobs touching the sky region's own bounding box edges strongly (bands)
        cands.append(dict(blob=blob,area=ar,cx=xs.mean(),cy=ys.mean(),W=int(W),H=int(H),
                          fill=ar/(W*H)))
    return a,cands

def describe(a,c,n):
    blob=c['blob']; ys,xs=np.nonzero(blob)
    y0,x0=ys.mean(),xs.mean(); yy=ys-y0; xx=xs-x0
    C=np.array([[(xx*xx).mean(),(xx*yy).mean()],[(xx*yy).mean(),(yy*yy).mean()]])
    ev,evec=np.linalg.eigh(C)
    a_s=2*np.sqrt(max(ev[1],1e-9)); b_s=2*np.sqrt(max(ev[0],1e-9))
    e1=evec[:,1]; e2=evec[:,0]
    inner=ndimage.binary_erosion(blob,disk(4))
    r=dict(f=n,area=c['area'],W=c['W'],H=c['H'],WH=round(c['W']/c['H'],3),
           fill=round(c['fill'],3),cx=round(x0,1),cy=round(y0,1),
           a=round(a_s,1),b=round(b_s,1),
           ang=round(float(np.degrees(np.arctan2(e1[1],e1[0]))),1),
           hullmed=round(float(np.median(a[blob])),1))
    if inner.sum()>150:
        sm=ndimage.gaussian_filter(a,2.0)
        vals=np.where(inner,sm,-1)
        pk=vals.max()
        thr=max(pk-8, np.median(sm[inner])+0.6*(pk-np.median(sm[inner])))
        top=inner&(sm>=thr)
        hy,hx=ndimage.center_of_mass(top)
        d=np.array([hx-x0,hy-y0])
        r.update(hval=round(float(pk),1),hcon=round(float(pk-np.median(sm[inner])),1),
                 hpix=int(top.sum()),hx=round(float(hx),1),hy=round(float(hy),1),
                 u=round(float(d@e1)/a_s,3), v=round(float(d@e2)/b_s,3))
    return r

# --- track outward from a seed frame where the craft is unambiguous ---
SEED=1650
a,cs=candidates(SEED)
seed=max(cs,key=lambda c:c['area'])
print(f"seed f{SEED}: area {seed['area']} at ({seed['cx']:.0f},{seed['cy']:.0f}) W{seed['W']} H{seed['H']}")
res={}
fails={}
for direction in (+1,-1):
    prev=dict(seed); n=SEED; miss=0
    while True:
        n+=direction
        if n<1290 or n>1900: break
        if miss>25: fails[n]='gave up after 25 consecutive misses'; break
        a,cs=candidates(n)
        if not cs:
            fails[n]='no candidate blobs'; miss+=1; continue
        # choose candidate closest in centroid AND compatible in area
        best=None;bs=1e18
        for c in cs:
            d=np.hypot(c['cx']-prev['cx'], c['cy']-prev['cy'])
            ar=c['area']/prev['area']
            if d>150 or not (0.4<ar<2.5): continue
            score=d+400*abs(np.log(ar))
            if score<bs: bs=score;best=c
        if best is None:
            fails[n]=f'{len(cs)} blobs, none within gate of ({prev["cx"]:.0f},{prev["cy"]:.0f}) area {prev["area"]}'
            miss+=1; continue
        miss=0
        res[n]=describe(a,best,n)
        prev=best
res[SEED]=describe(*candidates(SEED)[:1]+(seed,),SEED) if False else describe(a if False else candidates(SEED)[0],seed,SEED)
ks=sorted(res)
json.dump([res[k] for k in ks],open("analysis/mk4/track.json","w"),indent=1)
print(f"tracked {len(ks)} frames: f{ks[0]}-f{ks[-1]}")
print(f"dropped {len(fails)} frames; first few reasons:")
for k in sorted(fails)[:6]: print(f"  f{k}: {fails[k]}")
print("\n  f     W    H   W/H  fill  hullmed  hi_con hpix    u      v")
for k in ks[::10]:
    r=res[k]
    print(f"{r['f']} {r['W']:4d} {r['H']:4d} {r['WH']:5.2f} {r['fill']:5.2f} {r['hullmed']:7.1f} "
          f"{r.get('hcon',float('nan')):7.1f} {r.get('hpix',0):4d} {r.get('u',float('nan')):6.3f} {r.get('v',float('nan')):6.3f}")
WH=[res[k]['WH'] for k in ks]; AR=[res[k]['area'] for k in ks]
print(f"\nW/H {min(WH):.2f} -> {max(WH):.2f}   area {min(AR)} -> {max(AR)} ({max(AR)/min(AR):.1f}x)")
