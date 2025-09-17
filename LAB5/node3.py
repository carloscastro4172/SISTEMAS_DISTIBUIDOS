import zmq
import threading
import time
from datetime import datetime
import random

# Configuración de puertos
PEERS = {
    1: 5001,
    2: 5002,
    3: 5003
}

def peer(node_id):
    context = zmq.Context()

    # Socket REP para recibir tiempos
    rep_socket = context.socket(zmq.REP)
    rep_socket.bind(f"tcp://*:{PEERS[node_id]}")

    # Sockets REQ para enviar tiempos a los demás
    req_sockets = {}
    for pid, port in PEERS.items():
        if pid != node_id:
            s = context.socket(zmq.REQ)
            s.connect(f"tcp://localhost:{port}")
            req_sockets[pid] = s

    # Tiempo local inicial con offset aleatorio
    local_time = datetime.utcnow().timestamp() + random.randint(-5, 5)
    print(f"Node {node_id} start time: {local_time}")

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
        for pid, s in req_sockets.items():
            s.send_string("time?")
            reply = s.recv_string()
            times.append(float(reply))

        avg_time = sum(times) / len(times)
        print(f"Node {node_id} -> before: {local_time:.2f}, after sync: {avg_time:.2f}")
        local_time = avg_time

        time.sleep(5)

if __name__ == "__main__":
    peer(3)
