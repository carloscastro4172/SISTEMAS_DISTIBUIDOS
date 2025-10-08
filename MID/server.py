import zmq

# Server principal: registra servicios y replica al nodo réplica
ctx = zmq.Context()

reg_api = ctx.socket(zmq.REP)        # registro de publishers
reg_api.bind("tcp://*:4431")

lookup_api = ctx.socket(zmq.REP)     # resolución de nombre -> endpoint
lookup_api.bind("tcp://*:4421")

to_replica = ctx.socket(zmq.PUSH)    # canal de replicación
to_replica.connect("tcp://localhost:4441")

catalog = {}  # {service_name: endpoint}

print(">>> Servidor principal operativo (registro: 4431, consultas: 4421) <<<")

poller = zmq.Poller()
poller.register(reg_api, zmq.POLLIN)
poller.register(lookup_api, zmq.POLLIN)

while True:
    ready = dict(poller.poll())

    if reg_api in ready:
        payload = reg_api.recv_json()
        svc = payload['name']
        endpoint = payload['address']
        catalog[svc] = endpoint

        to_replica.send_json(payload)            # replica el registro
        reg_api.send_json({'status': 'ok'})
        print(f"Servicio recibido y replicado: {svc} en {endpoint}")

    if lookup_api in ready:
        q = lookup_api.recv_json()
        endpoint = catalog.get(q['name'])
        if endpoint:
            lookup_api.send_json({'address': endpoint})
            print(f"Consulta resuelta: {q['name']} -> {endpoint}")
        else:
            lookup_api.send_json({'error': 'not found'})
            print(f"Consulta fallida: {q['name']} no existe en la base.")
