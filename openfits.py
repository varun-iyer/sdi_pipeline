import click
import sdi
from astropy.io import fits
import glob

@sdi.cli.command("open")
@click.option('-d', '--directory', type=str, help="Specify path to directory of fitsfiles.", required=True)
@sdi.generator
def open_(directory):
    paths = glob.glob("{}/*.fits*")
    hduls = [fits.open(p for p in paths)]
    return hduls
