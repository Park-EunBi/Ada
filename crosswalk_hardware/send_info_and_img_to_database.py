##################################
# In case of violation, the information is transmitted to the database
#
# 1) Time, latitude, longitude information
# 2) capture image
##################################

from GPS_get_data import normGPSData, readGPSData
import pymysql
import random
from PIL import Image
import boto3

totalViolationList = []

# Convert digital data to binary format
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# Store violation information to be passed to the database in a list
def saveViolationDataToList(violationImg):
    user_id = random.randrange(1, 7)
    normTime, gLatitude, gDirLat, gLongitude, gDirLon = normGPSData(readGPSData())
    violationDict = {"user_id":'', "normTime":'', "lat":'', "lon":'', "dirLat":'', "dirLon":'', "photo_name":'', "photo_url":''}
    violationDict["user_id"] = user_id
    violationDict["normTime"] = normTime
    violationDict["lat"] = gLatitude
    violationDict["lon"] = gLongitude
    violationDict["dirLat"] = gDirLat
    violationDict["dirLon"] = gDirLon

    normTime = str(normTime).replace(':', '-')
    normTime = normTime.replace(' ', '+')
    imageName = str(user_id)+'-'+str(normTime)

    image = Image.open(violationImg)
    image.save("/home/pi/Ada/violationPhoto/"+imageName+".jpg", "JPEG")
    violationDict["photo_name"] = imageName
    violationDict["photo_url"] = ""+imageName+".jpg"

    totalViolationList.append(violationDict)


#Connect to database and send information obtained in case of violation
def sendDataToDatabase():
    # when the implementation, randomly stores the user ID
    user_id = random.randrange(1,7)

    conn = pymysql.connect(host='', user='', password='', db='',charset='utf8', port=3306)
    cur = conn.cursor()

    sql = """insert into violation(user_id ,time,latitude, longitude, cardinal_points_NS, cardinal_points_EW, photo_url)
             values (%s, %s, %s, %s, %s, %s, %s)"""

    for i in range(len(totalViolationList)):
        cur.execute(sql, (totalViolationList[i]["user_id"], totalViolationList[i]["normTime"], totalViolationList[i]["lat"], totalViolationList[i]["lon"], totalViolationList[i]["dirLat"], totalViolationList[i]["dirLon"], totalViolationList[i]["photo_url"]))

    conn.commit()
    conn.close()

#connect to S3
def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="",
            aws_secret_access_key="",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

# sending violation photo to S3
def sendImg():
    s3 = s3_connection()
    try:
        for i in range(len(totalViolationList)):
            s3.upload_file("/home/pi/Ada/violationPhoto/"+totalViolationList[i]["photo_name"]+".jpg","ada-scooter",totalViolationList[i]["photo_name"]+".jpg")
    except Exception as e:
        print(e)
