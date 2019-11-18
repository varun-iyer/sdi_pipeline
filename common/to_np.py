"""
to_np
Takes either a numpy array or a FITS HDU and returns a numpy array
Used across the pipeline to be as flexible as possible with acceptible inputs
History
Created 2019-09-04
    Varun Iyer <varun_iyer@ucsb.edu>
"""
import numpy as np
from astropy.io.fits.hdu.image import ExtensionHDU, ImageHDU, PrimaryHDU

HDU_TYPES = (ExtensionHDU, ImageHDU, PrimaryHDU)


def to_np(np_or_hdu, err_msg="Cannot process unexpected type {}"):
    """
    to_np accepts a numpy array or fits HDU and returns a numpy array
    It throws a TypeError if the input is not one of these types
    Arguments
        np_or_hdu -- the array or fitsfile to convert
    Keyword Arguments
        err_msg -- the error to print if the input is of neither type; it is
            optionally formatted with the type that was actually passed in if
            the string contains a '{}'
            default -- 'Cannot process unexpected type {}'
    """
    if isinstance(np_or_hdu, np.ndarray):
        return np_or_hdu
    if isinstance(np_or_hdu, HDU_TYPES):
        return np_or_hdu.data
    raise TypeError(err_msg.format(type(np_or_hdu)))
