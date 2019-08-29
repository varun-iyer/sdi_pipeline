from os.path import expanduser

import sdi_pipeline
import os
from . import stats
import glob

loc = expanduser("~")

# Updated with SDI v1.2

#%%
#run on a new computer to create the sdi file system and use the pipeline
def initialize(loc):
    if os.path.exists(loc + "/sdi") == False:
        os.system("mkdir %s/sdi" % (loc))
        os.system("mkdir %s/sdi/targets" % (loc))
        os.system("mkdir %s/sdi/temp" % (loc))
        os.system("mkdir %s/sdi/sources" % (loc))
        os.system("mkdir %s/sdi/archive" % (loc))
        os.system("mkdir %s/sdi/pipeline" % (loc))
        os.system("mkdir %s/sdi/observations" % (loc))
        os.system("mkdir %s/sdi/simulations" % (loc))
        os.system("mkdir %s/sdi/archive/data" % (loc))
        os.system("mkdir %s/sdi/archive/templates" % (loc))
        os.system("mkdir %s/sdi/archive/residuals" % (loc))
        os.system("mkdir %s/sdi/scripts" % (loc))
        print(("-> sdi file system created in %s\n" % (loc)))
    else:
        print("-> SDI architecure already exists on this computer")
    
#%%
#creates a data, template, and residual directory
def create(location):
    dirs = ["data", "templates", "residuals", "sources", "psf"]
    for d in dirs: os.system("mkdir %s/%s" % (location, d))
    print(("-> data, templates, residuals, sources, and psf directories created in %s\n" % (location)))

#%%
def create_configs(location):
    check_configs = location + '/configs'
    if os.path.exists(check_configs) == False:
        os.mkdir(check_configs)
    config_loc = sdi_pipeline.module_path + '/config'
    for files in glob.glob(config_loc + '/*'):
        os.system('cp -n %s %s' % (files, check_configs))

#%%
def INITIALIZE():
    alert = 'y'
    #alert = raw_input("-> Create SDI directories in %s? (y/n): " % (loc))
    if alert == 'y':
        initialize(loc)
    elif alert == 'n':
        print("-> Change loc variable in initialize.py to desired SDI directory path, then run script again")
    else:
        print("-> Error: unknown input")
    #ais_install = raw_input("-> Install ISIS image subtraction on this machine? (y/n): ")
    ais_install = 'n'
    if ais_install == 'y':
        ais_run = sdi_pipeline.module_path + '/AIS/package/./install.csh'
        os.system(ais_run)
    elif ais_install == 'n':
        pass
    else:
        print("-> Error: unknown input")

        
#%%
#if this architecture does not exist, create it
###
# Change made on 5.14.19 to remove questions, as we currently do not utilize ISIS image subtraction
# and we do not need to ask the user if they want to proceed. If they're running .initialize, they should
# be aware of the directories they're creating, already.
###
if __name__ == '__main__':
    alert = 'y'
    #alert = raw_input("-> Create SDI directories in %s? (y/n): " % (loc))
    if alert == 'y':
        initialize(loc)
    elif alert == 'n':
        print("-> Change loc variable in initialize.py to desired SDI directory path, then run script again")
    else:
        print("-> Error: unknown input")
    #ais_install = raw_input("-> Install ISIS image subtraction on this machine? (y/n): ")
    ais_install = 'n'
    if ais_install == 'y':
        ais_run = sdi_pipeline.module_path + '/AIS/package/./install.csh'
        os.system(ais_run)
    elif ais_install == 'n':
        pass
    else:
        print("-> Error: unknown input")
