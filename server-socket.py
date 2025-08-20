# server_multithread.py
from socket import *
import threading

serverPort = 18000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)   # permite hasta 5 conexiones en cola
print("The server is ready to receive")

contador = 0
lock = threading.Lock()

def atender_cliente(connectionSocket, addr, client_id):
    try:
        print(f"[Cliente-{client_id}] Conectado desde {addr}")
        sentence = connectionSocket.recv(1024).decode()
        print(f"[Cliente-{client_id}] Mensaje recibido: {sentence}")
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
    except Exception as e:
        print(f"[Cliente-{client_id}] Error: {e}")
    finally:
        connectionSocket.close()
        print(f"[Cliente-{client_id}] Conexión cerrada")

while True:
    connectionSocket, addr = serverSocket.accept()
    with lock:
        contador += 1
        client_id = contador
    
    t = threading.Thread(target=atender_cliente, args=(connectionSocket, addr, client_id))
    t.start()
