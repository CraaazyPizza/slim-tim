import sys,numpy as np
from PIL import Image
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
SPEC={ # pre, label, string, list of (cellindex,char)
 'zb':('ZB788_2011','/07 00:08:41'),
 'rs':('RsQCX_2011',None),
 'oq':('Oqw96_2026',None),
 'l9':('l9RAh_2026',None),
}
def analyse(pre):
    B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
    lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
    outs=[]
    for o in order:
        a,b=runs[o]
        if b-a<10: continue
        m=B[a:b].astype(np.float32).mean(0)
        h=(m-blur(m,20))[4:-4,4:-4]
        P=np.clip(h,0,None)
        if P.max()<=0: continue
        P=P/P.max()
        hh=(P>0.30).sum(0); groups=[];cur=None
        for x in range(P.shape[1]):
            if hh[x]>0: cur=[x,x] if cur is None else [cur[0],x]
            else:
                if cur and cur[1]-cur[0]>=5: groups.append(tuple(cur))
                cur=None
        if cur and cur[1]-cur[0]>=5: groups.append(tuple(cur))
        if len(groups)!=11: continue
        def cen(g):
            x0,x1=g; sub=P[:,x0:x1+1]; w=sub.sum(0); xs=np.arange(x0,x1+1)
            return float((w*xs).sum()/w.sum())
        g5,g8=groups[5],groups[8]
        if not(8<=g5[1]-g5[0]+1<=20 and 8<=g8[1]-g8[0]+1<=20): continue
        c5,c8=cen(g5),cen(g8); p=(c8-c5)/3.0
        if not(38<p<50): continue
        outs.append((P,groups,c5,p,idx[a],idx[b-1],b-a))
    return outs
# cell index -> group index mapping for layout '/XX XX:XX:XX' (11 groups)
# groups: 0='/',1=c1,2=c2,3=c4,4=c5,5=':',6=c7,7=c8,8=':',9=c10,10=c11
GI={0:0,1:1,2:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9,11:10}
def extract(P,groups,gi,pad=4):
    x0,x1=groups[gi]
    sub=P[:,max(0,x0-pad):x1+1+pad]
    rows=np.nonzero(sub.max(1)>0.5)[0]
    return sub, rows
res={}
for pre in ['zb','rs','oq','l9']:
    outs=analyse('analysis/compare-eras/'+pre)
    print('%s: %d usable runs'%(pre,len(outs)))
    res[pre]=outs
np.save('analysis/compare-eras/nusable.npy',np.array([len(res[k]) for k in res]))
import pickle
pickle.dump({k:[(o[0],o[1],o[2],o[3],o[4],o[5],o[6]) for o in v] for k,v in res.items()},open('analysis/compare-eras/runs.pkl','wb'))
