import sys,os,numpy as np,hashlib
from PIL import Image
fd=sys.argv[1]; lim=int(sys.argv[2]) if len(sys.argv)>2 else 100000
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])[:lim]
h=[]
for f in files:
    a=np.asarray(Image.open(os.path.join(fd,f)).convert('L'))
    h.append(hashlib.md5(a.tobytes()).hexdigest())
# run-length of identical consecutive hashes
runs=[];cur=1
for i in range(1,len(h)):
    if h[i]==h[i-1]: cur+=1
    else: runs.append(cur); cur=1
runs.append(cur)
runs=np.array(runs)
uniq=len(set(h))
print(os.path.basename(fd.rstrip('/')), 'frames',len(h),'unique',uniq,'ratio %.4f'%(uniq/len(h)))
bc=np.bincount(runs)
print('  dup-run histogram (runlen:count):', {i:int(c) for i,c in enumerate(bc) if c>0})
print('  mean run %.3f'%runs.mean())
