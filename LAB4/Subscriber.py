import ldap
import getpass

def get_service(service_name):
    ldap_server = "ldap://localhost"
    base_dn = "ou=Services,dc=example,dc=com"
    search_filter = f"(cn={service_name})"

    # Pedir credenciales
    user_uid = input("Ingrese el uid del usuario: ")
    user_pw = getpass.getpass("Ingrese la contraseña: ")

    # Construir DN del usuario
    user_dn = f"uid={user_uid},ou=People,dc=example,dc=com"

    try:
        conn = ldap.initialize(ldap_server)
        conn.simple_bind_s(user_dn, user_pw)  # autenticación

        result = conn.search_s(
            base_dn,
            ldap.SCOPE_SUBTREE,
            search_filter,
            ['ipHostNumber','description']
        )

        if result:
            dn, attrs = result[0]
            ip = attrs['ipHostNumber'][0].decode()
            port = attrs['description'][0].decode()
            print(f"Service {service_name} found: {ip}:{port}")
            return ip, port
        else:
            print("Service not found.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.unbind_s()
