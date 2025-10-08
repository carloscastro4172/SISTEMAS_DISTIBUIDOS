import zmq

# Mantiene copia del registro y atiende lookups cuando el server falla
ctx = zmq.Context()

pull_replication = ctx.socket(zmq.PULL)
pull_replication.bind("tcp://*:4441")

rep_lookup = ctx.socket(zmq.REP)
rep_lookup.bind("tcp://*:4449")

registry = {}  # {service_name: endpoint}

print(">>> Réplica levantada (registros en 4441, consultas en 4449) <<<")

poller = zmq.Poller()
poller.register(pull_replication, zmq.POLLIN)
poller.register(rep_lookup, zmq.POLLIN)

while True:
    ready = dict(poller.poll())

    if pull_replication in ready:
        payload = pull_replication.recv_json()
        registry[payload['name']] = payload['address']
        print(f"Réplica guardó el servicio: {payload['name']} -> {payload['address']}")

    if rep_lookup in ready:
        query = rep_lookup.recv_json()
        endpoint = registry.get(query['name'])
        if endpoint:
            rep_lookup.send_json({'address': endpoint})
            print(f"Consulta recibida. Servicio {query['name']} entregado.")
        else:
            rep_lookup.send_json({'error': 'not found'})
            print(f"Consulta fallida. {query['name']} no existe en la réplica.")
