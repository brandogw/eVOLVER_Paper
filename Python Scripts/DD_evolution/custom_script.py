import eVOLVER_module
import numpy as np
import os.path




def test (OD_data, temp_data, vials, elapsed_time, exp_name):
    MESSAGE = "15,15,15,15,15,15,15,15,15,15,15,15,15,15,12,15,"
    eVOLVER_module.stir_rate(MESSAGE)
        
    control = np.power(2,range(0,32))
    flow_rate = np.array([1.07,1,1.15,1.05,0.96,1.11,1.18,1.01,1.07,1.04,1.1,1.03,1.1,1.1,0.95,1.07])#ml/sec
    volume =  15 #mL

    lower_thresh = np.array([0.05, 0.05,9999999,0.1,0.05,9999999,0.1,9999999,0.15,0.05,0.1,0.15,0.2,0.05,0.1,0.15])
    upper_thresh = np.array([0.1,0.15,9999999,0.15,0.2,9999999,0.2,9999999,0.2,0.25,0.25,0.25,0.25,0.3,0.3,0.3])

    #lower_thresh = np.array([.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05,.05])
    #upper_thresh = np.array([.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1])
    #lower_thresh = np.array([.6,.6,.6,.6,.6,.6,.6,.6,.6,.6,.6,.6,.6,.6,.6,.6])
    #upper_thresh = np.array([.65,.65,.65,.65,.65,.65,.65,.65,.65,.65,.65,.65,.65,.65,.65,.65])
    time_out =5
    pump_wait = 2; #wait between pumps (min)

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

                time_in = - (np.log((lower_thresh[x]-0.005)/average_OD)*volume)/flow_rate[x]

                if time_in > 30:
                    time_in = 30


                MESSAGE = "%s,0,%d," % ("{0:b}".format(control[x]+control[x+16]) , time_in)
                eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_in, 'n')
                MESSAGE = "%s,0,%d," % ("{0:b}".format(control[x+16]) , time_out)
                #eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_out,'n')
                eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_out,'y')
