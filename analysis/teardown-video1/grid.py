import sys
from PIL import Image, ImageDraw
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def grid(frames,out,cols=4,tw=440,box=None):
    ims=[]
    for f in frames:
        im=Image.open(F.format(f)).convert('RGB')
        if box: im=im.crop(box)
        r=tw/im.width
        im=im.resize((tw,int(im.height*r)),Image.LANCZOS)
        d=ImageDraw.Draw(im); d.rectangle([0,0,72,16],fill=(0,0,0)); d.text((3,3),str(f),fill=(255,255,0))
        ims.append(im)
    th=ims[0].height; rows=(len(ims)+cols-1)//cols
    c=Image.new('RGB',(cols*tw,rows*th),(30,30,30))
    for i,im in enumerate(ims): c.paste(im,((i%cols)*tw,(i//cols)*th))
    c.save(out); print(out,c.size)
if __name__=='__main__':
    a,b,st,out=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
    cols=int(sys.argv[5]) if len(sys.argv)>5 else 4
    grid(list(range(a,b+1,st)),out,cols=cols)
