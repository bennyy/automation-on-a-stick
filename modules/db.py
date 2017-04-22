import sys
sys.path.append("../models")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from TellstickModels import DeviceType, Device, Log

class HomeAutoDB(object):
    def __init__(self):
        self.mBase = declarative_base()

        self.mEngine = create_engine('sqlite:///../homeauto.db')

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        self.mBase.metadata.bind = self.mEngine

        DBSession = sessionmaker(bind=self.mEngine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.mSession = DBSession()

    def insertDeviceIfNotExist(self, tellstickId_, **kwargs):
        instance = self.mSession.query(Device).filter(Device.tellstickId == int(tellstickId_)).first()
        if instance:
            return instance
        else:
            instance = Device(**kwargs)
            self.mSession.add(instance)
            self.mSession.commit()
            return instance

    def logEvent(self, tellstickId, enabled_):
        device = self.mSession.query(Device).filter(Device.tellstickId == int(tellstickId)).first()
        if device:
            log = Log(device_id=device.id, enabled=enabled_)
            self.mSession.add(log)
            self.mSession.commit()
        else:
            print("ERROR: Could not find this device")

    def updateDeviceStatus(self, tellstickId, enabled_):
        device = self.mSession.query(Device).filter(Device.tellstickId == int(tellstickId)).first()
        if device:
            device.isOn = enabled_
            self.mSession.commit()
        else:
            print("ERROR: Could not find this device")
    
    def getAllDevices(self):
        return self.mSession.query(Device).all()

    def getSession(self):
        return self.mSession

    # Only for mock-up!
    def getDBDeviceStatus(self, tellstickId):
        device = self.mSession.query(Device).filter(Device.tellstickId == int(tellstickId)).first()
        if device:
            return device.isOn
        else:
            print("ERROR: Could not find this device")