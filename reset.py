import os
from . import initialize

# Updated with SDI v1.2

# reset script to reset the sdi folder to new

def RESET():
	os.system("rm -r sdi")
	initialize.INITIALIZE()
	print("The system reset itself properly.")

if __name__ == '__main__':
	os.system("rm -r sdi")
	initialize.INITIALIZE()
	print("The system reset itself properly.")