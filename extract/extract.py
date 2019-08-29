from . import sex
from . import psf
import glob
import inspect

# Updated with SDI v1.2

def EXTRACT():
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("extract.py is being ran as a subprocess of auto.py")
        path = extraction[0]
    if not automated: path = input("-> Enter path to target's exposure time directory: ")
    images = glob.glob(path + '/data/*.fits')
    psf_data = glob.glob(path + '/psf/*')
    if len(psf_data) == 3*len(images):
        sex.sextractor(path)
        sex.src_filter(path)
    else:
        sex.sextractor_psf(path)
        psf.psfex(path)
        sex.sextractor(path)
        sex.src_filter(path)

if __name__ == '__main__':
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("extract.py is being ran as a subprocess of auto.py")
        path = extraction[0]
    if not automated: path = input("-> Enter path to target's exposure time directory: ")
    images = glob.glob(path + '/data/*.fits')
    psf_data = glob.glob(path + '/psf/*')
    if len(psf_data) == 3*len(images):
        sex.sextractor(path)
        sex.src_filter(path)
    else:
        sex.sextractor_psf(path)
        psf.psfex(path)
        sex.sextractor(path)
        sex.src_filter(path)