import zmq
import threading
import time
import sys

def node(id, next_port, my_port):
    context = zmq.Context()

    # Socket para recibir token
    rep = context.socket(zmq.REP)
    rep.bind(f"tcp://*:{my_port}")

    # Socket para enviar token
    req = context.socket(zmq.REQ)
    req.connect(f"tcp://localhost:{next_port}")

    has_token = (id == 1)  # el nodo 1 empieza con el token

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
            time.sleep(2)  # SC
            print(f"Node {id} leaves critical section")

            # pasa token al siguiente
            req.send_string("token")
            _ = req.recv_string()
            has_token = False
        time.sleep(1)

if __name__ == "__main__":
    # usage: python3 node.py <id> <next_port> <my_port>
    node(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
