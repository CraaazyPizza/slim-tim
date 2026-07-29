import sys,numpy as np
from PIL import Image
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
res={}
for pre,label,colgroups in [('analysis/compare-eras/zb','zb2011',None),('analysis/compare-eras/rs','rs2011',None),
                            ('analysis/compare-eras/oq','oq2026',None),('analysis/compare-eras/l9','l92026',None)]:
    A=np.load(pre+'_A.npy'); P=np.clip(A,0,None).mean(0)
    H,W=P.shape; thr=P.max()*0.28; ink=(P>thr); h=ink.sum(0)
    groups=[];cur=None
    for x in range(W):
        if h[x]>0:
            cur=[x,x] if cur is None else [cur[0],x]
        else:
            if cur: groups.append(tuple(cur)); cur=None
    if cur: groups.append(tuple(cur))
    groups=[g for g in groups if g[1]-g[0]>=6]
    # colon = group whose max ink height is < 0.62 * median of large groups
    mh=[ink[:,a:b+1].sum(0).max() for a,b in groups]
    med=np.median(mh)
    cols=[(g,m) for g,m in zip(groups,mh) if m<0.72*med and (g[1]-g[0]+1)<=20]
    # subpixel centroid in x of each colon
    cens=[]
    for (a,b),m in cols:
        wgt=np.clip(P[:,a:b+1],0,None).sum(0)
        xs=np.arange(a,b+1)
        cens.append(float((wgt*xs).sum()/wgt.sum()))
    print('%-8s groups=%d medInkH=%.0f  colon candidates x=%s'%(label,len(groups),med,[round(c,2) for c in cens]))
    if len(cens)>=2:
        c1,c2=cens[0],cens[-1]
        p=(c2-c1)/3.0
        print('         colon1=%.2f colon2=%.2f  delta=%.2f  => pitch=%.3f px'%(c1,c2,c2-c1,p))
        res[label]=(c1,c2,p,P,groups,ink)
        np.save(pre+'_P2.npy',P); np.save(pre+'_cells.npy',np.array([c1,p]))
print()
for k,v in res.items(): print('%-8s pitch %.3f'%(k,v[2]))
