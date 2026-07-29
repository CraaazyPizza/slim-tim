import cv2, numpy as np, itertools
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
fs=list(range(1621,1836))
st=np.stack([cv2.GaussianBlur(cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32),(0,0),2.0) for f in fs])
def track1d(kind,k,c0,half=45,sign=+1):
    """track a bright(+)/dark(-) extremum of the 1-D profile along a scan line"""
    pos=[];c=c0
    for i in range(len(fs)):
        prof = st[i,k,:] if kind=='h' else st[i,:,k]
        lo=max(0,int(c-half)); hi=min(len(prof),int(c+half))
        if hi-lo<10: pos.append(np.nan); continue
        seg=prof[lo:hi].astype(np.float64)
        w = seg-seg.min() if sign>0 else seg.max()-seg
        w=np.clip(w-0.5*w.max(),0,None)
        if w.sum()<1e-6: pos.append(np.nan); continue
        p=lo+(w*np.arange(len(seg))).sum()/w.sum()
        pos.append(p); c=0.75*c+0.25*p
    return np.array(pos)
tracks={
 'V x=1300 dark band ~y250 (bldg top)':  ('v',1300,250,-1),
 'V x=1300 dark band ~y800 (bldg base)': ('v',1300,810,-1),
 'V x=520  dark band ~y500 (L terrain)': ('v',520,500,-1),
 'H y=200  bright ridge ~x1330':         ('h',200,1330,+1),
 'H y=430  bright band ~x900':           ('h',430,900,+1),
 'H y=880  bright band ~x1150':          ('h',880,1150,+1),
}
T={}
for lab,(kind,k,c0,s) in tracks.items():
    p=track1d(kind,k,c0,45,s); T[lab]=p
    print('%-40s pos %7.1f .. %7.1f  (p2p %5.1f px)  sd %5.2f  median|step| %.2f'%(
        lab,np.nanmin(p),np.nanmax(p),np.nanmax(p)-np.nanmin(p),np.nanstd(p),np.nanmedian(np.abs(np.diff(p)))))
np.save('walk_edge_tracks.npy',np.array([T[k] for k in tracks]))
print('\npairwise correlation of the (detrended) wobble series:')
def det(a):
    x=np.arange(len(a)); m=~np.isnan(a)
    c=np.polyfit(x[m],a[m],2); return a-np.polyval(c,x)
D={k:det(v) for k,v in T.items()}
ks=list(tracks)
for a,b in itertools.combinations(ks,2):
    m=~np.isnan(D[a])&~np.isnan(D[b])
    print('  %.3f   %-40s vs %s'%(np.corrcoef(D[a][m],D[b][m])[0,1],a,b))
plt.figure(figsize=(15,8))
plt.subplot(2,1,1)
for k in ks: plt.plot(fs,T[k],lw=1,label=k)
plt.ylabel('edge position (px)'); plt.legend(fontsize=7); plt.grid(alpha=.3)
plt.subplot(2,1,2)
for k in ks: plt.plot(fs,D[k],lw=1,label=k)
plt.ylabel('detrended wobble (px)'); plt.xlabel('frame'); plt.grid(alpha=.3)
plt.suptitle('Walkabout: sub-pixel 1-D tracking of six background edges')
plt.tight_layout(); plt.savefig('walk_edge_tracks.png',dpi=110); plt.close()
