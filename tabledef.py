from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    sid = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(Integer)
    email = Column(String)
    resume = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, sid, name, phone, email, resume):
        """"""
        self.sid = sid
        self.name = name
        self.phone = phone
        self.email = email
        self.resume = resume
 
# create tables
Base.metadata.create_all(engine)