from astropy.io import fits
from sys import argv, exit
from glob import glob
from .align import align
from .combine import combine
from .subtract import subtract
from .sources import extract
import pickle
import click
import os
file_list = list()
save_file = ("{spath}residual{index}{original}")

@click.command()
@click.option('-s', is_flag=True)
@click.argument('path')
@click.argument('save_path', nargs= -1) #nargs= -1 allows this argument to be optional but saves value as tuple
def run(s, path, save_path):
    save = False
    if path[-1] != "/":
        print("Please give the path to the files WITHOUT '*.fz' at the end.")
        print("Aborted!")
        exit(0)
    if s: 
        print("residuals will be saved")
        save_base = os.path.basename(glob("{}*.fz".format(path))[0])
        save = True
    for image in glob("{}*.fz".format(path)):
        file_list.append(image)
    science_images = [fits.open(f)["SCI"] for f in file_list]
    aligned = align.image(science_images)
    print("Finished alignment")
    template = combine(aligned)
    print("Finished combine")
    residuals = subtract(aligned, template)
    print("Finished subtract")
    if save:
        print("Saving Residuals")
        ri = [r[0] for r in residuals]
        save_path = os.path.expanduser(save_path)
        for count, p in enumerate(ri):
            fits.PrimaryHDU(p).writeto(save_file.format(spath = list(save_path)[0], index = count, original = save_base))
    im_sources = extract([res[0] for res in residuals])
    print("Finished extract")
    pickle.dump(im_sources, open("transient_candidates.pkl","wb"))


if __name__ == '__main__': 
	run()

