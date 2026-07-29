import numpy as np, sys
from PIL import Image
from scipy import ndimage as ndi

def load(n):
    return np.asarray(Image.open(f'/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f{n:05d}.png').convert('L')).astype(float)

def seg(a, box, thr=1.20, capthr=70):
    y0,y1,x0,x1 = box
    sub = a[y0:y1, x0:x1]
    bg = ndi.grey_erosion(sub, size=(111,111))
    bg = ndi.gaussian_filter(bg, 25)
    norm = sub/np.maximum(bg,1.0)
    bright = norm > thr
    caps  = sub < capthr
    m = bright | caps
    m = ndi.binary_closing(m, np.ones((9,9)))
    m = ndi.binary_opening(m, np.ones((5,5)))
    lab,n = ndi.label(m)
    sizes = ndi.sum(m, lab, range(1,n+1))
    k = int(np.argmax(sizes))+1
    hand = ndi.binary_fill_holes(lab==k)
    return sub, norm, hand

if __name__=='__main__':
    a=load(3866)
    box=(300,1000,520,1060)
    sub,norm,hand = seg(a,box)
    Image.fromarray(np.clip(norm*140,0,255).astype(np.uint8)).save('out/v3_norm.png')
    rgb=np.stack([np.clip((sub-29)/(176-29)*255,0,255).astype(np.uint8)]*3,-1)
    e=hand^ndi.binary_erosion(hand); rgb[e]=(0,255,0)
    Image.fromarray(rgb).resize((rgb.shape[1]*2,rgb.shape[0]*2)).save('out/v3_seg_overlay.png')
    print('area',hand.sum())
