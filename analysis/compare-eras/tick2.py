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
    c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
    x0=max(0,int(round(c5+3.6*p))+4); x1=min(B.shape[2],int(round(c5+5.6*p))+4)
    sub=B[:,:,x0:x1].astype(np.float32)
    H=[]
    for i in range(len(sub)):
        h=sub[i]-blur1(sub[i],8); H.append(h)
    H=np.stack(H)
    W=3
    A=np.stack([H[max(0,i-W+1):i+1].mean(0) for i in range(len(H))])
    A=A.reshape(len(A),-1); A=A-A.mean(1,keepdims=True)
    nr=np.linalg.norm(A,axis=1); nr[nr==0]=1; A=A/nr[:,None]
    # compare average ending at i with average starting at i+1 (offset by W to avoid overlap)
    d=[]
    for i in range(len(A)-W):
        d.append(1.0-float(A[i]@A[i+W]))
    d=np.array(d)
    thr=np.percentile(d,80)
    # local maxima above threshold, min separation 4
    cps=[]
    for i in range(1,len(d)-1):
        if d[i]>thr and d[i]>=d[i-1] and d[i]>=d[i+1]:
            if not cps or i-cps[-1]>=4: cps.append(i)
    sp=np.diff(cps)
    sp=sp[(sp>=4)&(sp<=60)]
    if len(sp)==0: print(name,'no spacings'); continue
    bc=np.bincount(sp)
    mode=int(bc.argmax())
    print('%-11s fps=%.4f  window x=%d..%d  ncp=%d'%(name,fps,x0,x1,len(cps)))
    print('   spacing histogram:',{int(i):int(c) for i,c in enumerate(bc) if c>0})
    print('   mode=%d  median=%.1f  mean=%.2f  (frames per source-second tick)'%(mode,np.median(sp),sp.mean()))
    for est,lab in [(mode,'mode'),(np.median(sp),'median')]:
        print('      via %-6s: %.3f source-seconds per playback-second  => %.3fx'%(lab,fps/est,fps/est))
