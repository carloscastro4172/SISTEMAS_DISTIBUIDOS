// server.c — Servidor TCP simple que reconoce mensajes "i|texto"
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
