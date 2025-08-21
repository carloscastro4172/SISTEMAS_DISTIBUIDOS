    // Explicación del programa:
    // Este cliente TCP interactivo crea una nueva conexión con el servidor en cada iteración del bucle principal,
    // apuntando a la dirección 127.0.0.1 y al puerto 18000. La entrada del programa proviene del usuario por
    // stdin: primero se solicita una cadena (se espera en minúsculas, aunque no es requisito técnico) y luego
    // se pregunta si desea enviar otro mensaje mediante una confirmación “Y/N”. Con cada ciclo, el cliente crea
    // un socket, establece la conexión con el servidor, envía exactamente los bytes de la cadena escrita por el
    // usuario y espera una respuesta hasta 1024 bytes. La salida del programa consiste en imprimir en consola
    // la línea “From Server: …” con el contenido recibido o un aviso si el servidor cerró la conexión o no envió
    // datos. Tras procesar la respuesta, el socket se cierra antes de volver a preguntar si se desea continuar,
    // por lo que cada mensaje se maneja con una conexión independiente (mismo comportamiento que un cliente que
    // “conecta, envía, recibe y cierra” por mensaje). En Windows se realiza la inicialización y limpieza de Winsock
    // con WSAStartup/WSACleanup; en sistemas POSIX se usan socket(), connect(), send(), recv() y close() normales.
    // Si el usuario introduce una cadena vacía, no se envía nada y se informa en pantalla. Cuando el usuario responde
    // ‘N’ o ‘n’ a la pregunta “Other message: (Y/N)”, el bucle termina y el programa finaliza.

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
