import xmlrpc.client

def read_array(prompt):
    arr = input(prompt)
    # Permitir entrada tipo: 1 2 3 4
    return [float(x) for x in arr.strip().split()]

server = input('Dirección del servidor: ')
port = input('Puerto del servidor: ')

proxy = xmlrpc.client.ServerProxy(f"http://{server}:{port}/test", allow_none=True)

print("\nOperaciones disponibles:")
print("1. Suma de arreglos")
print("2. Resta de arreglos")
print("3. Producto punto")
print("4. Máximo elemento a elemento")
print("5. Mínimo elemento a elemento")
op = input("Seleccione la operación (1-5): ")

arr1 = read_array("Ingrese el primer arreglo (números separados por espacio): ")
arr2 = read_array("Ingrese el segundo arreglo (números separados por espacio): ")

try:
    if op == '1':
        result = proxy.sum(arr1, arr2)
        print("Resultado de la suma:", result)
    elif op == '2':
        result = proxy.sub(arr1, arr2)
        print("Resultado de la resta:", result)
    elif op == '3':
        result = proxy.dotprod(arr1, arr2)
        print("Producto punto:", result)
    elif op == '4':
        result = proxy.max(arr1, arr2)
        print("Máximos elemento a elemento:", result)
    elif op == '5':
        result = proxy.min(arr1, arr2)
        print("Mínimos elemento a elemento:", result)
    else:
        print("Operación no válida.")
except Exception as e:
    print('Error en la operación:', e)
