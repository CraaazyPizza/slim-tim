"""Frame-precise burned-in-timecode tick measurement.

Input: analysis/timecode-ticks/band_<id>.raw  = gray8 crop  x 590..1209, y 895..1014 (620x120/frame)

Method
  1. locate the rightmost glyph cell of the timecode (the seconds-UNITS digit) from an
     averaged normalised top-hat over the window;
  2. per frame, high-pass that cell and normalise to unit norm;
  3. segment the sequence greedily into runs of constant glyph by NCC against the
     running run-mean;
  4. run length = video frames per source second ("frames per tick").
Frames whose glyph contrast falls well below the window median are flagged: a bright
flare washes a white glyph into a white background and the estimator cannot see it.
"""
import numpy as np, json, sys
from scipy import ndimage

BW,BH,BX,BY = 620,120,590,895

def band(vid):
    a=np.fromfile('analysis/timecode-ticks/band_%s.raw'%vid,dtype=np.uint8)
    return a.reshape(-1,BH,BW)

def find_cell(B, idx, yb):
    acc=None; n=0
    for i in idx:
        s=B[i,yb[0]-BY:yb[1]-BY].astype(np.float32)
        acc=(np.maximum(s-ndimage.uniform_filter(s,41),0) if acc is None
             else acc+np.maximum(s-ndimage.uniform_filter(s,41),0)); n+=1
    m=acc/n; cp=m[6:-6].mean(0)
    th=max(cp.max()*0.18,0.8); on=cp>th
    runs=[];cur=None
    for x,v in enumerate(on):
        if v: cur=[x,x] if cur is None else [cur[0],x]
        else:
            if cur and cur[1]-cur[0]>=6: runs.append(cur)
            cur=None
    if cur and cur[1]-cur[0]>=6: runs.append(cur)
    a,b=runs[-1]
    if b-a>62:                                  # two glyphs merged -> split at interior min
        seg=cp[a:b+1]; mid=len(seg)//2
        lo=max(6,mid-20); hi=min(len(seg)-6,mid+20)
        a=a+int(np.argmin(seg[lo:hi]))+lo+1
    return (a-5,b+6), cp, runs

def run(name, vid, lo, hi, yb=(928,1008), thr=0.55, verbose=True):
    B=band(vid); fr=np.arange(lo,hi+1)
    ii=fr-1                                      # PNG f00001 == raw index 0
    sub=[i for i in ii[::max(1,len(ii)//150)]]
    cell,cp,gr=find_cell(B,sub,yb)
    V=[];con=[]
    for i in ii:
        s=B[i,yb[0]-BY:yb[1]-BY, cell[0]:cell[1]].astype(np.float32)
        h=s-ndimage.uniform_filter(s,21)
        con.append(float(h.max()-h.min()))
        v=h.ravel()-h.mean(); nr=np.linalg.norm(v); V.append(v/(nr if nr>0 else 1))
    V=np.array(V); con=np.array(con)
    runs=[[0]]
    for k in range(1,len(V)):
        ref=V[runs[-1]].mean(0); ref=ref/np.linalg.norm(ref)
        if float(V[k]@ref)>thr: runs[-1].append(k)
        else: runs.append([k])
    L=[len(r) for r in runs]; st=[int(fr[r[0]]) for r in runs]
    med=float(np.median(con)); weak=[int(fr[k]) for k in np.nonzero(con<0.45*med)[0]]
    inner=L[1:-1]
    if verbose:
        print('\n=== %s   frames %d-%d   seconds-units cell abs x=%d..%d'%(
              name,lo,hi,BX+cell[0],BX+cell[1]))
        print('    glyph contrast median %.1f DN  min %.1f  |  low-contrast frames (flare): %d %s'%(
              med,con.min(),len(weak),weak[:20]))
        print('    run lengths : %s'%L)
        print('    run starts  : %s'%st)
        if inner:
            print('    INNER runs (window-truncated first/last dropped): n=%d  %s'%(len(inner),inner))
            print('      mean %.3f   median %.1f   sd %.2f   -> frames per tick'%(
                  np.mean(inner),np.median(inner),np.std(inner)))
    return dict(name=name,vid=vid,lo=lo,hi=hi,cell=[BX+cell[0],BX+cell[1]],
                lengths=L,starts=st,inner=inner,weak=weak,contrast_median=med)

if __name__=='__main__':
    JOBS=[
      ('v1 colour Mk.5 / Case 31 (T6-02)','OpSTlDJWFFI',2600,2905),
      ('v1 b/w Case 12 "pace lap"',       'OpSTlDJWFFI',1500,1950),
      ('v1 b/w Case 12 "taxi"',           'OpSTlDJWFFI',1290,1500),
      ('v1 b/w Case 11 "tin bird"',       'OpSTlDJWFFI',1050,1290),
      ('v1 b/w Case 26 "show and tell"',  'OpSTlDJWFFI',1960,2560),
      ('v2 Case 21 "Triage"',             'Oqw96jCOP7A',1195,1425),
      ('v2 Case 25 "Slim Tim"',           'Oqw96jCOP7A',1850,2420),
      ('v2 Case 11 "Tin bird primer"',    'Oqw96jCOP7A', 500, 700),
      ('v3 Case 18',                      'l9RAhmPHM_A',1000,1600),
      ('v3 Case 28',                      'l9RAhmPHM_A',3000,3600),
      ('2011 RsQCX (Case 25/26)',         'RsQCXN4o4Ps',1290,1500),
      ('2011 RsQCX earlier',              'RsQCXN4o4Ps', 700, 950),
      ('2011 ZB788',                      'ZB788PtqQvg', 150, 450),
    ]
    out=[]
    for j in JOBS:
        try: out.append(run(*j))
        except Exception as e: print('\n=== %s FAILED %r'%(j[0],e))
    json.dump(out,open('analysis/timecode-ticks/ticks.json','w'),indent=1)
