import threading
import time

N = 3  # número de procesos

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.vc = [0] * N

    def local_event(self):
        self.vc[self.pid] += 1
        print(f"P{self.pid+1} local event -> VC = {self.vc}")

    def send_event(self, other):
        self.vc[self.pid] += 1
        print(f"P{self.pid+1} sends to P{other.pid+1} -> VC = {self.vc}")
        other.receive_event(self.vc)

    def receive_event(self, msg_vc):
        # merge con el máximo de cada posición
        self.vc = [max(self.vc[i], msg_vc[i]) for i in range(N)]
        self.vc[self.pid] += 1
        print(f"P{self.pid+1} receives -> VC = {self.vc}")

def simulate():
    P1 = Process(0)
    P2 = Process(1)
    P3 = Process(2)

    # Simulación de eventos
    P1.local_event()
    time.sleep(1)

    P1.send_event(P2)
    time.sleep(1)

    P2.local_event()
    time.sleep(1)

    P2.send_event(P3)
    time.sleep(1)

    P3.local_event()
    time.sleep(1)

    P3.send_event(P1)

if __name__ == "__main__":
    simulate()
