"""
align contains methods to align astronomical data to the same orientation based
on a reference image
METHODS
    align -- performs image registration
    saturation -- determines the saturation level of images
    ref_image -- chooses the best image to use as a reference from a set of ims
"""
from .align import align
from .saturation import saturation
from .ref_image import ref_image
