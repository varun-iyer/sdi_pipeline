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
    data = Column(Text(255))

    def __repr__(self):
        return "<Source {} Image:{} Record:{}>".format(self.id, self.image_id, self.record_id)

 
class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    path = Column(Text(255), unique=True)
    time = Column(DateTime, unique=True)
    ra = Column(Float)
    ra_max = Column(Float)
    ra_min = Column(Float)
    dec = Column(Float)
    dec_max = Column(Float)
    dec_min = Column(Float)
    sources = relationship("Source", backref="image", lazy="dynamic", foreign_keys="Source.image_id")
    hash = Column(Text(32), unique=True, index=True)

    def __repr__(self):
        return "<Image {} Time:{} Path:{}>".format(self.id, self.time, self.path)


def create_session():
    engine = create_engine(r'sqlite:////seti_data/sdi.db', echo=True) #connect to database
    Base.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
    return sessionmaker(bind=engine)()
