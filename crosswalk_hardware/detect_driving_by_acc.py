######################################
# Determining if the kickboard is moving using the MPU6050 sensor
######################################

import smbus  # import SMBus module of I2C
from time import sleep  # import

# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B #107
SMPLRT_DIV = 0x19 #25
CONFIG = 0x1A #26
GYRO_CONFIG = 0x1B #27
INT_ENABLE = 0x38 #56
ACCEL_XOUT_H = 0x3B #59
ACCEL_YOUT_H = 0x3D #61
ACCEL_ZOUT_H = 0x3F #63
preAx=0
preAy=0


def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def read_raw_data(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if (value > 32768):
        value = value - 65536
    return value


def detect_acc():
    MPU_Init()
    global preAx
    global preAy

    print(" Reading Data of Gyroscope and Accelerometer")

    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)

    Ax = acc_x / 16384.0
    Ay = acc_y / 16384.0

    diffAx = abs(Ax-preAx)
    diffAy = abs(Ay-preAy)

    print(str(diffAy*100) + ' ' + str(diffAy*100))

    preAx = Ax
    preAy = Ay

    if (diffAx*100>=10) and (diffAy*100>=10):
        return True

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
sleep(1)
Device_Address = 0x68  # MPU6050 device address