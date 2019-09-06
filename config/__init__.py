"""
Config manages and reads configuration files for the pipeline as well as
Sextractor and PSFextractor
History:
    Created 2019-09-05
        Varun Iyer <varun_iyer@ucsb.edu>
Methods:
Values:
    PSFEX_PARAMS -- location of the default parameter file for source extraction
        for psf
    DEFAULT_CONV -- locaiton of the default convolution file
    TMPDIR -- location of a directory to rw temp files
"""
from os import path
from .sextractor import Sextractor
 
 
_cdir = path.dirname(path.realpath(__file__))
 
# TODO these should be in YAML
PSFEX_PARAMS_PATH = "{}/default.psfex".format(_cdir)
DEFAULT_CONV_PATH = "{}/default.conv".format(_cdir)
SEX_DEFAULT = "{}/default.sex"
SEX_DEFAULT_VERBOSE = "{}/default_verbose.sex"
PSFEX_DEFAULT = "{}/psfex.config"
TMPDIR = "/tmp"
