from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/test',)

def array_sum(arr1, arr2):
    return [a + b for a, b in zip(arr1, arr2)]

def array_sub(arr1, arr2):
    return [a - b for a, b in zip(arr1, arr2)]

def array_dotprod(arr1, arr2):
    return sum(a * b for a, b in zip(arr1, arr2))

def array_max(arr1, arr2):
    return [max(a, b) for a, b in zip(arr1, arr2)]

def array_min(arr1, arr2):
    return [min(a, b) for a, b in zip(arr1, arr2)]

with SimpleXMLRPCServer(('172.23.199.4', 12000),
                        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()
    server.register_function(array_sum, 'sum')
    server.register_function(array_sub, 'sub')
    server.register_function(array_dotprod, 'dotprod')
    server.register_function(array_max, 'max')
    server.register_function(array_min, 'min')

    print("Servidor de arreglos numéricos escuchando en 12000...")
    server.serve_forever()
