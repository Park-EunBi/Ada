##################################
# Receive GPS information and normalize the value to be passed to the database
##################################

import os, sys
import serial
import time
import datetime

ser = serial.Serial('/dev/ttyUSB0', 192000, timeout=5)

# Receive GPRMC protocol data from GPS
def readGPSData():
    while True:
        line = ser.readline()
        if line[0:6] =="$GPRMC":
            return line

now = datetime.datetime.now()
now = str(now)
nowDate = now[0:11]

datetime_format = "%Y-%m-%d %H%M%S.%f"

# Normalize received GPS data
def normGPSData(data):
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print("no satellite data available")
            return
        gpsTime = sdata[1]
        gpsDatetime = nowDate + gpsTime

        normTime = datetime.datetime.strptime(gpsDatetime, datetime_format)

        gLatitude = sdata[3]
        gDirLat = sdata[4]
        gLongitude = sdata[5]
        gDirLon = sdata[6]

        print("---Parsing GPRMC---\ntime : %s\nlatitude : %s, %s\nlongitude : %s, %s" %(normTime, gLatitude, gDirLat, gLongitude, gDirLon))

        return normTime, gLatitude, gDirLat, gLongitude, gDirLon

