"""
ref_image finds the best reference image from a set of astronomical data
HISTORY
    Subtantially refactored on 2019-09-01
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import numpy as np
from ..common import to_np


INV_TYPE_ERR = """Cannot determine mean of unexpected type {}; expected Numpy Array or FITS HDU"""


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
    best_mean = np.mean(to_np(best, INV_TYPE_ERR))
    for data in fits_list:
        data_mean = np.mean(to_np(data, INV_TYPE_ERR))
        if data_mean < best_mean:
            best = data
            best_mean = data_mean
    return best
