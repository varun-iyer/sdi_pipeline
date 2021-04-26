"""
ref -- this module matches sources to reference stars
HISTORY
    Created 2021-04-24
        Varun Iyer <varun_iyer@ucsb.edu>
"""
# general imports

import click
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits
from astroquery.gaia import Gaia
from . import _cli as cli

def _in_cone(coord: SkyCoord, cone_center: SkyCoord, cone_radius: u.degree):
    """
    Checks if SkyCoord coord is in the cone described by conecenter and
    cone_radius
    """
    d = (coord.ra - cone_center.ra) ** 2 + (coord.dec - cone_center.dec) ** 2
    # The 0.0001 so we don't get edge effects
    return d < ((cone_radius - u.Quantity(0.05, u.deg)) ** 2)

def ref(hduls, read_ext="CAT", write_ext="REF", threshold=0.05):
    """
    add information about remote reference stars to a 'REF' BinTableHDU
    \b
    Reference adds a new BinTableHDU entitled 'REF' which contains retrieved
    information about reference stars and their associations with the sources in
    'CAT'.  Each index of 'CAT' will correspond to the same index in 'REF'; e.g.
    reference star info associated with hduls[0]['CAT'].data[0] will be in
    hduls[0]['REF'].data[0]. If there is no associated reference information,
    any(hduls[0]['REF'].data[0]) will be False.

    :param hdul: A collection or generator of HDUL
    :param read_ext: the HDU extname to read source information from.
        Must include 'ra' and 'dec' fields.
    :param write_ext: the HDU extname to write reference information from.
    """

    blank_result = Gaia.cone_search_async(SkyCoord(0, 0, unit=(u.deg,)*2),
                                          radius=u.Quantity(0, u.deg))
    gaia_dtype = blank_result.get_results().as_array().dtype
    breakpoint()

    queried_coords = []
    cached_coords = []
    cached_table = np.recarray(shape=0, dtype=gaia_dtype)

    radius = u.Quantity(threshold * 100, u.deg)
    threshold = u.Quantity(threshold, u.deg)
    for hdul in hduls:
        sources = hdul[read_ext].data
        output_table = np.recarray(shape=0, dtype=gaia_dtype)
        for source in sources:
            ra = source["ra"]
            dec = source["dec"]
            coord = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg))

            ########### Query an area if we have not done so already ###########
            # Check to see if we've queried the area
            if not any((_in_cone(coord, query, radius) \
                        for query in queried_coords)):
                # we have never queried the area. Do a GAIA cone search
                data = Gaia.cone_search_async(coord, radius).get_results()
                for d in data:
                    # construct Coord objects for the new data
                    cached_coords.append(SkyCoord(d["ra"], d["dec"],
                                         unit=(u.deg, u.deg)))
                # add the cache table to the data
                cached_table = np.hstack((cached_table, data))
                breakpoint()
                # note that we have now queried this arrea
                queried_coords.append(coord)

            ########### Look through our cache for matches #####################
            appended = False
            for ct, cs in zip(cached_table, cached_coords):
                # look through the cache to find a match
                if _in_cone(coord, cs, threshold):
                    # if we find a match, copy it to the output table
                    output_table = np.hstack((output_table, np.copy(ct)))
                    appended = True
                    break

            ########### Add a blank if we didn't find anything #################
            if not appended:
                # If we do not find one cached, then add a blank
                blank = np.empty(shape=0, dtype=gaia_dtype)
                output_table = np.hstack((output_table, blank))

        ########## After going through all sources, add an HDU #################
        extname = write_ext
        header = fits.Header([fits.Card("HISTORY", "From the GAIA remote db")])
        hdul.append(fits.BinTableHDU(data=output_table, header=header,
                                     name=extname))
        yield hdul
    return

@cli.cli.command("ref")
@click.option("-r", "--read-ext", default="CAT", help="The HDU to match")
@click.option("-w", "--write-ext", default="REF", help="The HDU to load ref into")
@click.option("-t", "--threshold", default=0.001, type=float,
              help="The threshold in degrees for a cone search")
@cli.operator
def ref_cmd(hduls, read_ext="CAT", write_ext="REF"):
    """
    add information about remote reference stars to a 'REF' BinTableHDU
    \b
    Reference adds a new BinTableHDU entitled 'REF' which contains retrieved
    information about reference stars and their associations with the sources in
    'CAT'.  Each index of 'CAT' will correspond to the same index in 'REF'; e.g.
    reference star info associated with hduls[0]['CAT'].data[0] will be in
    hduls[0]['REF'].data[0]. If there is no associated reference information,
    any(hduls[0]['REF'].data[0]) will be False.

    :param hdul: A collection or generator of HDUL
    :param read_ext: the HDU extname to read source information from. Must include 'ra' and 'dec' fields.
    :param write_ext: the HDU extname to write reference information from.
    """
    try:
        read_ext = int(read_ext)
    except ValueError:
        pass
    try:
        write_ext = int(write_ext)
    except ValueError:
        pass
    return ref(hduls, read_ext, write_ext)
