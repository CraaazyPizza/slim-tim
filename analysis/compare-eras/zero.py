import pickle,numpy as np
from PIL import Image
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],
     'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],
     'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
T={}
for k in C:
    for i,c in enumerate(C[k]):
        ch=LAB[k][i] if i<len(LAB[k]) else '?'
        T.setdefault((k,ch),[]).append(c)
def outer_width_profile(m):
    mm=m/m.max(); ink=mm>0.45
    rows=np.nonzero(ink.any(1))[0]
    prof=[]
    for r in rows:
        xs=np.nonzero(ink[r])[0]
        prof.append((r,xs.min(),xs.max(),xs.max()-xs.min()+1))
    return rows,prof
print('=== 0 vs 8 discrimination: outer ink width at mid vs quarter heights ===')
for (k,ch),lst in sorted(T.items()):
    if ch not in ('0','8'): continue
    c=max(lst,key=lambda x:x['n']); m=c['mean']
    rows,prof=outer_width_profile(m)
    if len(rows)<10: continue
    h=len(rows); w=np.array([p[3] for p in prof])
    q1,mid,q3=w[int(h*0.25)],w[int(h*0.50)],w[int(h*0.75)]
    print('%-11s %s n=%-3d  width@25%%=%2d  @50%%=%2d  @75%%=%2d   mid/mean(q1,q3)=%.3f  -> %s'%(
        NAME[k],ch,c['n'],q1,mid,q3,mid/((q1+q3)/2), 'ZERO-like (no waist)' if mid/((q1+q3)/2)>0.97 else 'EIGHT-like (waist pinch)'))
print()
print('=== interior stroke orientation inside the zero counter ===')
print('    (Radon-style: variance of bright ridge projected along angle; peak angle = stroke direction)')
for (k,ch),lst in sorted(T.items()):
    if ch!='0': continue
    c=max(lst,key=lambda x:x['n']); m=c['mean'].copy()
    mm=m/m.max()
    ink=mm>0.45
    rows=np.nonzero(ink.any(1))[0]; cols=np.nonzero(ink.any(0))[0]
    # interior region = inside bbox, eroded by ~stroke width (5px)
    r0,r1,c0,c1=rows.min(),rows.max(),cols.min(),cols.max()
    pad=8
    inner=mm[r0+pad:r1-pad+1, c0+pad:c1-pad+1]
    if inner.size<50: print(NAME[k],'too small'); continue
    inner=inner-inner.mean()
    H,W=inner.shape
    ys,xs=np.mgrid[0:H,0:W]; ys=ys-(H-1)/2.; xs=xs-(W-1)/2.
    best=None
    for ang in range(0,180,2):
        th=np.deg2rad(ang)
        # coordinate along the putative stroke direction
        u=xs*np.cos(th)+ys*np.sin(th)          # across the stroke
        # project: sum brightness into bins of u; a stroke perpendicular gives a sharp peak
        bins=np.round(u).astype(int); bins-=bins.min()
        acc=np.bincount(bins.ravel(),weights=inner.ravel(),minlength=bins.max()+1)
        cnt=np.bincount(bins.ravel(),minlength=bins.max()+1).clip(1)
        p=acc/cnt
        v=p.max()-p.min()
        if best is None or v>best[1]: best=(ang,v,p)
    ang=best[0]
    # stroke runs perpendicular to the 'across' axis
    strokeang=(ang+90)%180
    print('%-11s n=%-3d inner %dx%d  across-axis=%3d deg  => interior stroke at %3d deg from horizontal  (contrast %.3f)'%(
        NAME[k],c['n'],H,W,ang,strokeang,best[1]))
# montage of the zeros, big
ims=[]
for k in ['zb','rs','oq','l9']:
    if (k,'0') in T:
        c=max(T[(k,'0')],key=lambda x:x['n']); m=c['mean']; ims.append(m/m.max())
W=sum(i.shape[1]+8 for i in ims); H=max(i.shape[0] for i in ims)
can=np.zeros((H,W)); x=0
for i in ims: can[:i.shape[0],x:x+i.shape[1]]=i; x+=i.shape[1]+8
Image.fromarray((np.clip(can,0,1)*255).astype(np.uint8)).resize((W*8,H*8),Image.LANCZOS).save('analysis/compare-eras/ZEROS.png')
print('\nsaved ZEROS.png (ZB788_2011, RsQCX_2011, Oqw96_2026, l9RAh_2026)')
