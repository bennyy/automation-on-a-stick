#!/home/benny/.python_envs/homeauto/bin/python3

import ephem
import pytz, datetime
import sys
from threading import Timer

from modules.TellstickLib import TellstickLib
tellstickLib = TellstickLib()

def turnOnAllLights():
    print("Turning on all lights...")
    for device in tellstickLib.getDevices():
        print("Turn on lamp-id: {}").format(device.getId())
        tellstickLib.turnOn(device.getId())
    print("...Done.")


def turnOffAllLights():
    print("Turning off all lights...")
    for device in tellstickLib.getDevices():
        print("Turn off lamp-id: {}").format(device.getId())
        tellstickLib.turnOff(device.getId())
    print("...Done")

LOCAL_TIME_ZONE = pytz.timezone("Europe/Stockholm")

def getSecondsToNextSunrise(ep):
    sunrise = ep.next_rising(ephem.Sun())
    sunriseLocalTime = pytz.utc.localize(sunrise.datetime(), is_dst=None).astimezone(LOCAL_TIME_ZONE)
    secondsToSunrise = (sunrise.datetime() - datetime.datetime.utcnow()).total_seconds()

    print("[Sunrise] UTC: {} GMT+2: {}".format(sunrise.datetime(), sunriseLocalTime))
    print("Seconds to sunrise: {}".format(secondsToSunrise))
    print("Time to sunrise (power off): {}".format(datetime.timedelta(seconds=secondsToSunrise)))

    return secondsToSunrise

def getSecondsToNextSunset(ep):
    sunset = ep.next_setting(ephem.Sun())
    sunsetLocalTime = pytz.utc.localize(sunset.datetime(), is_dst=None).astimezone(LOCAL_TIME_ZONE)
    secondsToSunset = (sunset.datetime() -  datetime.datetime.utcnow()).total_seconds()

    print("[Sunset]  UTC: {} GMT+2: {}".format(sunset.datetime(), sunsetLocalTime))
    print("Seconds to sunset: {}".format(secondsToSunset))
    print("Time to sunset (power on): {}".format(datetime.timedelta(seconds=secondsToSunset)))

    return secondsToSunset

def main(argv):
    print("Current UTC_TIME: " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

    ep = ephem.Observer()
    ep.date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") #ephem wants UTC
    ep.lon = str(15.6214)
    ep.lat = str(58.4108)
    ep.elev = 52
    ep.pressure= 0
    ep.horizon = '-0:34'

    sunriseTimer = Timer(int(getSecondsToNextSunrise(ep)), turnOffAllLights)
    sunsetTimer = Timer(int(getSecondsToNextSunset(ep)), turnOnAllLights)

    sunriseTimer.start()
    sunsetTimer.start()

    while True:
        if not sunriseTimer.is_alive():
            sunriseTimer = Timer(int(getSecondsToNextSunrise(ep)), turnOffAllLights)
            sunriseTimer.start()

        if not sunsetTimer.is_alive():
            sunsetTimer = Timer(int(getSecondsToNextSunset(ep)), turnOnAllLights)
            sunsetTimer.start()

if __name__ == '__main__':
    main(sys.argv[1:])