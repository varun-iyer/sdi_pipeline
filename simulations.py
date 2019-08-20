#!/usr/bin/env python

##### Moffat Simulation Script | Alex Polanski #####
##### June 20th 2019 #####

import os
from os import path
import sys
import glob
from initialize import loc
import moffat_maker
import combine_numpy
import align_astroalign
import ref_image
import check_saturation
import subtract_hotpants
import sex
import psf
import cross_correlation


if __name__ == '__main__':
    data_dir = raw_input("Enter the path to the data directory:\n")
    #Check for existence of the directory
    path_exists = os.path.exists(data_dir)
    if path_exists == False:
        print("Data directory does not exist\n Exiting.")
        sys.exit()
    #Create new directories
    split = data_dir.split("/",6)
    target_dir = data_dir.replace(split[6], "")
    sim_dir = data_dir.replace("targets", "simulations")
    #Remove previous directory (if any) and copy data contents to simulations directory
    path_exists = os.path.exists(sim_dir)
    if path_exists == True:
        os.system("rm -r %s/%s/sdi/simulations/%s" %(split[1], split[2], split[5]))
    os.system("cp -r %s %s/sdi/simulations/" % (target_dir,loc ))
    #Align and median combine images
    images = glob.glob("%s/*.fits" % (sim_dir))
    check_saturation.check_saturate(sim_dir)
    ref_image.ref_image(sim_dir)
    align_astroalign.align2(sim_dir)
    combine_numpy.combine_median(sim_dir)
    #Select random science frame, randomize sources and fluxes.
    source_im = moffat_maker.moffat(sim_dir)
    print(source_im)
    #run the pipeline as usual.
    subtract_hotpants.hotpants(sim_dir[:-5])
    
    images = glob.glob(sim_dir[:-5] + '/data/*.fits')
    psf_data = glob.glob(sim_dir[:-5] + '/psf/*')
    if len(psf_data) == 3*len(images):
        sex.sextractor(sim_dir[:-5])
        sex.src_filter(sim_dir[:-5])
    else:
        sex.sextractor_psf(sim_dir[:-5])
        psf.psfex(sim_dir[:-5])
        sex.sextractor(sim_dir[:-5])
        sex.src_filter(sim_dir[:-5])
    print("Done. Now cross-correlating sources.")
    cross_correlation.get_data(sim_dir[:-5], source_im)
    #graph = raw_input("Continue with the plotting script?\n")
    #if graph == "yes":






