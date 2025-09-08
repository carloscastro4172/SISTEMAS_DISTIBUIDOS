import ldap
import getpass

ldap_server = "ldap://localhost"
base_dn = "ou=People,dc=example,dc=com"  # ajusta a tu dominio

uid = input("Enter LDAP uid: ")
password = getpass.getpass("Enter LDAP password: ")

# construir DN completo
username = f"uid={uid},{base_dn}"

try:
    conn = ldap.initialize(ldap_server)
    conn.simple_bind_s(username, password)
    print("Authentication successful!")
except ldap.INVALID_CREDENTIALS:
    print("Authentication failed! Invalid username or password.")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.unbind_s()
