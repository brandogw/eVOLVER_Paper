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

#valving (mux_command, vial_num = 0, media_type = 0, step_size = 5000, vials = range(0,16), x=1, elapsed_time = 99999, pump_wait = 1, exp_name = 'mux_test1', time_in = 1):

x=1 #why is this needed?
elapsed_time=99999 #ensures fluidic commands not stopped by timing
pump_wait=1 #ensures fluidic commands not stopped by timing
exp_name='mux_test1' #match with main_eVOLVER.py
time_in=1 #also not needed


#values to be changed
washtime = 10 # approx. n mL liquid per wash step, + syringe cleaning volume
syringevolume = 5000 #amount of cleaning to do on syringe

eVOLVER_module.fluid_command('clear', x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')


exp_continue = raw_input('Sterilize media lines, influx lines, and efflux lines ~30 mins (y/n): ')
while exp_continue == 'y':
    #sterilize media lines using syringe pump, dispense through two vial influx lines
    for j in range(0,8):
        custom_script.pump(j,[j],[syringevolume], logging = 'n')
        custom_script.pump(j+8,[j],[syringevolume], logging = 'n')
    exp_continue = raw_input('Want to sterilize media lines, influx lines, and efflux lines again? (y/n): ')

exp_continue = raw_input('Flush all media lines? [hook up media bottles] ~2 mins (y/n): ')
while exp_continue == 'y':
    #flush media lines using syringe pump, dispense through two vial influx lines
    for j in range(0,8):
        custom_script.valving('flush',vials = [0], media_type = [j]) #pull media from each media type (ends with wash fluid)
    exp_continue = raw_input('Want to flush media lines again? (y/n): ')

exp_continue = raw_input('Flush all influx/efflux lines with wash fluid and air? [keep influx and efflux in same container] ~30 mins (y/n): ')
while exp_continue == 'y':
    for k in range(0,16):
        custom_script.valving('syringe',k,[7],preflush = 4000) #syringe pump each influx line with wash fluid, flush with large air preflush
        custom_script.valving('efflux',vials = [k],logging='n')
    exp_continue = raw_input('Want to flush influx/efflux lines again? (y/n): ')

print('It is now safe to hook up vials.')

