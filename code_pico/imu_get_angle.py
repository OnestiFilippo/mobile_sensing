from imu import MPU6050
import time
from machine import Pin, I2C
import math

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
imu = MPU6050(i2c)

previous_time = time.ticks_ms()
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

alpha = 0.98  # Coefficiente del filtro complementare

print(previous_time)

while True:
    ax = imu.accel.x
    ay = imu.accel.y
    az = imu.accel.z
    gx = imu.gyro.x
    gy = imu.gyro.y
    gz = imu.gyro.z
    
    current_time = time.ticks_ms()
    dt = time.ticks_diff(current_time, previous_time) / 1000.0
    previous_time = current_time

    # Calcolo dell'angolo da accelerometro
    accel_angle_x = math.atan2(ay, az) * 180 / math.pi
    accel_angle_y = math.atan2(ax, az) * 180 / math.pi

    # Calcolo dell'angolo dal giroscopio (integrazione)
    angle_x = alpha * (angle_x + gx * dt) + (1 - alpha) * accel_angle_x
    angle_y = alpha * (angle_y + gy * dt) + (1 - alpha) * accel_angle_y

    # Stampa gli angoli calcolati
    #print("Angolo X:", angle_x, "\n")
    print("Angolo Y:", int(angle_y), "\n")

