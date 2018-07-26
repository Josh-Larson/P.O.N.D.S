# Author: Connor Hamlet et. al. 
# Description: This is code for the pond Raspberry Pi's
# The Pi will create a unique identifier and register a connection
# With the central Pi server. It will then send status messages
# once per second

import xmlrpc.client, uuid, threading
#ENV variables
CENTRAL_IP_ADDRESS = 'localhost'
CENTRAL_IP_PORT = '8000'
rpc_cont = xmlrpc.client.ServerProxy('http://'
            +CENTRAL_IP_ADDRESS
            +':'
            +CENTRAL_IP_PORT)

# Creates a unique and random id. 
uid = str(uuid.uuid4())
print(rpc_cont.register_connection(uid, "east"))

# Print list of available methods
print(rpc_cont.system.listMethods())

# This is the PAI which will be replaced by Azure
class API_Pond_Status:
    pond_status = True
    def get_pond_status(self):
        return self.pond_status

pond_api = API_Pond_Status()

#Sends the pond status every second. 
def send_status():
    threading.Timer(1.0, send_status).start()
    print(rpc_cont.setPondStatus(
        pond_api.get_pond_status()
        ));



send_status()
