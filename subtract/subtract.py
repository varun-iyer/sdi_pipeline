"""
Subtract employs algorithms to take the difference of set of astronomical data
from a template
HISTORY
    Created/Extensively Refactored 2019-09-04
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import os
from subprocess import check_output
from astropy.io import fits
from ..config import TMPDIR
from ..common import HDU_TYPES

 
def subtract(sources, template, method="hotpants"):
    """
    Subtract takes the difference of a set of astronomical data from a template
    Arguments:
        sources -- a fits HDU, numpy array, or list of either
        template -- a template to subtract from, fits HDU or numpy array
    Keyword Arguments: 
        method -- the subtraction algorithm to use; currently only 'hotpants' is
            implemented and it is the default
    """
    data_list = []
    if isinstance(sources, list):
        data_list = sources
    else:
        data_list.append(sources)
    if method != "hotpants":
        # TODO see below
        raise NotImplementedError("""Subtraction methods other than hotpants
            (IBIS, AIS) are unimplemented.""")
    tmplim = "{}/tmplim.fits".format(TMPDIR)
    inim = "{}/inim.fits".format(TMPDIR)
    try:
        os.remove(tmplim)
    except OSError:
        pass
    if isinstance(template, HDU_TYPES):
        template.writeto(tmplim)
    else:
        fits.writeto(tmplim, template)
    outputs = []
    for data in data_list:
        # We need to have unique filenames that are persistent in tmpdir 
        # because fitsio uses lazy loading
        # memmap keeping the file open might have left the fileno alone, but
        # I didn’t want to depend on that -- Varun Iyer <varun_iyer@ucsb.edu>
        try:
            os.remove(inim)
        except OSError:
            pass
        if isinstance(data, HDU_TYPES):
            data.writeto(inim)
        else:
            fits.writeto(inim, data)
        outim = "{}/{}_subtracted_.fits".format(TMPDIR, data.header["TRACKNUM"])
        # use check_output so that it throws an error if the return code ain’t
        # good
        print(check_output(
            "hotpants -inim {} -tmplim {} -outim {}".format(inim, tmplim, outim),
            shell=True
        ))
        out = fits.open(outim)[0]
        out.data = out.data.byteswap().newbyteorder()
        outputs.append(out)
    return outputs if isinstance(sources, list) else outputs[0]
