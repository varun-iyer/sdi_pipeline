import click
import cli
from astropy.io import fits
import glob

@cli.cli.command("read")
@click.option('-d', '--directory', type=str, help="Specify path to directory of fitsfiles.", required=True)
@cli.generator
def read(directory):
    paths = glob.glob("{}/*.fits*".format(directory))
    hduls = [fits.open(p) for p in paths]
    return hduls

@cli.cli.command("write")
@click.option('-d', '--directory', type=str, help="Specify path to directory to save fitsfiles.", default="./")
@click.option('-f', '--format', "format_", type=str, help="Specify string format for filename.", default="{number}.fits")
@cli.operator
def write(hduls, directory, format_):
    import os
    for i, h in enumerate(hduls):
        path = os.path.join(directory, format_.format(number=i))
        click.echo(f"writing hdul to {path}")
        h.writeto(path)
    return hduls
