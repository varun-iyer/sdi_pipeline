from . import align_astroalign
from .ref_image import ref_image
from . import check_saturation
import inspect

# Updated with SDI v1.2

def ALIGN():
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("align.py is being ran as a subprocess of auto.py")
        location = alignment[0]
        check = alignment[1]
        move = alignment[2]
    if not automated: location = input("-> Enter path to data directory: ")
    sat = check_saturation.check_saturate(location)
    if sat == 0:
        ref_image(location)
        align_astroalign.align2(location)
    else:
        if not automated: check = input("-> Saturated images found, continue image alignment? (y/n) (leave blank for default = y): ")
        if ((check == 'y') or (check == '')):
            if not automated: move = input("-> Move saturated images to SDI archives before continuing? (y/n) (leave blank for default = n): ")
            if move == 'y':
                check_saturation.move_arch(sat)
                ref_image(location)
                align_astroalign.align2(location)
            elif ((move == 'n') or (move == '')):
                ref_image(location)
                align_astroalign.align2(location)
            else:
                print("-> Unknown input: must be y or n")
        elif check =='n':
            pass
        else:
            print("-> Unknown input: must be y or n")



if __name__ == '__main__':
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("align.py is being ran as a subprocess of auto.py")
        location = alignment[0]
        check = alignment[1]
        move = alignment[2]
    if not automated: location = input("-> Enter path to data directory: ")
    sat = check_saturation.check_saturate(location)
    if sat == 0:
        ref_image(location)
        align_astroalign.align2(location)
    else:
        if not automated: check = input("-> Saturated images found, continue image alignment? (y/n) (leave blank for default = y): ")
        if ((check == 'y') or (check == '')):
            if not automated: move = input("-> Move saturated images to SDI archives before continuing? (y/n) (leave blank for default = n): ")
            if move == 'y':
                check_saturation.move_arch(sat)
                ref_image(location)
                align_astroalign.align2(location)
            elif ((move == 'n') or (move == '')):
                ref_image(location)
                align_astroalign.align2(location)
            else:
                print("-> Unknown input: must be y or n")
        elif check =='n':
            pass
        else:
            print("-> Unknown input: must be y or n")