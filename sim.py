#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:34:10 2018

@author: alex
"""
import requests
from .initialize import loc
import os
import sys
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from astropy.io import fits
import glob
from time import strftime
from time import gmtime
from . import ref_image
from . import align_astroalign
from . import combine_numpy
from . import sex
from . import psf
from . import subtract_hotpants
from . import align_chi2
from . import align_imreg
from . import check_saturation
from os import path


#### script to take a data set, randomly select a frame in which to insert a transient source and insert it. ####

data_dir = input("Enter path to targets data directory")
split = data_dir.split("/",6)
target_dir = data_dir.replace(split[6], "")
sim_dir = data_dir.replace("targets", "simulations")


# check for existence of directory
path_exists = os.path.exists(data_dir)

if path_exists == False:
    print("Data directory does not exist")
    sys.exit()

# copy data contents

os.system("cp -r %s %s/sdi/simulations/" % (target_dir,loc ))


# align and median combine the images 

images = glob.glob("%s/*.fits" % (sim_dir))

check_saturation.check_saturate(sim_dir)
ref_image.ref_image(sim_dir)
align_astroalign.align2(sim_dir)
combine_numpy.combine_median(sim_dir)


# select random image to insert source into

images = glob.glob("%s/*.fits" % (sim_dir))

upper = len(images)

rand_num = np.random.randint(0,upper,size=1)

source_im = images[rand_num[0]]

print(("\n %s selected as the source image, adding simulated source..." % (source_im)))

hdu = fits.getdata(source_im)
hdu1 = fits.open(source_im)
Header = hdu1[0].header
h, w = img_shape = np.shape(hdu)
rand_pos = np.random.random(2)
#pos_x = int(round((w-10)*rand_pos[0]))  #This inserts a random source, you can uncomment this and comment out the following two lines if you wish.
#pos_y = int(round((h-10)*rand_pos[1]))
pos_x = 1500
pos_y = 1500
fluxes = 200000 
img = np.zeros(img_shape)
img[pos_x,pos_y] = fluxes

img = gaussian_filter(img, sigma=2.0, mode='constant', truncate=10.0)

final = fits.PrimaryHDU(hdu+img, header=Header)
final.writeto(source_im, overwrite=True)

print(("\n Source inserted at %s,%s!" %(pos_x,pos_y)))

subtract_hotpants.hotpants(sim_dir[:-5])

print(("""
Residual Images Produced. 

Image containing the Souce: %s

Source Position: (%s,%s).

Now run the extract command on the simulation time exposure directory.
""" % (source_im, pos_x, pos_y)))
