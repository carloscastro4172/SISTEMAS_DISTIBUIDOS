    // Explicación del programa:
    // Este es un servidor TCP escrito en C que escucha únicamente en la dirección 127.0.0.1 y en el puerto 18000.
    // En primer lugar crea un socket de tipo stream (TCP), configura la opción SO_REUSEADDR para permitir reutilizar
    // el puerto rápidamente tras un cierre, y luego lo asocia a la dirección y puerto especificados mediante bind.
    // Después, el servidor pasa a escuchar conexiones entrantes con listen, manteniendo una cola de hasta 10 clientes.
    // En el bucle principal, acepta conexiones una por una con accept. Al establecerse la conexión, imprime en consola
    // la dirección y el puerto del cliente y entra en un bucle dedicado a la comunicación con ese cliente. En cada
    // iteración recibe datos con recv, verificando si el cliente cerró la conexión (cuando recv devuelve 0). Si se
    // recibe un mensaje, se guarda en el buffer, se imprime en la consola del servidor y luego se construye una
    // respuesta que indica cuántos bytes se recibieron y un eco del mismo mensaje. Esta respuesta se envía de vuelta
    // al cliente usando send. Cuando el cliente cierra la conexión o ocurre un error, el servidor cierra el descriptor
    // de esa conexión y vuelve a esperar nuevos clientes. El programa se ejecuta indefinidamente hasta que se detenga
    // manualmente. La entrada del servidor son los mensajes enviados por los clientes a través de sockets TCP, y la
    // salida consiste en imprimir por consola los mensajes recibidos y responder a cada cliente con una cadena del
    // tipo "OK N bytes recibidos | eco: mensaje". Un ejemplo de interacción sería: si un cliente envía la cadena
    // "hola mundo", el servidor imprime "[Servidor] Recibido: hola mundo" y responde al cliente con "OK 11 bytes
    // recibidos | eco: hola mundo". Cuando el cliente se desconecta, el servidor muestra en consola que la conexión
    // se cerró y continúa disponible para atender a nuevos clientes.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define PORT        18000
#define BACKLOG     10
#define BUF_SIZE    2048

int main(void) {
    int listen_fd = -1, conn_fd = -1;
    struct sockaddr_in addr, cliaddr;
    socklen_t clilen = sizeof(cliaddr);
    char buf[BUF_SIZE];

    // 1) Crear socket
    listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) {
        perror("socket");
        return 1;
    }

    // Reusar puerto inmediatamente tras cerrar
    int yes = 1;
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0) {
        perror("setsockopt SO_REUSEADDR");
        close(listen_fd);
        return 1;
    }

    // 2) Enlazar a 127.0.0.1:PORT (solo localhost)
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr) <= 0) {
        perror("inet_pton");
        close(listen_fd);
        return 1;
    }

    if (bind(listen_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(listen_fd);
        return 1;
    }

    // 3) Escuchar
    if (listen(listen_fd, BACKLOG) < 0) {
        perror("listen");
        close(listen_fd);
        return 1;
    }

    printf("[Servidor] Escuchando en 127.0.0.1:%d ...\n", PORT);

    for (;;) {
        // 4) Aceptar conexión
        conn_fd = accept(listen_fd, (struct sockaddr*)&cliaddr, &clilen);
        if (conn_fd < 0) {
            perror("accept");
            continue; // intenta aceptar otro
        }

        char ipstr[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &cliaddr.sin_addr, ipstr, sizeof(ipstr));
        printf("[Servidor] Conexión de %s:%d\n", ipstr, ntohs(cliaddr.sin_port));

        // 5) Atender al cliente hasta que cierre
        for (;;) {
            ssize_t n = recv(conn_fd, buf, sizeof(buf) - 1, 0);
            if (n < 0) {
                perror("[Servidor] recv");
                break;
            } else if (n == 0) {
                printf("[Servidor] Cliente cerró la conexión\n");
                break;
            }
            buf[n] = '\0';

            printf("[Servidor] Recibido: %s\n", buf);

            char reply[BUF_SIZE];
            snprintf(reply, sizeof(reply), "OK %ld bytes recibidos | eco: %s", (long)n, buf);

            if (send(conn_fd, reply, strlen(reply), 0) < 0) {
                perror("[Servidor] send");
                break;
            }
        }

        close(conn_fd);
        conn_fd = -1;
    }

    close(listen_fd);
    return 0;
}
