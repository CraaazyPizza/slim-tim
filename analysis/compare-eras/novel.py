import pickle,numpy as np
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
NAME={'zb':('ZB788_2011',25.0),'rs':('RsQCX_2011',25.0),'oq':('Oqw96_2026',30000/1001),'l9':('l9RAh_2026',30000/1001)}
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
W=8
ker=np.zeros((2*W,2*W))
ker[:W,:W]=1; ker[W:,W:]=1; ker[:W,W:]=-1; ker[W:,:W]=-1
for k in ['zb','rs','oq','l9']:
    name,fps=NAME[k]
    B=np.load('analysis/compare-eras/%s_band.npy'%k); idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
    runs=np.load('analysis/compare-eras/%s_runs.npy'%k)
    c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
    xc=c5+5.0*p+4
    x0=max(0,int(round(xc-0.45*p))); x1=min(B.shape[2],int(round(xc+0.45*p)))
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    print('=== %s  fps=%.4f  cell x=%d..%d'%(name,fps,x0,x1))
    sps=[]
    for oi in order[:5]:
        a,b=runs[oi]
        if b-a<70: continue
        sub=B[a:b,:,x0:x1].astype(np.float32)
        Hh=np.stack([sub[i]-blur1(sub[i],6) for i in range(len(sub))])
        V=Hh.reshape(len(Hh),-1); V=V-V.mean(1,keepdims=True)
        nr=np.linalg.norm(V,axis=1); nr[nr==0]=1; V=V/nr[:,None]
        M=V@V.T; n=len(M)
        nov=np.full(n,np.nan)
        for i in range(W,n-W):
            nov[i]=(M[i-W:i+W,i-W:i+W]*ker).sum()/(2*W*W)
        v=nov[~np.isnan(nov)]
        thr=np.nanpercentile(nov,60)
        pk=[]
        for i in range(W+1,n-W-1):
            if nov[i]>thr and nov[i]>=nov[i-1] and nov[i]>=nov[i+1]:
                if not pk or i-pk[-1]>=8: pk.append(i)
        sp=np.diff(pk)
        if len(sp)>=2:
            sps+=list(sp)
            print('   f%-5d-%-5d n=%-4d transitions at rel frames %s'%(idx[a],idx[b-1],b-a,pk[:14]))
            print('        spacings %s   median=%.1f'%(list(sp[:14]),np.median(sp)))
    if sps:
        sps=np.array(sps); sps=sps[(sps>=10)&(sps<=90)]
        if len(sps):
            med=np.median(sps)
            print('   POOLED: n=%d spacings, median=%.1f mean=%.2f sd=%.2f  IQR %.1f-%.1f'%(len(sps),med,sps.mean(),sps.std(),np.percentile(sps,25),np.percentile(sps,75)))
            print('   => %.2f video frames per source-second tick'%med)
            print('   => %.4f source-seconds per playback-second  (%.3fx)'%(fps/med,fps/med))
