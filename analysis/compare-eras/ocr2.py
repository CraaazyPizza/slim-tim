import pickle,numpy as np
from collections import Counter
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
C=pickle.load(open('analysis/compare-eras/clusters.pkl','rb'))
LAB={'zb':['0','2','7','4','5','1','1','3'],'rs':['0','5','2','1'],
     'oq':['0','2','1','5','3','4'],'l9':['2','1','0','8','3','5','4','9','7','9','?']}
NAME={'zb':('ZB788_2011',25.0),'rs':('RsQCX_2011',25.0),'oq':('Oqw96_2026',30000/1001),'l9':('l9RAh_2026',30000/1001)}
POOL={'zb':['zb','rs'],'rs':['zb','rs'],'oq':['oq','l9'],'l9':['oq','l9']}
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
CAN=64
def build(keys):
    acc={}
    for kk in keys:
        for i,c in enumerate(C[kk]):
            if i>=len(LAB[kk]) or LAB[kk][i]=='?': continue
            lab=LAB[kk][i]
            acc.setdefault(lab,[]).append((c['n'],c['mean'].astype(np.float32)))
    T=[]
    for lab,v in sorted(acc.items()):
        w=sum(n for n,_ in v)
        m=sum(n*mm for n,mm in v)/w
        m=m-m.mean(); T.append((lab,m/np.linalg.norm(m)))
    return T
for k in ['zb','rs','oq','l9']:
    name,fps=NAME[k]
    T=build(POOL[k])
    B=np.load('analysis/compare-eras/%s_band.npy'%k); runs=np.load('analysis/compare-eras/%s_runs.npy'%k)
    idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
    c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
    xc=c5+5.0*p+4
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    print('=== %s fps=%.4f templates=%s'%(name,fps,''.join(t[0] for t in T)))
    good=[]
    for oi in order[:8]:
        a,b=runs[oi]
        if b-a<70: continue
        seq=[]
        for i in range(a,b):
            fr=B[i].astype(np.float32); h=fr-blur1(fr,20)
            x0=int(round(xc-CAN/2)); y0=max(0,(h.shape[0]-CAN)//2)
            w=np.zeros((CAN,CAN),np.float32)
            xs0=max(0,x0); xs1=min(h.shape[1],x0+CAN); ys1=min(h.shape[0],y0+CAN)
            w[:ys1-y0,xs0-x0:xs0-x0+(xs1-xs0)]=h[y0:ys1,xs0:xs1]
            best=(-9,'?')
            for lab,tm in T:
                for dx in (-2,0,2):
                    for dy in (-2,0,2):
                        ww=np.roll(np.roll(w,dy,0),dx,1)
                        u=ww-ww.mean(); nu=np.linalg.norm(u)
                        if nu<=0: continue
                        s=float((u/nu*tm).sum())
                        if s>best[0]: best=(s,lab)
            seq.append(best[1])
        sm=[Counter(seq[max(0,i-3):i+4]).most_common(1)[0][0] for i in range(len(seq))]
        tr=[i for i in range(1,len(sm)) if sm[i]!=sm[i-1]]
        # keep only fragments whose smoothed sequence is a clean staircase (>=3 long blocks)
        blocks=[];cur=[sm[0],1]
        for i in range(1,len(sm)):
            if sm[i]==cur[0]: cur[1]+=1
            else: blocks.append(tuple(cur)); cur=[sm[i],1]
        blocks.append(tuple(cur))
        big=[bb for bb in blocks if bb[1]>=20]
        s=''.join(sm)
        print('   f%-5d-%-5d n=%-4d blocks=%s'%(idx[a],idx[b-1],b-a,blocks[:12]))
        if len(big)>=2:
            # spacings between starts of consecutive big blocks
            pos=[];acc=0
            for bb in blocks:
                pos.append((bb[0],acc,bb[1])); acc+=bb[1]
            bigpos=[pp for pp in pos if pp[2]>=20]
            sp=[bigpos[j+1][1]-bigpos[j][1] for j in range(len(bigpos)-1)]
            sp=[x for x in sp if 20<=x<=90]
            if sp: good+=sp; print('        big-block spacings: %s'%sp)
    if good:
        q=np.array(good,float); med=np.median(q)
        print('   POOLED n=%d  median=%.2f mean=%.2f sd=%.2f'%(len(q),med,q.mean(),q.std()))
        print('   => %.2f frames per source-second => %.4f source-s per playback-s (%.3fx)'%(med,fps/med,fps/med))
