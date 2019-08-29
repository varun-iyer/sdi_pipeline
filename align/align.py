# general
import numpy as np
_unable = "Unable to find {} module(s); {} alignment method is disabled."
# for astroalign method
try:
    import astroalign
except ImportError:
    print(_unable.format("astroalign", "astroalign"))
# for skimage method
try:
    from skimage.feature import register_translation
    from scipy.ndimage import fourier_shift
except ImportError:
    print(_unable.format("skimage or scipy", "skimage"))
# for chi2 method
try:
    from image_registration import chi2_shift
    from image_registration import fft_tools
except ImportError:
    print(_unable.format("image_registration", "chi2"))
# for imreg method
try:
    import imreg_dft
except ImportError:
    print(_unable.format("imreg_dft", "imreg"))
# types
from numpy import ndarray
from astropy.io.fits.hdu.image import ExtensionHDU, ImageHDU, PrimaryHDU


_hdu_types = (ExtensionHDU, ImageHDU, PrimaryHDU)


def _to_np(np_or_hdu):
    """
    Returns a numpy array or the data; or throws an error.
    Only for internal use within align.py
    """
    if isinstance(np_or_hdu, np.ndarray):
        return np_or_hdu
    elif isinstance(np_or_hdu, _hdu_types):
        return np_or_hdu.data
    else:
        raise TypeError("Cannot align to unexpected type {}".format( \
                        type(np_or_hdu)))

_dis = "Alignment method {} is disabled because the {} module(s) is/are not installed."

 
def align(source_s, reference, method="astroalign"):
    """
    Aligns the source astronomical image(s) to the reference astronomical image
    Arguments:
        source_s -- the image(s) to align; fitsio HDU object, numpy array,
            or a list of either one of the above
        reference -- the image against which to align the source image;
            fitsio HDU object or numpy array
    Keyword Arguments:
        method -- the library to use to align the images. options are:
            astroalign (default), skimage, imreg, skimage, chi2
    Return:
        returns a transformed copy of the source image[s] in the same data type
        which was passed in
    """
    np_ref = _to_np(reference)
    # make sure that we can handle source as a list
    sources = []
    outputs = []
    if isinstance(source_s, list):
        sources = source_s
    else:
        sources.append(source_s)

    for source in sources:
        np_src = _to_np(source)
        # possibly unneccessary but unsure about scoping
        output = np.array([])

        if method == "astroalign":
            try:
                output = astroalign.register(np_src, np_ref)[0]
            except NameError:
                rase ValueError(_dis.format(method, "astroalign"))
        elif method == "skimage":
            try:
                shift, error, diffphase = register_translation(np_ref, np_src, 100)
                output_fft = fourier_shift(np.fft.fftn(np_src), shift)
                output = np.fft.ifftn(output_fft)
            except NameError:
                raise ValueError(_dis.format(method, "scipy or numpy"))
        elif method == "chi2":
            try:
                dx, dy, edx, edy = chi2_shift(np_ref, np_src, upsample_factor='auto')
                output = fft_tools.shift.shiftnd(data, (-dx, -dy))
            except NameError:
                raise ValueError(_dis.format(method, "image_registration"))
        elif method == "imreg":
            try:
                output = imreg_dft.similarity(np_ref, np_src)["timg"]
            except NameError:
                raise ValueError(_dis.format(method, "imreg_dft"))
        else:
            raise ValueError("Unexpected alignment method {}!".format(method))

        if isinstance(source, _hdu_types):
            output = PrimaryHDU(output, source.header)
        outputs.append(output)

    return outputs if len(outputs) > 1 else outputs[0]
