from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/test',)

# Create server
with SimpleXMLRPCServer(('localhost', 12000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register a function under a different name
    def add(x, y):
        print("Received: ", x, y)
        return x + y
    server.register_function(add, 'add')

    # Run the server's main loop
    print("Server is listening on port 12000...")
    server.serve_forever()
