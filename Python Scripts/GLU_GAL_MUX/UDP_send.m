function recieved_data = UDP_send(config,ip,port)
u = udp(ip,port,'timeout',3,'LocalPort',57379);
fopen(u);
flushinput(u);
fwrite(u, config, 'char');
recieved_data = fscanf(u);
fclose(u);
delete(u);
clear u;