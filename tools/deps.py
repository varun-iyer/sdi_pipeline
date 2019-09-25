#!/usr/bin/python33
import importlib
import subprocess
import re

pydeps = ["numpy", "scipy", "pyd9", "astropy", "pyvo", "skimage", "astroalign", "pytest", "requests", "pylint", "pytest"]
for dep in pydeps:
	lib = importlib.import_module(dep)
	print("{}: {}".format(dep, lib.__version__))


binvers = ["hotpants"]
# this should use non-capturing groups for the last digit probably
for b in binvers:
    proc = subprocess.Popen(b, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = "".join([p.decode('utf-8') for p in proc.communicate()])
    ver = re.findall("\d+\.\d+\.?\d*", output)[0]
    print("{}: {}".format(b.split(" ")[0], ver))
