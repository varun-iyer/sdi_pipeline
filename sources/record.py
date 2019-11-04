from . import db
from datetime import datetime
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
    for source in cat.data:
        img = session.query(db.Image).filter(db.Image.lcoid==sci.header["TRACKNUM"]).first()
        if not img:
            time = datetime.strptime("{} {}".format(sci.header["DATE"],
                               sci.header["UTSTART"]), '%Y-%m-%d %H:%M:%S.%f')
            img = db.Image(path=path, time=time, lcoid=sci.header["TRACKNUM"])
            session.add(img)
        r = round(source["ra"], 3)
        d = round(source["dec"], 3)
        rec = session.query(db.Record).filter(db.Record.ra==r, db.Record.dec==d).first()
        if not rec:
            rec = db.Record(ra=r, dec=d)
            session.add(rec)
        s = db.Source(data=source.__repr__())
        session.add(s)
        rec.sources.append(s)
        img.sources.append(s)
    session.commit()
