import numpy as np, json
from scipy import ndimage as ndi

def polar_tips(mask, ctr=None, nth=2880, rmax=1200):
    ys,xs=np.nonzero(mask)
    if ctr is None:
        ycut=np.percentile(ys,70); ctr=(xs[ys>ycut].mean(), ys[ys>ycut].mean())
    cx,cy=ctr
    th=np.linspace(-np.pi,np.pi,nth,endpoint=False)
    rr=np.arange(0,rmax,1.0)
    R=np.zeros(nth)
    for i,t in enumerate(th):
        x=cx+rr*np.cos(t); y=cy+rr*np.sin(t)
        ok=(x>=0)&(x<mask.shape[1]-1)&(y>=0)&(y<mask.shape[0]-1)
        v=np.zeros_like(rr,bool)
        v[ok]=mask[np.round(y[ok]).astype(int), np.round(x[ok]).astype(int)]
        R[i]= rr[np.nonzero(v)[0][-1]] if v.any() else 0
    return th,R,(cx,cy)

if __name__=='__main__':
    out={}
    for t in ['t55','t64','t72']:
        m=np.load(f'work/xju_mask_{t}.npy')
        th,R,ctr=polar_tips(m)
        Rs=ndi.uniform_filter1d(R,9,mode='wrap')
        N=len(Rs)
        pk=[]
        for i in range(N):
            w=[Rs[(i+k)%N] for k in range(-60,61)]
            if Rs[i]>=max(w) and Rs[i]>300: pk.append(i)
        g=[]
        for i in pk:
            if g and i-g[-1][-1]<=60: g[-1].append(i)
            else: g.append([i])
        if len(g)>1 and (g[0][0]+N-g[-1][-1])<=60: g[0]=g[-1]+g[0]; g.pop()
        tips=[]
        for grp in g:
            i=grp[int(np.argmax([Rs[j] for j in grp]))]
            tips.append((ctr[0]+R[i]*np.cos(th[i]), ctr[1]+R[i]*np.sin(th[i]), R[i], th[i]))
        tips.sort(key=lambda z:z[0])
        print(t,'centre',np.round(ctr,1))
        for x,y,r,a in tips: print('   tip',round(x,1),round(y,1),'r',round(r,1),'th',round(np.degrees(a),1))
        out[t]=dict(ctr=list(map(float,ctr)),tips=[[float(a) for a in z] for z in tips])
        np.save(f'work/xju_{t}_polar.npy', np.stack([th,R]))
    json.dump(out,open('work/xju_tips.json','w'),indent=1)
