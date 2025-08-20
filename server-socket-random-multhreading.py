# server_multithread.py
import socket
import threading

serverPort = 14000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)   # hasta 5 conexiones en cola
print("Servidor listo y escuchando en el puerto", serverPort)

contador = 0
lock = threading.Lock()

def atender_cliente(connectionSocket, addr, client_id):
    try:
        print(f"[Cliente-{client_id}] Conectado desde {addr}")

        while True:
            data = connectionSocket.recv(1024)
            if not data:   # conexión cerrada por el cliente
                break
            sentence = data.decode()
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
    
    # atender a cada cliente en un hilo independiente
    t = threading.Thread(target=atender_cliente, args=(connectionSocket, addr, client_id), daemon=True)
    t.start()
