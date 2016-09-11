from ctypes import * 

class TellstickLib:
    def __init__(self):
        try:
            self.devices = {}
            self.lib = cdll.LoadLibrary('libtelldus-core.so.2')

            for device in range(0, self.getNumberOfDevices()):
                deviceId = self.lib.tdGetDeviceId(device)
                self.getDeviceStatus(deviceId)

                # Get device name
                funcGetName = self.lib.tdGetName        # The Telldus-lib function name
                funcGetName.restype = c_void_p          # Return pointer is void*
                cp = c_char_p(funcGetName(deviceId))    # Cast it to a char*
                deviceName = cp.value                   # Copy over the string to "Python-space"
                self.lib.tdReleaseString(cp)            # Free up that buffer!

                self.devices[deviceId] = deviceName.decode("utf-8")
            print(self.devices)
        except OSError:
            print("Error loading Telldus library.")

    def turnOn(self, id):
        self.lib.tdTurnOn(int(id))

    def turnOff(self, id):
        self.lib.tdTurnOff(int(id))

    def getDeviceStatus(self, id):
        pass
        #print(self.lib.tdLastSentCommand(id))

    def getNumberOfDevices(self):
        return self.lib.tdGetNumberOfDevices()

    def getDevices(self):
        return self.devices



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
