import os
import dns.resolver
import socket

class MenuDNS:
    def __init__(self):
        self.SALIR = 10
        self.OPCION = 0

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu(self):
        print("=" * 50)
        print("          MENÚ DE CONSULTAS DNS")
        print("=" * 50)
        print("1)  Resolución directa (Dominio → IP)")
        print("2)  Resolución inversa (IP → Dominio)")
        print("3)  Consulta con servidor DNS específico")
        print("4)  Obtener registros MX")
        print("5)  Obtener registros NS")
        print("6)  Obtener registro SOA")
        print("7)  Verificar registro CNAME")
        print("8)  Modo debug detallado (nslookup)")
        print("9)  Consultar dominio inexistente")
        print("10) Salir")
        print("=" * 50)

    def ejecutar_opcion(self, OPCION):
        if OPCION == 1:
            self.consulta_directa()
        elif OPCION == 2:
            self.consulta_inversa()
        elif OPCION == 3:
            self.consulta_servidor_especifico()
        elif OPCION == 4:
            self.consulta_mx()
        elif OPCION == 5:
            self.consulta_ns()
        elif OPCION == 6:
            self.consulta_soa()
        elif OPCION == 7:
            self.consulta_cname()
        elif OPCION == 8:
            self.modo_debug()
        elif OPCION == 9:
            self.consulta_inexistente()
        else:
            print("Opción no válida.")

    # ---------- MÉTODOS DE CONSULTA ----------
    def consulta_directa(self):
        DOMINIO = input("Introduce el dominio: ").strip()
        try:
            RESPUESTAS = dns.resolver.resolve(DOMINIO, 'A')
            for RDATA in RESPUESTAS:
                print(f"IP: {RDATA}")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def consulta_inversa(self):
        IP = input("Introduce la IP: ").strip()
        try:
            NOMBRE = socket.gethostbyaddr(IP)[0]
            print(f"Nombre asociado: {NOMBRE}")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def consulta_servidor_especifico(self):
        DOMINIO = input("Introduce el dominio: ").strip()
        SERVIDOR = input("Introduce el servidor DNS (ej. 1.1.1.1): ").strip()
        try:
            RESOLVER = dns.resolver.Resolver()
            RESOLVER.nameservers = [SERVIDOR]
            RESPUESTAS = RESOLVER.resolve(DOMINIO, 'A')
            for RDATA in RESPUESTAS:
                print(f"IP desde {SERVIDOR}: {RDATA}")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def consulta_mx(self):
        DOMINIO = input("Introduce el dominio: ").strip()
        try:
            RESPUESTAS = dns.resolver.resolve(DOMINIO, 'MX')
            for RDATA in RESPUESTAS:
                print(f"MX: {RDATA.exchange} (prioridad {RDATA.preference})")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def consulta_ns(self):
        DOMINIO = input("Introduce el dominio: ").strip()
        try:
            RESPUESTAS = dns.resolver.resolve(DOMINIO, 'NS')
            for RDATA in RESPUESTAS:
                print(f"NS: {RDATA}")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def consulta_soa(self):
        DOMINIO = input("Introduce el dominio: ").strip()
        try:
            RESPUESTAS = dns.resolver.resolve(DOMINIO, 'SOA')
            for RDATA in RESPUESTAS:
                print(f"SOA: {RDATA.mname}")
                print(f"   Correo admin: {RDATA.rname}")
                print(f"   Serial: {RDATA.serial}")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def consulta_cname(self):
        DOMINIO = input("Introduce el dominio: ").strip()
        try:
            RESPUESTAS = dns.resolver.resolve(DOMINIO, 'CNAME')
            for RDATA in RESPUESTAS:
                print(f"CNAME: {RDATA}")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    def modo_debug(self):
        DOMINIO = input("Introduce el dominio para debug: ").strip()
        os.system(f"nslookup -debug {DOMINIO}")
        input("\nPresiona ENTER para continuar...")

    def consulta_inexistente(self):
        DOMINIO = input("Introduce el dominio inexistente: ").strip()
        try:
            dns.resolver.resolve(DOMINIO, 'A')
            print("El dominio existe (inesperado).")
        except dns.resolver.NXDOMAIN:
            print("NXDOMAIN: el dominio no existe.")
        except Exception as ERROR:
            print(f"Error: {ERROR}")
        input("\nPresiona ENTER para continuar...")

    # ---------- BUCLE PRINCIPAL ----------
    def iniciar(self):
        while True:
            self.limpiar_pantalla()
            self.mostrar_menu()
            try:
                self.OPCION = int(input("Seleccione una opción: "))
                if self.OPCION == self.SALIR:
                    print("Saliendo...")
                    break
                self.ejecutar_opcion(self.OPCION)
            except ValueError:
                print("Por favor ingrese un número válido.")
                input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    MENU = MenuDNS()
    MENU.iniciar()
