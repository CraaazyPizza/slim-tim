import json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=json.load(open('/home/user/new-skinny-bob/analysis/cyrillic/kx2.json'))
kx=np.array(D['kx']); faces=[k for k in D if k!='kx']
fig,ax=plt.subplots(figsize=(11,6.2),dpi=170)
cols=plt.cm.tab10(np.linspace(0,1,10))
for i,f in enumerate(faces):
    y=np.array(D[f]['f983']); ax.plot(kx,y,lw=2.4,color=cols[i],label='%s  (peak %.3f at kx=%.2f)'%(f,y.max(),kx[y.argmax()]))
nul=np.max([np.array(D[f]['null']) for f in faces],axis=0)
ax.plot(kx,nul,lw=2.0,ls='--',color='0.35',label='caption-free control frames (best of all faces)')
ax.axvline(1.0,color='0.6',lw=1.2); ax.text(1.005,0.03,'kx = 1.00\n(what every previous\nanalysis assumed)',fontsize=9,color='0.3',va='bottom')
ax.set_xlabel('horizontal stretch applied to the template  $k_x$',fontsize=12)
ax.set_ylabel('best normalised cross-correlation with the real pixels',fontsize=12)
ax.set_title('The hidden caption is HORIZONTALLY STRETCHED — line 1, frame 983, known text',fontsize=13.5,weight='bold')
ax.legend(fontsize=8.6,loc='upper left',framealpha=0.95)
ax.grid(alpha=0.25); ax.set_xlim(kx.min(),kx.max()); ax.set_ylim(0,0.85)
fig.text(0.012,0.012,'At $k_x=1$ (isotropic scaling) no installed face exceeds r = 0.25. Allowing a free horizontal scale takes the same fonts to r = 0.67-0.78 at $k_x\\approx1.15-1.45$.\nEvery typeface number previously recorded for this caption was measured at $k_x=1$ and is therefore meaningless.',fontsize=8.8)
fig.tight_layout(rect=[0,0.055,1,1])
fig.savefig('/home/user/new-skinny-bob/figs/cyrillic/FIG3_stretch_evidence.png')
print('FIG3 ok')
