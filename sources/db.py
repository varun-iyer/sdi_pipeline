import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Text, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()


class Record(Base):
    __tablename__ = "Record"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ra = Column(Float)
    dec = Column(Float)
    sources = db.relationship("Source", backref="record", lazy="dynamic")

    def __repr__(self):
        return "<Record {} RA:{} DEC:{}>".format(self.id, self.ra, self.dec)


class Source(Base):
    __tablename__ = "Source"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_id = Column(Integer, ForeignKey('Image.id'))
    time = Column(Date, ForeignKey('Image.time'))
    record_id = Column(Integer, ForeignKey('Record.id'))
    data = Column(Text(255))

    def __repr__(self):
        return "<Source {} Image:{} Record:{}>".format(self.id, self.image_id, self.record_id)

 
class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    path = Column(Text(255), unique=True)
    time = Column(Date, unique=True)
    sources = db.relationship("Source", backref="image", lazy="dynamic")
    lcoid = Column(Integer, unique=True)

    def __repr__(self):
        return "<Image {} Time:{} Path:{}>".format(self.id, self.time, self.path)


def create_session():
    engine = create_engine(r'sqlite:///sdi.db', echo=True) #connect to database
    Base.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
    return sessionmaker(bind=engine)()
