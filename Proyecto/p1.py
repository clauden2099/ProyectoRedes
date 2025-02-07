import subprocess
import re
import socket
import ipaddress
import psutil

# Obtener las redes Wi-Fi disponibles
def listar_redes():
    resultado = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], capture_output=True, text=True)
    redes = re.findall(r'SSID (\d+) : (.+)', resultado.stdout)
    return [nombre for _, nombre in redes]

# Conectarse a una red Wi-Fi con SSID y contraseña
def conectar_wifi(ssid, password):
    print(f"🔗 Intentando conectar a {ssid}...")
    subprocess.run(f'netsh wlan connect name="{ssid}"', shell=True)
    subprocess.run(f'cmdkey /add:{ssid} /user:WiFi /pass:{password}', shell=True)

# Obtener dirección IP de la red
def obtener_direccion_ip():
    for interfaz, datos in psutil.net_if_addrs().items():
        for direccion in datos:
            if direccion.family == socket.AF_INET and not direccion.address.startswith("169.254"):
                return direccion.address
    return None

# Obtener máscara de subred
def obtener_mascara_subred():
    for interfaz, datos in psutil.net_if_addrs().items():
        for direccion in datos:
            if direccion.family == socket.AF_INET and direccion.netmask:
                return direccion.netmask
    return None

# Obtener la dirección de red
def obtener_direccion_red():
    ip_local = obtener_direccion_ip()
    mascara_subred = obtener_mascara_subred()

    if ip_local and mascara_subred:
        red = ipaddress.IPv4Network(f"{ip_local}/{mascara_subred}", strict=False)
        return str(red.network_address), red.prefixlen
    return None, None

# Escanear dispositivos en la red usando ARP y Nmap
def escanear_dispositivos():
    print("\n🔎 Escaneando dispositivos en la red...\n")

    ip_local, mascara_subred = obtener_direccion_ip(), obtener_mascara_subred()
    if not ip_local or not mascara_subred:
        print("❌ No se pudo obtener la IP y la máscara de subred.")
        return
    
    red = ".".join(ip_local.split(".")[:3]) + ".0/24"
    print(f"📡 Escaneando en la red: {red}\n")

    # Escaneo con arp -a
    print("🔹 Dispositivos detectados con ARP:")
    resultado_arp = subprocess.run("arp -a", capture_output=True, text=True)
    print(resultado_arp.stdout)

    # Escaneo con Nmap
    print("🔹 Dispositivos detectados con Nmap:")
    resultado_nmap = subprocess.run(f"nmap -sn {red}", shell=True, capture_output=True, text=True)
    print(resultado_nmap.stdout)

    # Intentar resolver los nombres de host de los dispositivos detectados
    print("🔹 Resolviendo nombres de host:")
    dispositivos = re.findall(r'(\d+\.\d+\.\d+\.\d+)', resultado_nmap.stdout)
    for ip in dispositivos:
        try:
            host = socket.gethostbyaddr(ip)
            print(f"🖥 {ip} -> {host[0]}")
        except socket.herror:
            print(f"⚠ {ip} -> No se pudo resolver el nombre")

# Listar redes Wi-Fi y permitir al usuario elegir una
redes_disponibles = listar_redes()
if redes_disponibles:
    print("\n📶 Redes disponibles:")
    for i, red in enumerate(redes_disponibles, 1):
        print(f"{i}. {red}")

    seleccion = int(input("\nSeleccione el número de la red a la que desea conectarse: ")) - 1
    if 0 <= seleccion < len(redes_disponibles):
        ssid = redes_disponibles[seleccion]
        password = input(f"Ingrese la contraseña para {ssid}: ")
        conectar_wifi(ssid, password)
    else:
        print("❌ Selección no válida.")
else:
    print("❌ No se encontraron redes disponibles.")

# Mostrar información de la red
print("\n🌐 Información de la red:")
print(f"📌 IP Local: {obtener_direccion_ip()}")
print(f"📌 Máscara de subred: {obtener_mascara_subred()}")

# Ejecutar escaneo de dispositivos en la red
escanear_dispositivos()
