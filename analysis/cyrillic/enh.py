"""Local-contrast normalisation for display: divides out the slow amplitude
variation (vignette / codec block gain) without touching glyph-scale structure."""
import numpy as np
from scipy.ndimage import gaussian_filter as gf
def localnorm(X, sig=60.0, floor=0.25):
    m = gf(X, sig)
    d = X - m
    s = np.sqrt(gf(d*d, sig))
    s = np.maximum(s, floor*np.median(s))
    return d/s
