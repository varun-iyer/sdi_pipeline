from astropy.io import fits
from sys import argv
from glob import glob
from .align import align
from .combine import combine
from .subtract import subtract
from .extract import extract
import pickle

file_list = argv[1:]
science_images = [fits.open(f)["SCI"] for f in file_list]
residuals = [fits.open(f)["SCI"] for f in glob("./*.fits")]
aligned = align(science_images)
print("Finished alignment")
template = combine(aligned)
print("Finished combine")
residuals = subtract(aligned, template)
print("Finished subtract")
for i, r in enumerate(residuals):
    r.writeto("./{}residual.fits".format(i))
sources = extract(residuals)
pickle.dump(sources, open("srcs.pkl", "wb"))
print("Finished extract")
