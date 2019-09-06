"""
ref_image finds the best reference image from a set of astronomical data
HISTORY
    Subtantially refactored on 2019-09-01
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import numpy as np
from ..common import to_np


def ref_image(fits_list):
    """
    Given a list-like set of fits data, ref_image finds the one most suitable
    to be used as a reference image.
    ARGUMENTS
        fits_list -- list of array-likes or fitsdata
    RETURNS
        A reference to the most suitable array
    """
    best = fits_list[0]
    best_mean = np.mean(best)
    for data in fits_list:
        data_mean = np.mean(to_np(data, """Cannot determine mean of unexpected 
            type {}; expected Numpy Array or FITS HDU"""))
        if data_mean < best_mean:
            best = data
            best_mean = data_mean
    return best
