# Explicación del programa:
# Este cliente TCP en Python establece una conexión con un servidor en 'localhost' y puerto 18000 de forma iterativa.
# En cada ciclo del bucle principal, el programa crea un nuevo socket, lo conecta al servidor, solicita al usuario que
# introduzca una cadena en minúsculas desde la entrada estándar, y la envía codificada al servidor. Después espera una
# respuesta de hasta 1024 bytes, que imprime en consola con el prefijo "From Server:". Una vez procesado el mensaje, 
# pregunta al usuario si desea enviar otro mensaje mediante la entrada "Other message: (Y/N)". Si el usuario responde 
# con 'N' (mayúscula o minúscula), la variable de control `next` se pone en False y el bucle termina; en cualquier otro 
# caso, se repite el ciclo creando un nuevo socket en cada iteración. La entrada del programa es por tanto el texto 
# escrito por el usuario en la consola, y la salida es la impresión de la respuesta que devuelve el servidor. El cierre 
# del socket ocurre al final de cada ciclo, asegurando que cada mensaje se maneje con una conexión independiente. 
# Un ejemplo de interacción sería:
# Input lowercase sentence: hola
# From Server: HOLA
# Other message: (Y/N) Y
# Input lowercase sentence: adios
# From Server: ADIOS
# Other message: (Y/N) N
# (en ese momento el programa finaliza).

from socket import *
serverName = 'localhost'
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
