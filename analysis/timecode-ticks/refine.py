"""Exact tick onsets: detect coarse boundaries, then refine each to the first frame on
which the NEW digit template beats the OLD one.  Removes the +-1 frame jitter of the
sliding-window detector, so inter-tick gaps are integers you can actually trust."""
import numpy as np, json
from scipy import ndimage
BH,BW,BX,BY=120,620,590,895
CELL={'OpSTlDJWFFI':(966,1014),'Oqw96jCOP7A':(963,1011),'l9RAhmPHM_A':(923,970),
      'RsQCXN4o4Ps':(969,1017),'ZB788PtqQvg':(968,1014)}
def band(v): return np.fromfile('analysis/timecode-ticks/band_%s.raw'%v,dtype=np.uint8).reshape(-1,BH,BW)
def nrm(v):
    v=v.ravel()-v.mean(); n=np.linalg.norm(v); return v/(n if n>0 else 1)
class Seg:
    def __init__(s,vid,lo,hi):
        A=band(vid); cx=CELL[vid]; s.lo=lo
        s.C=[];s.con=[]
        for i in range(lo,hi+1):
            f=A[i-1,33:111,cx[0]-BX:cx[1]-BX].astype(np.float32)
            h=f-ndimage.uniform_filter(f,21)
            s.con.append(float(np.percentile(h,99)-np.percentile(h,1))); s.C.append(h)
        s.C=np.array(s.C); s.con=np.array(s.con); s.n=len(s.C)
    def cell(s,i): return s.C[i-s.lo]
    def coarse(s,w=8,minsep=30):
        d=np.full(s.n,np.nan)
        for k in range(w,s.n-w+1):
            d[k]=1-float(nrm(s.C[k-w:k].mean(0))@nrm(s.C[k:k+w].mean(0)))
        med=np.nanmedian(d)
        cand=[k for k in range(w+1,s.n-w) if d[k]>=d[k-1] and d[k]>=d[k+1] and d[k]>1.5*med]
        cand.sort(key=lambda k:-d[k]); sel=[]
        for k in cand:
            if all(abs(k-j)>=minsep for j in sel): sel.append(k)
        return sorted(s.lo+np.array(sel)), d
    def refine(s,b,r=9,m=18):
        a0,a1=b-3-m,b-3; b0,b1=b+3,b+3+m
        if a0<s.lo or b1>s.lo+s.n-1: return b,0.,0.
        A=nrm(s.C[a0-s.lo:a1-s.lo].mean(0)); B=nrm(s.C[b0-s.lo:b1-s.lo].mean(0))
        sep=1-float(A@B)
        on=None
        for i in range(b-r,b+r+1):
            v=nrm(s.cell(i))
            if float(v@B)>float(v@A):
                if on is None: on=i
            else: on=None
        return (on if on is not None else b), sep, float(np.median(s.con[b-s.lo-r:b-s.lo+r]))

def go(name,vid,lo,hi,fps,minsep=30):
    S=Seg(vid,lo,hi); cb,_=S.coarse(minsep=minsep)
    cm=float(np.median(S.con)); rows=[]
    for b in cb:
        on,sep,lc=S.refine(int(b))
        rows.append((int(b),int(on),sep,lc))
    ons=[r[1] for r in rows]
    print('\n%-26s f%d-%d  contrast med %.1f DN'%(name,lo,hi,cm))
    print('   %-8s %-8s %-7s %-7s %s'%('coarse','onset','sep','localC','gap'))
    prev=None; gaps=[]; good=[]
    for b,on,sep,lc in rows:
        g='' if prev is None else on-prev
        flag='' if (sep>0.25 and lc>0.5*cm) else '  <<flare/weak'
        print('   %-8d %-8d %-7.3f %-7.1f %s%s'%(b,on,sep,lc,g,flag))
        if prev is not None:
            gaps.append(on-prev)
            if sep>0.25 and lc>0.5*cm and prevok: good.append(on-prev)
        prev=on; prevok=(sep>0.25 and lc>0.5*cm)
    if gaps:
        print('   gaps       %s'%gaps)
        print('   TRUSTED (both endpoints clean) n=%d %s  mean %.2f  sd %.2f -> %.4fx'%(
            len(good),good,np.mean(good) if good else float('nan'),
            np.std(good) if good else float('nan'), fps/np.mean(good) if good else float('nan')))
        if len(ons)>1:
            span=ons[-1]-ons[0]
            print('   span %d frames over %d intervals = %.3f f/tick -> %.4fx'%(
                span,len(ons)-1,span/(len(ons)-1),fps/(span/(len(ons)-1))))
    return dict(name=name,vid=vid,onsets=ons,gaps=gaps,trusted=good,fps=fps)
if __name__=='__main__':
    N=30000/1001.
    JOBS=[('v1 b/w C11 tinbird','OpSTlDJWFFI',1055,1290,N),
          ('v1 b/w C12 taxi','OpSTlDJWFFI',1295,1560,N),
          ('v1 b/w C12 pacelap','OpSTlDJWFFI',1560,1900,N),
          ('v1 b/w C26 show&tell','OpSTlDJWFFI',1960,2560,N),
          ('v1 COLOUR C31 Mk.5','OpSTlDJWFFI',2600,2905,N),
          ('v2 C11 primer','Oqw96jCOP7A',495,700,N),
          ('v2 C20 brownboys','Oqw96jCOP7A',690,1105,N),
          ('v2 C21 triage','Oqw96jCOP7A',1200,1425,N),
          ('v2 C25 slimtim','Oqw96jCOP7A',1845,2415,N),
          ('v3 C18','l9RAhmPHM_A',990,1610,N),
          ('v3 C18 b','l9RAhmPHM_A',1610,2300,N),
          ('v3 C28','l9RAhmPHM_A',2990,3610,N),
          ('v3 C28 b','l9RAhmPHM_A',3610,4200,N),
          ('2011 RsQCX A','RsQCXN4o4Ps',690,1010,25.),
          ('2011 RsQCX B','RsQCXN4o4Ps',1090,1490,25.),
          ('2011 ZB788 A','ZB788PtqQvg',145,610,25.),
          ('2011 ZB788 B','ZB788PtqQvg',690,1160,25.),
         ]
    json.dump([go(*j) for j in JOBS],open('analysis/timecode-ticks/refine.json','w'),indent=1)
