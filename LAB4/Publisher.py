import ldap
import ldap.modlist as modlist

def register_or_update_service(service_name, ip, port):
    ldap_server = "ldap://localhost"
    admin_dn = "cn=admin,dc=example,dc=com"
    admin_pw = "123456789"  # tu contraseña de admin
    base_dn = "ou=Services,dc=example,dc=com"

    dn = f"cn={service_name},{base_dn}"

    attrs = {
        'objectClass': [b'top', b'device', b'ipHost'],
        'cn': [service_name.encode()],
        'ipHostNumber': [ip.encode()],
        'description': [str(port).encode()],
    }

    conn = ldap.initialize(ldap_server)
    conn.simple_bind_s(admin_dn, admin_pw)

    try:
        ldif = modlist.addModlist(attrs)
        conn.add_s(dn, ldif)
        print(f"✅ Servicio '{service_name}' registrado en {ip}:{port}")
    except ldap.ALREADY_EXISTS:
        mods = [
            (ldap.MOD_REPLACE, 'ipHostNumber', ip.encode()),
            (ldap.MOD_REPLACE, 'description', str(port).encode())
        ]
        conn.modify_s(dn, mods)
        print(f"🔄 Servicio '{service_name}' actualizado a {ip}:{port}")
    finally:
        conn.unbind_s()


# ====== USO AUTOMÁTICO ======
if __name__ == "__main__":
    # Lista de servicios: (nombre, ip, puerto)
    services = [
        ("EchoService", "172.23.204.149", 5001),
        ("ChatService", "172.23.204.149", 6000),
        ("DBService", "172.23.204.149", 3306),
        ("APIGateway", "172.23.204.149", 8080)
    ]

    for name, ip, port in services:
        register_or_update_service(name, ip, port)
