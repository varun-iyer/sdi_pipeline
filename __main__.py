from astropy.io import fits
from sys import argv
from glob import glob
from . import align
from .combine import combine
from .subtract import subtract
from .sources import extract
import pickle

file_list = argv[1:]
if len(file_list) < 2:
    print("ERROR: Not enough filenames specified. Try\n\t python3 -m sdi_pipeline /path/to/fitsfiles/*.fz\n or something similar.")
    sys.exit(1)
science_images = [fits.open(f)["SCI"] for f in file_list]
aligned = align.image(science_images)
print("Finished alignment")
template = combine(aligned)
print("Finished combine")
residuals = subtract(aligned, template)
print("Finished subtract")
im_sources = extract(residuals)
with open("sources.txt", "w") as out:
    for sci, sourcelist in zip(science_images, im_sources):
        out.write("{}T{}\n".format(sci.header["DATE"], sci.header["UTSTART"]))
        out.write("-" * 80 + "\n")
        out.write(",".join(iter(sourcelist[0].dtype.fields)) + "\n")
        for source in sourcelist[0]:
            out.write(",".join([str(s) for s in iter(source)]) + "\n")
print("Finished extract")
