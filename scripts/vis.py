from pyds9 import DS9
import numpy as np

#hduls should be a list of hdul(s), cat should be a string containing the path to a .npy file.
def image(hduls, cat=None):
    d = DS9()
    d.set("scale mode zscale")

    if cat == None:
        for hdul in hduls:
        d.set("frame new")
        d.set_pyfits(hdul)
        d.set("zoom to fit")
    else:
        for hdul in hduls:
            d.set("frame new")
            d.set_pyfits(hdul)
            d.set("zoom to fit")
            coords = np.load(cat)
        for coord in coords:
            d.set('regions command {{circle {} {} 40 #text=""}}'.format(coord[0], coord[1]))

    d.set("frame first")
    d.set("frame delete")



