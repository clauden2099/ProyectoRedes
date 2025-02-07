import subprocess
import re
import socket
import nmap

def listar_redes():
    resultado = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], capture_output=True, text=True)
    redes = re.findall(r'SSID (\d+) : (.+)', resultado.stdout)
    return [nombre for _, nombre in redes]

print(listar_redes())

def conectar_wifi(ssid, password):
    comando = f'netsh wlan connect name="{ssid}"'
    subprocess.run(comando, shell=True)
    print(f"Intentando conectar a {ssid}...")

conectar_wifi("HUAWEI-021K9M_Wi-Fi5", "PDF2099@")



#Mostrar ip local
def obtener_ip_local():
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    return ip_local

# Obtén la IP local
ip_local = obtener_ip_local()
print(f"Tu dirección IP local es: {ip_local}")


#Mostrar Dispositivos
def obtener_dispositivos():
    # Obtener la dirección IP de la red (ejemplo: 192.168.1.0/24)
    ip_red = "192.168.3.1/24"  # Modifica esto según tu red
    print("Desde aquí")
    # Escanear la red con nmap
    nm = nmap.PortScanner()
    print("Desde aquí")
    nm.scan(hosts=ip_red, arguments='-T4 -A')  # Escaneo intenso para obtener más información
    print("lUL")

    print("Dispositivos conectados:")
    for host in nm.all_hosts():
        print("En el for a shit jajaj")
        if nm[host].state() == 'up':  # Mostrar solo dispositivos activos
            print(f" - IP: {host}")
            if 'mac' in nm[host]['addresses']:
                mac = nm[host]['addresses']['mac']
                print(f"   MAC: {mac}")
            if 'vendor' in nm[host]['addresses']:
                vendor = nm[host]['addresses']['vendor']
                print(f"   Proveedor: {vendor}")
            if 'hostname' in nm[host]:
                hostname = nm[host]['hostname']
                print(f"   Nombre de host: {hostname}")
            if 'osmatch' in nm[host]:
                osmatch = nm[host]['osmatch']
                print(f"   Sistema operativo: {osmatch}")

# Ejecutar la función
obtener_dispositivos()