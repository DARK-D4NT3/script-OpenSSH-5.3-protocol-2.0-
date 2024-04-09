import ftplib
import socket

def scan_ftp(target, port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(target, port, timeout=5)
        ftp.login()  # Intenta iniciar sesión como usuario anónimo
        print("[+] FTP service found at {}:{}".format(target, port))
        # Realiza un análisis de vulnerabilidades básico aquí, por ejemplo:
        # - Verificar si se permite el acceso anónimo
        # - Listar los archivos y directorios disponibles
        # - Realizar otras operaciones básicas de FTP
        ftp.quit()
    except ftplib.error_perm as e:
        print("[-] FTP error:", e)
    except socket.error:
        print("[-] FTP connection failed or timed out.")

def main():
    target = input("Enter target IP address: ")
    # Escanear puertos FTP comunes
    ftp_ports = [21, 2121]  # Puertos FTP estándar y alternativos
    for port in ftp_ports:
        scan_ftp(target, port)

if __name__ == "__main__":
    main()

