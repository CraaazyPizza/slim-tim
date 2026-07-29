import numpy as np, os
from PIL import Image
from scipy.ndimage import gaussian_filter, uniform_filter
V={'OpSTlDJWFFI':'/home/user/new-skinny-bob/frames/OpSTlDJWFFI',
'Oqw96jCOP7A':'/home/user/new-skinny-bob/frames/Oqw96jCOP7A',
'l9RAhmPHM_A':'/home/user/new-skinny-bob/frames/l9RAhmPHM_A',
'ZB788PtqQvg':'/home/user/new-skinny-bob/frames/ZB788PtqQvg',
'RsQCXN4o4Ps':'/home/user/new-skinny-bob/frames/RsQCXN4o4Ps',
'Xju_CY5ZESA':'/home/user/new-skinny-bob/frames/Xju_CY5ZESA',
'a6TLGkrfNKI':'/home/user/new-skinny-bob/frames/a6TLGkrfNKI'}
ERA={'OpSTlDJWFFI':2026,'Oqw96jCOP7A':2026,'l9RAhmPHM_A':2026,
     'ZB788PtqQvg':2011,'RsQCXN4o4Ps':2011,'Xju_CY5ZESA':2011,'a6TLGkrfNKI':2011}
def F(k,i,rgb=False):
    im=Image.open(os.path.join(V[k],'f%05d.png'%i))
    return np.asarray(im.convert('RGB' if rgb else 'L'),dtype=np.float64)
def nframes(k): return len(os.listdir(V[k]))
def hp(p,sigma=2.0):
    "high-pass: remove structure coarser than sigma"
    return p-gaussian_filter(p,sigma)
def radial_ps(noise):
    "radially averaged power spectrum; returns (freq cyc/px, power)"
    a=noise-noise.mean()
    n=a.shape[0]
    w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
    A=np.fft.fftshift(np.fft.fft2(a*w))
    P=np.abs(A)**2/(a.shape[0]*a.shape[1])
    cy,cx=np.array(P.shape)//2
    y,x=np.indices(P.shape)
    fy=(y-cy)/P.shape[0]; fx=(x-cx)/P.shape[1]
    r=np.sqrt(fy**2+fx**2)
    nb=64; edges=np.linspace(0,0.5,nb+1)
    idx=np.digitize(r.ravel(),edges)-1
    pr=np.bincount(idx,weights=P.ravel(),minlength=nb)[:nb]
    ct=np.bincount(idx,minlength=nb)[:nb]
    ok=ct>0
    f=0.5*(edges[:-1]+edges[1:])
    return f[ok],(pr[ok]/np.maximum(ct[ok],1))
def acorr2(noise):
    a=noise-noise.mean()
    A=np.fft.fft2(a)
    c=np.fft.fftshift(np.real(np.fft.ifft2(A*np.conj(A))))
    return c/c.max()
def acorr_fwhm(noise):
    "radial autocorrelation; return radius where it drops to 0.5 (interp), in px"
    c=acorr2(noise)
    cy,cx=np.array(c.shape)//2
    y,x=np.indices(c.shape); r=np.sqrt((y-cy)**2+(x-cx)**2)
    nb=40
    prof=[]
    for i in range(nb):
        m=(r>=i-0.5)&(r<i+0.5)
        prof.append(c[m].mean() if m.any() else np.nan)
    prof=np.array(prof)
    # first crossing of 0.5
    for i in range(1,nb):
        if prof[i]<0.5:
            f=(prof[i-1]-0.5)/(prof[i-1]-prof[i])
            return (i-1)+f, prof
    return np.nan,prof

# conservative picture-area rects (y0,y1,x0,x1) inside the gate / active image
PIC={'OpSTlDJWFFI':(70,1010,340,1570),
     'Oqw96jCOP7A':(70,1010,350,1560),
     'l9RAhmPHM_A':(90,990,320,1580),
     'ZB788PtqQvg':(40,1010,270,1690),
     'RsQCXN4o4Ps':(40,1000,290,1660),
     'Xju_CY5ZESA':(60,1020,300,1490),
     'a6TLGkrfNKI':(35,430,10,630)}
# matte / outside-gate rects
MATTE={'OpSTlDJWFFI':(300,1000,40,270),
       'Oqw96jCOP7A':(200,900,60,280),
       'l9RAhmPHM_A':(300,1000,30,280),
       'ZB788PtqQvg':(300,1000,40,190),
       'RsQCXN4o4Ps':(300,1000,40,210),
       'Xju_CY5ZESA':(300,1000,40,250),
       'a6TLGkrfNKI':(200,400,2,30)}
