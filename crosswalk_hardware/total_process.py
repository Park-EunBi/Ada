##################################
# Determination of electric driving crossing violations
#
# Conditions deemed to be in violation
# 1) Crosswalk is recognized
# 2) the scooter moves
# 3) The rider boards the scooter
##################################

import os
import threading
from send_info_and_img_to_database import saveViolationDataToList, sendDataToDatabase, sendImg
from alert_by_buzzer import onBuzzer
from detect_driving_by_acc import detect_acc
from detect_press_by_switch import detect_switch
import time

# Determination of violations while driving
def driving_violation_check():
    i =0
    no_line = 0
    while True:
        line = fileRead.readline()

        if f'{i}' in line:
            time.sleep(0.1)
            no_line = 0
            print(line)
            i+=1

            # If true, crosswalks are recognized
            if "True" in line:
                # If true, the scooter moves
                if detect_acc():
                    # If true, the rider is on the scooter
                    if detect_switch():
                        # In case of violation, a buzzer sounds and the violation data is saved
                        onBuzzer()
                        thSaveVioList = threading.Thread(target=saveViolationDataToList)
                        thSaveVioList.start()
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            if not no_line:
                no_line +=1
            if no_line>10000:
                break
            continue


if __name__ == '__main__':
    violation_img = "/home/pi/Ada/result/crosswaik_model/result/detect.jpg"
    filename = "/home/pi/Ada/crosswalk_model/crosswalk_result.txt"
    file = open(filename, 'w')
    file.write(' ')
    file.close()

    thSaveVioList = threading.Thread(target=saveViolationDataToList, args=(violation_img))
    fileRead = open(filename, mode='r')

    i=0
    while True:
        i+=1
        line = fileRead.readline()
        print(line)
        if "start" in line:
            break

    print("---------------------------")
    print("start Driving\nI will ckeck your violation")
    print("---------------------------")
    driving_violation_check()

    print("---------------------------")
    print("End Driving")
    print("---------------------------")

    sendDataToDatabase()
    sendImg()
    os._exit()

    print("---------------------------")
    print("Send Data to server & database")
    print("---------------------------")
