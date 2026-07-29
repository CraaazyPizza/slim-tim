import pickle,numpy as np
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
NAME={'zb':('ZB788_2011',25.0),'rs':('RsQCX_2011',25.0),'oq':('Oqw96_2026',30000/1001),'l9':('l9RAh_2026',30000/1001)}
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
for k in ['zb','rs','oq','l9']:
    name,fps=NAME[k]
    B=np.load('analysis/compare-eras/%s_band.npy'%k); idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
    runs=np.load('analysis/compare-eras/%s_runs.npy'%k)
    c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
    # seconds-UNITS cell = cell 11 -> centre c5+5p ; take +/-0.5p
    xc=c5+5.0*p+4
    x0=max(0,int(round(xc-0.45*p))); x1=min(B.shape[2],int(round(xc+0.45*p)))
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    print('%-11s fps=%.4f  seconds-units cell x=%d..%d (w=%d)'%(name,fps,x0,x1,x1-x0))
    allsp=[]
    for oi in order[:6]:
        a,b=runs[oi]
        if b-a<40: continue
        sub=B[a:b,:,x0:x1].astype(np.float32)
        Hh=np.stack([sub[i]-blur1(sub[i],6) for i in range(len(sub))])
        V=Hh.reshape(len(Hh),-1); V=V-V.mean(1,keepdims=True)
        nr=np.linalg.norm(V,axis=1); nr[nr==0]=1; V=V/nr[:,None]
        M=V@V.T
        t=np.percentile(M[np.triu_indices(len(M),3)],75)
        # greedy segmentation: extend block while mean corr of new frame with block > t
        blocks=[];cur=[0]
        for i in range(1,len(M)):
            mc=M[i,cur].mean()
            if mc>t: cur.append(i)
            else: blocks.append(cur); cur=[i]
        blocks.append(cur)
        bl=[len(x) for x in blocks if len(x)>=2]
        if len(bl)>=3:
            allsp+=bl
            print('    run f%-5d-%-5d n=%-4d thr=%.3f nblocks=%-3d blocklens=%s'%(idx[a],idx[b-1],b-a,t,len(bl),bl[:16]))
    if allsp:
        allsp=np.array(allsp)
        print('    ALL blocks: n=%d  median=%.1f  mean=%.2f  IQR=%.1f-%.1f'%(len(allsp),np.median(allsp),allsp.mean(),np.percentile(allsp,25),np.percentile(allsp,75)))
        med=np.median(allsp)
        print('    => %.1f frames per source-second  => %.3f source-s per playback-s (%.3fx)'%(med,fps/med,fps/med))
