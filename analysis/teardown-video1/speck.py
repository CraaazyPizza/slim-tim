import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
fr=list(range(950,1042))
S=[]
for f in fr:
    a=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)[150:900,360:1570]
    S.append(a-np.median(a))
S=np.array(S); med=np.median(S,0); res=S-med
# find top isolated dark events
flat=res.reshape(len(fr),-1)
order=np.argsort(flat.min(0))
done=[]
for pix in order[:400000]:
    y,x=divmod(pix,res.shape[2])
    if any(abs(y-yy)<25 and abs(x-xx)<25 for yy,xx in done): continue
    done.append((y,x))
    ts=res[:,y,x]
    i=int(np.argmin(ts))
    print('mark at (y=%d,x=%d) abs(%d,%d)  min %.1f at frame %d'%(y,x,y+150,x+360,ts[i],fr[i]))
    lo=max(0,i-4); hi=min(len(fr),i+5)
    print('   ',' '.join('%d:%+.1f'%(fr[j],ts[j]) for j in range(lo,hi)))
    if len(done)>=10: break
