#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:34:10 2018

@author: alex
"""
import requests
from initialize import loc
import os
import sys
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from astropy.io import fits
import glob

#### script to take a data set, randomly select a frame in which to insert a transient source and insert it. ####

data_dir = input("Enter path to time exposure directory")
obj = input("Input target name")
sim_dir = "%s/sdi/simulations" % (loc)

# check for existence of directory
path_exists = os.path.exists(data_dir)

if path_exists == False:
    print("Data directory does not exist")
    sys.exit()

# create new sim directory 

os.system("mkdir %s/sdi/simulations/%s" %(loc, obj))

# copy data contents

os.system("cp -r %s/* %s/%s" % (data_dir, sim_dir, obj))

# select random image to insert source into

images = glob.glob("%s/sdi/simulations/%s/data/*.fits" % (loc,obj))

upper = len(images)

rand_num = np.random.randint(0,upper,size=1)

source_im = images[rand_num[0]]

print("\n %s selected as the source image, adding simulated source..." % (source_im))

hdu = fits.getdata(source_im)
h, w = img_shape = np.shape(hdu)
rand_pos = np.random.random(2)
pos_x = int(round((w-10)*rand_pos[0]))
pos_y = int(round((h-10)*rand_pos[1]))
print(pos_y)
fluxes = 2000 * 300.0
img = np.zeros(img_shape)
img[pos_x,pos_y] = fluxes

img = gaussian_filter(img, sigma=2.0, mode='constant')

final = fits.PrimaryHDU(hdu+img)
final.writeto(source_im, overwrite=True)

print("\n Source inserted.")

os.system("ds9 %s" % (source_im))
