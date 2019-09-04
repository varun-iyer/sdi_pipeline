import glob
import subprocess.check_output
from astropy.io import fits


# FIXME this tmpdir should be in a config file rather than direclty in python
TMPDIR = "/tmp"


def subtract(data, template, method="hotpants"):
    datas = []
    if isinstance(data, list):
    else:
        datas.append(data)
    if method != "hotpants":
        # TODO see below
        raise NotImplementedError("Subtraction methods other that hotpants (IBIS, AIS) are unimplemented.")
    tmplim = "{}/tmplim.fits".format(TMPDIR)
    fits.writeto(tmpllim, template)
    outputs = []
    for d in data:
        inim = "{}/inim.fits".format(TMPDIR)
        fits.writeto(inim, d)
        outim = "{}/outim.fits".format(TMPDIR)
        sub_out = subprocess.check_output(
            "hotpants -inim {} -timplm {} -outim {}".format(inim, tmplim, outim),
            shell=True
        )
        outputs.append(fits.open(outim)[0])
    return outputs


