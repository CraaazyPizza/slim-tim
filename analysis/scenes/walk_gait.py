import numpy as np
from scipy import signal as sg
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=np.load('walk_head_bbox.npy'); E=np.load('walk_edge_tracks.npy')
labels=['V x1300 y250','V x1300 y800 (bldg base)','V x520 y500 (L terrain)','H y200 x1330','H y430 x900','H y880 x1150']
f=R[:,0]; w=R[:,3]; cy=R[:,2]+R[:,4]/2; cx=R[:,1]+R[:,3]/2
def det(a,deg=3):
    x=np.arange(len(a)); m=np.isfinite(a)
    return a-np.polyval(np.polyfit(x[m],a[m],deg),x)
# robust growth
m=np.isfinite(w)
k=np.polyfit(f[m],np.log(w[m]),1)
print('head-cap width: log-linear fit -> growth x%.3f over the shot (214 frames); sd of log residual %.3f'%(
    np.exp(k[0]*214), np.std(np.log(w[m])-np.polyval(k,f[m]))))
hy=det(cy); hx=det(cx)
bgY=[det(E[1]),det(E[2])]     # the two faithful vertical-motion tracks
bgX=[det(E[3]),det(E[4]),det(E[5])]
bgy=np.nanmean(np.array(bgY),axis=0); bgx=np.nanmean(np.array(bgX),axis=0)
mm=np.isfinite(hy)&np.isfinite(bgy)
print('\nhead-y residual vs background-y wobble: corr %+.3f   (amplitudes: head sd %.1f px, bg sd %.1f px)'%(
    np.corrcoef(hy[mm],bgy[mm])[0,1],np.nanstd(hy),np.nanstd(bgy)))
mm2=np.isfinite(hx)&np.isfinite(bgx)
print('head-x residual vs background-x wobble: corr %+.3f   (head sd %.1f px, bg sd %.1f px)'%(
    np.corrcoef(hx[mm2],bgx[mm2])[0,1],np.nanstd(hx),np.nanstd(bgx)))
# head motion RELATIVE to background
rel=hy-bgy*(np.nanstd(hy)/np.nanstd(bgy)) if False else hy-bgy
fps=30000/1001
for nm,sig in [('head-y residual',hy),('background-y wobble',bgy),('head-y MINUS background-y',rel)]:
    s=sig[np.isfinite(sig)]
    fr,P=sg.welch(s,fs=fps,nperseg=128)
    i=np.argmax(P[1:])+1
    print('%-28s peak %.2f Hz (video) = %.2f Hz source-rate; power/median %.0f ; sd %.1f px'%(
        nm,fr[i],fr[i]/0.666,P[i]/np.median(P[1:]),s.std()))
plt.figure(figsize=(14,8))
plt.subplot(2,1,1); plt.plot(f,hy,label='head-y residual'); plt.plot(f,bgy,label='background-y wobble (mean of 2 edges)')
plt.legend(); plt.ylabel('px'); plt.grid(alpha=.3); plt.title('Walkabout: does the head bob relative to the background?')
plt.subplot(2,1,2)
for nm,sig in [('head-y res',hy),('bg-y',bgy),('head minus bg',rel)]:
    s=sig[np.isfinite(sig)]; fr,P=sg.welch(s,fs=fps,nperseg=128); plt.semilogy(fr,P,label=nm)
plt.xlabel('Hz (video rate)'); plt.ylabel('PSD'); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig('walk_gait.png',dpi=110); plt.close()
