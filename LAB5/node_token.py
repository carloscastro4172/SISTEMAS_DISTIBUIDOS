import zmq
import threading
import time
import sys

def node(id, next_ip, next_port, my_port):
    context = zmq.Context()

    # Socket para recibir token
    rep = context.socket(zmq.REP)
    rep.bind(f"tcp://*:{my_port}")  # escucha en su puerto

    # Socket para enviar token
    req = context.socket(zmq.REQ)
    req.connect(f"tcp://{next_ip}:{next_port}")  # conecta al siguiente nodo

    has_token = (id == 1)  # El nodo 1 arranca con el token

    def listener():
        nonlocal has_token
        while True:
            msg = rep.recv_string()
            if msg == "token":
                has_token = True
            rep.send_string("ok")

    threading.Thread(target=listener, daemon=True).start()

    while True:
        if has_token:
            print(f"Node {id} enters critical section")
            time.sleep(2)  # Simula sección crítica
            print(f"Node {id} leaves critical section")

            # pasa token al siguiente
            req.send_string("token")
            _ = req.recv_string()
            has_token = False
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3 node.py <id> <next_ip> <next_port> <my_port>")
        sys.exit(1)

    node(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
