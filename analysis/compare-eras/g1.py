import sys,numpy as np
from PIL import Image
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
pre,label,pick,string=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens); a,b=runs[order[pick]]
m=B[a:b].astype(np.float32).mean(0)
h=(m-blur(m,20))[4:-4,4:-4]
P=np.clip(h,0,None); P/=P.max()
ink=P>0.30
hh=ink.sum(0); ww=ink.sum(1)
groups=[];cur=None
for x in range(P.shape[1]):
    if hh[x]>0: cur=[x,x] if cur is None else [cur[0],x]
    else:
        if cur and cur[1]-cur[0]>=5: groups.append(tuple(cur))
        cur=None
if cur and cur[1]-cur[0]>=5: groups.append(tuple(cur))
print('== %s  run f%d-f%d n=%d  string="%s"  ngroups=%d'%(label,idx[a],idx[b-1],b-a,string,len(groups)))
info=[]
for (x0,x1) in groups:
    sub=P[:,x0:x1+1]; wgt=sub.sum(0); xs=np.arange(x0,x1+1)
    cx=float((wgt*xs).sum()/wgt.sum())
    rows=np.nonzero(sub.max(1)>0.30)[0]
    inkfrac=float((sub>0.30).sum())/sub.size
    info.append((x0,x1,cx,rows.min(),rows.max(),rows.max()-rows.min()+1,round(inkfrac,3)))
for t in info: print('   x %3d-%3d cx=%7.2f  w=%2d  rows %2d-%2d h=%2d  inkfrac=%.3f'%(t[0],t[1],t[2],t[1]-t[0]+1,t[3],t[4],t[5],t[6]))
np.save(pre+'_run%d.npy'%pick,h)
open(pre+'_run%d.txt'%pick,'w').write(string)
