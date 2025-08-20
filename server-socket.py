from socket import *
import threading

serverPort = 14000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("Servidor listo para recibir conexiones...")

contador = 0
lock = threading.Lock()

def atender_cliente(connectionSocket, addr):
    try:
        data = connectionSocket.recv(1024).decode()
        # Formato recibido: "<client_id>|<mensaje>"
        client_id, sentence = data.split("|", 1)
        print(f"[Cliente-{client_id}] Conectado desde {addr}")
        print(f"[Cliente-{client_id}] Mensaje recibido: {sentence}")
        capitalized = sentence.upper()
        connectionSocket.send(f"{client_id}|{capitalized}".encode())
    except Exception as e:
        print(f"[Cliente-?] Error: {e}")
    finally:
        connectionSocket.close()
        if 'client_id' in locals():
            print(f"[Cliente-{client_id}] Conexión cerrada")

# Bucle principal
while True:
    connectionSocket, addr = serverSocket.accept()
    with lock:
        contador += 1
        # El servidor ya no pasa client_id como parámetro; lo recibe en el mensaje
    t = threading.Thread(target=atender_cliente, args=(connectionSocket, addr))
    t.start()