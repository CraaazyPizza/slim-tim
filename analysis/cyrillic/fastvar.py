"""Extend fast.py's font loader to understand variable-instance specs of the form
    /path/Inter.ttf#wght=575          or   /path/Inter.ttf#wght=575,opsz=14
so every existing code path (base_render, capsize, place, Field.match) works on
variable-font instances without change."""
import sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
import fast
from PIL import ImageFont

_FC2={}
def _font_var(spec, size):
    k=(spec,size)
    if k in _FC2: return _FC2[k]
    if '#' not in spec:
        f=ImageFont.truetype(spec,size)
    else:
        fp,q=spec.split('#',1)
        want={}
        for kv in q.split(','):
            a,b=kv.split('='); want[a.strip()]=float(b)
        f=ImageFont.truetype(fp,size)
        ax=f.get_variation_axes()
        vals=[]
        for a in ax:
            nm=a['name'].decode() if isinstance(a['name'],bytes) else a['name']
            tag='wght' if 'Weight' in nm else ('opsz' if 'Optical' in nm else nm)
            vals.append(float(want.get(tag,a['default'])))
        f.set_variation_by_axes(vals)
    _FC2[k]=f
    return f

fast._font = _font_var          # monkey-patch: capsize + base_render now use it
fast._CS.clear(); fast._RC.clear()
