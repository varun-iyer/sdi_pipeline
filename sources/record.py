import db
import sep


def record(image):
    """
    only works with lco shit for now
    """
    # bkg = sep.background(image.data)
    # recarray = sep.extract(image.data - bkg.back(), bkg.globalrms * 3.0)
    session = db.create_session()
    cat = image["CAT"]
    sci = image["SCI"]
    for source in cat.data:
        r = db.Record(ra=source["ra"], dec=source["dec"])
        session.add(r)
    session.commit()

