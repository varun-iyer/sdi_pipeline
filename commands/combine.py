"""
Combine merges a set of astronomical data from a template
History:
    Created/Extensively Refactored 2019-09-05
        Andrew Bluth <abluth@ucsb.edu>
"""
import click
import sdi
import numpy as np
from common import to_np
from astropy.io import fits

@sdi.cli.command("combine")
@sdi.operator
def combine(hduls, method="numpy"):
    """
    Combine merges a set of astronomical data from a template
    Arguments:
        hduls --list of fits hdul's
    Keyword Arguments:
        method -- the comination algorithm to use, currently only "numpy" 
        is implemented and it is the default
    """
    hduls_list = [hdul for hdul in hduls]
    hdu = [hdul["SCI"] for hdul in hduls_list]
#    if isinstance(hduls, list):
#        hdu = hduls
#    else:
#        hdu.append(hduls)

    if method != "numpy":
        # TODO see below
        raise NotImplementedError("""Combine method other than numpy (swarp) 
        is unimplemented.""")
    data = [to_np(i) for i in hdu]
    comb = np.median(data, axis=0)
    hdu = fits.PrimaryHDU(comb)
    hduls_list += [fits.HDUList([hdu])]
    return (hdul for hdul in hduls_list)
