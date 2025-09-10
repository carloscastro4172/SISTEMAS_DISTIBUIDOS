import ldap

def lookup_service(service_name):
    ldap_server = "ldap://localhost"
    admin_dn = "cn=admin,dc=example,dc=com"
    admin_pw = "123456789"
    base_dn = "ou=Services,dc=example,dc=com"

    conn = ldap.initialize(ldap_server)
    conn.simple_bind_s(admin_dn, admin_pw)

    search_filter = f"(cn={service_name}-*)"
    result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, ["ipHostNumber", "description"])
    conn.unbind_s()

    if result:
        print(f"✅ Se encontraron instancias del servicio '{service_name}':")
        for dn, attrs in result:
            ip = attrs['ipHostNumber'][0].decode()
            port = attrs['description'][0].decode()
            print(f"   → {ip}:{port}")
    else:
        print(f"❌ No se encontraron instancias de '{service_name}'.")


if __name__ == "__main__":
    lookup_service("EchoService")
