import zmq

# Subscriber: resuelve nombre -> endpoint y se suscribe
SERVICE = input(">>> Ingrese el nombre del servicio al que desea suscribirse: ").strip()

ctx = zmq.Context()

# Lookup en el server principal
req = ctx.socket(zmq.REQ)
req.connect("tcp://localhost:4421")
poller = zmq.Poller()
poller.register(req, zmq.POLLIN)

req.send_json({'name': SERVICE})
ready = dict(poller.poll(2000))  # 2s

if req in ready:
    res = req.recv_json()
    if 'address' not in res:
        print(">>> Servicio no encontrado en el servidor principal <<<")
        raise SystemExit(1)
    endpoint = res['address']
    print(f">>> Dirección obtenida del servidor principal: {endpoint} <<<")
else:
    print(">>> Timeout. Falló el primario, intentando con réplica... <<<")
    req = ctx.socket(zmq.REQ)
    req.connect("tcp://localhost:4449")
    req.send_json({'name': SERVICE})
    res = req.recv_json()
    if 'address' not in res:
        print(">>> Servicio no encontrado en la réplica <<<")
        raise SystemExit(1)
    endpoint = res['address']
    print(f">>> Dirección obtenida del servidor réplica: {endpoint} <<<")

sub = ctx.socket(zmq.SUB)
sub.connect(endpoint)
sub.setsockopt_string(zmq.SUBSCRIBE, SERVICE)
print(f">>> Suscripción establecida en {endpoint}, esperando mensajes... <<<")

count = 0
while count < 5:
    msg = sub.recv_string()
    print(f">>> Mensaje recibido: {msg} <<<")
    count += 1
