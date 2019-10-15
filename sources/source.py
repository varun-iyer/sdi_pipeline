"""
source.py

Contains a class to accumulate information about point sources in an image
History:
    Created 2019-09-09
        Varun Iyer <varun_iyer@ucsb.edu>
"""
from skimage.transform import matrix_transform

class Source:

    def from_hdu(cat, sci):
        """
        Returns a list of Sources generated from a catalog image and a science
        image
        Arguments:
            cat -- a HDU catalog
            sci -- a HDU science image
        Returns:
            A list of Sources in the catalog

        """
        output = []
        for c in cat.data:
            output.append(Source(c, im=sci, dtype=cat.data.dtype))
        return output

    # TODO create __repr__/__str__

    def __init__(self, recarray, im=None, dtype=None):
        """
        Initializes a source object
        Arguments:
            recarray -- a numpy record array of values representing a source
        Keyword:
            dtype -- if recarray is a fitsrecord or does not have a .dtype
                member, you can pass one in
            im -- image this source is from

        """
        if dtype is None:
            dtype = recarray.dtype
        # FIXME is the slice iterable conversion necessary?
        for name, value in zip(iter(dtype.names), iter(recarray)):
            self.__dict__[name.lower()] = value
        self.image = im
        self.pos = [self.x, self.y]
        if hasattr(self, "ra") and hasattr(self, "dec"):
            self.wcs = [self.ra, self.dec]
        if self.image is not None:
            self.scaled_peak = self._scale_peak(self.peak)

    def transform(self, T):
        """
        Applies a skimage Transformation to self.x and self.y
        The original coords are stored at self.x_orig and self.y_orig
        The new coordinates can also be found at self.x_t and self.y_t
        Arguments:
            T -- A skimage Transformation to apply

        """
        self.x_orig = self.x
        self.y_orig = self.y
        self.x, self.y = matrix_transform([self.x, self.y], T.params)[0]
        self.x_t, self.y_t = self.x, self.y
        self.pos = [self.x, self.y]
         
    def same(self, source, tol=2):
        """
        Determines if the given source is the same as this one in a different
        image
        Arguments:
            source -- the other source to compare against
        Keyword Arguments:
            tolerance=2 -- the number of pixels away the other source can be
                before it is "not the same"

        """
        # TODO this algorithm can definitely be better
        distance = (self.x - source.x) ** 2 + (self.y - source.y) ** 2
        if distance < tol ** 2:
            return True
        return False

    # FIXME this should be in an Image/fitsfile class
    def _scale_peak(self, peak):
        """
        Returns the value of a peak scaled to electrons/second
        
        """
        return (self.image.header["GAIN"] * peak) / self.image.header["EXPTIME"]
