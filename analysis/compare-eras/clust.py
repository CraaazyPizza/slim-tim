import pickle,numpy as np,sys
from PIL import Image
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
CAN=64
def canvas(core):
    o=np.zeros((CAN,CAN),np.float32)
    h,w=core.shape
    if h>CAN or w>CAN: return None
    # centre by ink centroid
    ys,xs=np.nonzero(core>0.5)
    if len(ys)==0: return None
    cy,cx=ys.mean(),xs.mean()
    oy=int(round(CAN/2-cy)); ox=int(round(CAN/2-cx))
    for y in range(h):
        ty=y+oy
        if 0<=ty<CAN:
            x0=max(0,ox); x1=min(CAN,w+ox)
            if x1>x0: o[ty,x0:x1]=core[y,max(0,-ox):max(0,-ox)+(x1-x0)]
    return o
def ncc(a,b,rng=3):
    best=-9
    for dy in range(-rng,rng+1):
        for dx in range(-rng,rng+1):
            bs=np.roll(np.roll(b,dy,0),dx,1)
            u=a-a.mean(); v=bs-bs.mean()
            d=np.sqrt((u*u).sum()*(v*v).sum())
            if d>0: best=max(best,float((u*v).sum()/d))
    return best
ALL={}
for k in ['zb','rs','oq','l9']:
    glyphs=[]
    for P,groups,c5,p,i0,i1,n in R[k]:
        for gi,g in enumerate(groups):
            if gi in (0,5,8): continue      # skip '/' and colons
            x0,x1=g
            sub=P[:,max(0,x0-5):min(P.shape[1],x1+6)].copy()
            if sub.max()<=0: continue
            sub=sub/sub.max()
            rows=np.nonzero(sub.max(1)>0.5)[0]; cols=np.nonzero(sub.max(0)>0.5)[0]
            if len(rows)<20 or len(cols)<5: continue
            core=sub[rows.min():rows.max()+1, cols.min():cols.max()+1]
            c=canvas(core)
            if c is not None: glyphs.append((c,core.shape[0],core.shape[1],gi,i0))
    print('%s: %d glyph instances'%(NAME[k],len(glyphs)))
    # greedy clustering
    cls=[]
    for g in glyphs:
        placed=False
        for c in cls:
            if ncc(c['mean'],g[0])>0.88:
                c['items'].append(g); c['mean']=np.mean([i[0] for i in c['items']],0); placed=True; break
        if not placed: cls.append({'items':[g],'mean':g[0]})
    cls=[c for c in cls if len(c['items'])>=3]
    cls.sort(key=lambda c:-len(c['items']))
    print('   clusters(>=3): ',[len(c['items']) for c in cls])
    ALL[k]=cls
    # montage
    ims=[c['mean'] for c in cls]
    W=len(ims)*(CAN+6)
    can=np.zeros((CAN,W))
    for i,m in enumerate(ims): can[:,i*(CAN+6):i*(CAN+6)+CAN]=m/max(1e-9,m.max())
    Image.fromarray((np.clip(can,0,1)*255).astype(np.uint8)).resize((W*3,CAN*3),Image.LANCZOS).save('analysis/compare-eras/CL_%s.png'%k)
    # per-cluster metrics
    for i,c in enumerate(cls):
        hs=[it[1] for it in c['items']]; ws=[it[2] for it in c['items']]
        print('     cl%d n=%2d  inkH=%.2f+/-%.2f  inkW=%.2f+/-%.2f  W/H=%.4f'%(i,len(c['items']),np.mean(hs),np.std(hs),np.mean(ws),np.std(ws),np.mean(ws)/np.mean(hs)))
pickle.dump({k:[{'mean':c['mean'],'n':len(c['items']),'H':np.mean([i[1] for i in c['items']]),'W':np.mean([i[2] for i in c['items']])} for c in v] for k,v in ALL.items()},open('analysis/compare-eras/clusters.pkl','wb'))
print('saved CL_zb.png CL_rs.png CL_oq.png CL_l9.png')
