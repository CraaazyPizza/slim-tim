"""The glyph after «АА» on line 2 — ranked over the whole Cyrillic alphabet.
Geometry is fixed by fitting the PREFIX «предупреждало об АА» only, so the prefix
cannot pay for the last glyph.  The score window covers ONLY the last-glyph cell."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
from fast import _font
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
R2=(998,1078)
def obs(fs,XS):
    return (-RESL[[FR.index(f) for f in fs]].mean(0))[(R2[0]-Y0):(R2[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
PREFIX='предупреждало об АА'
UP='АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ'
LO='абвгдежзийклмнопрстуфхцчшщъыьэюя'
EXTRA=[')','.',',','?','!','-',':','"','']
def render_at(fp,text,size,kx,H,W,xleft,baseline):
    """render `text` with its ink-left at xleft and baseline at `baseline` (window coords)"""
    f=_font(fp,size); b=f.getbbox(text)
    w=max(2,b[2]-b[0]+8); h=max(2,b[3]-b[1]+8)
    im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-b[0],4-b[1]),text,font=f,fill=0)
    A=np.asarray(im,dtype=np.uint8)
    nw=max(2,int(round(w*kx)))
    T=1.0-np.asarray(Image.fromarray(A).resize((nw,h),Image.LANCZOS),dtype=np.float64)/255.0
    # baseline within A: default anchor puts the ascender top at the draw y
    asc,_desc = f.getmetrics()
    by = 4 - b[1] + asc
    out=np.zeros((H,W)); y0=int(round(baseline-by)); x0=int(round(xleft-4*kx))
    a,bb=max(0,y0),min(H,y0+h); c,d=max(0,x0),min(W,x0+nw)
    if bb<=a or d<=c: return out
    out[a:bb,c:d]=T[a-y0:bb-y0,c-x0:d-x0]; return out

def ncc_win(obsW, tmplW, hpsig=12.0):
    """NCC of two same-shape arrays after the same row-mean + high-pass prep."""
    def pr(X):
        Y=X-X.mean(axis=1,keepdims=True); Y=Y-gf(Y,hpsig,truncate=3.0); return Y-Y.mean()
    a=pr(obsW); b=pr(tmplW)
    n=np.sqrt((a*a).sum()*(b*b).sum())
    return float((a*b).sum()/n) if n>1e-15 else 0.0

if __name__=='__main__':
    XS=(432,1680); H=R2[1]-R2[0]; W=XS[1]-XS[0]
    OBS={'f983':obs([983],XS),'best5':obs([983,973,974,984,981],XS),'stack20':obs(CAP,XS),
         'NULL20':obs(list(range(1010,1030)),XS),'NULL1':obs([1020],XS)}
    G=json.load(open('l2geo.json'))          # written by l2fit.py
    out={}
    for tag,O in OBS.items():
        fp=ALL[G['font']]; size=G['size']; kx=G['kx']; bl=G['blur']
        xleft=float(G['xleft'])-XS[0]; base=float(G['baseline'])-R2[0]
        # last-glyph cell: from the right edge of the second А to +1.3 advances
        cellx0=int(round(G['cell_x0']))-XS[0]; cellx1=int(round(G['cell_x1']))-XS[0]
        sel=(slice(0,H), slice(max(0,cellx0-10), min(W,cellx1+10)))
        rows=[]
        for ch in list(UP)+list(LO)+EXTRA:
            ink=render_at(fp,PREFIX+ch,size,kx,H,W,xleft,base)
            t=gf(ink,bl)
            rows.append((ch, ncc_win(O[sel], t[sel])))
        rows.sort(key=lambda t:-t[1])
        vals=np.array([r[1] for r in rows])
        mu,sd=vals.mean(),vals.std()
        out[tag]=[(c,v,(v-mu)/sd) for c,v in rows]
        print('\n=== last glyph after «АА», %s === (window x %d..%d)  field mean %.4f sd %.4f'%(tag,G['cell_x0'],G['cell_x1'],mu,sd))
        for c,v in rows[:14]: print('   %-3s r=%.4f   z=%+.2f'%(repr(c),v,(v-mu)/sd))
        print('   ... bottom: '+', '.join('%s %.3f'%(repr(c),v) for c,v in rows[-5:]))
        sys.stdout.flush()
    json.dump(out,open('l2last.json','w'),indent=1,ensure_ascii=False)
