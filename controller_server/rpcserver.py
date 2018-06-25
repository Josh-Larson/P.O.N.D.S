from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
     requestHandler=RequestHandler)
server.register_introspection_functions()


class PondController:
    current_connections = {}
    pond_status = False

    

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
class ServerMethods:
    def setPondStatus(incoming_status):
        PondController.pond_status = incoming_status
        print("Received incoming_status as: "+ str(incoming_status))
        return PondController.pond_status
    def register_connection(uuid, name ):
        PondController.current_connections[uuid] = name
        print("Current connections:")
        print(PondController.current_connections)
        return True

   

server.register_instance(ServerMethods)

# Run the server's main loop
server.serve_forever()