import numpy as np, json
from lib import *
from scipy.ndimage import gaussian_filter
# (label, frame, y0, x0, size)
P={
'OpSTlDJWFFI':[('DARK',1650,582,1236,256),('BRIGHT',2200,300,900,256),('BRIGHT2',930,390,596,256)],
'Oqw96jCOP7A':[('DARK',800,646,1246,256),('BRIGHT',1900,326,414,256),('BRIGHT2',500,80,800,256)],
'l9RAhmPHM_A':[('DARK',3296,150,400,256),('BRIGHT',1098,538,640,256)],
'ZB788PtqQvg':[('DARK',1009,488,462,256),('BRIGHT',297,104,1102,256)],
'RsQCXN4o4Ps':[('DARK',1125,488,994,256),('BRIGHT',1275,552,1314,256)],
'Xju_CY5ZESA':[('DARK',2208,60,492,256)],
'a6TLGkrfNKI':[('DARK',1986,60,340,180),('MID',350,40,30,180)],
}
READF=[0.05,0.10,0.20,0.30,0.40]
def report(name,noise):
    f,p=radial_ps(noise)
    vals=[np.interp(t,f,p) for t in READF]
    m=(f>=0.04)&(f<=0.45)&(p>0)
    sl=np.polyfit(np.log10(f[m]),np.log10(p[m]),1)[0]
    fw,prof=acorr_fwhm(noise)
    # separable 1D spectra (row-direction = horizontal freq; col = vertical freq)
    a=noise-noise.mean()
    Ph=(np.abs(np.fft.rfft(a*np.hanning(a.shape[1])[None,:],axis=1))**2).mean(0)
    Pv=(np.abs(np.fft.rfft((a.T*np.hanning(a.shape[0])[None,:]),axis=1))**2).mean(0)
    fh=np.fft.rfftfreq(a.shape[1]); fv=np.fft.rfftfreq(a.shape[0])
    nyq_v=Pv[-1]/np.median(Pv[len(Pv)//4:]); nyq_h=Ph[-1]/np.median(Ph[len(Ph)//4:])
    print('   %-9s std=%6.4f  P(0.05/0.1/0.2/0.3/0.4)= %s  slope=%+6.2f  ACF_hw=%5.2fpx  Vnyq/med=%6.2f Hnyq/med=%6.2f'%(
      name,noise.std(),' '.join('%9.3e'%v for v in vals),sl,fw,nyq_v,nyq_h))
    return dict(std=float(noise.std()),P=[float(v) for v in vals],slope=float(sl),acf=float(fw),vnyq=float(nyq_v),hnyq=float(nyq_h))
res={}
for k,plist in P.items():
    print('==== %s  (era %d)'%(k,ERA[k]))
    res[k]={}
    for lab,fr,y,x,b in plist:
        a=F(k,fr)[y:y+b,x:x+b]
        print('  patch %s f%05d y[%d:%d] x[%d:%d] mean=%.1f'%(lab,fr,y,y+b,x,x+b,a.mean()))
        n1=a-gaussian_filter(a,8.0)
        r1=report('HP(s=8)',n1)
        n2=a-gaussian_filter(a,2.0)
        r2=report('HP(s=2)',n2)
        # temporal difference (needs static-ish); use f, f+1
        d=(F(k,fr+1)[y:y+b,x:x+b]-a)/np.sqrt(2)
        r3=report('tdiff k=1',d-gaussian_filter(d,8.0))
        d5=(F(k,fr+5)[y:y+b,x:x+b]-a)/np.sqrt(2)
        r4=report('tdiff k=5',d5-gaussian_filter(d5,8.0))
        res[k][lab]=dict(frame=fr,rect=[y,y+b,x,x+b],mean=float(a.mean()),hp8=r1,hp2=r2,td1=r3,td5=r4)
json.dump(res,open('taskA.json','w'),indent=1)
