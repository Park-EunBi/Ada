##################################
# Pressure sensing using a switch as an alternative to the FSR402 sensor
##################################
import RPi.GPIO as GPIO

switch = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)

#Returns True when the switch is pressed
def detect_switch():
    if GPIO.input(switch)==0:
        return True