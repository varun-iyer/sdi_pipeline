#!/usr/bin/env python

##### Fake Source Generator | Alex Polanski #####
##### June 20th 2019 #####

import os 
import glob
from os import path
import glob 
from astropy.io import fits
import astropy.convolution as convo
import numpy as np
from itertools import product
import psf_grabber

def moffat(path):
    #Select images and choose one at random
    images = glob.glob("%s/*.fits" %(path))
    upper = len(images)
    rand_num = np.random.randint(0, upper, size=1)
    source_im = images[rand_num[0]]
    print("\n %s selected as the source image. \n" % (source_im))
    #Grab FWHM
    fwhm = psf_grabber.psf_grabber(path,source_im)
    #Define parameters for Moffat distribution
    beta = 4.765
    alpha = fwhm/(2*np.sqrt(2**(1/beta)-1))
    kernal = convo.Moffat2DKernel(alpha,beta)
    ######
    num_sources = int(raw_input("How many sources do you want to simulate with?\n"))
    constant_flux = raw_input("Random Flux Values or Constant? (random or constant)\n")
    if constant_flux == 'constant':
        flux_val = int(raw_input("Choose a flux Value.\n"))
        flux_val = np.zeros(num_sources) + flux_val
    elif constant_flux == 'random':
        lower = raw_input("Place lower limit on the flux value?\n")
        if lower == 'yes':
            lower_limit = int(raw_input("What is the minimum flux?\n"))
            flux_val = np.random.randint(lower_limit, 89600, size=num_sources)
        else:
            flux_val = np.random.randint(0,89600, size=num_sources)
    else:
        lower_limit = False
    print(flux_val)
    #Open selected fits file
    source_hdu = fits.open(source_im)
    source_data = fits.getdata(source_im)
    original_header = source_hdu[0].header
    h, w = img_shape = np.shape(source_data)
    #Create empty array
    source = np.zeros(img_shape)
    #Get random x and y coordinates and fluxes
    pos_x = np.random.randint(10,h-10, size=num_sources)
    pos_y = np.random.randint(10,w-10, size=num_sources)
    if constant_flux == 'random':
        if lower_limit == False:
            flux_val = np.random.randint(10,9000,size=num_sources)
        else:
            flux_val = np.random.randint(lower_limit,9000,size=num_sources)
    pos_flux_pair = np.stack((pos_x,pos_y,flux_val), axis=-1)
    pos_flux_pair = pos_flux_pair.astype(int)
    #Create List of Fakes
    fake_list = path[:-5] + '/sources/fake_list.txt'
    fake = open(fake_list, 'w+')
    fake.write('#' + source_im + '\n')
    fake.write(
    '''#   1 NUMBER                 Running object number                                     
#   2 FLUX_ISO               Isophotal flux                                             [count]
#   3 X_IMAGE                Object position along x                                    [pixel]
#   4 Y_IMAGE                Object position along y                                    [pixel]
#   5 SPREAD_MODEL           Spread parameter from model-fitting \n''')
    fake.close()
    with open(fake_list, 'a') as catalog:
        for i in pos_flux_pair:
            catalog.write('%d,%d,%d \n' %(i[2],i[1],i[0]))
        catalog.close()
    #Add imperfections to sources and insert into empty matrix
    vibrations = np.random.randint(1,50)
    for i in pos_flux_pair:
        flux_frac = np.floor(i[2]/vibrations)
        counts = np.zeros(vibrations)
        for count in counts:
            dx = np.random.randint(-2,2)
            dy = np.random.randint(-2,2)
            pos_dx, pos_dy = (i[0] + dx), (i[1] + dy) 
            source[pos_dx, pos_dy] = source[pos_dx, pos_dy] + flux_frac
    #Convolve with a Moffat Distribution
    source_convo = convo.convolve(source, kernal)
    #Add together the images
    final_source = fits.PrimaryHDU(source_data + source_convo, header = original_header)
    final_source.writeto(source_im, overwrite=True)
    print("Fake sources were inserted!")
    split = source_im.split('/')
    source_im = split[10][:-8]
    return(source_im)   





