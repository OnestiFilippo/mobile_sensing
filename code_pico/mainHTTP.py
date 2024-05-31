from machine import Pin, SoftI2C, I2C, PWM, UART
import ssd1306
from time import sleep
from imu import MPU6050
import neopixel
import network
import secrets
import urequests
import ujson
from micropyGPS import MicropyGPS
import os

# MPU6050
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
imu = MPU6050(i2c)

# NEOPIXEL
leds = neopixel.NeoPixel(machine.Pin(21), 2)

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

status = 0

axis = 'X'
z_thresh_value = 100
z_diff_value = 100

records = []
g_values = [0]*10

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

def send():
    if len(os.listdir("/records")) != 0:
        oled.fill(0)
        oled.text("Connecting to", 5,10)
        oled.text("WiFi..", 5,20)
        oled.show()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True) # power up the WiFi chip
        sleep(5) # wait three seconds for the chip to power up and initialize
        wlan.connect(secrets.SSID, secrets.PASSWORD)
        sleep(4)
        if wlan.isconnected():
            oled.fill(0)
            oled.text("Connected!", 5,10)
            oled.show()
            sleep(2)
        for filename in os.listdir("/records"):
            print(filename)
            with open("records/"+filename, "r") as file:
                records_file = file.read()
        
            if records_file:
                if wlan.isconnected():
                    oled.fill(0)
                    oled.text("Sending", 5,20)
                    oled.text(filename, 5,40)
                    oled.show()
                    print(records_file)
                    url = 'http://filippoonesti.ovh:83/mobile_sensing.php'
                    res = urequests.post(url, headers = {'Content-Type': 'application/json'}, data = records_file)
                    sleep(2)
                    print(res.status_code)
                    if res.status_code == 200:
                        oled.fill(0)
                        oled.text("Successfully", 5,10)
                        oled.text("sent!", 5,20)
                        oled.show()
                    else:
                        oled.fill(0)
                        oled.text("Error while", 5,10)
                        oled.text("sending!", 5,20)
                        oled.show()
                    sleep(3)
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

def z_thresh(g):
    print(g[9])
    if g[9] > z_thresh_value:
        return True
    else:
        return False
    
def z_diff(g):
    print(abs(g[9]-g[8]))
    if abs(g[9]-g[8]) > z_diff_value:
        return True
    else:
        return False

def record():    
    if axis == 'X':
        g=round(imu.gyro.x)
    elif axis == 'Y':
        g=round(imu.gyro.y)
    elif axis == 'Z':
        g=round(imu.gyro.z)
        
    g_values.pop(0)
    g_values.append(abs(g))
    
    #print("g",axis, " : ", g," ",end="\r")
    
    if z_thresh(g_values):
        try:
            t = my_gps.timestamp
            dt = my_gps.date_string(formatting="s_dmy")
            ts = '{:02d}-{:02d}'.format(t[0], t[1])
            #t[0] => hours : t[1] => minutes : t[2] => seconds
            gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
            latitude = convert(my_gps.latitude)
            longitude = convert(my_gps.longitude)
            if latitude != None and longitude != None:
                data_dict = {
                    "datetime": gpsTime,
                    "lat": latitude,
                    "long": longitude,
                    "g_value": g_values[9]
                    }
                records.append(data_dict)
                filename = "records/record_"+dt+"_"+ts+".json"
                to_write = str(records).replace("'", '"')
                with open(filename, "w") as file:
                    file.write(to_write)
                    file.close()
                print(to_write)
            leds[1] = (0,0,50)
            leds.write()
            buzzer.freq(700)
            buzzer.duty_u16(1000)
            sleep(1)
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

while True:
    length = gps_module.any()
    if length>0:
        b = gps_module.read(length)
        for x in b:
            msg = my_gps.update(chr(x))

    latitude = convert(my_gps.latitude)
    longitude = convert(my_gps.longitude)

    t = my_gps.timestamp
    #t[0] => hours : t[1] => minutes : t[2] => seconds
    gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
    
    # STATUS
    if status == 0:
        oled.fill(0)
        oled.text("-> RECORD", 5,20)
        oled.text("-> SEND RECORDS", 5,50)
        if latitude != None and latitude != None:
            oled.text("GPS", 100,5)
        else:
            oled.text("-", 110,5)
        oled.show()
        leds[0] = (10,10,10)
        leds[1] = (10,10,10)
        leds.write()
    elif status == 1:
        record()
        oled.fill(0)
        #oled.text("RECORDING..", 20,10)
        for i in range(1,11):
            oled.text(".", (i*10)+4, 20-int(g_values[i-1]/10), 1)
            print(int(g_values[i-1]/10))
        oled.text("> STOP", 5,45)
        if latitude != None and latitude != None:
            oled.text("GPS", 100,45)
        else:
            oled.text("-", 110,45)
        oled.show()
    elif status == 2:
        send()
        status = 0
    
    # BUTTON PRESSED 
    if button1.value() == 0:
        if status == 0:
            while latitude == None and latitude == None:
                oled.fill(0)
                oled.text("Waiting GPS..", 5,20)
                oled.show()
                sleep(0.1)
            
            records=[]
            status=1
        sleep(0.2)
            
    if button2.value() == 0:
        if status == 0:
            status=2
        elif status == 1:
            t = my_gps.timestamp
            dt = my_gps.date_string(formatting="s_dmy")
            ts = '{:02d}-{:02d}'.format(t[0], t[1])
            filename = "records/record_"+dt+"_"+ts+".json"
            name = "record_"+dt+"_"+ts+".json"
            data_dict = { "name": name }
            records.append(data_dict)
            to_write = str(records).replace("'", '"')
            with open(filename, "w") as file:
                file.write(to_write)
                file.close()
            status=0
        sleep(0.2)
             
    sleep(0.1)

