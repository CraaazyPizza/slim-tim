import numpy as np
from PIL import Image
from scipy import ndimage as ndi

med = np.load('work/xju_med.npy')
Y0,Y1,X0,X1 = 8,1050,492,1382
sub = med[Y0:Y1, X0:X1].astype(float)
np.save('work/xju_sub.npy', sub)

# paper level: horizontal max over a window wider than a digit, then mild smoothing.
bg = ndi.maximum_filter(sub, size=(21,161))
bg = ndi.gaussian_filter(bg, (6,25))
norm = sub/np.maximum(bg,1.0)
np.save('work/xju_norm.npy', norm)
Image.fromarray(np.clip(norm*230,0,255).astype(np.uint8)).save('out/xju_norm.png')

# ink-step reference levels
print('norm pct', np.round(np.percentile(norm,[0.5,2,10,50,90,99]),3))

def build(thr):
    m = norm < thr
    m = ndi.binary_closing(m, np.ones((9,9)))
    m = ndi.binary_opening(m, np.ones((5,5)))
    lab,n = ndi.label(m)
    sizes = ndi.sum(m, lab, range(1,n+1))
    objs = ndi.find_objects(lab)
    keep = np.zeros_like(m)
    for k in range(n):
        if sizes[k] < 3000: continue
        sl = objs[k]
        # drop anything touching the frame border (vignette)
        if sl[0].start<3 or sl[1].start<3 or sl[0].stop>m.shape[0]-3 or sl[1].stop>m.shape[1]-3: continue
        keep |= (lab==k+1)
    return ndi.binary_fill_holes(keep)

for name,thr in [('t55',0.55),('t64',0.64),('t72',0.72)]:
    h=build(thr)
    np.save(f'work/xju_mask_{name}.npy',h)
    print(name,'area',int(h.sum()),'bbox',ndi.find_objects(h.astype(int))[0])

# overlay
base=np.clip(norm*230,0,255).astype(np.uint8); rgb=np.stack([base]*3,-1)
for name,col in [('t55',(255,0,0)),('t64',(0,255,0)),('t72',(0,160,255))]:
    h=np.load(f'work/xju_mask_{name}.npy'); e=h^ndi.binary_erosion(h); rgb[e]=col
Image.fromarray(rgb).save('out/xju_mask_overlay.png')
