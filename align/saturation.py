from .align import _to_np
 
  
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
    if isinstance(data, list):
        datas = data
    else:
        datas.append(data)

    outputs = []
    for datum in datas:
        sat = hdu.header['SATURATE']
        lin = hdu.header['MAXLIN']
        saturated = (hdu > max(lin, sat)).sum()
        outputs.append(sum(saturated) / saturated.size)

    return outputs if isinstance(data, list) else outputs[0]
