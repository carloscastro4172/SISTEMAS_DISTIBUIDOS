# Explicación del programa:
# Este es un servidor TCP multihilo en Python que escucha conexiones entrantes en el puerto 14000. 
# El servidor crea un socket, lo liga a la dirección local y comienza a escuchar con una cola de hasta 5 clientes en espera. 
# Cada vez que un cliente se conecta, el servidor acepta la conexión y lanza un hilo independiente para atenderlo mediante la 
# función atender_cliente. En esta función se reciben mensajes de hasta 1024 bytes enviados por el cliente; si el cliente 
# cierra la conexión, el bucle se interrumpe. Cada mensaje recibido se decodifica, se imprime en consola junto con el número 
# de cliente asignado, se transforma a mayúsculas y se devuelve al cliente como respuesta. La variable contador, protegida 
# con un candado (lock), asigna un identificador único a cada cliente para distinguirlos en la salida por consola. El flujo 
# general es que el servidor permanece en un bucle infinito aceptando nuevas conexiones y, por cada una, crea un hilo que se 
# encarga de la comunicación con ese cliente hasta que se cierre la conexión. La entrada del programa son los mensajes que 
# envían los clientes a través de sockets TCP, y la salida consiste en imprimir en pantalla el detalle de las conexiones y 
# mensajes, además de enviar de vuelta al cliente la misma cadena convertida a mayúsculas. Un ejemplo de interacción sería:
# Cliente envía: "hola mundo"
# Servidor imprime: [Cliente-1] Mensaje recibido: hola mundo
# Servidor responde al cliente: "HOLA MUNDO"
# Cuando el cliente se desconecta, el servidor imprime: [Cliente-1] Conexión cerrada
# y continúa disponible para atender nuevas conexiones.

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
