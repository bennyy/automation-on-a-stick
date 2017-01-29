#!/home/benny/.python_envs/homeauto/bin/python3

import ephem
import pytz, datetime
import sys
from threading import Timer
import time

from modules.TellstickLib import TellstickLib
tellstickLib = TellstickLib()

def turnOnAllLights():
    for device in tellstickLib.getDevices():
        tellstickLib.turnOn(device.getId())

def turnOffAllLights():
    for device in tellstickLib.getDevices():
        tellstickLib.turnOff(device.getId())

LOCAL_TIME_ZONE = pytz.timezone("Europe/Stockholm")
EXTRA_SECONDS = 5

def getSecondsToNextSunrise(ep):
    sunrise = ep.next_rising(ephem.Sun())
    sunriseLocalTime = pytz.utc.localize(sunrise.datetime(), is_dst=None).astimezone(LOCAL_TIME_ZONE)
    secondsToSunrise = (sunrise.datetime() - datetime.datetime.utcnow()).total_seconds()

    print("[Sunrise] UTC: {} GMT+2: {}".format(sunrise.datetime(), sunriseLocalTime))
    print("Seconds to sunrise: {}".format(secondsToSunrise))
    print("Time to sunrise (power off): {}".format(datetime.timedelta(seconds=secondsToSunrise)))
    sys.stdout.flush()

    return secondsToSunrise + EXTRA_SECONDS

def getSecondsToNextSunset(ep):
    sunset = ep.next_setting(ephem.Sun())
    sunsetLocalTime = pytz.utc.localize(sunset.datetime(), is_dst=None).astimezone(LOCAL_TIME_ZONE)
    secondsToSunset = (sunset.datetime() -  datetime.datetime.utcnow()).total_seconds()

    print("[Sunset]  UTC: {} GMT+2: {}".format(sunset.datetime(), sunsetLocalTime))
    print("Seconds to sunset: {}".format(secondsToSunset))
    print("Time to sunset (power on): {}".format(datetime.timedelta(seconds=secondsToSunset)))
    sys.stdout.flush()

    return secondsToSunset + EXTRA_SECONDS

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
            ep.date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            sunriseTimer = Timer(int(getSecondsToNextSunrise(ep)), turnOffAllLights)
            sunriseTimer.start()

        if not sunsetTimer.is_alive():
            ep.date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            sunsetTimer = Timer(int(getSecondsToNextSunset(ep)), turnOnAllLights)
            sunsetTimer.start()

        time.sleep(1)

if __name__ == '__main__':
    main(sys.argv[1:])
