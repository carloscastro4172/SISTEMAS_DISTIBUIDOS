import socket
import threading
import random
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 14000

PALABRAS = {
    "saludos": ["hola", "adiós", "hello", "bye", "buenas"],
    "animales": ["perro", "gato", "elefante", "tigre", "pájaro"],
    "lugares": ["casa", "escuela", "trabajo", "parque", "oficina"],
    "cosas": ["computadora", "teclado", "pantalla", "mouse", "internet"],
    "verbos": ["corre", "salta", "lee", "escribe", "mira"]
}

CANTIDAD_CLIENTES = 9

def generar_mensaje_aleatorio():
    return " ".join([
        random.choice(PALABRAS["saludos"]),
        random.choice(PALABRAS["animales"]),
        "en",
        random.choice(PALABRAS["lugares"]),
        random.choice(PALABRAS["verbos"]),
        random.choice(PALABRAS["cosas"])
    ])

# Crear mensajes aleatorios para cada hilo (ordenado por hilo)
mensajes = {idx: generar_mensaje_aleatorio() for idx in range(1, CANTIDAD_CLIENTES + 1)}

# Lista de hilos ordenada
hilos_ordenados = list(range(1, CANTIDAD_CLIENTES + 1))

# Desordenar el orden de envío
orden_envio = hilos_ordenados.copy()
random.shuffle(orden_envio)

def cliente(idx: int):
    try:
        time.sleep(random.uniform(0.1, 0.5))  # Retraso aleatorio para simular desorden
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_HOST, SERVER_PORT))
        mensaje = f"{idx}|{mensajes[idx]}"
        sock.sendall(mensaje.encode())
        respuesta = sock.recv(1024).decode()
        print(f"[Hilo-{idx}] Enviado: '{mensaje}' | Recibido: '{respuesta}'")
    except Exception as e:
        print(f"[Hilo-{idx}] Error: {e}")
    finally:
        sock.close()

print(f"Generando {CANTIDAD_CLIENTES} hilos en orden...")
print(f"Enviando mensajes en orden aleatorio de hilos: {orden_envio}\n")

# Crear hilos en orden
hilos = []
for idx in hilos_ordenados:
    hilo = threading.Thread(target=cliente, args=(idx,), daemon=True)
    hilos.append(hilo)

# Iniciar hilos en orden aleatorio
for idx in orden_envio:
    hilos[idx - 1].start()
    time.sleep(0.05)  # Pequeño retraso para visualizar desorden

# Esperar a que todos terminen
for h in hilos:
    h.join()

print("\nTodos los hilos han terminado.")