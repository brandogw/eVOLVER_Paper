#!/usr/bin/python

import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.GPIO as GPIO
import serial, time, os.path, struct, fcntl, os, zlib

##Set up Connection
UART.setup("UART4")
GPIO.setup("P9_15", GPIO.OUT)
GPIO.output("P9_15", GPIO.HIGH)
GPIO.setup("P8_33", GPIO.OUT)
GPIO.output("P8_33", GPIO.LOW)
ser = serial.Serial(port = "/dev/ttyO4", baudrate=9600, timeout = 3)
ser.flushInput()
ser.flushOutput()

#SETUP FILE LOCATIONS
save_path = '/root/'

#Config Files
Fan_Name = os.path.join(save_path, "fan_config.txt")
Temp_Name = os.path.join(save_path, "temp_config.txt")
OD_Name = os.path.join(save_path, "OD_config.txt")
Fluid_Name = os.path.join(save_path, "fluid_config.txt")
Pause_Name = os.path.join(save_path, "paused.txt")
#Data Files
Temp_Data = os.path.join(save_path, "temp_data.txt")
OD_Data = os.path.join(save_path, "OD_data.txt")

ser.close()


def read_text(file_name, address, end):
        config = open(file_name,"r")
        lines = config.readlines()
        #print lines
        for eachLine in lines:
                line  = eachLine.strip()
                output = address + eachLine[:len(eachLine)-1]+ end
                return output


def readfluidic_text(file_name, address, end):
        config = open(file_name,"r")
        lines = config.readlines()
        for eachLine in lines:
                line  = eachLine.strip()
                output = line.split(',')
                return output

def Arduino_Send(output,empty):
        if (output is None) or (len(output) == 0):
                print "Config Empty"
        else:
                ser.open()
                GPIO.output("P9_15", GPIO.HIGH)
#               print "Serial is open!"
                print output
                ser.write(output)
                time.sleep(.05)
                ser.close()
                GPIO.output("P9_15", GPIO.LOW)

def Fluidic_status(address):
        ser.open()
        GPIO.output("P9_15", GPIO.HIGH)
        ser.write(address)
        print address
        ser.close()

        GPIO.output("P9_15", GPIO.LOW)
        ser.open()
#        time.sleep(.5)
        response =  ser.readline()
        ser.close()
        print response
        if 'ready' in response:
                return 1

def Arduino_Input(data_name, address, msg_rcv, msg_repeat,time_repeat):
        GPIO.output("P9_15", GPIO.LOW)
        ser.open()
#        time.sleep(3)
        response =  ser.readline()
        ser.close()
        print response
        if response[:4] == address and response[-3:] == 'end':
                print "Response:", response[4:-3]
                log = open(data_name, "w")
                log.write(response[4:-3])

def delete_line(file_name):
        with open(file_name, 'r') as fin:
                data = fin.read().splitlines(True)
        with open(file_name, 'w') as fout:
                fout.writelines(data[1:])

def Arduino_Fluidic(file_name, address, ending, status_check, empty):
        if (Fluidic_status(status_check)):
                print "Sending Fluidic Command..."
                config = read_text(file_name,address,ending)
                time.sleep(.5)
                Arduino_Send(config, empty)
                time.sleep(.1)
                delete_line(file_name)
        else:
                print "Arduino Busy!"
        time.sleep(1)

def Arduino_Temperature(file_name, address, ending, repeat_msg, msg_recieved, e$
        print "Sending Temperature Commands..."
        config = read_text(file_name,address,ending)
#       time.sleep(.1)
        Arduino_Send(config, empty)
#        time.sleep(.1)
        Arduino_Input(Temp_Data,'temp',msg_recieved,repeat_msg, 0)
        time.sleep(1)

def Arduino_OD(file_name, address, ending, repeat_msg, msg_recieved, empty):
        print "Getting OD Measurements..."
        config = read_text(file_name,address,ending)
        time.sleep(.1)
        Arduino_Send(config, empty)
        time.sleep(.1)
        Arduino_Input(OD_Data,'turb',msg_recieved,repeat_msg, 0)
        time.sleep(5)

def Arduino_Stir(file_name, address, ending, empty):
        print "Getting Stir Settings..."
        config = read_text(file_name,address,ending)
        time.sleep(.1)
        Arduino_Send(config, empty)
        time.sleep(.1)

while (1):
        Arduino_Fluidic(Fluid_Name, 'st', ' !', 're !','nc !')

        Arduino_Stir(Fan_Name, 'zv',' !','wq !')
        Arduino_Temperature(Temp_Name,'xr',' !','pf !','qe !','em !')
        Arduino_Temperature(Temp_Name,'xr',' !','pf !','qe !','em !')

#       Arduino_Fluidic(Fluid_Name, 'st', ' !', 're !','nc !')
#        Arduino_Stir(Fan_Name, 'zv',' !','wq !')

        Arduino_OD(OD_Name, 'we',' !','oq !','tr !','cd !')

#       Arduino_Stir(Fan_Name, 'zv',' !','wq !')




