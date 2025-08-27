import xmlrpc.client

server = input('Server address: ')
port = input('Server port: ')

# Create a client proxy
proxy = xmlrpc.client.ServerProxy("http://" + server + ":" + port + "/test")

# Call the remote method 'add'
try:    
    result = proxy.add(5, 3)
    print("5 + 3 =", result)
except:
    print('Error....')
