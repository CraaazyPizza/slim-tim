import numpy as np, json
from skimage import measure
from scipy import ndimage as ndi
from PIL import Image, ImageDraw

def landmarks(mask):
    lab,n=ndi.label(mask); sz=ndi.sum(mask,lab,range(1,n+1))
    main=(lab==int(np.argmax(sz))+1)
    C=max(measure.find_contours(main.astype(float),0.5),key=len)[:,::-1]
    ys,xs=np.nonzero(main); ycut=np.percentile(ys,65)
    cx=xs[ys>ycut].mean(); cy=ys[ys>ycut].mean()
    r=np.hypot(C[:,0]-cx,C[:,1]-cy)
    rs=ndi.uniform_filter1d(r,15,mode='wrap'); N=len(rs)
    def locmax(w):
        out=[]
        for i in range(N):
            if rs[i]>=max(rs[(i+k)%N] for k in range(-w,w+1)): out.append(i)
        g=[]
        for i in out:
            if g and i-g[-1][-1]<=w: g[-1].append(i)
            else: g.append([i])
        if len(g)>1 and (g[0][0]+N-g[-1][-1])<=w: g[0]=g[-1]+g[0]; g.pop()
        return [int(np.median(x)) for x in g]
    pk=locmax(70)
    pk=[i for i in pk if rs[i]>350]
    pk.sort(key=lambda i: C[i,0])   # left to right
    return main,C,(cx,cy),rs,pk

for t in ['t55','t64','t72']:
    m=np.load(f'work/xju_mask_{t}.npy')
    main,C,ctr,rs,pk=landmarks(m)
    print(t,'centre',np.round(ctr,1),'tips:',[ (int(C[i,0]),int(C[i,1]),round(rs[i])) for i in pk])
    np.save(f'work/xju_{t}_C.npy',C); np.save(f'work/xju_{t}_rs.npy',rs)
    json.dump({'ctr':list(map(float,ctr)),'pk':list(map(int,pk))},open(f'work/xju_{t}_pk.json','w'))
