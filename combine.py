import combine_swarp
import combine_numpy
import inspect

# Updated with SDI v1.2

def COMBINE():
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("combine.py is being ran as a subprocess of auto.py")
        location = combination[0]
        method = combination[1]
    if not automated: location = raw_input("-> Enter path to data directory: ")
    if not automated: method = raw_input("\n-> Choose combination method-- numpy (default) or swarp: ")
    if method == "swarp":
        combine_swarp.swarp(location)
    elif method == "numpy" or method == "":
        combine_numpy.combine_median(location)
    else:
        print("-> Error: unknown method entered")

if __name__ == '__main__':
    current_processes = str(inspect.getouterframes(inspect.currentframe(), 2))
    automated = True if "auto.py" in current_processes else False
    if automated:
        print("combine.py is being ran as a subprocess of auto.py")
        location = combination[0]
        method = combination[1]
    if not automated: location = raw_input("-> Enter path to data directory: ")
    if not automated: method = raw_input("\n-> Choose combination method-- numpy (default) or swarp: ")
    if method == "swarp":
        combine_swarp.swarp(location)
    elif method == "numpy" or method == "":
        combine_numpy.combine_median(location)
    else:
        print("-> Error: unknown method entered")