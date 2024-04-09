from ftplib import FTP
import os
import schedule
import time

def backup_ftp_files(ftp_host, ftp_user, ftp_pass, remote_dir, local_dir):
    try:
        # Conexión al servidor FTP
        ftp = FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)

        # Cambiar al directorio remoto
        ftp.cwd(remote_dir)

        # Lista de archivos en el directorio remoto
        files = ftp.nlst()

        # Descargar cada archivo en el directorio remoto
        for filename in files:
            local_filename = os.path.join(local_dir, filename)
            with open(local_filename, 'wb') as local_file:
                ftp.retrbinary('RETR ' + filename, local_file.write)

        # Cerrar la conexión FTP
        ftp.quit()
        print("Backup completed successfully.")

    except Exception as e:
        print("An error occurred during backup:", e)

def main():
    # Configuración del servidor FTP y directorios
    ftp_host = 'ftp.example.com'
    ftp_user = 'username'
    ftp_pass = 'password'
    remote_dir = '/remote/directory'
    local_dir = '/local/directory'

    # Realizar copia de seguridad de archivos
    backup_ftp_files(ftp_host, ftp_user, ftp_pass, remote_dir, local_dir)

# Ejecutar la copia de seguridad cada día a la medianoche
schedule.every().day.at("00:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)  # Esperar 60 segundos antes de verificar si hay nuevas tareas a ejecutar

