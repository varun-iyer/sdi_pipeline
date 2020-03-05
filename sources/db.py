import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, Text, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()


class Record(Base):
    __tablename__ = "Record"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ra = Column(Float)
    dec = Column(Float)
    ra_std = Column(Float)
    dec_std = Column(Float)
    sources = relationship("Source", backref="record", lazy="dynamic", foreign_keys="Source.record_id")

    def __repr__(self):
        return "<Record {} RA:{} DEC:{}>".format(self.id, self.ra, self.dec)


class Source(Base):
    __tablename__ = "Source"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_id = Column(Integer, ForeignKey('Image.id'))
    time = Column(DateTime, ForeignKey('Image.time'))
    record_id = Column(Integer, ForeignKey('Record.id'))
    x = Column(Float)
    y = Column(Float)
    xwin = Column(Float)
    ywin = Column(Float)
    xpeak = Column(Float)
    ypeak = Column(Float)
    flux= Column(Float)
    fluxerr = Column(Float)
    peak = Column(Float)
    fluxaper1 = Column(Float)
    fluxerr1= Column(Float)
    fluxaper2 = Column(Float)
    fluxerr2 = Column(Float)
    fluxaper3 = Column(Float)
    fluxerr3 = Column(Float)
    fluxaper4 = Column(Float)
    fluxerr4 = Column(Float)
    fluxaper5= Column(Float)
    fluxerr5 = Column(Float)
    fluxaper6 = Column(Float)
    fluxerr6 = Column(Float)
    background = Column(Float)
    fwhm = Column(Float)
    a = Column(Float)
    b = Column(Float)
    theta= Column(Float)
    kronrad = Column(Float)
    ellipticity = Column(Float)
    fluxrad = Column(Float)
    fluxrad50 = Column(Float)
    fluxrad75= Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    xy= Column(Float)
    flag = Column(Float)
    ra = Column(Float)
    dec = Column(Float)

    def __repr__(self):
        return "<Source {} Image:{} Record:{}>".format(self.id, self.image_id, self.record_id)

 
class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    path = Column(Text(255), unique=True)
    time = Column(DateTime, unique=True)
    ra = Column(Float)
    dec = Column(Float)
    sources = relationship("Source", backref="image", lazy="dynamic", foreign_keys="Source.image_id")
    hash = Column(Text(32), unique=True, index=True)

    def __repr__(self):
        return "<Image {} Time:{} Path:{}>".format(self.id, self.time, self.path)


def create_session():
    engine = create_engine(r'sqlite:////seti_data/sdi.db', echo=True) #connect to database
    Base.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
    return sessionmaker(bind=engine)()
