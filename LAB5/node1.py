import zmq
import threading
import time
from datetime import datetime
import random

# Datos del otro nodo (tu amigo)
hostname = "172.23.210.237"   # IP de Node2
port = "4444"                 # puerto de Node2

def peer1():
    context = zmq.Context()

    # REP socket para escuchar en tu PC
    rep_socket = context.socket(zmq.REP)
    rep_socket.bind("tcp://*:5001")   # Node1 escucha en el puerto 5001

    # REQ socket para enviar al Node2
    req_socket = context.socket(zmq.REQ)
    req_socket.connect(f"tcp://{hostname}:{port}")  # conecta a Node2

    # Tiempo inicial con offset
    local_time = datetime.utcnow().timestamp() + random.randint(-5, 5)
    print(f"Node 1 start time: {local_time}")

    # Hilo receptor
    def receiver():
        nonlocal local_time
        while True:
            _ = rep_socket.recv_string()
            rep_socket.send_string(str(local_time))

    threading.Thread(target=receiver, daemon=True).start()

    # Ciclo de sincronización
    while True:
        times = [local_time]
        req_socket.send_string("time?")
        reply = req_socket.recv_string()
        times.append(float(reply))

        avg_time = sum(times) / len(times)
        print(f"Node 1 -> before: {local_time:.2f}, after sync: {avg_time:.2f}")
        local_time = avg_time

        time.sleep(5)

if __name__ == "__main__":
    peer1()
