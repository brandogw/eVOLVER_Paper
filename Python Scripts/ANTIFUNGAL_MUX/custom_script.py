import eVOLVER_module
import numpy as np
import os.path




def test (OD_data, temp_data, vials, elapsed_time, exp_name):

    ### Set Stir Rate
    #### Message Stir Rates
    MESSAGE = ""
    for x in vials:
        stir_rate_path =  "%s/%s/stir_rate/vial%d_stir_rate.txt" % (save_path,exp_name,x)
        data = np.genfromtxt(stir_rate_path, delimiter=',')
        stir_set = data[len(data)-1][1]
        MESSAGE += str(stir_set)
        MESSAGE += ","

    eVOLVER_module.stir_rate(MESSAGE)

    
    control = np.power(2,range(0,32))
    #flow_rate = np.array([1.11,1.11,1.1,1.08,1.1,1.12,1.04,1.1,1.13,1.12,0.93,1.1,1.1,1.17,1.07,1.1])#ml/sec
    volume =  35#mL

    #lower_thresh = np.array([.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25])
    #upper_thresh = np.array([.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3,.3])

    lower_thresh = np.array([.25,.25,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999])
    upper_thresh = np.array([.3,.3,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999])


    
    time_out =5
    pump_wait = 10; #wait between pumps (min)

    save_path = os.path.dirname(os.path.realpath(__file__))

    drug_dose_start = 10 #hours
    vial2vial_timeThresh = 14 #hours

    #### Change media based on before or after drug dose
    if elapsed_time > drug_dose_start:
        media = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    else:
        media = np.array([1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

        #media 0- YPD
        #media 1- YPD + chx
        #media 2- YPD + keto
        #media 3- YPD + chx + keto
        #media 4- YPD + 20x chx
        #media 5- YPD + 20x keto
        #media 7- YPD + 20x keto + 20x chx


    ###### Make decision to dilute or not ################

    for x in vials:
        ODset_path =  "%s/%s/ODset/vial%d_ODset.txt" % (save_path,exp_name,x)
        data = np.genfromtxt(ODset_path, delimiter=',')
        ODset = data[len(data)-1][1]


        OD_path =  "%s/%s/OD/vial%d_OD.txt" % (save_path,exp_name,x)
        data = np.genfromtxt(OD_path, delimiter=',')
        average_OD = 0

        if len(data) > 15:
            ## Averages last 5 data points
            for n in range(1,6):
                average_OD = average_OD + (data[len(data)-n][1]/5)

            ######### Set OD thresholds ########

            #### Set to lower target growth rate for dilutions
            if (average_OD > upper_thresh[x]) and (ODset != lower_thresh[x]):
                text_file = open(ODset_path,"a+")
                text_file.write("%f,%s\n" %  (elapsed_time, lower_thresh[x]))
                text_file.close()
                ODset = lower_thresh[x]

                ########## Measure and record growth rate when hits OD threshold###########
                growth_rate = measure_growthRate(x, save_path, exp_name)
                growth_rate_path =  "%s/%s/growth_rate/vial%d_growth_rate.txt" % (save_path,exp_name,x)
                text_file = open(growth_rate_path,"a+")
                text_file.write("%f,%s\n" %  (elapsed_time, growth_rate))
                text_file.close()

            if (average_OD < (lower_thresh[x] + 0.005)) and (ODset != upper_thresh[x]):
                text_file = open(ODset_path,"a+")
                text_file.write("%f,%s\n" %  (elapsed_time, upper_thresh[x]))
                text_file.close()
                ODset = upper_thresh[x]

            ### Average last three growth rates ######
            growth_rate_path =  "%s/%s/growth_rate/vial%d_growth_rate.txt" % (save_path,exp_name,x)
            rate_data = np.genfromtxt(growth_rate_path, delimiter=',')
            average_rate = 0
            num_averaged = 3
            if len(rate_data) > num_averaged:
                for n in range(1,num_averaged+1):
                    average_rate = average_rate + (rate_data[len(rate_data)-n][1]/num_averaged)

            ##### Make decision on growth rates #####
            if elapsed_time > vial2vial_timeThresh:
                rate_thresholds = np.array(np.mat('0 99999; 1 99999; 0 99999; 1 99999')) ## [vial_output, growth_rate threshold]
                next_vial_0 = np.array(np.mat('2 4; 5 7; 8 10; 11 13'))
                next_vail_1 = np.array(np.mat('3 4; 6 7; 9 10; 12 13')) ## ['vial_in1, vial_in2']
                for n in range(0,len(rate_thresholds)):
                    if x == rate_thresholds[n][0]: ## checks to see if correct vial output
                        if average_rate > rate_thresholds[n][1]: ## check to see what the rate threshold is

                            rate_thresh_path =  "%s/%s/rate_thresh/vial%d_rate_thresh.txt" % (save_path,exp_name,x)
                            data = np.genfromtxt(rate_thresh_path, delimiter=',')
                            last_rate_thresh = data[len(data)-1][1]

                            if rate_thresholds[n][1] > last_rate_thresh:

                                rate_thresh_path =  "%s/%s/rate_thresh/vial%d_rate_thresh.txt" % (save_path,exp_name,x)
                                text_file = open(rate_thresh_path,"a+")
                                text_file.write("%f,%s\n" %  (elapsed_time, rate_thresholds[n][1]))
                                text_file.close()

                                ## media, vialOut, vialIn1, vialIn2
                                MESSAGE = "v2v_2x,%d,2000,0,%d,%d,%d,100,5,2000," % (media[0], 0, next_vial_0[n][0], next_vial_0[n][1]) 
                                eVOLVER_module.fluid_command(MESSAGE, 0, elapsed_time, pump_wait *60, exp_name, time_out,'y')

                                ODset_path =  "%s/%s/ODset/vial%d_ODset.txt" % (save_path,exp_name,0)
                                text_file = open(ODset_path,"a+")
                                text_file.write("%f,%s\n" %  (elapsed_time, upper_thresh[0]))
                                text_file.close()

                                ## media, vialOut, vialIn1, vialIn2
                                MESSAGE = "v2v_2x,%d,2000,0,%d,%d,%d,100,5,2000," % (media[1], 1, next_vial_1[n][0], next_vial_1[n][1])
                                eVOLVER_module.fluid_command(MESSAGE, 1, elapsed_time, pump_wait *60, exp_name, time_out,'y') 

                                ODset_path =  "%s/%s/ODset/vial%d_ODset.txt" % (save_path,exp_name,1)
                                text_file = open(ODset_path,"a+")
                                text_file.write("%f,%s\n" %  (elapsed_time, upper_thresh[1]))
                                text_file.close()


            #### Make decision for stir rates if above a certain density then change stir rate
            stir_thresh = .8
            if average_OD > stir_thresh:
                
                stir_rate_path =  "%s/%s/stir_rate/vial%d_stir_rate.txt" % (save_path,exp_name,x)
                data = np.genfromtxt(stir_rate_path, delimiter=',')
                stir_set = data[len(data)-1][1]

                if stir_set == 0:
                    stir_rate_path =  "%s/%s/stir_rate/vial%d_stir_rate.txt" % (save_path,exp_name,x)
                    text_file = open(stir_rate_path,"a+")
                    text_file.write("%f,%s\n" %  (elapsed_time, 0))
                    text_file.close()


            if average_OD > ODset:
                time_in = 0
                step_size = (((-1)*np.log(lower_thresh[x]/average_OD)*volume)+.1)/(.0009)

                if step_size < 1000:
                    step_size = 1000

                MESSAGE = "dilute,%d,%d,0,%d,3,5,0,0,0," % (media[x], step_size, x)
                eVOLVER_module.fluid_command(MESSAGE, x, elapsed_time, pump_wait *60, exp_name, time_out,'y')



def measure_growthRate(x, save_path, exp_name):
    ## Load files from proper directories
    OD_path =  "%s/%s/OD/vial%d_OD.txt" % (save_path,exp_name,x)
    ODset_path =  "%s/%s/ODset/vial%d_ODset.txt" % (save_path,exp_name,x)
    OD_data = np.genfromtxt(OD_path, delimiter=',')
    ODset_data = np.genfromtxt(ODset_path, delimiter=',')

    ### Gets time frame from last diution event to current event
    growth_start= ODset_data[len(ODset_data)-2][0]
    growth_end = ODset_data[len(ODset_data)-1][0]

    ## Gets part of data that is part of the growth curve
    segmented_OD = OD_data[np.where(np.logical_and(OD_data >=growth_start, OD_data<=growth_end))[0]]

    ## Averages the OD data from start of curve and end of curve
    averaged_values = 10
    OD_start = np.mean(segmented_OD[0,1])
    OD_end = np.mean(segmented_OD[len(segmented_OD)-averaged_values :len(segmented_OD),1])

    ## Calculates growth rate
    growth_rate = ((OD_end-OD_start)/OD_start)/(growth_end - growth_start )

    return growth_rate
