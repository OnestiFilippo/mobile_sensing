from machine import Pin, SoftI2C, I2C, PWM, UART
import ssd1306
from time import sleep
from imu import MPU6050
import neopixel
import network
import secrets
from umqttsimple import MQTTClient
import ujson
from micropyGPS import MicropyGPS
import os
import math
import time

# Components initialization
# MPU6050
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
imu = MPU6050(i2c)

# NEOPIXEL
leds = neopixel.NeoPixel(Pin(21), 2)

#BUZZER
buzzer = PWM(Pin(20))

# OLED
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

oled_width = 128
oled_height = 64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# NEO6M
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

TIMEZONE = 2
my_gps = MicropyGPS(TIMEZONE)

# BUTTONS
button1 = Pin(18, Pin.IN, Pin.PULL_UP)
button2 = Pin(19, Pin.IN, Pin.PULL_UP)

# Variables initialization

previous_time = time.ticks_ms()
angle_y = 0.0

status = 'MAIN'
#z_thresh_value = 20
z_diff_value = 20

records = []
g_values = [0]*10

filename = ""

# MQTT 
mqtt_server = '192.168.1.55'
client_id = "mobile_sensor"
topic_pub = b'records'

# Function to convert GPS data
def convert(parts):
    if (parts[0] == 0):
        return None
        
    data = parts[0]+(parts[1]/60.0)
    # parts[2] contain 'E' or 'W' or 'N' or 'S'
    if (parts[2] == 'S'):
        data = -data
    if (parts[2] == 'W'):
        data = -data

    data = '{0:.6f}'.format(data) # to 6 decimal places
    return str(data)

# Function to send records to the server via MQTT
def send():
    if len(os.listdir("/records")) != 0:
        oled.fill(0)
        oled.text("Connecting to", 5,10)
        oled.text("WiFi..", 5,20)
        oled.show()

        # Connect to WiFi
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True) # power up the WiFi chip
        sleep(5) # wait three seconds for the chip to power up and initialize
        wlan.connect(secrets.SSID, secrets.PASSWORD)
        while not wlan.isconnected():
            sleep(0.2)
        oled.fill(0)
        oled.text("WiFi Connected", 5,10)
        oled.show()
        sleep(2)

        # Connect to MQTT
        client = MQTTClient(client_id, mqtt_server)
        client.connect()
        oled.fill(0)
        oled.text("MQTT Connected", 5,10)
        oled.show()
        sleep(2)

        # Send records 
        for filename in os.listdir("/records"):
            print(filename)
            with open("records/"+filename, "r") as file:
                records_file = file.read()
                file.close()
            
            if records_file:
                if wlan.isconnected():
                    oled.fill(0)
                    oled.text("Sending..", 5,20)
                    oled.text(filename[7:21], 5,40)
                    oled.show()
                    print(records_file)

                    # Publish the record on the topic
                    client.publish(topic_pub, records_file)

                    sleep(2)
                    oled.fill(0)
                    oled.text("Successfully", 5,10)
                    oled.text("sent!", 5,20)
                    oled.show()
                    sleep(2)
                else:
                    oled.fill(0)
                    oled.text("Error while", 5,10)
                    oled.text("connecting", 5,20)
                    oled.show()
                    sleep(3)
                    return 0
        return 1
    else:
        oled.fill(0)
        oled.text("No records", 5,10)
        oled.text("to send!", 5,20)
        oled.show()
        sleep(3)
        return 0

# Function Z_Thresh to detect a Z drop
#def z_thresh(g):
    #print(g[9])
    #if g[9] > z_thresh_value:
    #    return True
    #else:
    #    return False

# Function Z_Diff to detect a Z drop
def z_diff():
    #print(abs(g_values[9]-g_values[8]))
    if abs(g_values[9]-g_values[8]) > z_diff_value:
        # Reset value to avoid multiple detections
        g_values[9] = g_values[8]
        return True
    else:
        return False

# Function to get the angle used to detect a ramp
def get_angle():
    ax = imu.accel.x
    ay = imu.accel.y
    az = imu.accel.z
    gx = imu.gyro.x
    gy = imu.gyro.y
    gz = imu.gyro.z
    
    alpha = 0.98  # Filter coefficient
    
    global previous_time
    global angle_y
    
    current_time = time.ticks_ms()
    dt = time.ticks_diff(current_time, previous_time) / 1000.0
    previous_time = current_time

    # Angle calculation from accelerometer
    accel_angle_y = math.atan2(ax, az) * 180 / math.pi

    # Angle calculation from gyroscope (integration)
    angle_y = alpha * (angle_y + gy * dt) + (1 - alpha) * accel_angle_y

    return abs(int(angle_y))

# Function to draw an arrow on the OLED
def write_arrow(x, y):
    for i in range(0,6):
        oled.pixel(x+i, y-i, 1)
        oled.pixel(x+1+i, y-i, 1)
        oled.pixel(x+3, y-5, 1)
        oled.pixel(x+4, y-5, 1)
        oled.pixel(x+6, y-4, 1)
        oled.pixel(x+5, y-3, 1)
        oled.pixel(x+6, y-3, 1)
        oled.pixel(x+6, y-2, 1)
        oled.show()

# Function to record data
def record(filename):    
    # Z axis acceleration data from the accelerometer
    g=round(imu.accel.z,2)*10
        
    # Update the detections list
    g_values.pop(0)
    g_values.append(abs(g))
    
    # If Z drop detected
    if z_diff():
        try:
            # Get the GPS data and timestamp
            t = my_gps.timestamp
            gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
            latitude = convert(my_gps.latitude)
            longitude = convert(my_gps.longitude)
            
            # Update the records dictionary
            if latitude != None and longitude != None:
                data_dict = {
                    "datetime": gpsTime,
                    "lat": latitude,
                    "long": longitude,
                    "type":1, # Z Drop
                    "g_value": g_values[9]
                    }
                records.append(data_dict)

                # Write the records to file
                to_write = str(records).replace("'", '"')
                with open(filename, "w") as file:
                    file.write(to_write)
                    file.close()
                print(to_write)
            
            # Feedback to the user
            leds[0] = (0,0,50)
            leds[1] = (0,0,50)
            leds.write()
            buzzer.freq(700)
            buzzer.duty_u16(1000)
            sleep(1)
            leds[0] = (0,0,0)
            leds[1] = (0,0,0)
            leds.write()
            buzzer.duty_u16(0)
        except:
            oled.fill(0)
            oled.text("ERROR!",10,25)
            oled.show()
            sleep(1)
    else:
        leds[0] = (50,0,0)
        leds[1] = (0,0,0)
        leds.write()

    # If a ramp with a slope > 20° is detected save the start and stop coordinates of the ramp
    a = get_angle()
    started = 0
    while a > 20:
        if(started == 0):
            started = 1
            write_arrow(80, 50)
            # Save start coordinates
            try:
                # Get the GPS data and timestamp
                t = my_gps.timestamp
                gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
                latitude = convert(my_gps.latitude)
                longitude = convert(my_gps.longitude)
                
                # Update the records dictionary
                if latitude != None and longitude != None:
                    data_dict = {
                        "datetime": gpsTime,
                        "lat": latitude,
                        "long": longitude,
                        "type": 2 # Ramp Start
                        }
                    records.append(data_dict)

                    # Write the records to file
                    to_write = str(records).replace("'", '"')
                    with open(filename, "w") as file:
                        file.write(to_write)
                        file.close()
                    print(to_write)

                # Feedback to the user
                leds[1] = (0,50,0)
                leds.write()
            except:
                oled.fill(0)
                oled.text("ERROR!",10,25)
                oled.show()
                time.sleep(1)
            
        a = get_angle()
    else:
        # Save stop coordinates
        if started == 1:
            try:
                # Get the GPS data and timestamp
                t = my_gps.timestamp
                gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
                latitude = convert(my_gps.latitude)
                longitude = convert(my_gps.longitude)
                
                # Update the records dictionary
                if latitude != None and longitude != None:
                    data_dict = {
                        "datetime": gpsTime,
                        "lat": latitude,
                        "long": longitude,
                        "type": 3 # Ramp Stop
                        }
                    records.append(data_dict)

                    # Write the records to file
                    to_write = str(records).replace("'", '"')
                    with open(filename, "w") as file:
                        file.write(to_write)
                        file.close()
                    print(to_write)

                # Feedback to the user
                leds[1] = (0,0,0)
                leds.write()
            except:
                oled.fill(0)
                oled.text("ERROR!",10,25)
                oled.show()
                time.sleep(1)
            started = 0

# Play a sound when the device is ready
buzzer.freq(700)
buzzer.duty_u16(1000)
leds[0] = (10,10,10)
leds[1] = (10,10,10)
leds.write()
sleep(0.3)
buzzer.freq(800)
buzzer.duty_u16(1000)
leds[0] = (0,0,0)
leds[1] = (0,0,0)
leds.write()
sleep(0.3)
buzzer.freq(900)
buzzer.duty_u16(1000)
leds[0] = (10,10,10)
leds[1] = (10,10,10)
leds.write()
sleep(0.3)
buzzer.duty_u16(0)
leds[0] = (0,0,0)
leds[1] = (0,0,0)
leds.write()

# Main loop
while True:
    # Read the GPS data
    length = gps_module.any()
    if length>0:
        b = gps_module.read(length)
        for x in b:
            msg = my_gps.update(chr(x))

    latitude = convert(my_gps.latitude)
    longitude = convert(my_gps.longitude)

    t = my_gps.timestamp
    # t[0] => hours : t[1] => minutes : t[2] => seconds
    gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
    
    # STATUS = 'MAIN' => Main menu with two options
    # STATUS = 'RECORD' => Record data and save it to a file
    # STATUS = 'SEND => Send records to the server

    # MAIN MENU
    if status == 'MAIN':
        oled.fill(0)
        oled.text("-> RECORD", 5,20)
        oled.text("-> SEND RECORDS", 5,50)
        if latitude != None and longitude != None:
            oled.text("GPS", 100,5)
        else:
            oled.text("-", 110,5)
        oled.show()

    # RECORDING
    elif status == 'RECORD':
        # Get the timestamp from the GPS
        t = my_gps.timestamp
        dt = my_gps.date_string(formatting="s_dmy")
        ts = '{:02d}-{:02d}'.format(t[0], t[1])
        # Create the filename
        if filename=="":
            filename = "records/record_"+dt+"_"+ts+".json"
        # Call the record function
        record(filename)
        oled.fill(0)

        # Display the data graph on the OLED
        for i in range(1,11):
            oled.text(".", (i*10)+4, 20-int(g_values[i-1]), 1)

        oled.text("> STOP", 5,45)
        if latitude != None and longitude != None:
            oled.text("GPS", 100,45)
        else:
            oled.text("-", 110,45)
        oled.show()

    # SEND RECORDS
    elif status == 'SEND':
        send()
        status = 'MAIN'
    
    # Buttons management
    if button1.value() == 0:
        if status == 'MAIN':
            # Wait for GPS
            while latitude == None and longitude == None:
                oled.fill(0)
                oled.text("Waiting GPS..", 5,20)
                oled.show()
                sleep(0.1)
            
            # Start recording
            records=[]
            status='RECORD'
        sleep(0.2)
            
    if button2.value() == 0:
        # Send records
        if status == 'MAIN':
            status='SEND'
        
        # Stop recording and save the file
        elif status == 'RECORD':
            # Turn leds off
            leds[0] = (0,0,0)
            leds[1] = (0,0,0)
            leds.write()
            # Append the filename to the records
            name = filename[8:]
            data_dict = { "name": name }
            records.append(data_dict)
            to_write = str(records).replace("'", '"')
            with open(filename, "w") as file:
                file.write(to_write)
                file.close()
                
            # Return to the main menu
            status='MAIN'
        sleep(0.2)