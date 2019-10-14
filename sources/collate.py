"""
collate.py
Arranges a history of a source in chronological order
History:
    Created 2019-09-09
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import numpy as np
import datetime as dt


def collate(sources, thresh=2):
    """
    Correlate takes a list of sources and images and attempts to combine like
    sources
    Arguments:
        sources -- list of Source objects
        images -- list of HDU images
    Keyword Arguments:
        thresh=2 -- how close pixels need to be before they are discarded
    Returns:
        An astropy TimeSeries
        
    """

    collated = []
    # TODO get pixel values from sources that do not appear in all images
    # FIXME this is *really* slow, should be done in C or Cython
    # or maybe some clever numpy optimization?
    for source in sources[0]:
        sourcelist = [source]
        for im_idx, others in enumerate(sources[1:]):
            for o in others:
                if source.same(o):
                    sourcelist.append(o)
                    continue
        if len(sourcelist) == 10:
            collated.append(sourcelist)
    return collated
