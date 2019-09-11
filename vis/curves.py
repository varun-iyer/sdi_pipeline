"""
light_curves finds the intensity of a list of sources over time
History:
    Created on 2019-09-06
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from .. import align
from ..sources import collate

def curves(sources, images, num=20, detected=[], fname="", show=False):
    """
    Generate a plot of light curves for each source
    Arguments:
        sources -- list of catalog file HDUs
        images -- list of science images
    Keyword Arguments:
        num=100 -- how many of the curves to graph
        detected=100 -- list of sources to graph in a different color as detected
        fname="" -- path to save the image; if not "", the image is saved to the
            specified path
        show=False -- whether to display the plot
    """
    start = [dt.datetime.strptime(
                " ".join((d.header["DATE"], d.header["UTSTART"])),
                "%Y-%m-%d %H:%M:%S.%f")
                for d in images]
    end = [dt.datetime.strptime(
                " ".join((d.header["DATE"], d.header["UTSTOP"])),
                "%Y-%m-%d %H:%M:%S.%f")
                for d in images]
    align.sources(sources) 
    collated = collate(sources) 
     
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    ax.set_yscale("log")
    for c in collated[:num]:
        # FIXME do this better
        ordered = list(zip(start, [a.scaled_peak for a in c]))
        ordered.sort(key=lambda x:x[0])
        ax.plot_date(*list(zip(*ordered)), fmt="o-")
    ax.set_xlabel("Start Time of Image Capture (UTC)")
    ax.set_ylabel("Peak Flux (electrons/second)")
    if fname:
        fig.savefig(fname)
    if show:
        fig.show() 
