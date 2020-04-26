from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import Angle
import re
from datetime import datetime
from . import db
from astropy.utils.data import compute_hash
import sep


def record(image, path):
    """
    only works with lco shit for now
    """
    # bkg = sep.background(image.data)
    # recarray = sep.extract(image.data - bkg.back(), bkg.globalrms * 3.0)
    session = db.create_session()
    cat = image["CAT"]
    sci = image["SCI"]
     
    hash_ = compute_hash(path)
    img = session.query(db.Image).filter(db.Image.hash==hash_).first()
    if img is None:
        datestr = re.search(r"\d{4}-\d{2}-\d{2}", sci.header["DATE"]).group()
        timestr = re.search(r"\d{2}:\d{2}:\d{2}\.?\d+", sci.header["UTSTART"]).group()
        dt = datetime.strptime(" ".join([datestr, timestr]), "%Y-%m-%d %H:%M:%S.%f")
        w = WCS(sci.header, image)
        wcs_minmax = w.all_pix2world([[1, 1], sci.data.shape], 1)
        img = db.Image(path=path, time=dt, hash=compute_hash(path),
                       ra=Angle(sci.header["RA"], unit="hourangle").deg,
                       dec=Angle(sci.header["DEC"], unit="degree").deg,
                       ra_min=wcs_minmax[0][0], ra_max=wcs_minmax[1][0],
                       dec_min=wcs_minmax[0][1], dec_max=wcs_minmax[1][1])
        session.add(img)
         
    for source in cat.data:
        r = round(source["ra"], 2)
        d = round(source["dec"], 2)
        # rec = session.query(db.Record).filter(db.Record.ra==r, db.Record.dec==d).first()
        # if rec is None:
            # rec = db.Record(ra=r, dec=d)
        #     session.add(rec)
        s = db.Source(data=source.__repr__())
        session.add(s)
        # rec.sources.append(s)
        img.sources.append(s)
    session.commit()
