from astropy.io import fits
from sys import argv
from glob import glob
from .align import align
from .combine import combine
from .subtract import subtract
from .extract import extract

file_list = argv[1:]
science_images = [fits.open(f)["SCI"] for f in file_list]
aligned = align(science_images)
print("Finished alignment")
template = combine(aligned)
print("Finished combine")
residuals = subtract(aligned, template)
print("Finished subtract")
print(len(science_images))
print(len(residuals))
sources = extract(science_images, residuals)
print("Finished extract")
print(sources)
