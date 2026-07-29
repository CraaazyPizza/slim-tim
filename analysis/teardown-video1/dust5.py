import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
box=(400,140,1350,520)
fr=list(range(1600,1950))
H=[]
for f in fr:
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(10))).astype(np.float32)
    H.append(a-bg)
H=np.array(H)
recs=[]
for i,f in enumerate(fr):
    m=H[i]<-22
    lab,n=ndimage.label(m)
    if n==0: continue
    sz=ndimage.sum(m,lab,range(1,n+1))
    cen=ndimage.center_of_mass(m,lab,range(1,n+1))
    for s,c in zip(sz,cen):
        if 12<=s<=600:
            recs.append((f,int(s),box[1]+c[0],box[0]+c[1]))
print('n compact dark blobs:',len(recs))
# group into tracks by proximity in space, consecutive frames
recs.sort()
used=[False]*len(recs)
tracks=[]
for i,(f,s,y,x) in enumerate(recs):
    if used[i]: continue
    tr=[(f,s,y,x)]; used[i]=True
    cf,cy,cx=f,y,x
    for j in range(i+1,len(recs)):
        if used[j]: continue
        f2,s2,y2,x2=recs[j]
        if f2>cf+1: 
            if f2>cf+1: break
        if abs(f2-cf)<=1 and abs(y2-cy)<12 and abs(x2-cx)<12:
            tr.append(recs[j]); used[j]=True; cf,cy,cx=f2,y2,x2
    tracks.append(tr)
lens=np.array([len(t) for t in tracks])
print('n tracks',len(tracks),'length hist',np.bincount(lens,minlength=8)[:8],'mean %.2f'%lens.mean())
for t in sorted(tracks,key=lambda t:-len(t))[:12]:
    print('  len %d  frames %d-%d  size %d  y %.0f->%.0f x %.0f->%.0f'%(len(t),t[0][0],t[-1][0],t[0][1],t[0][2],t[-1][2],t[0][3],t[-1][3]))
