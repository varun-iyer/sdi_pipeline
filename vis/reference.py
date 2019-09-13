"""
Plots a fitsfile with found reference stars from the MIT-Amsterdam M31 Catalog
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from .. import sources

def reference(hdulist_or_cat, sci=None, fname="", show=False):
    """
    Plots a fitsfile with reference stars named and circled.
    Run with either a catalog and a science HDU or an hdulist
    Arguments:
        hdulist_or_cat -- an HDUList with ["SCI"] and ["CAT"] members or a
            catalog HDU
    Keyword Arguments:
        sci -- a science image HDU
        fname -- filename to save image to; default "" to not save a file
        show -- whether to display the image, default False
    """
    # FIXME Should take Sources
    if sci is None:
        cat = hdulist_or_cat["CAT"]
        sci = hdulist_or_cat["SCI"]
    else:
        cat = hdulist_or_cat
    
    results = sources.reference(cat)

    fig, ax = plt.subplots(1)
    ax.set_aspect("equal")

    # FIXME please plot this better
    ax.imshow(sci.data, vmin=np.mean(sci.data), vmax=np.mean(sci.data) * 4,
                origin="lower")
     
    for c, r in results:
        if len(r) != 1:
            print("Unexpected result!")
            print(r)
            continue
        circ = Circle((c["X"], c["Y"]), 20, color="red",
            fill=False)
        ax.add_patch(circ)
        ax.text(c["X"] + 20, c["Y"] + 20, r[0].id.decode("utf-8"), fontsize=6)
    if fname:
        fig.savefig(fname)

    if show:
        fig.show()
