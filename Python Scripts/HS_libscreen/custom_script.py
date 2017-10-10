import eVOLVER_module
import numpy as np
import os.path




def test (OD_data, temp_data, vials, elapsed_time, exp_name):
    MESSAGE = "8,8,8,8,8,8,8,8,14,8,8,14,8,8,8,8,"
    eVOLVER_module.stir_rate(MESSAGE)
    
    control = np.power(2,range(0,32))
    flow_rate = np.array([1.11,1.11,1.1,1.08,1.1,1.12,1.04,1.1,1.13,1.12,0.93,1.1,1.1,1.17,1.07,1.1])#ml/sec
    volume =  30#mL

    lower_thresh = np.array([.17,.17,.17,.17,.17,.17,.17,.17,.17,.17,.17,.17,.17,.17,.17,.17])
    upper_thresh = np.array([.2,.2,.2,.2,.2,.2,.2,.2,.2,.2,.2,.2,.2,.2,.2,.2])

    heat_shockdelay = 5.5 #hours
    normal_temp = 30.0 #degrees C
    temp_mag = np.array([30,33,33,33,36,36,36,36,39,39,39,39,42,42,42,42])
    temp_period = np.array([9999,2,6,48,9999,2,6,48,9999,2,6,48,9999,2,6,48])

    #temp_mag = np.array([42,42,42,42,39,39,39,39,36,36,36,36,33,33,33,30])
    #temp_period = np.array([2,6,48,9999,2,6,48,9999,2,6,48,9999,2,6,48,9999])
    
    
    time_out =5
    pump_wait = 3; #wait between pumps (min)

    save_path = os.path.dirname(os.path.realpath(__file__))

    for x in vials:
        if elapsed_time > heat_shockdelay:
            tempconfig_path =  "%s/%s/temp_config/vial%d_tempconfig.txt" % (save_path,exp_name,x)
            temp_config = np.genfromtxt(tempconfig_path, delimiter=',')
            last_tempset = temp_config[len(temp_config)-1][0]

            if (len(temp_config) is 2):
                text_file = open(tempconfig_path,"a+")
                text_file.write("%f,%s\n" %  (elapsed_time, temp_mag[x]))
                text_file.close()

            if ((elapsed_time - last_tempset) > (float(temp_period[x])/2)):
                text_file = open(tempconfig_path,"a+")
                if (len(temp_config) % 2 == 0):
                    text_file.write("%f,%s\n" %  (elapsed_time, temp_mag[x]))
                else:
                    text_file.write("%f,%s\n" %  (elapsed_time, normal_temp))
                text_file.close()

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

                time_in = - (np.log(lower_thresh[x]/average_OD)*volume)/flow_rate[x]

                if time_in > 20:
                    time_in = 20


                MESSAGE = "%s,0,%d," % ("{0:b}".format(control[x]+control[x+16]) , time_in)
                eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
                MESSAGE = "%s,0,%d," % ("{0:b}".format(control[x+16]) , time_out)
                #eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_out,'n')
                eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_out,'y')

