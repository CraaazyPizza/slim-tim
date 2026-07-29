"""Render the run-averaged seconds-units glyph for each inter-boundary run, so the digit
SEQUENCE can be read off directly.  If the digits step by exactly one per run with no
skips, then no tick boundary was missed and (last-first)/(n_runs) is the true cadence."""
import numpy as np, sys
from PIL import Image
from scipy import ndimage
BW,BH,BX,BY=620,120,590,895
CELL={'OpSTlDJWFFI':(946,1016),'Oqw96jCOP7A':(943,1013),'l9RAhmPHM_A':(903,973),
      'RsQCXN4o4Ps':(949,1019),'ZB788PtqQvg':(948,1016)}
YB=(928,1006)
def band(vid): return np.fromfile('analysis/timecode-ticks/band_%s.raw'%vid,dtype=np.uint8).reshape(-1,BH,BW)
def mont(vid,bnd,out,pad=4,scale=5,wide=None):
    A=band(vid); cx=wide or CELL[vid]
    tiles=[]
    for a,b in zip(bnd[:-1],bnd[1:]):
        seg=A[a-1+pad:b-1-pad, YB[0]-BY:YB[1]-BY, cx[0]-BX:cx[1]-BX].astype(np.float32)
        m=seg.mean(0); m=m-ndimage.uniform_filter(m,25)
        m=(m-m.min())/(m.max()-m.min()+1e-9)
        tiles.append((m*255).astype('uint8'))
    h,w=tiles[0].shape
    M=Image.new('L',(len(tiles)*(w+4),h))
    for k,t in enumerate(tiles): M.paste(Image.fromarray(t),(k*(w+4),0))
    M=M.resize((M.width*scale,M.height*scale),Image.LANCZOS); M.save(out)
    print(out,M.size,'runs:',[ (a,b,b-a) for a,b in zip(bnd[:-1],bnd[1:])])
if __name__=='__main__':
    mont('OpSTlDJWFFI',[2617,2660,2706,2751,2788,2845,2884],'/tmp/vq7/seq_v1col.png',
         wide=(880,1020),scale=4)
    mont('OpSTlDJWFFI',[1585,1630,1676,1720,1765,1810,1855,1890],'/tmp/vq7/seq_v1pace.png',
         wide=(880,1020),scale=4)
    mont('RsQCXN4o4Ps',[1131,1176,1222,1267,1298,1344,1389,1435,1481],'/tmp/vq7/seq_rs.png',
         wide=(880,1030),scale=4)
