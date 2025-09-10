import ldap

def lookup_service(service_name):
    ldap_server = "ldap://localhost"
    admin_dn = "cn=admin,dc=example,dc=com"
    admin_pw = "123456789"  # tu contraseña real
    base_dn = "ou=Services,dc=example,dc=com"

    try:
        conn = ldap.initialize(ldap_server)
        conn.simple_bind_s(admin_dn, admin_pw)

        search_filter = f"(cn={service_name})"
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, ["ipHostNumber", "description"])
        conn.unbind_s()

        if result:
            dn, attrs = result[0]
            ip = attrs['ipHostNumber'][0].decode()
            port = attrs['description'][0].decode()
            return f"✅ Servicio '{service_name}' disponible en {ip}:{port}"
        else:
            return f"❌ Servicio '{service_name}' no encontrado en LDAP."
    except Exception as e:
        return f"⚠️ Error al consultar LDAP: {e}"


if __name__ == "__main__":
    print("=== Subscriber LDAP (consulta de servicios) ===")
    while True:
        service = input("\n🔎 Ingresa el nombre del servicio (o 'salir' para terminar): ").strip()
        if service.lower() == "salir":
            print("👋 Saliendo del subscriber...")
            break
        print(lookup_service(service))
