"""
align.phot contains methods to perform photometric regression
"""
from scipy.stats import linregress

def phot(aligned_hduls, reference=None):
    """
    Performs photometric alignment.
    Accepts aligned images and compares pixel values of stars betweem them, then
    applying a linear regression.
    Arguments:
        aligned_hduls -- HDULs that have been aligned and have a TRC and TRS HDUS
    Keyword Arguments:
        reference=None -- a HDUL chosen as a ref image; if None, the first
                          element is chosen
    Returns:
        aligned_hduls; operates in-place
    """
    if reference is None:
        reference = aligned_hduls[0]
    refpix = [reference["TRS"].data[int(round(y)),int(round(x))] \
              for x, y in iter(reference["TRC"].data)]
    for a in aligned_hduls:
        apix = [a["TRS"].data[int(round(y)),int(round(x))] \
                for x, y in iter(reference["TRC"].data)]
        gain, bias, r, p, stderr = linregress(apix, refpix)
        a["TRS"].data *= gain
        a["TRS"].data += bias
    return aligned_hduls
