#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os

# Function to get flux,xcoord,ycoord


def get_data(path, source_im, master):
    ####################
    #DEFINITIONS
    ####################
    sourcelistfile = path + '/sources/filtered_sources.txt'
    fakelistfile = path + '/sources/fake_list.txt'
    tol=str(input('input coordinate tolerance (in pixels):'))
    #leaving this tolerance out for now.
    #flux_tol=str(input('input flux tolerance:'))
    sourceflux = []
    sourcex = []
    sourcey = []
    fakeflux = []
    fakex = []
    fakey = []
    ####################
    #FILE PROCESSING
    ####################
    #Copy only the catalogue section containing the fakes into a new text file.
    flag = 'temp/' + source_im + '_hotpants'
    with open(sourcelistfile) as infile, open( path + "/sources/random_source.txt", "w+") as outfile:
        copy = False 
        for (i, line) in enumerate(infile):
            if line.strip() == flag:
                copy = True
            if len(line) == 1:
                copy = False
            if copy:
                outfile.write(line)
    #Comment out the file name in catalog. (allows np.loadtxt to run more efficiently)
    old = open( path + "/sources/random_source.txt").read()
    old = old.replace(flag, '#' + flag)
    new = open( path + "/sources/random_source.txt", 'w')
    new.write(old)
    new.close()
    #Loading lists with values (floats)
    sourcelist = np.loadtxt( path + "/sources/random_source.txt")
    sourcelist = sourcelist.astype(float)
    fakelist = np.loadtxt(fakelistfile, delimiter = ',')
    sourcespread = sourcelist[:,4]
    sourceflux=sourcelist[:,1]
    fakeflux=fakelist[:,0]
    sourcex=sourcelist[:,2]
    fakex=fakelist[:,1]
    sourcey=sourcelist[:,3]
    fakey=fakelist[:,2]
    fakepair = np.stack((fakex,fakey,fakeflux), axis=-1)
    sourcepair = np.stack((sourcex, sourcey, sourcespread), axis = -1)
    #######################
    #DATA EXTRACTION
    #######################
    foundlist = []
    not_found = []
    num = 0
    for i in fakepair:
        for j in sourcepair:
            if np.isclose(i[0],j[0],atol=float(tol)) and np.isclose(i[1],j[1],atol=float(tol)):
                foundlist.append((i[0],i[1],i[2],j[2]))
                delete = np.where(np.all(i==fakepair, axis=1))[0][0]
                fakepair = np.delete(fakepair,delete,axis=0)
                num = num + 1

    foundlist = np.array(foundlist)
    #not_found = np.array(not_found)
    ######################
    #OUTPUT FILE
    ######################
    foundlistfile= open(master + "/foundlist.txt" ,"a+")
    foundlistfile.write("##### New Run #####\n")
    foundlistfile.write("#[[x-coord][y-coord][flux][spread model][Found =1.0, Not = 0.0]#\n")
    for i in range(len(foundlist)):
        foundlistfile.write("%.4f %.4f %.4f %.4f %.1f\n" %(foundlist[i][0],foundlist[i][1],foundlist[i][2],foundlist[i][3], 1.0))
    for i in range(len(fakepair)):
        foundlistfile.write("%.4f %.4f %.4f %.4f %.1f\n" %(fakepair[i][0], fakepair[i][1], fakepair[i][2], 0.0, 0.0))
    
    foundlistfile.close()

    
    print("Cross correlation complete. %s fakes found. The list order is:\n [x-coord][y-coord][flux][spread model]" %(num))
    return(foundlistfile)


