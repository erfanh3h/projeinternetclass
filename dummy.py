import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Create and object of class User
user = User(111, "admin","password", "a@b.com", "qom")
# add() is used to place instances in the session.
# For transient (i.e. brand new) instances, this will have the effect of an INSERT taking place for those instances
# upon the next flush.
session.add(user)
 
user = User(112, "python","python", "p@p.com", "tehran")
session.add(user)
 
# write the record the database
session.commit()