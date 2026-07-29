import numpy as np, json, sys, os
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from PIL import Image, ImageDraw
from run_2026 import measure

def dot(dr,p,c,r=6,lab=None):
    dr.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],outline=c,width=2)
    if lab: dr.text((p[0]+r+2,p[1]-6),lab,fill=c)

def draw2026(n,frac,path,box=(320,900,540,1020)):
    r=measure(n,frac)
    img=np.asarray(Image.open(f'/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f{n:05d}.png').convert('L')).astype(float)
    lo,hi=np.percentile(img[box[0]:box[1],box[2]:box[3]],[1,99])
    v=np.clip((img-lo)/(hi-lo)*255,0,255).astype(np.uint8)
    im=Image.fromarray(np.stack([v]*3,-1)).crop((box[2],box[0],box[3],box[1]))
    im=im.resize((im.width*3,im.height*3),Image.LANCZOS)
    dr=ImageDraw.Draw(im)
    def T(p): return ((p[0]-box[2])*3,(p[1]-box[0])*3)
    for k,c in [('C23',(255,60,60)),('C34',(255,60,60))]:
        p=r[k]; dot(dr,T(p),c,10,k)
        pr=r[k+'_prof']
        for xx,yy in zip(pr['x'],pr['y']): dr.point(T((xx,yy)),fill=(0,200,255))
    for k,p in r['tips'].items(): dot(dr,T(p),(60,255,60),10,k)
    dr.line([T(r['tips']['T3']),T(r['C34'])],fill=(255,220,0),width=2)
    dr.line([T(r['tips']['T4']),T(r['C34'])],fill=(255,120,255),width=3)
    dr.line([T(r['tips']['T2']),T(r['C23'])],fill=(255,220,0),width=2)
    dr.text((10,10),f'f{n:05d}  frac={frac}',fill=(255,255,0))
    im.save(path); return r
if __name__=='__main__':
    for fr in [0.5,0.7,0.85]:
        draw2026(3866,fr,f'out/v3_f3866_landmarks_frac{int(fr*100)}.png')
    print('done')
