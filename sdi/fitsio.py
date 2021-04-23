import sys
import click
import sdi
from astropy.io import fits
import glob
from tkinter.filedialog import askdirectory

def read(directory):
    # add try (evaluate if the try is efficient)
    if directory == None:
        try:
            directory = askdirectory()
        except:
            click.echo("Visual file dialog does not exist, please use option -d and specify path to directory to read fitsfiles.", err=True)
            quit()
    paths = glob.glob("{}/*.fits*".format(directory))
    if not paths:
        sys.exit("No fits files in directory")
    hduls = [fits.open(p) for p in paths]
    return hduls

def write(hduls, directory, format_):
    import os
    for i, h in enumerate(hduls):
        path = os.path.join(directory, format_.format(number=i))
        click.echo(f"writing hdul to {path}")
        h.writeto(path)
    return hduls

@sdi.cli.command("write")
@click.option('-d', '--directory', type=str, help="Specify path to directory to save fitsfiles.", default="./")
@click.option('-f', '--format', "format_", type=str, help="Specify string format for filename.", default="{number}.fits")
@sdi.operator

## write function wrapper
def write_cmd(hduls, directory, format_):
    return write(hduls, directory, format_)

@sdi.cli.command("read")
@click.option('-d', '--directory', type=str, help="Specify path to directory of fitsfiles.", required=True)
@sdi.generator

## read function wrapper
def read_cmd(directory):
    return read(directory)
