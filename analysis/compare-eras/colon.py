import sys,numpy as np
pre,label=sys.argv[1],sys.argv[2]
A=np.load(pre+'_A.npy')
P=np.clip(A,0,None).mean(0)
H,W=P.shape
thr=P.max()*0.28
ink=(P>thr)
h=ink.sum(0)                     # ink height per column
tot=ink.sum()
# candidate colon columns: ink present but height small
print(label,'H=%d W=%d'%(H,W))
runs=[];cur=None
for x in range(W):
    if h[x]>0:
        if cur is None: cur=[x,x]
        else: cur[1]=x
    else:
        if cur: runs.append(tuple(cur)); cur=None
if cur: runs.append(tuple(cur))
print('  ink column-groups (x0,x1,width,maxinkheight):')
out=[]
for a,b in runs:
    mh=h[a:b+1].max()
    out.append((a,b,b-a+1,int(mh)))
for t in out: print('   ',t)
