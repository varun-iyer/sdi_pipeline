import numpy as np
from common import to_np

def combine(images):
    np_ims = [to_np(i) for i in images]
    return np.median(np_ims, axis=0)

