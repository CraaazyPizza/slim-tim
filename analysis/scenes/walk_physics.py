import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=np.load('walk_head_bbox.npy')   # f, x, y, w, h
f=R[:,0]; w=R[:,3]; cx=R[:,1]+R[:,3]/2; cy=R[:,2]+R[:,4]/2
def sm(a,k=21):
    ker=np.ones(k)/k; return np.convolve(np.pad(a,(k//2,k//2),mode='edge'),ker,mode='valid')
ws=sm(w); cys=sm(cy); cxs=sm(cx)
# 1) is head-cap width monotone-ish? robustness
print('head width: start %.1f end %.1f ratio %.3f; fraction of frames where smoothed w decreases: %.2f'%(
    ws[0],ws[-1],ws[-1]/ws[0],(np.diff(ws)<0).mean()))
# 2) ground-plane test: y_head should be LINEAR in w (both ~ 1/distance)
A=np.polyfit(ws,cys,1); pred=np.polyval(A,ws)
ss=1-((cys-pred)**2).sum()/((cys-cys.mean())**2).sum()
print('\nGROUND-PLANE TEST  y_head = a + b*w  ->  b=%.3f  a=%.1f  R^2=%.4f  residual rms %.2f px'%(A[0],A[1],ss,np.std(cys-pred)))
print('  implied horizon row (w->0): y=%.1f'%A[1])
# control: quadratic gains?
A2=np.polyfit(ws,cys,2); ss2=1-((cys-np.polyval(A2,ws))**2).sum()/((cys-cys.mean())**2).sum()
print('  quadratic R^2=%.4f (gain %.4f) -> linear model adequate' % (ss2, ss2-ss))
# 3) constant-speed test: 1/w should be LINEAR in time
inv=1/ws
B=np.polyfit(f,inv,1); ssv=1-((inv-np.polyval(B,f))**2).sum()/((inv-inv.mean())**2).sum()
print('\nCONSTANT-SPEED TEST  1/w = c - v*t  ->  R^2=%.4f'%ssv)
B2=np.polyfit(f,inv,2); ssv2=1-((inv-np.polyval(B2,f))**2).sum()/((inv-inv.mean())**2).sum()
print('  quadratic R^2=%.4f (gain %.4f)'%(ssv2,ssv2-ssv))
# 4) lateral: cx vs w  (walking on a straight line offset from optical axis -> also linear in w)
C=np.polyfit(ws,cxs,1); ssc=1-((cxs-np.polyval(C,ws))**2).sum()/((cxs-cxs.mean())**2).sum()
print('\nLATERAL TEST  x_head = a + b*w  -> R^2=%.4f  residual rms %.2f px'%(ssc,np.std(cxs-np.polyval(C,ws))))
# 5) gait: residual of head height about the smooth trend -> bobbing?
res=cy-cys
from scipy import signal as sg
fr,P=sg.welch(res,fs=30000/1001,nperseg=128)
i=np.argmax(P[1:])+1
print('\nGAIT/BOB TEST: residual head-y sd %.2f px; strongest periodicity %.2f Hz (period %.1f frames), power ratio to median %.1f'%(
    res.std(),fr[i],(30000/1001)/fr[i],P[i]/np.median(P[1:])))
plt.figure(figsize=(14,9))
plt.subplot(2,2,1); plt.plot(f,w,'.',ms=2,alpha=.4); plt.plot(f,ws,lw=2); plt.xlabel('frame'); plt.ylabel('head-cap width (px)'); plt.title('figure apparent size: x%.2f over the shot'%(ws[-1]/ws[0])); plt.grid(alpha=.3)
plt.subplot(2,2,2); plt.plot(ws,cys,'.'); plt.plot(ws,pred,'r'); plt.xlabel('head width (px)  [~1/distance]'); plt.ylabel('head centre y'); plt.gca().invert_yaxis()
plt.title('ground-plane consistency: R^2=%.4f'%ss); plt.grid(alpha=.3)
plt.subplot(2,2,3); plt.plot(f,inv,'.'); plt.plot(f,np.polyval(B,f),'r'); plt.xlabel('frame'); plt.ylabel('1/width  [~distance]'); plt.title('constant approach speed: R^2=%.4f'%ssv); plt.grid(alpha=.3)
plt.subplot(2,2,4); plt.plot(f,res,lw=1); plt.xlabel('frame'); plt.ylabel('head-y residual (px)'); plt.title('residual about smooth trend (gait bob?)'); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig('walk_physics.png',dpi=110); plt.close()
