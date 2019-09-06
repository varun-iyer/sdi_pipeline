"""
Extracts variable sources
History:
    Created by 2019-09-05
        Varun Iyer <varun_iyer@ucsb.edu>
"""
from subprocess import check_output
from astropy.io import fits
import ..config


def _ex_sci_conf(conf_name, cat_name):
    """
    Sets parameters to extract sources from science images
    Only for internal use in extract
    """
    sex_conf = config.Sextractor(config.SEX_DEFAULT)
    sex_conf["CATALOG_TYPE"] = "FITS_LDAC"
    sex_conf["CATALOG_NAME"] = cat_name
    sex_conf["PARAMETERS_NAME"] = config.PSFEX_PARAMS_PATH
    sex_conf["FILTER_NAME"] = config.DEFAULT_CONV_PATH
    sex_conf.write(conf_name)
     
      
def _psfex_conf(conf_name):
    """
    Sets psf_dir to /tmp
    """
    psf_conf = config.Sextractor(config.PSFEX_DEFAULT)
    sex_conf["PSF_DIR"] = config.TMPDIR
    sex_conf.write(conf_name)
     
      
def _sex_psf_conf(conf_name):
    """
    Sets psf_dir to /tmp
    """
    sex_conf = config.Sextractor(config.SEX_DEFAULT)
    sex_conf["CATALOG_TYPE"] = "ASCII_HEAD"
    sex_conf["CATALOG_NAME"] = "STDOUT"
    sex_conf["PARAMETERS_NAME"] = config.PSFEX_PARAMS_PATH
    sex_conf["FILTER_NAME"] = config.DEFAULT_CONV_PATH
    sex_conf["PSF_NAME"] = config.DEFAULT_CONV_PATH
    sex_conf.write(conf_name)


def extract(science, residual):
    """
    Uses sextractor to determine variable light sources in astronomical data
    Arguments:
        science -- HDU containing science image
        residual -- HDU containing residual image
    Returns:
        A list of Source objects representing the location and various metrics
            of detected variable sources
    """
    # Change I/O of sextractor to match our purposes
    # TODO these are really constants
    img = "{}/temp.fits".format(config.TMPDIR)
    psf = "{}/temp.psf".format(config.TMPDIR)
    cat = "{}/temp.cat".format(config.TMPDIR)
    sex_conf = "{}/temp.sex".format(config.TMPDIR)
    sex_psf_conf = "{}/temp_psf.sex".format(config.TMPDIR)
    psfcfg = "{}/psfex.config".format(config.TMPDIR)
    _ex_sci_conf(sex_conf, cat)
    _psfex_conf(psfcfg)
    _sex_psf_conf(sex_psf_conf, psf_file)

    outputs = []
     
    for sci, res in zip(science, residual):
        sci.writeto(tmpimage)
        # TODO the original bizzarely had [0] after the filename, is that nec.?
        check_output("sextractor {} -c {}".format(tmpimage, tmpconf))
        check_output("psfex {} > {} -c {}".format(tmpcat, tmppsf, tmpconf))
        sci.writeto(tmpimage)
        sources_string = check_output("sextractor {} -c {}".format(tmpimage, tmpconf))
        outputs.append(sources_string)
    return outputs
