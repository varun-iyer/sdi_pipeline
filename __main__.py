from astropy.io import fits
from sys import argv
from glob import glob
from .align import align
from .combine import combine
from .subtract import subtract
from .sources import extract
import pickle
import click
import os
file_list = list()
save_file = ('resduals.fits.fz', 'extra')


@click.command()
@click.option('-s', is_flag=True)
@click.argument('path')
@click.argument('save_path', nargs= -1) #nargs= -1 allows this argument to be optional but saves value as tuple
def run(s, path, save_path):
    if s: 
        print("residuals will be saved")
        for image in glob("{}*.fz".format(path)):
            file_list.append(image)
            save = True
    else: 
        for image in glob("{}*.fz".format(path)):
            file_list.append(image)
            save = False
    science_images = [fits.open(f)["SCI"] for f in file_list]
    aligned = align.image(science_images)
    print("Finished alignment")
    template = combine(aligned)
    print("Finished combine")
    residuals = subtract(aligned, template)
    print("Finished subtract")
    i = int(-1)
    if bool(save) == True:
        print("Saving Residuals")
        ri = [r[0] for r in residuals]
        for p in ri:
            i += 1
            fits.PrimaryHDU(p).writeto("{spath}residual{count}{original}".format(spath = list(save_path)[0], count = str(i), original = os.path.basename(glob("{}*.fz".format(path))[0])))
    im_sources = extract([res[0] for res in residuals])
    print("Finished extract")
    pickle.dump(im_sources, open("transient_candidates.pkl","wb"))


if __name__ == '__main__': 
	run()

