#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:28:32 2018

@author: andrew
"""

import glob
import numpy as np
from astropy.io import fits
import os
from .initialize import loc
import sys
#%%
#checks all fits images in a directory for saturation
def check_saturate(location):
    print("\n-> checking images for saturation...")
    Max = []
    im = []
    m = []
    x = 0
    y = 0
    z = 0
    images = glob.glob(location + "/*.fits")
    length = len(location) + 6

    if len(images) ==0:
        print("No Images")
        sys.exit(1)

    for i in images:
        hdu = fits.open(i)
        lin = hdu[0].header['SATURATE']
        satur = hdu[0].header['MAXLIN']
        data = hdu[0].data
        if satur > lin:
            lin = satur
        sat = ((data>lin)).sum()
#        ind = np.unravel_index(np.argmax(data, axis=None), data.shape)
#        excess = data[ind[0], ind[1]] - lin
        if sat > 10:
#            print "\n%s saturated | # saturated pixels = %d | max pixel location = (%d, %d)\nmax value over linearity limit = %d" % (i[length:], x, ind[0], ind[1], excess)
            y += 1
            im.append(i)
            m.append(np.max(data))
        
        Max.append(np.max(data))
#       x = 0
        sat = 0
        hdu.close()
###removing print statements for a bit

    if y > 0:
        print(("\n-> %d/%d saturated images" % (y, len(images))))
        print(("\n-> average saturation level (ADU) = %d" % (np.mean(m)-lin)))
        return im
    if y == 0:
        diff = lin - np.max(Max)
        print(("\n-> no saturated images in %s" % (location)))
        print(("\n-> closest value to saturation = %d" % (np.max(Max))))
        print(("\n-> difference between this value and saturation level = %d\n" % (diff)))

        return y
    
#%%
#move images into archives
def move_arch(images):
    archive_data_loc = loc + "/sdi/archive/saturated_images"
    check = os.path.exists(archive_data_loc)
    if check == False:
        os.mkdir(archive_data_loc)
    for i in images:
        os.system("mv %s %s" % (i, archive_data_loc))
    print("-> Saturated images moved to SDI archives")
