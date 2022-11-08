##################################
# In case of violation, a warning notification to the occupants using buzzer
##################################

import RPi.GPIO as GPIO
import time

scales = [1864, 493]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer = 24
p = GPIO.PWM(buzzer, 1864)

def onBuzzer():
    p.start(50)
    for i in range(7):
        p.ChangeFrequency(scales[(i%2)])
        time.sleep(0.1)
    p.stop()