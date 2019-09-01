"""
ref_image finds the best reference image from a set of astronomical data
History
Subtantially refactored on 2019-09-01
    Varun Iyer <varun_iyer@ucsb.edu>
"""
import numpy as np
from .align import _to_np


def ref_image(fits_list):
    """
    Given a list-like set of fits data, ref_image finds the one most suitable
    to be used as a reference image.
    Arguments
    fits_list -- list of array-likes or fitsdata
    Returns
    A reference to the most suitable array
    """
    best = fits_list[0]
    best_mean = np.mean(best)
    for data in fits_list:
        data_mean = np.mean(_to_np(data))
        if data_mean < best_mean:
            best = data
            best_mean = data_mean
    return best
