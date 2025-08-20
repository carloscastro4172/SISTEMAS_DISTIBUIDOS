
  #include <sys/types.h>
  #include <sys/socket.h>
  #include <netinet/in.h>
  #include <arpa/inet.h>
  #include <unistd.h>
  #include <errno.h>
  #define INVALID_SOCKET (-1)
  #define SOCKET_ERROR   (-1)
  typedef int SOCKET;


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SERVER_IP  "127.0.0.1"
#define SERVER_PORT 18000
#define BUF_SIZE 1024

static void strip_newline(char *s) {
    size_t n = strlen(s);
    if (n && (s[n-1] == '\n' || s[n-1] == '\r')) s[n-1] = '\0';
}

int main(void) {
#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) {
        fprintf(stderr, "WSAStartup failed\n");
        return 1;
    }
#endif

    int keep_going = 1;
    char line[BUF_SIZE];
    char yn[8];

    while (keep_going) {
        // Crear socket y conectar (igual que tu Python en cada ciclo)
#ifdef _WIN32
        SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
#else
        SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
#endif
        if (sock == INVALID_SOCKET) {
            perror("socket");
            break;
        }

        struct sockaddr_in serv;
        memset(&serv, 0, sizeof(serv));
        serv.sin_family = AF_INET;
        serv.sin_port = htons(SERVER_PORT);
        serv.sin_addr.s_addr = inet_addr(SERVER_IP);

        if (connect(sock, (struct sockaddr*)&serv, sizeof(serv)) == SOCKET_ERROR) {
            perror("connect");
#ifdef _WIN32
            closesocket(sock);
            WSACleanup();
#else
            close(sock);
#endif
            return 1;
        }

        printf("Input lowercase sentence: ");
        if (!fgets(line, sizeof(line), stdin)) {
            fprintf(stderr, "Error leyendo entrada\n");
            break;
        }
        strip_newline(line);

        // Enviar
        int to_send = (int)strlen(line);
        if (to_send == 0) {
            printf("Cadena vacía, no se envía nada.\n");
        } else {
            if (send(sock, line, to_send, 0) == SOCKET_ERROR) {
                perror("send");
#ifdef _WIN32
                closesocket(sock);
                WSACleanup();
#else
                close(sock);
#endif
                return 1;
            }

            // Recibir
            char buf[BUF_SIZE];
            int n = recv(sock, buf, sizeof(buf)-1, 0);
            if (n > 0) {
                buf[n] = '\0';
                printf("From Server: %s\n", buf);
            } else {
                printf("Servidor cerró la conexión o no envió datos.\n");
            }
        }

        // Cerrar socket de esta iteración
#ifdef _WIN32
        closesocket(sock);
#else
        close(sock);
#endif

        printf("Other message: (Y/N) ");
        if (!fgets(yn, sizeof(yn), stdin)) break;
        strip_newline(yn);
        if (yn[0] == 'N' || yn[0] == 'n') keep_going = 0;
    }

#ifdef _WIN32
    WSACleanup();
#endif
    return 0;
}