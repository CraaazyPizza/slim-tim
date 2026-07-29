import sys,os,numpy as np
from PIL import Image
def run(fd,label,f0,f1):
    files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
    acc=None;n=0
    for i in range(f0,f1+1):
        a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
        acc=a if acc is None else acc+a; n+=1
    M=acc/n
    reg=M[880:1060, 200:1200]
    base=float(np.median(reg))
    dark=reg<base*0.5
    # largest connected dark blob via row/col projections of the dominant component
    colf=dark.mean(0); rowf=dark.mean(1)
    cs=np.nonzero(colf>0.25)[0]; rs=np.nonzero(rowf>0.15)[0]
    if len(cs)==0 or len(rs)==0: print('%-12s no bar'%label); return
    # refine: take contiguous run containing the max
    def contig(v,thr):
        idx=np.nonzero(v>thr)[0]
        if len(idx)==0: return None
        best=[idx[0],idx[0]]; cur=[idx[0],idx[0]]
        for x in idx[1:]:
            if x==cur[1]+1: cur[1]=x
            else:
                if cur[1]-cur[0]>best[1]-best[0]: best=cur[:]
                cur=[x,x]
        if cur[1]-cur[0]>best[1]-best[0]: best=cur[:]
        return best
    cb=contig(colf,0.25); rb=contig(rowf,0.15)
    x0,x1=200+cb[0],200+cb[1]; y0,y1=880+rb[0],880+rb[1]
    blob=M[y0:y1+1,x0:x1+1]
    print('%-12s f%d-%d  bar x=%d..%d (w=%d)  y=%d..%d (h=%d)  luma=%.1f (min %.1f)  bg=%.1f  ratio=%.3f'%(
        label,f0,f1,x0,x1,x1-x0+1,y0,y1,y1-y0+1,blob.mean(),blob.min(),base,blob.mean()/base))
run('frames/ZB788PtqQvg','ZB788_2011',181,274)
run('frames/RsQCXN4o4Ps','RsQCX_2011',1389,1485)
run('frames/Oqw96jCOP7A','Oqw96_2026',1207,1410)
run('frames/l9RAhmPHM_A','l9RAh_2026',1942,2099)
run('frames/OpSTlDJWFFI','OpSTl_2026',1300,1400)
