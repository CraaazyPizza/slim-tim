import sys,os,numpy as np
from PIL import Image
def gb(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
DS=2
# --- build template from OpSTlDJWFFI f959-1000, band y934-994 x420-1520
fd='frames/OpSTlDJWFFI'; files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
acc=None;n=0
for i in range(959,1001):
    a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
    acc=a if acc is None else acc+a; n+=1
M=acc/n
Tfull=(M-gb(M,22))[934:994,420:1520]
H,W=Tfull.shape
T=np.asarray(Image.fromarray(Tfull,mode='F').resize((W//DS,H//DS),Image.BOX),dtype=np.float32)
T=T-T.mean(); T/=np.linalg.norm(T)
th,tw=T.shape
print('template %dx%d (downscale %d) built from OpSTlDJWFFI f959-1000 y934-994 x420-1520'%(th,tw,DS))
def ncc_max(frame):
    g=frame-gb(frame,22)
    gh,gw=g.shape
    A=np.asarray(Image.fromarray(g,mode='F').resize((gw//DS,gh//DS),Image.BOX),dtype=np.float32)
    ah,aw=A.shape
    if ah<th or aw<tw: return -9
    # sliding NCC via FFT
    fs=(ah,aw)
    F=np.fft.rfft2(A,s=fs); Tp=np.zeros(fs,np.float32); Tp[:th,:tw]=T[::-1,::-1]
    num=np.fft.irfft2(F*np.fft.rfft2(Tp,s=fs),s=fs)
    ones=np.zeros(fs,np.float32); ones[:th,:tw]=1
    s1=np.fft.irfft2(np.fft.rfft2(A,s=fs)*np.fft.rfft2(ones[::-1,::-1],s=fs),s=fs)
    s2=np.fft.irfft2(np.fft.rfft2(A*A,s=fs)*np.fft.rfft2(ones[::-1,::-1],s=fs),s=fs)
    cnt=th*tw
    var=s2-s1*s1/cnt
    var=np.where(var>1e-6,var,np.inf)
    r=num/np.sqrt(var)
    valid=r[th-1:ah,tw-1:aw] if ah>=th and aw>=tw else r
    return float(np.nanmax(valid))
SETS=[('OpSTlDJWFFI','frames/OpSTlDJWFFI',2998),('Oqw96jCOP7A','frames/Oqw96jCOP7A',2503),
      ('l9RAhmPHM_A','frames/l9RAhmPHM_A',4395),
      ('ZB788PtqQvg','frames/ZB788PtqQvg',1188),
      ('RsQCXN4o4Ps','frames/RsQCXN4o4Ps',1500),
      ('Xju_CY5ZESA','frames/Xju_CY5ZESA',2598),
      ('a6TLGkrfNKI','frames/a6TLGkrfNKI',2337)]
STEP=6
for name,d,cnt in SETS:
    fl=sorted([f for f in os.listdir(d) if f.endswith('.png')])
    best=(-9,None); vals=[]
    for i in range(1,len(fl)+1,STEP):
        fr=np.asarray(Image.open(os.path.join(d,fl[i-1])).convert('L'),dtype=np.float32)
        v=ncc_max(fr); vals.append(v)
        if v>best[0]: best=(v,i)
    vals=np.array([v for v in vals if v>-8])
    print('%-12s frames scanned=%d  max NCC=%.4f at frame %s   p50=%.4f p99=%.4f'%(name,len(vals),best[0],best[1],np.percentile(vals,50),np.percentile(vals,99)))
