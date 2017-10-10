import socket
import os.path
import shutil
import time
import pickle
import numpy as np
import numpy.matlib
import requests

import eVOLVER_module
import custom_script

def dilute(media_type, step_size, vial):
    MESSAGE = "dilute,%d,%d,0,%d,3,5,0,0,0," % (media_type, step_size, vial)
    clean_commands(MESSAGE)
    print(MESSAGE)

def dilutemix(media1_type, step_size1, media2_type, step_size2, vial):
    MESSAGE = "dilutemix,%d,%d,%d,%d,0,%d,3,5,0," % (media1_type, step_size1, media2_type, step_size2, vial)
    clean_commands(MESSAGE)
    print(MESSAGE)

def cleanML (): 
    MESSAGE = "cleanML,5,0,0,0,0,0,0,0,0,"
    clean_commands(MESSAGE)
    print(MESSAGE)

def washHM (): 
    MESSAGE = "washHM,0,0,0,0,0,0,0,0,0,"
    clean_commands(MESSAGE)
    print(MESSAGE)

def cleanVL (): 
    MESSAGE = "cleanVL,5,0,0,0,0,0,0,0,0,"
    clean_commands(MESSAGE)
    print(MESSAGE)

def cleanDev (): 
    MESSAGE = "cleanDev,7000,700,1,0,0,0,0,0,0,"
    clean_commands(MESSAGE)
    print(MESSAGE)

def washLines (): 
    MESSAGE = "washLines,3000,700,5,0,0,0,0,0,0,"
    clean_commands(MESSAGE)
    print(MESSAGE)

def vial2vial(media_type, step_size, prime_size, vial_out, vial_in):
    MESSAGE = "v2v,%d,%d,%d,%d,%d,100,5,2000,0," % (media_type, step_size, prime_size, vial_out, vial_in)
    clean_commands(MESSAGE)
    print(MESSAGE)

def vial2vial_2x(media_type, step_size, prime_size, vial_out, vial_in1, vial_in2):
    MESSAGE = "v2v_2x,%d,%d,%d,%d,%d,%d,100,5,2000," % (media_type, step_size, prime_size, vial_out, vial_in1, vial_in2)
    clean_commands(MESSAGE)
    print(MESSAGE)    

def clean_commands(MESSAGE):
    IP = "10.241.24.11"
    PORT = 5556
    save_path = os.path.dirname(os.path.realpath(__file__))
    data = {
        'values':[MESSAGE]
    }
    try:
        r = requests.post('http://' + str(IP) + ':' + str(PORT) + '/updateFluidics/', json = data, timeout = 10)

    except requests.exceptions.RequestException as e:
        print "Fluidics Connection Error"

def clearCommands (): 
    MESSAGE = "clear"
    clean_commands(MESSAGE)
    print(MESSAGE)

if __name__ == '__main__':
    clearCommands()

    ##### DO vial to vial transfers to vial 14 to make diploids
    ##vial2vial(media_type, step_size, prime_size, vial_out, vial_in)
    exp_continue = raw_input('Do vial to vial transfer from vial 0 to vial 14? (y/n): ')
    while exp_continue == 'y':
        vial2vial(0, 2000, 0, 0, 14)
        exp_continue = raw_input('v0 to v14 again? (y/n): ')


    exp_continue = raw_input('Do vial to vial transfer from vial 1 to vial 14? (y/n): ')
    while exp_continue == 'y':
        vial2vial(0, 2000, 0, 1, 14)
        exp_continue = raw_input('v1 to v14 again? (y/n): ')


    volume = 35
    media_amount = raw_input('Calculate stepsize: How much media do you want to put in (mL)?')
    step_size = (media_amount+.1)/(.0009)
    print step_size


    exp_continue = raw_input('Meter media 4 (20x chx) to vial 0 (y/n): ')
    while exp_continue == 'y':
        dilute(4, step_size, 0)
        exp_continue = raw_input('20x chx to v0? (y/n) again?: ')

    exp_continue = raw_input('Meter media 5 (20x keto) to vial 1 (y/n): ')
    while exp_continue == 'y':
        dilute(5, step_size, 1)
        exp_continue = raw_input('20x keto to v1 again?? (y/n): ')

    exp_continue = raw_input('Meter media 7 (20x chx + 20x keto) to vial 15 (y/n): ')
    while exp_continue == 'y':
        dilute(7, step_size, 15)
        exp_continue = raw_input('20x chx + 20x keto to v15 again? (y/n): ')














