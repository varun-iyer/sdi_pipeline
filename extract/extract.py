"""
Extracts variable sources
History:
    Created by 2019-09-05
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import os
import sep
from ..common import to_np
 
 
def extract(residual_s, thresh=None):
    """
    Uses sep to find sources on a residual image(s)
    Arguments:
        residuals -- image of residuals from hotpants or a list of images
    Returns:
        A list of Source objects representing the location and various metrics
            of detected variable sources
    """
    residuals = []
    if isinstance(residuals, list):
        residuals = residual_s
    else:
        residuals.append(residual_s)
    sources = []
    for r in residuals:
        r_np = to_np(r).byteswap().newbyteorder()
        if thresh is None:
            # from astroalign’s settings
            thresh = sep.Background(r_np).globalrms * 3
        sources.append(sep.extract(r_np, thresh, segmentation_map=True))
    return sources if isinstance(residuals, list) else sources[0]
