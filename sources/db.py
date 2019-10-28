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
    dec = Column(Text(255))

    def __repr__(self):
        return "<Record {} RA:{} DEC:{}>".format(self.id, self.ra, self.dec)

class Source(Base):
    __tablename__ = "Source"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    image_id = Column(Integer, ForeignKey('Image.id'))
    record_id = Column(Integer, ForeignKey('Record.id'))
    record = Column(Text(255))

class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    path = Column(Text(255), unique=True)
    time = Column(Date, unique=True)
    lcoid = Column(Integer, unique=True)


if __name__ == '__main__':
    print('running sqlalchemy ' + sqlalchemy.__version__)
    engine = create_engine(r'sqlite:///sdi.db', echo=True) #connect to database
    Base.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
    session = sessionmaker(bind=engine)()
