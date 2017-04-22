from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime

Base = declarative_base()

class DeviceType(Base):
    __tablename__ = 'device_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    devices = relationship("Device")

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    tellstickId = Column(Integer)
    name = Column(String)
    deviceType_id = Column(Integer, ForeignKey('device_type.id'))
    isOn = Column(Boolean)
    watt = Column(Integer, default=0)

    logs = relationship("Log")

    def __repr__(self):
        return "<User(name='%s', deviceType='%s', watt='%s')>" % (self.name, self.deviceType_id.name, self.watt)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id'))
    enabled = Column(Boolean)
    eventDate = Column(DateTime, default=datetime.datetime.utcnow)
