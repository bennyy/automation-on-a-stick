import sys
sys.path.append("../models")

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import TellstickModels

from TellstickModels import DeviceType

# Todo(Benjamin): Global name for the db-name?
# Create an engine that stores data in the homeauto.db file.
engine = create_engine('sqlite:///../homeauto.db')
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
TellstickModels.Base.metadata.create_all(engine)

TellstickModels.Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

d = DeviceType(name="Lamp")
session.add(d)
session.commit()
