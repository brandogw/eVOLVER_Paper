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

x=1 #why is this needed?
elapsed_time=99999 #ensures fluidic commands not stopped by timing
pump_wait=1 #ensures fluidic commands not stopped by timing
exp_name='mux_test1' #match with main_eVOLVER.py
time_in=1 #also not needed


eVOLVER_module.fluid_command('clear', x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
exp_continue = raw_input('Conduct pump test (y/n): ')
while exp_continue == 'y':
	custom_script.pump(3,[7],[5000], logging = 'n')
	print('Testing...')
	exp_continue = raw_input('Conduct test again(y/n): ')

exp_continue = raw_input('Conduct pump test with precleaning (y/n): ')
while exp_continue == 'y':
	custom_script.precleaned_pump(3,[7],[5000], logging = 'n')
	print('Testing...')
	exp_continue = raw_input('Conduct test again(y/n): ')

exp_continue = raw_input('Conduct wash (y/n): ')
while exp_continue == 'y':
	custom_script.valving('flush',vials=[3],media_type=[7])
	print('Washing...')
	exp_continue = raw_input('Conduct wash (y/n): ')

exp_continue = raw_input('Conduct efflux (y/n): ')
while exp_continue == 'y':
	custom_script.valving('efflux')
	print('Washing...')
	exp_continue = raw_input('Conduct efflux (y/n): ')


