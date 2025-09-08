import ldap
import ldap.modlist as modlist
import getpass

def register_service(service_name, ip, port):
    ldap_server = "ldap://localhost"

    # Pedir credenciales al usuario
    user_uid = input("Ingrese el uid del usuario: ")
    user_pw = getpass.getpass("Ingrese la contraseña: ")

    # Construir DN a partir del uid
    user_dn = f"uid={user_uid},ou=People,dc=example,dc=com"

    dn = f"cn={service_name},ou=Services,dc=example,dc=com"
    attrs = {
        'objectClass': [b'top', b'device'],
        'cn': [service_name.encode()],
        'ipHostNumber': [ip.encode()],
        'description': [str(port).encode()],
    }

    try:
        conn = ldap.initialize(ldap_server)
        # Autenticación con el usuario y contraseña ingresados
        conn.simple_bind_s(user_dn, user_pw)

        ldif = modlist.addModlist(attrs)
        conn.add_s(dn, ldif)
        print(f"Service {service_name} registered successfully!")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.unbind_s()
