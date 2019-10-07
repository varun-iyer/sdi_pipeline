"""
align -- this module aligns sets of astronomical data
HISTORY
    Created/Substantially refactored on 2019-09-01
        Varun Iyer <varun_iyer@ucsb.edu>
"""
# general imports
import numpy as np
# types
from astropy.io.fits import PrimaryHDU, BinTableHDU, ImageHDU
from astropy.table import Table
from skimage.transform import matrix_transform
from ..common import to_np, HDU_TYPES
from .ref_image import ref_image
from ..sources import Source
import astroalign


def image(source_s, reference=None):
    """
    Aligns the source astronomical image(s) to the reference astronomical image
    Arguments:
        source_s -- the image(s) to align; fitsio HDU object, numpy array,
            or a list of either one of the above
    Keyword Argumemts;
        reference -- the image against which to align the source image;
            fitsio HDU object or numpy array. If None, the best option is chosen
            from among the sources.
    Returns:
        a transformed copy of the source image[s] in the same data type
        which was passed in
    """
    # make sure that we can handle source as a list
    sources = []
    outputs = []
    if isinstance(source_s, list):
        sources = source_s
    else:
        sources.append(source_s)

    if reference is None:
        reference = ref_image(sources)
    np_ref = to_np(reference, "Cannot align to unexpected type {}; expected numpy array or FITS HDU")

    for source in sources:
        np_src = to_np(source, "Cannot align unexpected type {}; expected numpy array or FITS HDU")
        # possibly unneccessary but unsure about scoping
        output = np.array([])

        output = astroalign.register(np_src, np_ref)[0]

        if isinstance(source, HDU_TYPES):
            output = PrimaryHDU(output, source.header)
        outputs.append(output)

    return outputs if isinstance(source_s, list) else outputs[0]

 
def sources(hduls, reference=None):
    """
    Aligns the images based on the sources in the HDUList Catalog.
    Operates in-place. 
        TRS: TRansformed Science, the transformed image
        TRC: TRansformed Catalog, a table of X Y coords from the catalog
    Arguments:
        hduls: A list of hdulists to align
    Keyword Arguments:
        reference -- An HDUL to use as a reference image; default None
    Returns:
        the input hduls. operates in place
        Adds the TRS and TRC data HDUs toi the HDUlist
        TRS: TRansformed Science, the input image transformed
        TRC: TRansformed Catalog, the transformed x,y coords of the cat
    """
    # FIXME this is really slow, move to Cython or do some numpy magic with
    # Sources class
    if reference is None:
        reference = hduls[0]
    refs = np.array([reference["CAT"].data["X"], reference["CAT"].data["Y"]]).T
    if isinstance(hduls[0], PrimaryHDU):
        hduls = [hduls]
    for hdul in hduls:
        sources = np.array([hdul["CAT"].data["X"], hdul["CAT"].data["Y"]]).T
        T, _ = astroalign.find_transform(sources, refs)
        transformed = matrix_transform(sources, T.params)
        hdul.append(ImageHDU(astroalign.apply_transform(T, hdul["SCI"].data, hdul["SCI"].data)[0], name="TRS"))
        # FIXME this should be appended to "CAT" instead of its own thing
        hdul.append(BinTableHDU(Table(transformed, names=["x", "y"]), name="TRC"))
    return hduls
