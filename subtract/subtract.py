import ois
import os
from astropy.io import fits
<<<<<<< HEAD

def subtract(sources, template, gausslist):
    output = []

    if type(sources) == list:
        for element in sources:
            diff = ois.optimal_system(image=element.data, refimage=template, method='Bramich')[0]
            output.append(diff)     
            
    return output
