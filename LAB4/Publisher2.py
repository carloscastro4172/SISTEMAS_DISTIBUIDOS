import ldap
import ldap.modlist as modlist

def register_or_update_service(service_name, ip, port):
    ldap_server = "ldap://localhost"
    admin_dn = "cn=admin,dc=example,dc=com"
    admin_pw = "123456789"
    base_dn = "ou=Services,dc=example,dc=com"

    dn = f"cn={service_name}-{ip},{base_dn}"   # clave: nombre + IP

    attrs = {
        'objectClass': [b'top', b'device', b'ipHost'],
        'cn': [f"{service_name}-{ip}".encode()],
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
        print(f"🔄 Servicio '{service_name}' actualizado en {ip}:{port}")
    finally:
        conn.unbind_s()


if __name__ == "__main__":
    # mismo servicio, dos IPs diferentes
    register_or_update_service("EchoService", "172.23.204.149", 5001)
    register_or_update_service("EchoService", "192.168.1.50", 5001)
