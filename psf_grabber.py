#!/usr/bin/env python

##### PSF FWHM Grabbing Script | Alex Polanski #####
##### June 24th 2019 #####

import initialize
import os
import glob
from astropy.io import fits
import numpy as np
from os import path
import sys

def psf_grabber(sim_dir, image):
    #Convert to time exposure directory
    sim_dir = sim_dir[:-5]
    #Check for the existence of appropriate configuration files.
    print("%s/sim_configs" %(sim_dir))
    path_exists = os.path.exists("%s/sim_configs" %(sim_dir))
    if path_exists == True:
        files = glob.glob("%s/sim_configs/*" %(sim_dir))
        if len(files) == 0:
            print("No configuration files found!")
            sys.exit()
    else:
        initialize.create_simconfigs(sim_dir)
        #Correct directory locations in configuration files

        #SExtractor Correction:
        sex_config = sim_dir + '/sim_configs/psf.sex'
        with open(sex_config, 'r') as config:
            data = config.readlines()
            config.close()
        data[6] = 'CATALOG_NAME' + '        ' + sim_dir + '/psf/random_image.cat' + '\n'
        data[9] = 'PARAMETERS_NAME' + '        ' + sim_dir + '/sim_configs/default.psfex' + '\n'
        data[20] = 'FILTER_NAME' + '        ' + sim_dir + '/sim_configs/default.conv' + '\n'
        with open(sex_config, 'w') as config:
            config.writelines(data)
            config.close()

        #PSFex Correction:
        psf_config = sim_dir + '/sim_configs/psfex.config'
        with open(psf_config,'r') as config:
            data = config.readlines()
            config.close()
        data[85] = 'PSF_DIR' + '        ' + sim_dir + '/psf' + '\n'
        with open(psf_config,'w') as config:
            data = config.writelines(data)
            config.close()

    #Run SExtractor and PSFex to obtain FWHM value for the image.
    image_split = image.split("/", 10)
    image_name = image_split[10]
    os.system("sextractor %s -c %s/sim_configs/psf.sex" %(image, sim_dir))
    print("Extracting sources...\n")
    os.system("psfex %s/psf/random_image.cat -c %s/sim_configs/psfex.config" %(sim_dir, sim_dir))
    print("Obtaining FWHM...\n")
    psf_hdu = fits.open("%s/psf/random_image.psf" %(sim_dir))
    fwhm = psf_hdu[1].header[23]
    #Remove .psf file to prevent complications later in the pipeline.
    os.system("rm %s/psf/*" %(sim_dir))
    print("The PSF FWHM value is %s\n" %(fwhm))
    return(fwhm)


