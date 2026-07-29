import numpy as np, subprocess, sys, os
os.chdir('/home/user/new-skinny-bob')
JOBS=[('videos/2026/OpSTlDJWFFI.mkv',2985,2997,1920,1080),('videos/2026/Oqw96jCOP7A.mkv',2470,2502,1920,1080),
      ('videos/2026/l9RAhmPHM_A.mkv',4360,4394,1920,1080),('videos/2011/Xju_CY5ZESA.mkv',2560,2597,1920,1080),
      ('videos/2011/RsQCXN4o4Ps.mkv',0,25,1920,1080),('videos/2011/ZB788PtqQvg.mkv',0,25,1920,1080),
      ('videos/2011/a6TLGkrfNKI.mkv',0,25,640,480)]
for path,lo,hi,W,H in JOBS:
    subprocess.run(['ffmpeg','-v','error','-i',path,'-vf','select=between(n\\,%d\\,%d)'%(lo,hi),
                    '-vsync','0','-pix_fmt','yuv420p','-f','rawvideo','/tmp/vq7/b.yuv','-y'],check=True)
    sz=W*H*3//2; a=np.fromfile('/tmp/vq7/b.yuv',dtype=np.uint8); n=len(a)//sz
    hit=False
    for k in range(n):
        Y=a[k*sz:k*sz+W*H].reshape(H,W); u=np.unique(Y)
        if len(u)<=3 and u.min()<=17:
            mn=u.min(); tot=int((Y>mn).sum())
            bl=Y[0:32,0:32]; inb=int((bl>mn).sum())
            br=None
            if W>=992:
                br=Y[0:32,960:992]; inb+=int((br>mn).sum())
            print('%-26s f%-5d %dx%d  Y uniques %-14s  non-min px %-6d  in 32x32 corner block(s) %-6d  outside %-4d  L==R %s'%(
                os.path.basename(path),lo+k,W,H,str(list(u)),tot,inb,tot-inb,
                (np.array_equal(bl,br) if br is not None else 'n/a')))
            hit=True; break
    if not hit: print('%-26s no near-uniform black frame found in f%d-%d'%(os.path.basename(path),lo,hi))
