#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 13:00:46 2018

@author: andrew
"""

import glob
from time import strftime
from time import gmtime
import numpy as np
from astropy.io import fits
import sys
import os

#%%
#combine all aligned images in data directory to make a template using the median method and move the temp to the templates dir
def combine_median(location):
    location = location[:-5]
    test = glob.glob(location + "/templates/*.fits")
    if len(test) != 0:
        os.system("ls")
        decision = raw_input("Template already found, skip combination step?\n")
        if decision == 'y':
            return None

    data = []
    good_images = []
    seeing = []
    images = glob.glob(location + "/data" + "/*_A_.fits")
    log_loc = location + "/templates/log.txt"
    log_list = open(log_loc, "a+")
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ##### Obtaining best seeing images #####
    for i in images:
        hdu = fits.open(i)
        fwhm = float(hdu[0].header['L1FWHM'])
        seeing.append([images.index(i),fwhm])
    seeing = np.array(seeing)
    minimum = int(raw_input('Enter number of best seeing images to be combined.\n'))
    best = np.argsort(seeing[:,1])[:minimum]
    
    interface = raw_input("Is a graphic-user interface available to you?\n")
    
    if interface == 'y':
        for i in best:
            os.system("ds9 %s -zscale -zoom to fit" % (images[i]))
            defect = raw_input("Does the image contain defects?\n")
            if defect =='n':
                good_images.append(images[i])
        if len(good_images) ==0:
            print("No images available to combine!\nExiting...\n")
            sys.exit()
    else:
        print("""\n\n***It is recommended that you visually inspect 
any image being used as a template.***\n\nProceeding with the best-seeing images.\n""")
        for i in best:
            good_images.append(images[i])
    #####
    print('\n-> Combining images...')
    for i in good_images:
        hdu1 = fits.open(i)
        data1 = hdu1[0].data
        data1 = np.array(data1, dtype="float64")
        data.append(data1)
        Header = hdu1[0].header
        hdu1.close()
    comb = np.median(data, axis=0)
    combined_name = location + "/templates/median_%d.fits" % (len(good_images))
    hdu = fits.PrimaryHDU(comb, header=Header)
    hdu.writeto(combined_name)
    log_list.write("template updated at %s UTC | method = median (numpy) | images = %d\n" % (str(time), len(good_images)))
    log_list.close()
    print("-> image combination successful!\ntemplate log updated\n")
    return comb
