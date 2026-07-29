import pickle,numpy as np,sys
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
def blur1(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
# high-precision transition finder: build clean templates from user-specified stable windows,
# then find zero-crossing of (corr_A - corr_B) for each frame.
k=sys.argv[1]
segs=[tuple(map(int,s.split(':'))) for s in sys.argv[2:]]   # stable windows f0:f1
B=np.load('analysis/compare-eras/%s_band.npy'%k); idx=np.load('analysis/compare-eras/%s_idx.npy'%k)
c5=float(np.median([o[2] for o in R[k]])); p=float(np.median([o[3] for o in R[k]]))
xc=c5+5.0*p+4
x0=max(0,int(round(xc-0.5*p))); x1=min(B.shape[2],int(round(xc+0.5*p)))
def cell(i):
    fr=B[i].astype(np.float32); h=fr-blur1(fr,20)
    return h[:,x0:x1]
def tmpl(f0,f1):
    i0,i1=int(np.searchsorted(idx,f0)),int(np.searchsorted(idx,f1))
    m=np.mean([cell(i) for i in range(i0,i1)],0)
    m=m-m.mean(); return m/np.linalg.norm(m)
Ts=[(s,tmpl(*s)) for s in segs]
print('%s: cell x=%d..%d  templates from %s'%(k,x0,x1,segs))
lo=min(s[0] for s in segs)-30; hi=max(s[1] for s in segs)+30
i0,i1=int(np.searchsorted(idx,lo)),int(np.searchsorted(idx,hi))
scores=[]
for i in range(i0,i1):
    c=cell(i); c=c-c.mean(); n=np.linalg.norm(c)
    if n<=0: scores.append([0]*len(Ts)); continue
    c=c/n
    scores.append([float((c*t).sum()) for _,t in Ts])
S=np.array(scores)
# smooth
def sm(v,w=5):
    o=np.convolve(v,np.ones(w)/w,mode='same'); return o
S=np.stack([sm(S[:,j]) for j in range(S.shape[1])],1)
for j in range(len(Ts)-1):
    d=S[:,j]-S[:,j+1]
    cross=None
    for i in range(1,len(d)):
        if d[i-1]>0 and d[i]<=0:
            # linear interp
            f=d[i-1]/(d[i-1]-d[i]); cross=idx[i0+i-1]+f
    print('   transition %s -> %s at frame %.1f'%(segs[j],segs[j+1],cross if cross else float('nan')))
