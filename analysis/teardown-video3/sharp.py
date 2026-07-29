import numpy as np, json
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
out={}
for i in range(460,4255,5):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    r=a[120:1000,300:1560]
    gx=np.diff(r,axis=1); gy=np.diff(r,axis=0)
    # normalise by local contrast so sharpness isn't just "brighter"
    sd=r.std()+1e-6
    # radial spectrum ratio: high-freq energy / total
    F=np.fft.rfft2(r*np.hanning(r.shape[0])[:,None]*np.hanning(r.shape[1])[None,:])
    P=np.abs(F)**2
    ny,nx=P.shape
    fy=np.fft.fftfreq(r.shape[0])[:,None]; fx=np.fft.rfftfreq(r.shape[1])[None,:]
    rad=np.sqrt(fy**2+fx**2)
    tot=P[rad>0.005].sum()
    hi=P[(rad>0.12)].sum()
    mid=P[(rad>0.04)&(rad<=0.12)].sum()
    # scanline: power at fy~0.186, fx~0
    band=P[:, :4]
    fyv=np.abs(np.fft.fftfreq(r.shape[0]))
    sl=band[(fyv>0.16)&(fyv<0.21)].sum()/max(band[(fyv>0.02)&(fyv<0.16)].sum(),1e-9)
    out[i]=dict(mean=round(float(r.mean()),2), sd=round(float(sd),2),
                grad=round(float((np.abs(gx).mean()+np.abs(gy).mean())/2/sd),5),
                hifrac=round(float(hi/tot),6), midfrac=round(float(mid/tot),6),
                scanratio=round(float(sl),4))
json.dump(out,open('/home/user/new-skinny-bob/analysis/teardown-video3/sharp.json','w'))
print('ok')
