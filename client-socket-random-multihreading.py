# client_multithreading_random_ids.py
from socket import *
import threading
import time
import random

serverName = 'localhost'
serverPort = 18000

# Diccionario con palabras en inglés y español
diccionario = {
    "saludos": ["hola", "adios", "buenos dias", "buenas noches"],
    "animales": ["perro", "gato", "pajaro", "pez", "dog", "cat", "bird", "fish"],
    "lugares": ["casa", "escuela", "trabajo", "parque", "home", "school", "work", "park"],
    "objetos": ["computadora", "teclado", "pantalla", "internet", "computer", "keyboard", "monitor", "internet"]
}

# Aplana todas las palabras del diccionario y barájalas
palabras = [p for lista in diccionario.values() for p in lista]
random.shuffle(palabras)

# Crea una asignación aleatoria 1..N de "números de hilo" (únicos)
NUM_HILOS = len(palabras)
ids_hilo = list(range(1, NUM_HILOS + 1))
random.shuffle(ids_hilo)  # ahora el número de hilo es aleatorio para cada envío

def enviar_mensaje(sentence: str, hilo_id: int):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        # Etiqueta el mensaje con el número de hilo aleatorio
        mensaje = f"[HILO-{hilo_id:02d}] {sentence}"
        clientSocket.send(mensaje.encode())

        modifiedSentence = clientSocket.recv(1024)
        print(f"[HILO-{hilo_id:02d}] Enviado: {sentence}  |  From Server: {modifiedSentence.decode()}")
    except Exception as e:
        print(f"[HILO-{hilo_id:02d}] Error con '{sentence}': {e}")
    finally:
        try:
            clientSocket.close()
        except:
            pass

# Lanza un hilo por cada palabra (cada uno con un id de hilo aleatorio único)
hilos = []
for i, palabra in enumerate(palabras):
    hilo_id = ids_hilo[i]  # asignación aleatoria pero sin repetir
    t = threading.Thread(target=enviar_mensaje, args=(palabra, hilo_id), daemon=True)
    t.start()
    hilos.append(t)
    time.sleep(0.03)  # pequeño desfase para no saturar

# Espera a que todos terminen
for t in hilos:
    t.join()

print("Listo.")
