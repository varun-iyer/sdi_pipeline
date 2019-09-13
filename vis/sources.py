"""
Plots a fitsfile with sources circled in red
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from numpy import ma

def sources(sci, srclist, fname="", show=False):
    """
    Plot a fitsfile with given sources outlined in red
    Arguments:
        sci -- science image
        srclist -- list of Source objects
    Keyword Arguments:
        fname -- filename to save image to; default "" to not save a file
        show -- whether to display the image, default False
    """
    fig, ax = plt.subplots(1)
    ax.set_aspect("equal")
    # FIXME please plot this better
    ax.imshow(sci.data, vmin=np.mean(sci.data),
                vmax=np.mean(s) * 4, origin="lower")
     
    for s in srclist:
        circ = Circle((s.x, s.y), 20, color="red", fill=False)
        ax.add_patch(circ)
         
    if fname:
        fig.savefig(fname)
    if show:
        fig.show()
