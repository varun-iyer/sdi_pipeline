import click
import sdi
from astropy.io import fits
import glob
import sys

@sdi.cli.command("read") 
@click.option('-d', '--directory', type=str, help="Specify path to directory of fitsfiles.", required=True) 
@sdi.generator 

## read function wrapper
def read_cmd(directory):
    return read(directory)

def read(directory):
    paths = glob.glob("{}/*.fits*".format(directory))
    if not paths:
        sys.exit("No fits files in directory")
    hduls = [fits.open(p) for p in paths]
    return hduls

@sdi.cli.command("write")
@click.option('-d', '--directory', type=str, help="Specify path to directory to save fitsfiles.", default="./")
@click.option('-f', '--format', "format_", type=str, help="Specify string format for filename.", default="{number}.fits")
@sdi.operator

## write function wrapper
def write_cmd(hduls, directory, format_):
    return write(hduls, directory, format_)


def write(hduls, directory, format_):
    import os
    for i, h in enumerate(hduls):
        path = os.path.join(directory, format_.format(number=i))
        click.echo(f"writing hdul to {path}")
        h.writeto(path)
    return hduls
