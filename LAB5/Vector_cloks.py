import socket
import threading
import json
import time

N = 2  # número de procesos (ejemplo: 2 PCs)

class Process:
    def __init__(self, pid, port, peers):
        self.pid = pid
        self.vc = [0] * N
        self.port = port
        self.peers = peers  # lista [(ip, port), ...]

    def local_event(self):
        self.vc[self.pid] += 1
        print(f"P{self.pid+1} local event -> VC = {self.vc}")

    def send_event(self, target_ip, target_port):
        self.vc[self.pid] += 1
        msg = json.dumps(self.vc).encode("utf-8")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendall(msg)
            s.close()
            print(f"P{self.pid+1} sent to {target_ip}:{target_port} -> VC = {self.vc}")
        except Exception as e:
            print(f"Error sending: {e}")

    def receive_event(self, msg_vc):
        self.vc = [max(self.vc[i], msg_vc[i]) for i in range(N)]
        self.vc[self.pid] += 1
        print(f"P{self.pid+1} received -> VC = {self.vc}")

    def server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", self.port))  # escucha en su propio puerto
        s.listen(5)
        print(f"P{self.pid+1} listening on port {self.port}")

        while True:
            conn, addr = s.accept()
            data = conn.recv(1024).decode("utf-8")
            if data:
                msg_vc = json.loads(data)
                self.receive_event(msg_vc)
            conn.close()

def run_process(pid, port, peers):
    p = Process(pid, port, peers)

    # lanzar el servidor en hilo aparte
    threading.Thread(target=p.server, daemon=True).start()

    time.sleep(5)  

    # ejemplo de eventos
    if pid == 0:
        p.local_event()
        time.sleep(2)
        ip, port = peers[1]
        p.send_event(ip, port)

    elif pid == 1:
        time.sleep(5)
        p.local_event()

if __name__ == "__main__":

    peers = [("172.23.210.72", 5000),  # PC1
            ("172.23.210.237", 5001)]  # PC2

    run_process(pid=0, port=5000, peers=peers)
    # run_process(pid=1, port=5001, peers=peers)

