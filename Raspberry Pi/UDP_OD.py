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
                print "config cleared"
                results = open(completeName,"r")
                results_string =  results.read()
                results.close()
                socket.sendto(results_string, self.client_address)
                print "sent: %s" % results_string
                log = open(completeName, "w")
                log.close()
        else:
                log = open(completeName,"w")
                log.write("%s\n" % data)
                log.close()
                results = open(resultsName,"r")
                results_string =  results.read()
                results.close()
                socket.sendto(results_string, self.client_address)
                #print data

save_path = '/root/'
completeName = os.path.join(save_path, "OD_config.txt")
resultsName = os.path.join(save_path, "OD_data.txt")
BEAGLE, PORT =  "0.0.0.0", 5554
server = SocketServer.UDPServer((BEAGLE, PORT), MatlabUDPHandler)
while (1):
        server.handle_request()
        #server.serve_forever()

