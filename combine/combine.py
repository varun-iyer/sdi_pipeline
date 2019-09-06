"""
Combine merges a set of astronomical data from a template
History:
    Created/Extensively Refactored 2019-09-05
        Andrew Bluth <abluth@ucsb.edu>
"""

from . import combine_swarp
from . import combine_numpy
import inspect
from astropy.io import fits
from common import to_np

def combine(hdu_s, method="numpy"):
    """
    Combine merges a set of astronomical data from a template
    Arguments:
        hdu_s --a fits hdu or a list of fits hdu's
    Keyword Arguments:
        method -- the comination algorithm to use, currently only "numpy" 
        is implemented and it is the default
    """
    hdu = []
    if isinstance(hdu_s, list):
        hdu = hdu_s
    else:
        hdu.append(hdu_s)

    if method != "numpy":
        #TODO see below
        raise NotImplementedError("""Combine method other than numpy (swarp) 
        is unimplemented.""")
    print('\n-> Combining images...')
    data = [to_np(i) for i in hdu]
    comb = np.median(data, axis = 0)
    print("-> image combination successful!")
    return comb
