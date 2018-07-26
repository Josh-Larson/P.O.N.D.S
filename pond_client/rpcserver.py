# Author: Connor Hamlet. 
# Description: This code is housed on two Pi's, the east and west pond.

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

POND_IP_ADDRESS="localhost"
POND_RPC_PORT = 8000

#Used to hold status information. 
class PondController:
    pond_status = "False"

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer((POND_IP_ADDRESS, POND_RPC_PORT),
     requestHandler=RequestHandler)
server.register_introspection_functions()
    

# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class ServerMethods:
    def setPondStatus(incoming_status):
        PondController.pond_status = incoming_status
        #Set pump here, Price call "setPond" function here. 
        print("Received incoming_status as: "+ str(incoming_status))
        return PondController.pond_status
    def getPondStatus():
        return PondController.pond_status

server.register_instance(ServerMethods)

# Run the server's main loop
server.serve_forever()