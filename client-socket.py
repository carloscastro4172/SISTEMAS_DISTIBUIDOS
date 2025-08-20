from socket import *
serverName = '172.23.199.29'
serverPort = 18000
next = True
while (next):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())
    other = input('Other message: (Y/N)')
    if (other.upper() == 'N'): 
        next = False
    clientSocket.close()
