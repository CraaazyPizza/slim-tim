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
    # fixed cell geometry from median over usable runs
    c5s=[o[2] for o in R[k]]; ps=[o[3] for o in R[k]]
    c5=float(np.median(c5s)); p=float(np.median(ps))
    # seconds digits are cells 10,11 -> x = c5 + (10-6)*p ... (11-6)*p ; band was cropped by 4 in the run pipeline
    x0=int(round(c5+3.5*p))+4; x1=int(round(c5+5.6*p))+4
    x0=max(0,x0); x1=min(B.shape[2],x1)
    sub=B[:,:,x0:x1].astype(np.float32)
    print('%s: fps=%.4f  seconds-digit window x=%d..%d (w=%d), frames %d'%(name,fps,x0,x1,x1-x0,len(sub)))
    # per-frame high-pass then frame-to-frame distance
    V=[]
    for i in range(len(sub)):
        h=sub[i]-blur1(sub[i],8)
        V.append(h.ravel())
    V=np.stack(V)
    V=V-V.mean(1,keepdims=True)
    nrm=np.linalg.norm(V,axis=1); nrm[nrm==0]=1
    Vn=V/nrm[:,None]
    d=1.0-np.einsum('ij,ij->i',Vn[:-1],Vn[1:])
    d=d-d.mean()
    n=len(d)
    F=np.abs(np.fft.rfft(d*np.hanning(n))); fr=np.fft.rfftfreq(n)
    cands=[(1/fr[i],F[i]) for i in range(1,len(fr)) if fr[i]>0 and 4<=1/fr[i]<=60]
    cands.sort(key=lambda t:-t[1])
    top=cands[:5]
    print('   frame-to-frame change spectrum, top periods (frames/tick):',[(round(pp,2),round(v,1)) for pp,v in top])
    N=top[0][0]
    print('   => %.3f video frames per 1 s of burned-in source timecode'%N)
    print('   => source time advances %.4f s per second of playback  (i.e. %.3fx speed vs the burned-in clock)'%(fps/N,fps/N))
    # also autocorrelation check
    dd=d-d.mean(); ac=np.correlate(dd,dd,'full')[len(dd)-1:]; ac/=ac[0]
    pk=[(l,ac[l]) for l in range(4,61) if ac[l]>=ac[l-1] and ac[l]>=ac[l+1]]
    pk.sort(key=lambda t:-t[1])
    print('   autocorr peaks (lag,corr):',[(l,round(float(v),3)) for l,v in pk[:5]])
