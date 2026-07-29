"""Frames-per-tick by SLIDING-WINDOW step detection on the seconds-units glyph.

For each frame i, average the high-passed glyph cell over the w frames before it and
the w frames from it onward, then take 1 - NCC(before, after).  A digit change is a
step, so it produces a sharp peak; the moving picture underneath is smooth and does
not.  Averaging w frames buys ~sqrt(w) in SNR, which is what makes the low-contrast
fragments (glyph only ~8 DN above local background) measurable at all.

Reports every detected boundary frame, the gaps between them, and flags gaps that
coincide with low-glyph-contrast frames (bright lens flares) so a lost boundary cannot
masquerade as a long tick.
"""
import numpy as np, json, sys
from scipy import ndimage

BW,BH,BX,BY=620,120,590,895
CELL={'OpSTlDJWFFI':(966,1014),'Oqw96jCOP7A':(963,1011),'l9RAhmPHM_A':(923,970),
      'RsQCXN4o4Ps':(969,1017),'ZB788PtqQvg':(968,1014),'Xju_CY5ZESA':(969,1017)}
YB=(928,1006)

def cells(vid, lo, hi):
    A=np.fromfile('analysis/timecode-ticks/band_%s.raw'%vid,dtype=np.uint8).reshape(-1,BH,BW)
    cx=CELL[vid]; H=[];con=[]
    for i in range(lo-1,hi):
        s=A[i, YB[0]-BY:YB[1]-BY, cx[0]-BX:cx[1]-BX].astype(np.float32)
        h=s-ndimage.uniform_filter(s,21)
        con.append(float(np.percentile(h,99)-np.percentile(h,1))); H.append(h.ravel())
    return np.array(H), np.array(con)

def nrm(v):
    v=v-v.mean(); n=np.linalg.norm(v); return v/(n if n>0 else 1)

def boundaries(H, w=8, minsep=30):
    n=len(H); d=np.full(n,np.nan)
    for i in range(w,n-w+1):
        a=nrm(H[i-w:i].mean(0)); b=nrm(H[i:i+w].mean(0))
        d[i]=1.0-float(a@b)
    # peak pick: local max, greedy by height with min separation
    cand=[i for i in range(w+1,n-w) if d[i]>=d[i-1] and d[i]>=d[i+1] and d[i]>np.nanmedian(d)*1.5]
    cand.sort(key=lambda i:-d[i]); sel=[]
    for i in cand:
        if all(abs(i-j)>=minsep for j in sel): sel.append(i)
    return sorted(sel), d

def go(name,vid,lo,hi,fps,w=8,minsep=30,expect=None):
    H,con=cells(vid,lo,hi)
    sel,d=boundaries(H,w,minsep)
    cm=float(np.median(con))
    weak=set(int(k) for k in np.nonzero(con<0.45*cm)[0])
    bf=[lo+k for k in sel]
    gaps=np.diff(bf)
    flag=[]
    for a,b in zip(sel[:-1],sel[1:]):
        flag.append(len(weak&set(range(a,b)))>0)
    print('\n%-30s f%d-%d  glyph contrast median %.1f DN   w=%d'%(name,lo,hi,cm,w))
    print('   boundaries: %s'%bf)
    print('   gaps      : %s'%list(gaps))
    print('   flare in gap: %s'%['F' if f else '.' for f in flag])
    clean=[g for g,f in zip(gaps,flag) if not f]
    # de-alias: a gap near 2x or 3x the modal gap is a MISSED boundary, not a long tick
    if len(gaps):
        base=float(np.median([g for g in gaps if g<60])) if any(g<60 for g in gaps) else float(np.median(gaps))
        norm=[]
        for g in gaps:
            k=max(1,int(round(g/base)))
            norm.append(g/k)
        print('   modal gap %.1f -> de-aliased per-tick: %s'%(base,['%.1f'%x for x in norm]))
        na=np.array(norm)
        print('   ALL gaps  : n=%d  mean %.2f  median %.1f  sd %.2f  -> %.4fx'%(
              len(na),na.mean(),np.median(na),na.std(),fps/na.mean()))
        if clean:
            nc=[]
            for g,f in zip(gaps,flag):
                if f: continue
                k=max(1,int(round(g/base))); nc.append(g/k)
            nc=np.array(nc)
            print('   FLARE-FREE: n=%d  mean %.2f  median %.1f  sd %.2f  -> %.4fx  [%.4fx if median]'%(
                  len(nc),nc.mean(),np.median(nc),nc.std(),fps/nc.mean(),fps/np.median(nc)))
    return dict(name=name,vid=vid,lo=lo,hi=hi,fps=fps,bnd=bf,gaps=[int(g) for g in gaps],
                flare=[bool(f) for f in flag],contrast_median=cm)

if __name__=='__main__':
    N=30000/1001.
    JOBS=[
     ('v1 COLOUR Mk.5 Case31','OpSTlDJWFFI',2600,2905,N),
     ('v1 b/w Case11 tinbird','OpSTlDJWFFI',1055,1290,N),
     ('v1 b/w Case12 taxi','OpSTlDJWFFI',1295,1560,N),
     ('v1 b/w Case12 pacelap','OpSTlDJWFFI',1560,1900,N),
     ('v1 b/w Case26 show&tell','OpSTlDJWFFI',1960,2560,N),
     ('v2 Case21 Triage','Oqw96jCOP7A',1200,1425,N),
     ('v2 Case25 SlimTim','Oqw96jCOP7A',1845,2415,N),
     ('v2 Case20 Brownboys','Oqw96jCOP7A',690,1105,N),
     ('v2 Case11 primer','Oqw96jCOP7A',495,700,N),
     ('v3 Case18','l9RAhmPHM_A',990,1610,N),
     ('v3 Case28','l9RAhmPHM_A',2990,3610,N),
     ('2011 RsQCX A','RsQCXN4o4Ps',690,1010,25.0),
     ('2011 RsQCX B','RsQCXN4o4Ps',1090,1490,25.0),
     ('2011 ZB788 A','ZB788PtqQvg',145,610,25.0),
     ('2011 ZB788 B','ZB788PtqQvg',690,1160,25.0),
    ]
    res=[go(*j) for j in JOBS]
    json.dump(res,open('analysis/timecode-ticks/tickedge.json','w'),indent=1)
