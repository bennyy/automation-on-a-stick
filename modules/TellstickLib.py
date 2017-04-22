import sys
sys.path.append("../models")

from ctypes import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from TellstickModels import DeviceType, Device, Log
from db import HomeAutoDB

class TellstickLib:
    def __init__(self):
        self.db = HomeAutoDB()

        self.STUBBED_LIB = False

        try:
            self.lib = cdll.LoadLibrary('libtelldus-core.so.2')
            self.lib.tdInit()
            for device in range(0, self.getNumberOfDevices()):
                deviceId = self.lib.tdGetDeviceId(device)
                deviceStatus = self.getDeviceStatus(deviceId)

                # Get device name
                funcGetName = self.lib.tdGetName        # The Telldus-lib function name
                funcGetName.restype = c_void_p          # Return pointer is void*
                cp = c_char_p(funcGetName(deviceId))    # Cast it to a char*
                deviceName = cp.value                   # Copy over the string to "Python-space"
                self.lib.tdReleaseString(cp)            # Free up that buffer!
                
                self.db.insertDeviceIfNotExist(deviceId,
                tellstickId=deviceId, name=deviceName, isOn=deviceStatus)
                

        except OSError:
            self.STUBBED_LIB = True

            for i in range(7):
                self.db.insertDeviceIfNotExist(i,
                tellstickId=i, name="Room " + str(i), isOn=i%2)

            print("Error loading Telldus library.")


    def turnOn(self, id):
        self.db.updateDeviceStatus(id, 1)
        self.db.logEvent(id, 1)

        if self.STUBBED_LIB:
            print("Lamp {} turned ON.".format(id))
        else:
            self.lib.tdTurnOn(int(id))

    def turnOff(self, id):
        self.db.updateDeviceStatus(id, 0)
        self.db.logEvent(id, 0)

        if self.STUBBED_LIB:
            print("Lamp {} turned OFF.".format(id))
        else:
            self.lib.tdTurnOff(int(id))

        
    def getDeviceStatus(self, id):
        if not self.STUBBED_LIB:
            lastSentCommand = self.lib.tdLastSentCommand(int(id), 1)
            return lastSentCommand
        else:
            return self.db.getDBDeviceStatus(id)

    def getNumberOfDevices(self):
        if not self.STUBBED_LIB:
            return self.lib.tdGetNumberOfDevices()
        else:
            return len(self.getDevices())

    def updateDeviceStatus(self):
        for device in self.getDevices():
            if self.getDeviceStatus(device.tellstickId) == 1:
                self.db.updateDeviceStatus(device.tellstickId, True)
            else:
                self.db.updateDeviceStatus(device.tellstickId, False)

    def getDevices(self):
        return self.db.getAllDevices()

'''
0000a86c T tdAddDevice
00008e60 T tdBell
00008c60 T tdClose
0000ae84 T tdConnectTellStickController
0000b4e0 T tdController
0000b520 T tdControllerValue
00008f5c T tdDim
0000b008 T tdDisconnectTellStickController
00009260 T tdDown
00009068 T tdExecute
00009974 T tdGetDeviceId
0000a624 T tdGetDeviceParameter
00009a70 T tdGetDeviceType
0000ab60 T tdGetErrorString
0000a1d4 T tdGetModel
00009b6c T tdGetName
00009888 T tdGetNumberOfDevices
00009ea0 T tdGetProtocol
00008b90 T tdInit
00009554 T tdLastSentCommand
00009660 T tdLastSentValue
00009458 T tdLearn
0000aa54 T tdMethods
00008c24 T tdRegisterControllerEvent
00008bdc T tdRegisterDeviceChangeEvent
00008b94 T tdRegisterDeviceEvent
00008bb8 T tdRegisterRawDeviceEvent
00008c00 T tdRegisterSensorEvent
00008c64 T tdReleaseString
0000b89c T tdRemoveController
0000a958 T tdRemoveDevice
0000acc4 T tdSendRawCommand
0000b18c T tdSensor
0000b1d4 T tdSensorValue
0000b780 T tdSetControllerValue
0000a508 T tdSetDeviceParameter
0000a3fc T tdSetModel
00009d94 T tdSetName
0000a0c8 T tdSetProtocol
0000935c T tdStop
00008d64 T tdTurnOff
00008c68 T tdTurnOn
00008c48 T tdUnregisterCallback
00009164 T tdUp
'''
