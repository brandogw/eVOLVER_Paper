import eVOLVER_module
import numpy as np

def test (OD_data, temp_data, vials, elapsed_time, exp_name):
    control = np.power(2,range(0,32))
    flow_rate = np.array([1.01,1.05,1.06,1.03,1.05,1.04,1.07,1.1,1.03,1.07,1.02,1,0.99,1.04,1.05,1])#ml/sec
    volume =  30 #mL
    lower_thresh = np.array([0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,9999,9999,9999,9999])
    upper_thresh = np.array([0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,9999,9999,9999,9999])
    time_out =20
    pump_wait = 7; #wait between pumps (min)
    for x in vials:
        if OD_data[x] > upper_thresh[x]:
            time_in = - (np.log(lower_thresh[x]/upper_thresh[x])*volume)/flow_rate[x]
            MESSAGE = "%s,0,%d," % ("{0:b}".format(control[x]+control[x+16]) , time_in)
            eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
            MESSAGE = "%s,0,%d," % ("{0:b}".format(control[x+16]) , time_out)
            eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_out,'y')

