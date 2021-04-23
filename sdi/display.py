import sdi
import click
from pyds9 import DS9
import numpy as np

@sdi.cli.command("display")
@sdi.operator
def image(hduls, cats=None, color='green', size=40):
    """
    Opens multiple hduls on DS9 with the option of adding circles 
    to the images via numpy arrays.
    Arguments:
        hduls -- list of hduls
    Keyword arguments:
        cats -- list of 2xN numpy arrays (default None)
        color -- color of circles (default 'green')
        size -- size of circles (default 40)
    """
    d = DS9()
    d.set("scale mode zscale")
    if cats == None:
        for hdul in hduls:
            d.set("frame new")
            d.set_pyfits(hdul)
            d.set("zoom to fit")
    else:
        stuff = zip(hduls, cats)
        for hdul, cat in stuff:
            d.set("frame new")
            d.set_pyfits(hdul)
            d.set("zoom to fit")
            for coord in cat:
                d.set('regions command {{circle {} {} {} #color={}}}'.format(coord[0], coord[1], size, color))
    d.set("frame first")
    d.set("frame delete")
    
    return (hdul for hdul in hduls)

