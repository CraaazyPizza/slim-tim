"""Frames-per-tick by PERIODOGRAM on the seconds-units glyph.

Why not boundary-by-boundary segmentation: in v1's colour segment the glyph sits only
~8 DN above its local background (bright flares wash the white glyph into a white
field), so a greedy run-segmenter shreds into 1-3 frame runs and returns garbage.

The periodogram tests the whole hypothesis at once.  For a trial period p (real-valued)
and phase phi, every frame gets a block index b_i = floor((i-phi)/p).  If p is the true
frames-per-tick then frames in the same block show the same digit and frames in adjacent
blocks show different digits.  Score:

   S(p,phi) = mean NCC over near pairs in the SAME block
            - mean NCC over near pairs in ADJACENT blocks

maximised over phi.  A cadence of 44.5 and one of 46.0 make different, testable
predictions, and 2 of 7 boundaries lost to flares cost signal but not bias.
"""
import numpy as np, json
from scipy import ndimage

BW,BH,BX,BY=620,120,590,895
CELL={'OpSTlDJWFFI':(966,1014),'Oqw96jCOP7A':(963,1011),'l9RAhmPHM_A':(923,970),
      'RsQCXN4o4Ps':(969,1017),'ZB788PtqQvg':(968,1014),'Xju_CY5ZESA':(969,1017)}
YB=(928,1006)

def cells(vid, lo, hi):
    A=np.fromfile('analysis/timecode-ticks/band_%s.raw'%vid,dtype=np.uint8).reshape(-1,BH,BW)
    cx=CELL[vid]
    V=[];con=[]
    for i in range(lo-1,hi):
        s=A[i, YB[0]-BY:YB[1]-BY, cx[0]-BX:cx[1]-BX].astype(np.float32)
        h=s-ndimage.uniform_filter(s,21)
        con.append(float(h.max()-h.min()))
        v=h.ravel()-h.mean(); n=np.linalg.norm(v)
        V.append(v/(n if n>0 else 1))
    return np.array(V), np.array(con)

def periodogram(V, con, plo=38., phi_=54., dp=0.05, maxlag=6, mincon=None):
    n=len(V)
    ok=np.ones(n,bool)
    if mincon: pass
    if mincon is not None: ok = con >= minon if False else con>=minon if False else con>=minon
    return None

def score_curve(V, con, plo=38.0, phig=54.0, dp=0.05, maxlag=6, conmin=0.0):
    n=len(V); ok=con>=conmin
    ii,jj=[],[]
    for lag in range(1,maxlag+1):
        a=np.arange(0,n-lag)
        ii.append(a); jj.append(a+lag)
    ii=np.concatenate(ii); jj=np.concatenate(jj)
    keep=ok[ii]&ok[jj]; ii,jj=ii[keep],jj[keep]
    ncc=np.einsum('ij,ij->i',V[ii],V[jj])
    ps=np.arange(plo,phig+1e-9,dp); out=[]
    for p in ps:
        best=-9
        for ph in np.arange(0,p,0.5):
            bi=np.floor((ii-ph)/p); bj=np.floor((jj-ph)/p)
            same=bi==bj; adj=np.abs(bi-bj)==1
            if same.sum()<30 or adj.sum()<30: continue
            s=ncc[same].mean()-ncc[adj].mean()
            if s>best: best=s
        out.append(best)
    return ps, np.array(out)

def go(name, vid, lo, hi, fps, conmin_frac=0.0, plo=38.0, phig=54.0):
    V,con=cells(vid,lo,hi)
    cm=float(np.median(con)); conmin=conmin_frac*cm
    ps,sc=score_curve(V,con,plo,phig,conmin=conmin)
    k=int(np.argmax(sc))
    # parabolic refine
    if 0<k<len(ps)-1:
        y0,y1,y2=sc[k-1],sc[k],sc[k+1]; d=(y0-y2)/(2*(y0-2*y1+y2)) if (y0-2*y1+y2)!=0 else 0
    else: d=0
    pbest=ps[k]+d*(ps[1]-ps[0])
    # top peaks
    order=np.argsort(-sc)[:400]
    tops=[]
    for o in order:
        if all(abs(ps[o]-t)>0.8 for t,_ in tops): tops.append((float(ps[o]),float(sc[o])))
        if len(tops)>=4: break
    print('\n%-38s f%d-%d  n=%d  glyph contrast median %.1f DN'%(name,lo,hi,hi-lo+1,cm))
    print('   BEST p = %.2f frames/tick   score %.4f   -> playback %.4fx of source rate'%(
          pbest,sc[k],fps/pbest))
    print('   top peaks (p, score): %s'%['%.2f/%.3f'%t for t in tops])
    for cand in (44.5,45.0,46.0,46.5):
        j=int(round((cand-plo)/(ps[1]-ps[0])))
        if 0<=j<len(ps): print('      score at p=%.1f : %.4f   (=> %.4fx)'%(cand,sc[j],fps/cand))
    return dict(name=name,vid=vid,lo=lo,hi=hi,fps=fps,p=float(pbest),
                score=float(sc[k]),tops=tops,contrast_median=cm,
                ps=ps.tolist(),sc=sc.tolist())

if __name__=='__main__':
    N=30000/1001.
    JOBS=[
     ('v1 COLOUR Mk.5 / Case 31','OpSTlDJWFFI',2603,2900,N),
     ('v1 b/w Case 11 tin bird','OpSTlDJWFFI',1060,1285,N),
     ('v1 b/w Case 12 taxi+pace','OpSTlDJWFFI',1300,1900,N),
     ('v1 b/w Case 26 show&tell','OpSTlDJWFFI',1960,2560,N),
     ('v2 Case 21 Triage','Oqw96jCOP7A',1207,1420,N),
     ('v2 Case 25 Slim Tim','Oqw96jCOP7A',1850,2410,N),
     ('v2 Case 20 Brown boys','Oqw96jCOP7A',700,1100,N),
     ('v3 Case 18','l9RAhmPHM_A',1000,1600,N),
     ('v3 Case 28','l9RAhmPHM_A',3000,3600,N),
     ('2011 RsQCX A','RsQCXN4o4Ps',700,1000,25.0),
     ('2011 RsQCX B','RsQCXN4o4Ps',1100,1480,25.0),
     ('2011 ZB788','ZB788PtqQvg',150,600,25.0),
     ('2011 ZB788 b','ZB788PtqQvg',700,1150,25.0),
    ]
    res=[go(*j) for j in JOBS]
    json.dump(res,open('analysis/timecode-ticks/tickper.json','w'))
