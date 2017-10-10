#!/usr/bin/python

import SocketServer
import struct
import socket
import time
import os.path

class MatlabUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print "%s wrote:" % self.client_address[0]


        if data == 'clear':
                log = open(completeName, "w")
        else:
                log = open(completeName,"a")
                log.write("%s\n" % data)
        print data
        log.close()

        #log = open(completeName,"r")
        #values = log.read()
        #log.close()

        socket.sendto("Message Recieved", self.client_address)

save_path = '/root/'
completeName = os.path.join(save_path, "fluid_config.txt")
log = open(completeName, "w")
BEAGLE, PORT =  "0.0.0.0", 5552
server = SocketServer.UDPServer((BEAGLE, PORT), MatlabUDPHandler)
while (1):
        server.handle_request()
        #server.serve_forever()