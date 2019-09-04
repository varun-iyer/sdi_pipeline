"""
Subtract employs algorithms to take the difference of set of astronomical data
from a template
HISTORY
    Created/Extensively Refactored 2019-09-04
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import subprocess.check_output
from astropy.io import fits


# FIXME this tmpdir should be in a config file rather than direclty in python
TMPDIR = "/tmp"


def subtract(sources, template, method="hotpants"):
    """
    Subtract takes the difference of a set of astronomical data from a template
    ARGUMENTS
        data -- a fits HDU, numpy array, or list of either
        template -- a template to subtract from, fits HDU or numpy array
    KEYWORD ARGUMENTS
        method -- the subtraction algorithm to use; currently only 'hotpants' is
            implemented and it is the default
    """
    data_list = []
    if isinstance(sources, list):
        datas = sources
    else:
        datas.append(sources)
    if method != "hotpants":
        # TODO see below
        raise NotImplementedError("""Subtraction methods other than hotpants
            (IBIS, AIS) are unimplemented.""")
    tmplim = "{}/tmplim.fits".format(TMPDIR)
    fits.writeto(tmplim, template)
    outputs = []
    for data in data_list:
        inim = "{}/inim.fits".format(TMPDIR)
        fits.writeto(inim, data)
        outim = "{}/outim.fits".format(TMPDIR)
        # use check_output so that it throws an error if the return code ain’t
        # good
        subprocess.check_output(
            "hotpants -inim {} -timplm {} -outim {}".format(inim, tmplim, outim),
            shell=True
        )
        outputs.append(fits.open(outim)[0])
    return outputs if isinstance(sources, list) else outputs[0]
