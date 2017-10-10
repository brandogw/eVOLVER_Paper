fclose('all'); delete(instrfindall); clear all; close all; clc; 
expt_name = 'rk4_expt2_highdenfit_col1b_11';ip = '10.241.24.11';%ip = '192.168.1.4';


%Start UDP Communication
port_fan = 5551; port_fluid= 5552; port_temp= 5553; port_od=5554;
valve = 0;
UDP_send('clear', ip, port_fluid);

pump_rate = 1.15; %ml/sec
target_OD = 0.1; %OD
volume = 20; %mL

bits;
vials = [0 1 2 4 5 6 7 8 9 10 11 12 13 14 15];

for n=1:length(vials)

    file_dir = sprintf('%s/%s/OD/vial%d_OD.txt',pwd,expt_name, vials(n));
    OD_data = csvread(file_dir);
    current_OD = OD_data(end,2);
    pump_time(1,n) = real(vials(n));
    pump_time(2,n) = real(current_OD);
    
    if current_OD > .05
        pump_time(3,n) = real(round(-(log(target_OD/current_OD)* volume)/pump_rate));
    else
        pump_time(3,n) = 0;
    end
    
end

pump_time

exp_cont = input('Are you sure you want to dilute (y/n)?: ','s');
if exp_cont == 'y'
        % %%%% To Run each pump individually %%%%%%
    for s= 1:length(pump_time(1,:))

        valve = control(pump_time(1,s)+1) + control(pump_time(1,s)+17);
        valve = char(dec2bin(valve));
        time_on = pump_time(3,s); %seconds
        if time_on > 0
            sprintf('%s,%d,%d,',valve,0,time_on)
            UDP_send(sprintf('%s,%d,%d,',valve,0,time_on), ip, port_fluid);
            
            valve = control(pump_time(1,s)+17);
            valve = char(dec2bin(valve));
            time_on = 10; %seconds
            sprintf('%s,%d,%d,',valve,0,time_on)
            UDP_send(sprintf('%s,%d,%d,',valve,0,time_on), ip, port_fluid);
            
        end
        
    end
    
end

