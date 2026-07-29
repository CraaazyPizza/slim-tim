import pickle,numpy as np
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':('ZB788_2011',25.0),'rs':('RsQCX_2011',25.0),'oq':('Oqw96_2026',30000/1001),'l9':('l9RAh_2026',30000/1001)}
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
CAN=64
for k in ['zb','rs','oq','l9']:
    name,fps=NAME[k]
    # templates
    T=[]
    for i,c in enumerate(C[k]):
        if i>=len(LAB[k]) or LAB[k][i]=='?': continue
        m=c['mean'].astype(np.float32); m=m-m.mean(); m=m/np.linalg.norm(m)
        T.append((LAB[k][i],m))
    B=np.load('analysis/compare-eras/%s_band.npy'%k); runs=np.load('analysis/compare-eras/%s_runs.npy'%k)
    idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
    c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
    xc=c5+5.0*p+4
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    print('=== %s fps=%.4f  %d templates (%s)'%(name,fps,len(T),''.join(t[0] for t in T)))
    pooled=[]
    for oi in order[:5]:
        a,b=runs[oi]
        if b-a<70: continue
        seq=[]
        for i in range(a,b):
            fr=B[i].astype(np.float32)
            h=fr-blur1(fr,20)
            # window around the seconds-units cell, centred, canvas 64
            x0=int(round(xc-CAN/2)); y0=max(0,(h.shape[0]-CAN)//2)
            w=np.zeros((CAN,CAN),np.float32)
            xs0=max(0,x0); xs1=min(h.shape[1],x0+CAN)
            ys1=min(h.shape[0],y0+CAN)
            w[:ys1-y0,xs0-x0:xs0-x0+(xs1-xs0)]=h[y0:ys1,xs0:xs1]
            best=(-9,'?')
            for lab,tm in T:
                for dx in (-2,-1,0,1,2):
                    for dy in (-2,-1,0,1,2):
                        ww=np.roll(np.roll(w,dy,0),dx,1)
                        u=ww-ww.mean(); nu=np.linalg.norm(u)
                        if nu<=0: continue
                        s=float((u/nu*tm).sum())
                        if s>best[0]: best=(s,lab)
            seq.append(best[1])
        # median filter (mode of 5)
        from collections import Counter
        sm=[]
        for i in range(len(seq)):
            win=seq[max(0,i-2):i+3]
            sm.append(Counter(win).most_common(1)[0][0])
        # transitions
        tr=[i for i in range(1,len(sm)) if sm[i]!=sm[i-1]]
        sp=np.diff(tr)
        s=''.join(sm)
        print('   f%-5d-%-5d n=%-4d seq=%s'%(idx[a],idx[b-1],b-a,s[:120]))
        if len(sp): print('        transitions=%s spacings=%s'%(tr[:12],list(sp[:12])))
        pooled+=[x for x in sp if 10<=x<=90]
    if pooled:
        q=np.array(pooled); med=np.median(q)
        print('   POOLED n=%d median=%.1f mean=%.2f sd=%.2f  => %.4f source-s/playback-s (%.3fx)'%(len(q),med,q.mean(),q.std(),fps/med,fps/med))
