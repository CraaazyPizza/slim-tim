"""Per-frame label assignment against run-averaged templates.
Gives the exact first frame on which each new seconds value appears -> exact tick onsets."""
import numpy as np, sys
from scipy import ndimage
BW,BH,BX,BY=620,120,590,895
YB=(928,1006)
def band(vid): return np.fromfile('analysis/timecode-ticks/band_%s.raw'%vid,dtype=np.uint8).reshape(-1,BH,BW)
def hp(s): return s-ndimage.uniform_filter(s,21)
def nrm(v):
    v=v.ravel()-v.mean(); n=np.linalg.norm(v); return v/(n if n>0 else 1)
def go(vid,lo,hi,cx,tmplruns,names,label):
    A=band(vid)
    def cell(i): return hp(A[i-1, YB[0]-BY:YB[1]-BY, cx[0]-BX:cx[1]-BX].astype(np.float32))
    T=[]
    for a,b in tmplruns:
        T.append(nrm(np.mean([cell(i) for i in range(a+5,b-4)],axis=0)))
    T=np.array(T)
    print('\n=== %s  %s  f%d-%d  templates %s'%(label,vid,lo,hi,list(zip(names,tmplruns))))
    lab=[];sc=[]
    for i in range(lo,hi+1):
        v=nrm(cell(i)); s=T@v; k=int(np.argmax(s)); lab.append(k); sc.append(s)
    sc=np.array(sc)
    # smooth: median filter width 5 to kill single-frame flips
    lab=np.array(lab); labs=ndimage.median_filter(lab,5)
    runs=[];cur=[0]
    for k in range(1,len(labs)):
        if labs[k]==labs[cur[-1]]: cur.append(k)
        else: runs.append(cur); cur=[k]
    runs.append(cur)
    print('  label runs:')
    prev=None
    for r in runs:
        a,b=lo+r[0],lo+r[-1]
        mx=float(sc[r,labs[r[0]]].mean())
        gap='' if prev is None else '  (+%d)'%(a-prev)
        print('    %-4s f%-5d-%-5d  n=%-3d  mean NCC %.3f%s'%(names[labs[r[0]]],a,b,b-a+1,mx,gap))
        prev=a
    onsets=[lo+r[0] for r in runs]
    d=np.diff(onsets)
    print('  onsets %s  gaps %s'%(onsets,list(d)))
    return onsets
if __name__=='__main__':
    # v1 colour Mk.5: templates from the five legible runs (:58 :59 :00 :01 :02)
    go('OpSTlDJWFFI',2600,2905,(946,1016),
       [(2660,2706),(2706,2751),(2751,2788),(2788,2845),(2845,2884)],
       ['58','59','00','01','02'],'v1 COLOUR Mk.5 Case 31')
