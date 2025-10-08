import zmq
import time

SERVICE = "TIME"                         # nombre del servicio
PUB_ENDPOINT = "tcp://localhost:4432"    # dónde publica el publisher

ctx = zmq.Context()

# Registro en el server (REQ/REP)
reg_sock = ctx.socket(zmq.REQ)
reg_sock.connect("tcp://localhost:4431")
reg_sock.send_json({'name': SERVICE, 'address': PUB_ENDPOINT})
print(">>> Publisher solicitando registro en el servidor principal...")
reg_sock.recv_json()

# Socket de publicación (PUB/SUB)
pub_sock = ctx.socket(zmq.PUB)
pub_sock.bind(PUB_ENDPOINT)
print(f"Publisher activo, enviando datos en {PUB_ENDPOINT}")

while True:
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    pub_sock.send_string(f"{SERVICE} {ts}")
    print(f"Mensaje emitido: {SERVICE} {ts}")
    time.sleep(2)
