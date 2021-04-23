"""
Extracts sources from a list of hduls.
History:
    Created by 2019-09-05
        Varun Iyer <varun_iyer@ucsb.edu>
    Refactored for 2.0.0 on 2021-04-23
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import sep
from astropy.io import fits


def extract(hduls, stddev_thresh=3.0, read_ext=0, write_ext="XRT"):
    """
    Uses sep to find sources on a residual image(s)
    :param hduls: a list of HDUL to use as science data
    :param thresh: a threshold value for source extraction in terms of
        # of stddevs above background noise
    :param read_ext: the HDUL index to use as the base image. Default is 0. For
        LCO, 'SCI' would do the trick; for others 'PRIMARY'.
    :param write_ext: the HDUL index to write the catalog to. Default is 'XRT'
        for eXtRacT (close enough). Can also be a tuple (extname, extver)
    :return: a list of HDUL, each with a new `write_ext` HDU appended that is a
        record of extracted sources
    """
    for hdul in hduls:
        data = hdul[read_ext].data
        bkg = None
        try: 
            bkg = sep.Background(data)
        except:
            data = data.byteswap().newbyteorder()
            bkg = sep.Background(data)
        sources = sep.extract(data - bkg.back(), bkg.globalrms * stddev_thresh,
                       segmentation_map=False)
        extname = write_ext
        extver = None
        header = fits.Header([fits.Card("HISTORY", "Extracted by sep.")])
        try:
            extver = int(write_ext[1])
            name = read_ext[0]
        except (ValueError, TypeError):
            pass
        hdul.append(fits.BinTableHDU(data=sources, header=header,
                                     name=extname, ver=extver))

    return hduls
