from astropy.io import fits
from sys import argv
from glob import glob
from . import align
from .combine import combine
from .subtract import subtract
from .sources import extract
import pickle

file_list = argv[1:]
science_images = [fits.open(f)["SCI"] for f in file_list]
aligned = align.image(science_images)
print("Finished alignment")
template = combine(aligned)
print("Finished combine")
residuals = subtract(aligned, template)
print("Finished subtract")
sources = extract(residuals)
pickle.dump(sources, open("srcs.pkl", "wb"))
print("Finished extract")
