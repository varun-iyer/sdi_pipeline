"""
Subtract employs algorithms to take the difference of set of astronomical data
from a template
HISTORY
    Created/Extensively Refactored 2019-09-04
        Varun Iyer <varun_iyer@ucsb.edu>
"""
from subprocess import check_output
from astropy.io import fits
from ..config import TMPDIR

 
def subtract(sources, template, method="hotpants"):
    """
    Subtract takes the difference of a set of astronomical data from a template
    Arguments:
        data -- a fits HDU, numpy array, or list of either
        template -- a template to subtract from, fits HDU or numpy array
    Keyword Arguments: 
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
        # We need to have unique filenames that are persistent in tmpdir 
        # because fitsio uses lazy loading
        # memmap keeping the file open might have left the fileno alone, but
        # I didn’t want to depend on that -- Varun Iyer <varun_iyer@ucsb.edu>
        inim = "{}/inim.fits".format(TMPDIR)
        fits.writeto(inim, data)
        outim = "{}/{}_subtracted_.fits".format(TMPDIR, data.header["fname"])
        # use check_output so that it throws an error if the return code ain’t
        # good
        subprocess.check_output(
            "hotpants -inim {} -timplm {} -outim {}".format(inim, tmplim, outim),
            shell=True
        )
        outputs.append(fits.open(outim)[0])
    return outputs if isinstance(sources, list) else outputs[0]
