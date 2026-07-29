import numpy as np
from PIL import Image
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
res=np.load('walk_track_1625_1832.npy')
g=res[res[:,4]>0.85]
x,y,dx,dy=g[:,0],g[:,1],g[:,2],g[:,3]
# fit similarity: [dx,dy] = (s-1)*[x-cx, y-cy] + [tx,ty]
A=np.zeros((2*len(x),4)); b=np.zeros(2*len(x))
A[0::2,0]=x; A[0::2,1]=1; b[0::2]=dx
A[1::2,2]=y; A[1::2,3]=1; b[1::2]=dy
# solve independently for x and y scale
sx,bx=np.polyfit(x,dx,1); sy,by=np.polyfit(y,dy,1)
print('x-expansion coeff %.5f  (scale %.4f)  focus x0=%.1f'%(sx,1+sx,-bx/sx))
print('y-expansion coeff %.5f  (scale %.4f)  focus y0=%.1f'%(sy,1+sy,-by/sy))
pred_dx=sx*x+bx; pred_dy=sy*y+by
rx=dx-pred_dx; ry=dy-pred_dy
print('residual rms: x %.2f px, y %.2f px  (motion magnitude med %.1f px)'%(rx.std(),ry.std(),np.median(np.hypot(dx,dy))))
np.save('walk_resid.npy',np.c_[x,y,dx,dy,rx,ry,g[:,4]])
# quiver plot
im=np.asarray(Image.open('/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f01625.png').convert('L'))
fig,axs=plt.subplots(1,2,figsize=(20,6))
axs[0].imshow(im,cmap='gray',vmin=0,vmax=90); axs[0].quiver(x,y,dx,-dy,color='lime',angles='xy',scale_units='xy',scale=0.25,width=0.002)
axs[0].set_title('f1625 -> f1832 raw patch motion (x4)')
axs[1].imshow(im,cmap='gray',vmin=0,vmax=90); q=axs[1].quiver(x,y,rx,-ry,np.hypot(rx,ry),cmap='autumn',angles='xy',scale_units='xy',scale=0.06,width=0.002)
axs[1].set_title('residual after best global zoom+pan (x16)'); plt.colorbar(q,ax=axs[1])
for a in axs: a.set_xlim(300,1650); a.set_ylim(1060,20)
plt.tight_layout(); plt.savefig('walk_quiver.png',dpi=110); plt.close()
# depth stratification: compare expansion for image regions
for lab,m in [('upper bg y<350',y<350),('mid 350-650',(y>=350)&(y<650)),('lower y>650',y>=650),
              ('right building x>1150',x>1150),('left terrain x<800',x<800)]:
    if m.sum()<6: continue
    sxx=np.polyfit(x[m],dx[m],1)[0]; syy=np.polyfit(y[m],dy[m],1)[0]
    print('%-24s n=%3d  local x-expansion %.5f  y-expansion %.5f  mean|d|=%.1f'%(lab,m.sum(),sxx,syy,np.hypot(dx[m],dy[m]).mean()))
