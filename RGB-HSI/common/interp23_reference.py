"""NumPy reference for the RGB-HSI 23-tap interpolation check."""
import numpy as np
from scipy.ndimage import convolve1d

def _interp23tap(image, ratio=4):
    coeff = 2 * np.array([.5, .305334091185, 0, -.072698593239, 0, .021809577942,
                          0, -.005192756653, 0, .000807762146, 0, -.000060081482])
    coeff = np.r_[coeff[:0:-1], coeff]
    for stage in range(int(np.log2(ratio))):
        up = np.zeros((image.shape[0] * 2, image.shape[1] * 2))
        offset = 1 if stage == 0 else 0
        up[offset::2, offset::2] = image
        image = convolve1d(convolve1d(up, coeff, axis=0, mode="wrap"), coeff, axis=1, mode="wrap")
    return image
