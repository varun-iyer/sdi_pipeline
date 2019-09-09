"""
reference is a set of methods used to work with the Nasa M31 Star database
History:
    Created 2019-09-08
        Varun Iyer <varun_iyer@ucsb.edu>
"""
import pyvo as vo

 
service = vo.dal.SCSService("https://heasarc.gsfc.nasa.gov/cgi-bin/vo/cone/coneGet.pl?table=m31stars&")


def reference(catalogs, thresh=0.001):
    """
    Reference searches the database to see if sources in the given catalog(s)
    can be used as known reference stars
    Arguments:
        catalogs -- An HDU BinTable catalog or list of them provided by the LCO
    Keyword Arguments:
        thresh=0.001 -- how tight the search cone should be in degrees, .001 is
            the number of sigfigs we get from wcs proj. compared to ra/dec
    Returns:
        A list of tuples; each tuple is a catalog and an SCSResults object
        representing possible matches        
    """
    cats = []
    if isinstance(catalogs, list):
        cats = catalogs
    else:
        cats.append(catalogs)

    matches = []
    for cat in cats:
        for source in cat.data:
            # FIXME we should run one query and then do our own collisions
            # repeated querying is very, very slow
            references = service.search((source["ra"], source["dec"]), thresh)
            if len(references) > 0:
                matches.append((source, references))
    return matches
