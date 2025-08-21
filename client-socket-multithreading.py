# Explicación del programa:
# Este cliente multihilo en Python crea un socket TCP por cada mensaje de la lista 'mensajes' y se conecta al servidor 
# definido en 'localhost' en el puerto 18000. Cada mensaje se envía desde un hilo independiente, lo que permite 
# ejecutar múltiples envíos en paralelo simulando varios clientes a la vez. Entre la creación de hilos hay una pausa 
# de 0.03 segundos para no lanzar todas las conexiones simultáneamente. Luego el programa espera a que todos los hilos 
# terminen usando join(). Finalmente, cuando todos los mensajes han sido enviados y respondidos por el servidor, 
# aparece el texto "Listo." en la consola. La entrada no proviene del usuario, sino que son los mensajes definidos en 
# la lista, y la salida consiste en mostrar en pantalla cada mensaje enviado y la respuesta recibida. 
# Por ejemplo, si el servidor devuelve los textos en mayúsculas, la consola mostraría:
# [01] Enviado: hola       |  From Server: HOLA
# [02] Enviado: adios      |  From Server: ADIOS
# ...
# [24] Enviado: internet   |  From Server: INTERNET
# Listo.

# client_multithreading.py
from socket import *
import threading
import time

serverName = 'localhost'
serverPort = 18000

mensajes = [
    "hola", "adios", "perro", "gato", "casa", "escuela", "trabajo", "amigo",
    "house", "goodbye", "dog", "cat", "home", "school", "work", "friend",
    "computadora", "teclado", "pantalla", "internet",
    "computer", "keyboard", "monitor", "internet"
]

def enviar_mensaje(sentence: str, idx: int):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(1024)
        print(f"[{idx:02d}] Enviado: {sentence}  |  From Server: {modifiedSentence.decode()}")
    except Exception as e:
        print(f"[{idx:02d}] Error con '{sentence}': {e}")
    finally:
        try:
            clientSocket.close()
        except:
            pass

# Lanza varios hilos (multithreading) para enviar mensajes en paralelo
hilos = []
for i, msg in enumerate(mensajes, start=1):
    t = threading.Thread(target=enviar_mensaje, args=(msg, i), daemon=True)
    t.start()
    hilos.append(t)
    time.sleep(0.03)

for t in hilos:
    t.join()

print("Listo.")
