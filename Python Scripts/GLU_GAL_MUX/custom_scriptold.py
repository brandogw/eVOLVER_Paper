import eVOLVER_module
import numpy as np
import os.path

##### CM edit 1/31/2017 for multiplexer inputs

# Valve Descriptors
# 0 no valves open
# 1 valve 1 : vials 0-7 selector 
# 2 valve 2 : vials 8-15 selector
# 4 valve 3 : media tier 1a
# 8 valve 4 : media tier 1b
# 16 valve 5 : media tier 2a
# 32 valve 6 : media tier 2b
# 64 valve 7 : media tier 3a
# 128 valve 8 : media tier 3b
# 256 valve 9 : demux tier 1a
# 512 valve 10 : demux tier 1b
# 1024 valve 11 : demux tier 2a
# 2048 valve 12 : demux tier 2b
# 4096 valve 13 : demux tier 3a
# 8192 valve 14 : demux tier 3b
# 16384 valve 15 : vial influx
# 32768 valve 16 : bridge 
# 65536 valve 17 : vial efflux
# 131072 valve 18 : mux tier 1a
# 262144 valve 19 : mux tier 1b
# 524288 valve 20 : mux tier 2a
# 1048576 valve 21 : mux tier 2b
# 2097152 valve 22 : mux tier 3a
# 4194304 valve 23 : mux tier 3b
# 8388608 valve 24 : FREE

# Path arrays:
binvals = np.power(2,range(0,31))
binvals = np.insert(binvals,0,0)

media = [[3,5,7],[3,5,8],[3,6,7],[3,6,8],[4,5,7],[4,5,8],[4,6,7],[4,6,8]]
demux = [[1,9,11,13],[1,9,11,14],[1,9,12,13],[1,9,12,14],[1,10,11,13],[1,10,11,14],[1,10,12,13],[1,10,12,14],[2,9,11,13],[2,9,11,14],[2,9,12,13],[2,9,12,14],[2,10,11,13],[2,10,11,14],[2,10,12,13],[2,10,12,14]]
mux = [[1,18,20,22],[1,18,20,23],[1,18,21,22],[1,18,21,23],[1,19,20,22],[1,19,20,23],[1,19,21,22],[1,19,21,23],[2,18,20,22],[2,18,20,23],[2,18,21,22],[2,18,21,23],[2,19,20,22],[2,19,20,23],[2,19,21,22],[2,19,21,23]]

influx = [15]
bridge = [16]
efflux = [17]
peri = [25]

# 1,2,3 glucose 4,5,6 galactose 7 no sugar
mixture = np.array(np.mat('1 7; 1 4; 1 5; 1 6; 2 7; 2 4; 2 5; 2 6; 3 7; 3 4; 3 5; 3 6; 7 7; 7 4; 7 5; 7 6'))



def valving (mux_command, vial_num = 0, media_type = 0, step_size = 5000, vials = range(0,16), x=1, elapsed_time = 99999, pump_wait = 1, exp_name = 'mux_test1', time_in = 1, wash = 10, preflush = 2000, logging = 'n'):

    ## translates mux_command (formatted as string) to valving scheme
    if mux_command == 'syringe':
        y=vial_num

        #preflush with air
        path = list(set(media[0]))
        bin_path = format(sum([binvals[i] for i in path]),'032b')
        MESSAGE = "%s,0,%d," % (bin_path , preflush)
        eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
        #print(MESSAGE)

        #draw & dispense media
        path = list(set(media[media_type]))
        bin_path = format(sum([binvals[i] for i in path]),'032b')
        MESSAGE = "%s,0,%d," % (bin_path , step_size)
        eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
        #print(MESSAGE)

        path = list(set(demux[y] + influx + efflux + mux[y] + peri))
        bin_path = format(sum([binvals[i] for i in path]),'032b')
        MESSAGE = "%s,0,%d," % (bin_path , (-1*step_size) - preflush)
        eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
        #print(MESSAGE)      

    if mux_command == 'flush': #set vials in function call in order to not wash all lines, otherwise range(0,16)

        for y in vials: #wash using peristaltic
            path = list(set(media[media_type] + demux[y] + mux[y] + bridge + peri))
            bin_path = format(sum([binvals[i] for i in path]),'032b')
            MESSAGE = "%s,1,%d," % (bin_path , wash)
            eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
            #print(MESSAGE)

    if mux_command == 'efflux': #set vials in function call in order to not clear all efflux lines, otherwise range(0,16)
        for y in vials:
            path = list(set(mux[y] + efflux + peri))
            bin_path = format(sum([binvals[i] for i in path]),'032b')
            MESSAGE = "%s,1,%d," % (bin_path , wash)
            eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, logging)
            #print(MESSAGE)


def pump(vial_num, media_type, step_size, logging = 'y', x = 1, elapsed_time = 99999, pump_wait = 1, exp_name = 'mux_test1', time_in = 1): #use to combine commands for most common event
    valving('flush', vials = [vial_num], media_type = 7, x=x, elapsed_time = elapsed_time, pump_wait = pump_wait, exp_name = exp_name, time_in = time_in)
    valving('syringe',vial_num,media_type,step_size, logging = logging, x=x, elapsed_time = elapsed_time, pump_wait = pump_wait, exp_name = exp_name, time_in = time_in)
    valving('efflux',vials = [vial_num], wash = 3, x=x, elapsed_time = elapsed_time, pump_wait = pump_wait, exp_name = exp_name, time_in = time_in, logging = logging)


def test (OD_data, temp_data, vials, elapsed_time, exp_name):
    MESSAGE = "8,8,8,8,8,8,8,8,14,8,8,14,8,8,8,8,"
    eVOLVER_module.stir_rate(MESSAGE)
    
    control = np.power(2,range(0,32))
    #flow_rate = np.array([1.11,1.11,1.1,1.08,1.1,1.12,1.04,1.1,1.13,1.12,0.93,1.1,1.1,1.17,1.07,1.1])#ml/sec
    volume =  30#mL

    lower_thresh = np.array([.25,0.25,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999])
    upper_thresh = np.array([.3,0.3,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999])

    
    time_out =5
    pump_wait = 3; #wait between pumps (min)

    save_path = os.path.dirname(os.path.realpath(__file__))

    for x in vials:
        ODset_path =  "%s/%s/ODset/vial%d_ODset.txt" % (save_path,exp_name,x)
        data = np.genfromtxt(ODset_path, delimiter=',')
        ODset = data[len(data)-1][1]


        OD_path =  "%s/%s/OD/vial%d_OD.txt" % (save_path,exp_name,x)
        data = np.genfromtxt(OD_path, delimiter=',')
        average_OD = 0

        if len(data) > 15:
            for n in range(1,6):
                average_OD = average_OD + (data[len(data)-n][1]/5)


            if (average_OD > upper_thresh[x]) and (ODset != lower_thresh[x]):
                text_file = open(ODset_path,"a+")
                text_file.write("%f,%s\n" %  (elapsed_time, lower_thresh[x]))
                text_file.close()
                ODset = lower_thresh[x]

            if (average_OD < (lower_thresh[x] + 0.005)) and (ODset != upper_thresh[x]):
                text_file = open(ODset_path,"a+")
                text_file.write("%f,%s\n" %  (elapsed_time, upper_thresh[x]))
                text_file.close()
                ODset = upper_thresh[x]

            if average_OD > ODset:
                time_in = 0
                step_size = (((-1)*np.log(lower_thresh[x]/average_OD)*volume)+2.25)/(0.002)

                if step_size > 5000:
                    step_size = 5000

                # send command to syringe pump 
                pump(vial_num = x, media_type = 1, step_size = step_size, logging = 'y', x=x, elapsed_time = elapsed_time, pump_wait = pump_wait, exp_name = exp_name, time_in = time_in)

                





