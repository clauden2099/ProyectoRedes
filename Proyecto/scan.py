import nmap
import socket
import subprocess

def obtener_puerta_enlace():
    try:
        # Comando para obtener la puerta de enlace en Windows
        resultado = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lineas = resultado.stdout.splitlines()
        for linea in lineas:
            if 'Puerta de enlace predeterminada' in linea:
                return linea.split(':')[1].strip()
    except Exception as e:
        print(f"Error al obtener la puerta de enlace: {e}")
        return "Desconocida"

def obtener_mascara_subred(ip):
    try:
        # Comando para obtener la máscara de subred en Windows
        resultado = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lineas = resultado.stdout.splitlines()
        for linea in lineas:
            if ip in linea and "Máscara de subred" in linea:
                return linea.split(':')[1].strip()
    except Exception as e:
        print(f"Error al obtener la máscara de subred: {e}")
        return "Desconocida"

def escanear_dispositivos(red):
    escaner = nmap.PortScanner()

    # Escaneo de ping para descubrir hosts activos
    print(f"Escaneando la red {red}...")
    escaner.scan(hosts=red, arguments='-sn')

    puerta_enlace = obtener_puerta_enlace()
    mascara_subred = obtener_mascara_subred(red.split('/')[0])  # Obtener la IP base de la red

    dispositivos_conectados = []
    for host in escaner.all_hosts():
        if escaner[host].state() == 'up':
            try:
                nombre = escaner[host].hostname()
            except:
                nombre = "Desconocido"
            direccion_ip = escaner[host]['addresses']['ipv4']
            direccion_mac = escaner[host]['addresses'].get('mac', 'Desconocida')
            dispositivos_conectados.append((nombre, direccion_ip, direccion_mac))

    return dispositivos_conectados, puerta_enlace, mascara_subred

# Definir la red a escanear
red = "192.168.3.0/24"  # Asegúrate de que esta sea tu red correcta

# Escanear dispositivos en la red
dispositivos, puerta_enlace, mascara_subred = escanear_dispositivos(red)

print(f"Puerta de enlace: {puerta_enlace}")
print(f"Máscara de subred: {mascara_subred}")

print("\nDispositivos conectados en la red:")
for nombre, ip, mac in dispositivos:
    print(f"IP: {ip}, Nombre: {nombre}, MAC: {mac}")