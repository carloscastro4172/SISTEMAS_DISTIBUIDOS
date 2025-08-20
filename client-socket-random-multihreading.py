# client_random_multithread.py
import socket
import threading
import random
import time

# ----------------- CONFIGURACIÓN -----------------
SERVER_HOST = 'localhost'     # dirección del servidor
SERVER_PORT = 14000           # puerto del servidor
CANTIDAD_CLIENTES = 9         # número de hilos (clientes simultáneos)

# Diccionario de palabras
PALABRAS = {
    "saludos": ["hola", "adiós", "hello", "bye", "buenas"],
    "animales": ["perro", "gato", "elefante", "tigre", "pájaro"],
    "lugares": ["casa", "escuela", "trabajo", "parque", "oficina"],
    "cosas": ["computadora", "teclado", "pantalla", "mouse", "internet"],
    "verbos": ["corre", "salta", "lee", "escribe", "mira"]
}

# ----------------- FUNCIONES -----------------
def generar_mensaje_aleatorio() -> str:
    """
    Genera una frase aleatoria combinando categorías de palabras.
    Ejemplo: "hola perro en casa corre teclado"
    """
    return " ".join([
        random.choice(PALABRAS["saludos"]),
        random.choice(PALABRAS["animales"]),
        "en",
        random.choice(PALABRAS["lugares"]),
        random.choice(PALABRAS["verbos"]),
        random.choice(PALABRAS["cosas"])
    ])

def cliente(idx: int):
    """
    Cada hilo (cliente) se conecta al servidor, envía entre 1 y 20 mensajes
    generados aleatoriamente, espera respuesta y termina.
    """
    cantidad = random.randint(1, 20)  # número de mensajes que enviará este cliente
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
        for _ in range(cantidad):
            mensaje = generar_mensaje_aleatorio()
            envio = f"[HILO-{idx}] {mensaje}"
            sock.sendall(envio.encode())                 # enviar al servidor
            respuesta = sock.recv(1024).decode()         # recibir respuesta
            print(f"[Hilo-{idx}] Enviado: '{mensaje}' | Recibido: '{respuesta}'")
            time.sleep(random.uniform(0.10, 0.25))       # pausa breve entre mensajes
    except Exception as e:
        print(f"[Hilo-{idx}] Error: {e}")
    finally:
        sock.close()

# ----------------- MAIN -----------------
if __name__ == "__main__":
    hilos = []
    for idx in range(1, CANTIDAD_CLIENTES + 1):
        hilo = threading.Thread(target=cliente, args=(idx,), daemon=True)
        hilos.append(hilo)
        hilo.start()

    for h in hilos:
        h.join()

    print("\n✅ Todos los hilos han terminado.")
