from initialize import loc
from master_residual import MR
import subtract_hotpants
import subtract_ais
import inspect

# Updated with SDI v1.2

def SUBTRACT():
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("subtract.py is being ran as a subprocess of auto.py")
        path = subtraction[0]
        method = subtraction[1]
    if not automated: path = raw_input("\n-> Enter path to exposure time directory: ")
    if not automated: method = raw_input("\n-> Choose subtraction method: hotpants or AIS: (leave blank for default = hotpants): ")
    if method == 'hotpants' or method == '':
#        align_skimage.skimage_template(location)
        subtract_hotpants.hotpants(path)
#        MR(path)
    elif method == 'AIS':
#        align_chi2.chi2(location)
        subtract_ais.isis_sub(path)
#        MR(path)
    else:
        print("\n-> Error: Unknown method")

if __name__ == '__main__':
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("subtract.py is being ran as a subprocess of auto.py")
        path = subtraction[0]
        method = subtraction[1]
    if not automated: path = raw_input("\n-> Enter path to exposure time directory: ")
    if not automated: method = raw_input("\n-> Choose subtraction method: hotpants or AIS: (leave blank for default = hotpants): ")
    if method == 'hotpants' or method == '':
#        align_skimage.skimage_template(location)
        subtract_hotpants.hotpants(path)
#        MR(path)
    elif method == 'AIS':
#        align_chi2.chi2(location)
        subtract_ais.isis_sub(path)
#        MR(path)
    else:
        print("\n-> Error: Unknown method")