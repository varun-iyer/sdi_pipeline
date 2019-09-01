"""
saturation
determines how saturated astronomical data is based on information
in its fits header
History
    Substantially refactored on 2019-09-01
        Varun Iyer <varun_iyer@ucsb.edu>
"""


def saturation(hdu):
    """
    Calculates the ratio of saturated pixels in data.
    Arguments
    hdu -- fitsio HDU or list containing HDUs
    Returns
    (# of sat. pixels) / (# of pixels) or a list of ratios
    """
    # TODO Maybe look for saturated 'blobs' instead? Or use a saturation lib,
    # look at docs for saturation in astroalign
    # the algorithm currently being used is suspect at best
    datas = []
    if isinstance(hdu, list):
        datas = hdu
    else:
        datas.append(hdu)

    outputs = []
    for datum in datas:
        sat = datum.header['SATURATE']
        lin = datum.header['MAXLIN']
        saturated = (datum > max(lin, sat)).sum()
        outputs.append(sum(saturated) / saturated.size)

    return outputs if isinstance(hdu, list) else outputs[0]
