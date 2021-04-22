import click
import sdi
from astropy.io import fits
import glob
import sys

def read(directory):
    paths = glob.glob("{}/*.fits*".format(directory))
    if not paths:
        sys.exit("No fits files in directory")
    hduls = [fits.open(p) for p in paths]
    return hduls

@sdi.cli.command("read")
@click.option('-d', '--directory', type=str, help="Specify path to directory of fitsfiles.", required=True)
@sdi.generator

## read function wrapper
def read_cmd(directory):
    return read(directory)
