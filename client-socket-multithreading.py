# client_multithreading.py
from socket import *
import threading
import time

serverName = 'localhost'
serverPort = 14000

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
