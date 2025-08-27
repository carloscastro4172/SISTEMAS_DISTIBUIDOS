# Explicación del programa:
# Este servidor TCP en Python utiliza hilos para poder atender a varios clientes de manera simultánea. Primero se crea
# un socket asociado al puerto 14000 y se lo configura para escuchar conexiones entrantes con una cola máxima de 5 en
# espera. Cuando un cliente se conecta, el servidor acepta la conexión y asigna un identificador incremental protegido
# por un candado (lock) para evitar condiciones de carrera entre múltiples hilos. Luego lanza un hilo independiente que
# ejecuta la función atender_cliente. Dentro de esta función se recibe un único mensaje enviado por el cliente, se imprime
# en la consola indicando de qué cliente proviene, se convierte el texto a mayúsculas y se devuelve al cliente como
# respuesta. Después se cierra la conexión y se informa en la salida estándar que la comunicación con ese cliente ha
# terminado. El servidor principal permanece en un bucle infinito aceptando nuevas conexiones y generando hilos para
# cada una. La entrada del programa son los mensajes que envían los clientes a través de sockets TCP y la salida consiste
# en dos partes: por un lado, la impresión en consola de los eventos de conexión, mensajes recibidos y cierre de
# conexiones; por otro, la respuesta que reciben los clientes, que es siempre el mismo mensaje convertido en mayúsculas.
# Un ejemplo de interacción sería que el cliente envíe "hola mundo", el servidor imprima en consola "[Cliente-1] Mensaje
# recibido: hola mundo" y devuelva al cliente la cadena "HOLA MUNDO". Después, al cerrarse la conexión, el servidor
# muestra "[Cliente-1] Conexión cerrada" y queda listo para aceptar nuevos clientes.

from socket import *
import threading

serverPort = 14000
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
