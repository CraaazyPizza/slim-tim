import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
fs=list(range(1621,1836))
stack=np.stack([cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32) for f in fs])
print('stack',stack.shape)
np.save('walk_stack_mean.npy',stack.mean(0))
sd=stack.std(0)
# per-pixel temporal sd map
plt.figure(figsize=(16,6))
plt.subplot(1,2,1); plt.imshow(stack[0],cmap='gray'); plt.title('f1621'); plt.xlim(350,1600); plt.ylim(1040,40)
plt.subplot(1,2,2); im=plt.imshow(sd,cmap='inferno',vmin=0,vmax=np.percentile(sd[80:1000,380:1560],99.5))
plt.colorbar(im); plt.title('temporal SD over f1621-1835 (DN)'); plt.xlim(350,1600); plt.ylim(1040,40)
plt.tight_layout(); plt.savefig('walk_temporal_sd.png',dpi=110); plt.close()

# region MAD vs lag, referenced to f1621
regions={'building far R (x1300-1550,y350-800)':(1300,1550,350,800),
         'terrain top-L (x400-700,y100-300)':(400,700,100,300),
         'ground low-L (x400-620,y780-880)':(400,620,780,880),
         'bg just LEFT of figure (x430-520,y500-800)':(430,520,500,800),
         'bg just RIGHT of figure (x1080-1170,y450-800)':(1080,1170,450,800),
         'sky/terrain top-R (x1150-1450,y90-230)':(1150,1450,90,230)}
plt.figure(figsize=(13,6))
print('\nMAD vs f1621 (DN):   lag3    lag30   lag100  lag214   |  frame-to-frame median')
for lab,(x0,x1,y0,y1) in regions.items():
    A=stack[:,y0:y1,x0:x1]
    mad=np.abs(A-A[0]).mean(axis=(1,2))
    f2f=np.abs(np.diff(A,axis=0)).mean(axis=(1,2))
    print('%-44s %6.3f %7.3f %7.3f %7.3f  |  %6.3f'%(lab,mad[3],mad[30],mad[100],mad[-1],np.median(f2f)))
    plt.plot(fs,mad,label=lab)
plt.xlabel('frame'); plt.ylabel('mean |I(f)-I(1621)| (DN)'); plt.legend(fontsize=7); plt.grid(alpha=.3)
plt.title('Walkabout: background drift from the first frame, by region')
plt.tight_layout(); plt.savefig('walk_region_drift.png',dpi=110); plt.close()

# noise floor: shot-noise proxy from the flat black outside the aperture
out=stack[:,20:40,60:200]
print('\noutside-aperture (matte) temporal sd: %.4f DN  -> essentially zero'%out.std(0).mean())
