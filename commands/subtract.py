import sdi
import click
import ois
import os
from astropy.io import fits

@sdi.cli.command("subtract")
@sdi.operator
def subtract(hduls):
    """
    Returns differences of a set of images from a template image
    Arguments:
        hduls --list of fits hdul's where the last image is the template 
        image that the other images will be subtracted from
    """
    hduls_list = [hdul for hdul in hduls]
    output = []
    outputs = []
    # FIXME this is not a combined image
    template = hduls_list[-1][0]
    try:
        template = hduls_list[-1][0].data
    except AttributeError:
        pass
    return (fits.HDUList(fits.PrimaryHDU(ois.optimal_system( \
        image=hdu["SCI"].data, refimage=template, method="Bramich")[0])) \
        for hdu in hduls_list)
