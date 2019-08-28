import os
import readline
from .initialize import loc
from . import get
from . import align
from . import combine
from . import subtract
from . import extract
import subprocess
from . import initialize
from . import reset

# Updated with SDI v1.2
# Automation script for the SETI Pipeline initially written by Jamie Clark. Direct questions for the code to me / other contributors
# Contributors: Jeremy Badger,


def AUTO():
    


    ###
    # Align uses three inputs, location (the directory of the data), check (checks whether to continue alignment.
    # should almost always be yes), move (should we saturated files out? almost always no)
    ###

    getting = [1, 2, 3, 4]
    alignment = [1, 2, 3]
    combination = [1, 2]
    subtraction = [1, 2]
    extraction = [1]

    ###
    # Above are placeholder values that will be overwritten immediately.
    #this is the crucial part. asks user which mode. Then either sets values or asks user for more inputs, now.
    #then runs script
    ###


    ###
    # This part asks the user if they would like to reset their data structure.
    print("A reset will reset your sdi folder, deleting any data/results you may currently have in it.\n")
    print("Would you like to perform a reset? y/n (leave blank for default = y)")
    reset_check = input("Input: ")
    if ((reset_check.lower() == "y") or (reset_check == "")):
        reset.RESET()
    elif reset_check == "n":
        pass
    else:
        print("Input not supported. Not going to perform a reset.")

    #manual importing script
    import_check = input("Would you like to import data from /seti_data to %s/Downloads? (y/n) (leave blank for default = y)" % (loc))
    if import_check.lower() == 'y' or import_check == "":
        display_check = input("Would you like to display all possible importable files? (leave blank for default = y)")
        if display_check.lower() == "y" or display_check == "":
            possiblefiles = subprocess.check_output("echo $(find /seti_data/raw_data -name *.zip)", shell=True)
            possiblefiles = possiblefiles.replace(" ", "\n")
            options = possiblefiles.split('\n')
            for x in range(1, len(options)):
                print((str(x) + ": " + str(options[x-1])))
        filename = input("What is the number of the file you wish to import?")
        if not filename.isdigit(): 
            print("This is not a number. Exiting the script.")
            exit()
        elif int(filename) not in list(range(1, len(options))):
            print("This is out of bounds. Exiting the script.")
            exit()
        selected_file = options[int(filename)-1]
        print(("Attempting to copy %s to $(pwd)/Downloads/$(basename %s)...." % (selected_file, selected_file)))
        os.system("cp %s $(pwd)/Downloads/$(basename %s)" % (selected_file, selected_file))
        print(("Executed command to copy %s to $(pwd)/Downloads/$(basename %s)." % (selected_file, selected_file)))

    ###
    # this functionality is not done so it is commented out
    #print("Would you like to suppress verbosity(output of the pipeline)?")
    #verbosity_check = raw_input("Input: ")
    #if verbosity_check == "yes":
    #


    print("[E]asy, [I]ntermediate, or [A]dvanced? (leave blank for default = easy)")
    mode = input("Input: ")
    if mode.lower() == "easy" or mode.lower() == "e" or mode == "":
        # get values (request_check, unpack_check, check, download_location)
        getting[0] = 'unpack'
        getting[1] = 'y'
        getting[2] = 'y'
        getting[3] = ''
        # alignment values (check,move)
        alignment[1] = 'y'
        alignment[2] = 'n'
        # combine values (method)
        combination[1] = 'numpy'
        # subtract values (method)
        subtraction[1] = 'hotpants' 
    elif mode.lower() == "intermediate" or mode.lower() == "i":
        # get values (request_check, unpack_check, check, download_location)
        getting[0] = 'unpack'
        getting[1] = 'y'
        getting[2] = 'y'
        os.system('clear') 
        getting[3] = input("-> Enter LCO data location (leave blank for default=%s/Downloads): " % (loc))
        # alignment values (check,move)
        alignment[1] = 'y'
        alignment[2] = 'n'
        # combine values (method)
        os.system('clear') 
        combination[1] = input("\n-> Choose combination method-- numpy (default) or swarp: (leave blank for default = numpy): ")
        # subtract values (method)
        os.system('clear')
        subtraction[1] = input("\n-> Choose subtraction method: hotpants or AIS: (leave blank for default = hotpants): ")
    elif mode.lower() == "advanced" or mode.lower() == "a":
        # get values (request_check, unpack_check, check, download_location)
        os.system('clear') 
        getting[0] = input("-> Get data from LCO or unpack downloaded data? (dl/unpack) (leave blank for default = unpack): ")
        os.system('clear')
        getting[1] = input("-> Unpack downloaded data? (y/n) (leave blank for default = y): ")
        os.system('clear')
        getting[2] = input("-> Move data into target directory? (y/n) (leave blank for default = y): ")
        os.system('clear')
        getting[3] = input("-> Enter LCO data location (leave blank for default=%s/Downloads): " % (loc))
        # alignment values (check,move)
        os.system('clear')
        alignment[1] = input("-> Saturated images found, continue image alignment? (y/n) (leave blank for default = y): ")
        os.system('clear')
        alignment[2] = input("-> Move saturated images to SDI archives before continuing? (y/n) (leave blank for default = n): ")
        # combine values (method)
        os.system('clear')
        combination[1] = input("\n-> Choose combination method-- numpy (default) or swarp: (leave blank for default = numpy): ")
        # subtract values (method)
        os.system('clear')
        subtraction[1] = input("\n-> Choose subtraction method: hotpants or AIS: (leave blank for default = hotpants): ")
    else:
        print("Input not supported")
        exit()

    ###
    # first check if there is data to import. if not we need to error and stop the script
    ###
    if getting[3] == "":
        Data_Location = "%s/Downloads" % (loc)
    else:
        Data_Location = getting[3]
    Downloadscontents = subprocess.check_output("echo $(ls %s)" % (Data_Location), shell=True)
    if ".zip" not in Downloadscontents: 
        print("Error: No Data Found")
        exit()


    ###
    # this is important. this imports the "getting" variable into get, so we can reference it within get.
    # we will do a similar thing for the other function calls: align, combine, subtract, extract
    ###
    get.getting = getting
    get.GET()


    ###
    # Identifies the sdi structure path generated by the machine that the script feeds back into itself. 
    # This will look like /home/USERNAME/sdi/targets/TARGETNAME/numbers/air/numbers
    ###
    target = subprocess.check_output("echo $(ls $(pwd)/sdi/targets -t | head -n 1)", shell=True)
    target = target.replace("\n", "")
    radec = subprocess.check_output("echo $(ls $(pwd)/sdi/targets/%s -t -I raw_data | head -n 1)" % (target), shell=True)
    radec = radec.replace("\n", "")
    exposuretime = subprocess.check_output("echo $(ls $(pwd)/sdi/targets/%s/%s/air -t | head -n 1)" % (target, radec), shell=True)
    exposuretime = exposuretime.replace("\n", "")
    exposurepath = "$(pwd)/sdi/targets/target/air/radec/exposuretime"
    exposurepath = subprocess.check_output("echo $(pwd)/sdi/targets/%s/%s/air/%s" % (target, radec, exposuretime), shell=True)
    exposurepath = exposurepath.replace("\n", "")

    print(("Your exposure path is " + exposurepath + ". If this is wrong, check the code."))
    ###
    # Sets the path that the machine generates that is fed back, that was just defined. 
    # Alignment and combination call this "location" and subtraction and extraction call this "path".
    # "location" refers to exposurepath/data and "path" just refers to exposurepath
    ###
    alignment[0] = exposurepath + "/data"
    combination[0] = exposurepath + "/data"
    subtraction[0] = exposurepath
    extraction[0] = exposurepath



    align.alignment = alignment
    subtract.subtraction = subtraction
    combine.combination = combination
    extract.extraction = extraction


    align.ALIGN()
    combine.COMBINE()
    subtract.SUBTRACT()
    extract.EXTRACT()

    print("The automation script ran successfully! Check the sources and filtered sources files within the sdi/targets... directory.")





if __name__ == '__main__':


    print("\n***\nWelcome to SDI v1.2\n***\n")

    ###
    # Align uses three inputs, location (the directory of the data), check (checks whether to continue alignment.
    # should almost always be yes), move (should we saturated files out? almost always no)
    ###

    getting = [1, 2, 3, 4]
    alignment = [1, 2, 3]
    combination = [1, 2]
    subtraction = [1, 2]
    extraction = [1]

    ###
    # Above are placeholder values that will be overwritten immediately.
    #this is the crucial part. asks user which mode. Then either sets values or asks user for more inputs, now.
    #then runs script
    ###


    ###
    # This part asks the user if they would like to reset their data structure.
    print("A reset will reset your sdi folder, deleting any data/results you may currently have in it.\n")
    print("Would you like to perform a reset? y/n (leave blank for default = y)")
    reset_check = input("Input: ")
    if ((reset_check.lower() == "y") or (reset_check == "")):
        reset.RESET()
    elif reset_check == "n":
        pass
    else:
        print("Input not supported. Not going to perform a reset.")

     #manual importing script
    import_check = input("Would you like to import data from /seti_data to %s/Downloads? (y/n) (leave blank for default = y)" % (loc))
    if import_check.lower() == 'y' or import_check == "":
        display_check = input("Would you like to display all possible importable files? (leave blank for default = y)")
        if display_check.lower() == "y" or display_check == "":
            possiblefiles = subprocess.check_output("echo $(find /seti_data/raw_data -name *.zip)", shell=True)
            possiblefiles = possiblefiles.replace(" ", "\n")
            options = possiblefiles.split('\n')
            for x in range(1, len(options)):
                print((str(x) + ": " + str(options[x-1])))
        filename = input("What is the number of the file you wish to import?")
        if not filename.isdigit(): 
            print("This is not a number. Exiting the script.")
            exit()
        elif int(filename) not in list(range(1, len(options))):
            print("This is out of bounds. Exiting the script.")
            exit()
        selected_file = options[int(filename)-1]
        print(("Attempting to copy %s to $(pwd)/Downloads/$(basename %s)...." % (selected_file, selected_file)))
        os.system("cp %s $(pwd)/Downloads/$(basename %s)" % (selected_file, selected_file))
        print(("Executed command to copy %s to $(pwd)/Downloads/$(basename %s)." % (selected_file, selected_file)))

    ###
    # this functionality is not done so it is commented out
    #print("Would you like to suppress verbosity(output of the pipeline)?")
    #verbosity_check = raw_input("Input: ")
    #if verbosity_check == "yes":
    #
    #else:


    print("[E]asy, [I]ntermediate, or [A]dvanced? (leave blank for default = easy)")
    mode = input("Input: ")
    if mode.lower() == "easy" or mode.lower() == "e" or mode == "":
        # get values (request_check, unpack_check, check, download_location)
        getting[0] = 'unpack'
        getting[1] = 'y'
        getting[2] = 'y'
        getting[3] = ''
        # alignment values (check,move)
        alignment[1] = 'y'
        alignment[2] = 'n'
        # combine values (method)
        combination[1] = 'numpy'
        # subtract values (method)
        subtraction[1] = 'hotpants' 
    elif mode.lower() == "intermediate" or mode.lower() == "i":
        # get values (request_check, unpack_check, check, download_location)
        getting[0] = 'unpack'
        getting[1] = 'y'
        getting[2] = 'y'
        os.system('clear') 
        getting[3] = input("-> Enter LCO data location (leave blank for default=%s/Downloads): " % (loc))
        # alignment values (check,move)
        alignment[1] = 'y'
        alignment[2] = 'n'
        # combine values (method)
        os.system('clear') 
        combination[1] = input("\n-> Choose combination method-- numpy (default) or swarp: (leave blank for default = numpy): ")
        # subtract values (method)
        os.system('clear')
        subtraction[1] = input("\n-> Choose subtraction method: hotpants or AIS: (leave blank for default = hotpants): ")
    elif mode.lower() == "advanced" or mode.lower() == "a":
        # get values (request_check, unpack_check, check, download_location)
        os.system('clear') 
        getting[0] = input("-> Get data from LCO or unpack downloaded data? (dl/unpack) (leave blank for default = unpack): ")
        os.system('clear')
        getting[1] = input("-> Unpack downloaded data? (y/n) (leave blank for default = y): ")
        os.system('clear')
        getting[2] = input("-> Move data into target directory? (y/n) (leave blank for default = y): ")
        os.system('clear')
        getting[3] = input("-> Enter LCO data location (leave blank for default=%s/Downloads): " % (loc))
        # alignment values (check,move)
        os.system('clear')
        alignment[1] = input("-> Saturated images found, continue image alignment? (y/n) (leave blank for default = y): ")
        os.system('clear')
        alignment[2] = input("-> Move saturated images to SDI archives before continuing? (y/n) (leave blank for default = n): ")
        # combine values (method)
        os.system('clear')
        combination[1] = input("\n-> Choose combination method-- numpy (default) or swarp: (leave blank for default = numpy): ")
        # subtract values (method)
        os.system('clear')
        subtraction[1] = input("\n-> Choose subtraction method: hotpants or AIS: (leave blank for default = hotpants): ")
    else:
        print("Input not supported")
        exit()

    ###
    # first check if there is data to import. if not we need to error and stop the script
    ###
    if getting[3] == "":
        Data_Location = "%s/Downloads" % (loc)
    else:
        Data_Location = getting[3]
    Downloadscontents = subprocess.check_output("echo $(ls %s)" % (Data_Location), shell=True)
    if ".zip" not in Downloadscontents: 
        print("Error: No Data Found")
        exit()


    ###
    # this is important. this imports the "getting" variable into get, so we can reference it within get.
    # we will do a similar thing for the other function calls: align, combine, subtract, extract
    ###
    get.getting = getting
    get.GET()


    ###
    # Identifies the sdi structure path generated by the machine that the script feeds back into itself. 
    # This will look like /home/USERNAME/sdi/targets/TARGETNAME/numbers/air/numbers
    ###
    target = subprocess.check_output("echo $(ls $(pwd)/sdi/targets -t | head -n 1)", shell=True)
    target = target.replace("\n", "")
    radec = subprocess.check_output("echo $(ls $(pwd)/sdi/targets/%s -t -I raw_data | head -n 1)" % (target), shell=True)
    radec = radec.replace("\n", "")
    exposuretime = subprocess.check_output("echo $(ls $(pwd)/sdi/targets/%s/%s/air -t | head -n 1)" % (target, radec), shell=True)
    exposuretime = exposuretime.replace("\n", "")
    exposurepath = "$(pwd)/sdi/targets/target/air/radec/exposuretime"
    exposurepath = subprocess.check_output("echo $(pwd)/sdi/targets/%s/%s/air/%s" % (target, radec, exposuretime), shell=True)
    exposurepath = exposurepath.replace("\n", "")

    print(("Your exposure path is " + exposurepath + ". If this is wrong, check the code."))
    ###
    # Sets the path that the machine generates that is fed back, that was just defined. 
    # Alignment and combination call this "location" and subtraction and extraction call this "path".
    # "location" refers to exposurepath/data and "path" just refers to exposurepath
    ###
    alignment[0] = exposurepath + "/data"
    combination[0] = exposurepath + "/data"
    subtraction[0] = exposurepath
    extraction[0] = exposurepath



    align.alignment = alignment
    subtract.subtraction = subtraction
    combine.combination = combination
    extract.extraction = extraction


    align.ALIGN()
    combine.COMBINE()
    subtract.SUBTRACT()
    extract.EXTRACT()

    print("The automation script ran successfully! Check the sources and filtered sources files within the sdi/targets... directory.")
