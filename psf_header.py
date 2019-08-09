#!/usr/bin/env python 

from astropy.io import fits
import os
import glob
import numpy as np
from os import path
import sys

def fwhm(sim_dir, image):
    #Convert to time exposure directory
    sim_dir = sim_dir[:-5]
    #Open source image header
    print("Obtaining image FWHM from image header...\n")
    psf_hdu = fits.open(image)
    fwhm = psf_hdu[0].header['L1FWHM']
    plate_scale = psf_hdu[0].header['PIXSCALE']
    #Calculate FWHM in pixels
    fwhm_pix = fwhm/plate_scale
    print("The PSF FWHM value is %s\n" %(fwhm_pix))
    return(fwhm_pix)
