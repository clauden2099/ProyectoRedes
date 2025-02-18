import subprocess
import re
import socket
import netifaces
import os
import time
from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup
from datetime import datetime


#Función para escanear las redes
def listar_redes():
    time.sleep(1)
    comando = "netsh wlan show network mode=bssid"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True, errors="replace")
    # Verificar si la salida es None
    if resultado.stdout is None:
        print("Error: No se pudo obtener la lista de redes.")
        return []
    redes = re.findall(r'SSID (\d+) : (.+)', resultado.stdout)
    return [nombre for _, nombre in redes]

#Función para conectar a una red selecionada
def conectar_red(ssid,password):
    print(f"Intentando conectar a {ssid}...")
    #Obtiene la contraseña de la red ya exsitente
    comando = f'netsh wlan show profile name="{ssid}" key=clear'
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    #Comprueba si la red existe en el sistema
    print("Comprueba si existe")
    if resultado.returncode == 0:
        print("Si existio")
        #Saca la contraseña
        coincidencia = re.search(r'Contenido de la clave\s*:\s*(.+)', resultado.stdout)
        print(coincidencia)
        claveExtraida = coincidencia.group(1).strip()
        print(claveExtraida)
        print(type(claveExtraida))
        #Verifica amabas contraseñas
        if claveExtraida == password:
            subprocess.run(f'netsh wlan connect name="{ssid}"', shell=True)
            return True
    #Registrar una red nueva si no esta en el sistema
    else:
        print("La red no está registrada. Creando perfil...")
        # Agregar credenciales a Windows
        comando2 = f'cmdkey /add:{ssid} /user:"WiFi" /pass:{password}'
        resultado2 = subprocess.run(comando2, shell=True, capture_output=True, text=True)
        if resultado2.returncode == 0:
            print(f" Credenciales para la red {ssid} agregadas exitosamente.")
            # Crear el perfil de red manualmente
            perfil_xml = f"""<?xml version="1.0"?>
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>{ssid}</name>
                <SSIDConfig>
                    <SSID>
                        <name>{ssid}</name>
                    </SSID>
                </SSIDConfig>
                <connectionType>ESS</connectionType>
                <connectionMode>auto</connectionMode>
                <MSM>
                    <security>
                        <authEncryption>
                            <authentication>WPA2PSK</authentication>
                            <encryption>AES</encryption>
                            <useOneX>false</useOneX>
                        </authEncryption>
                        <sharedKey>
                            <keyType>passPhrase</keyType>
                            <protected>false</protected>
                            <keyMaterial>{password}</keyMaterial>
                        </sharedKey>
                    </security>
                </MSM>
            </WLANProfile>
            """
            # Guardar el perfil en un archivo temporal
            perfil_path = f"{ssid}.xml"
            with open(perfil_path, "w", encoding="utf-8") as f:
                f.write(perfil_xml)
            # Agregar el perfil de Wi-Fi
            subprocess.run(f'netsh wlan add profile filename="{perfil_path}"', shell=True)

            # Conectarse a la red agregada
            print("Conectando a la red...")
            resultado_conexion = subprocess.run(f'netsh wlan connect name="{ssid}"', capture_output=True, text=True, shell=True)
            time.sleep(3)
            
            #Verifica si se conecto a internet
            resultado_ping = subprocess.run('ping -n 1 www.google.com', capture_output=True, text=True, shell=True)
            #Si hay conexión quiere decir que el perfil guardado fue correcto
            if "TTL=" in resultado_ping.stdout:
                #Elimina el arhcivo xml del perfil de red
                os.remove(perfil_path)
                print("Conectado a Internet.")
                return True
            #Si no hay conexión quiere decir que el perfil de red estaba incorrecto
            else:
                print(f"Error al conectar a {ssid}: {resultado_conexion.stderr}")
                print("No hay conexión a Internet. Posiblemente la contraseña sea incorrecta.")
                os.remove(perfil_path) # Elimina el archivo xml
                # Eliminar el perfil de red temporal
                resultado_eliminar = subprocess.run(f'netsh wlan delete profile name="{ssid}"', capture_output=True, text=True, shell=True)
                if resultado_eliminar.returncode == 0:
                    print("Perfil de red temporal eliminado.")
                else:
                    print("Error al eliminar el perfil de red temporal.")
        print(f"No se pudieron agregar las credenciales para la red {ssid}.")
        return False
    

# Función para obtener el hostname de una IP
def obtener_hostname(ip):
    try:
        # Intenta obtener el nombre del host a partir de la IP
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "Desconocido"  # Si no se encuentra el hostname

# Función para obtener el fabricante de la tarjeta de red a partir de la MAC
def obtener_fabricante(mac):
    try:
        return MacLookup().lookup(mac)  # Busca el fabricante con mac-vendor-lookup
    except Exception:
        return "Desconocido"  # Si no se encuentra el fabricante

# Escanear la red con Scapy (paquetes ARP)
def escanear_red_scapy(red):
    print(f"\n Escaneando la red {red} con Scapy...\n")
    
    # Crear una solicitud ARP para preguntar qué dispositivos están activos en la red
    arp = ARP(pdst=red)  
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Dirección de broadcast para enviar la solicitud a todos
    paquete = ether / arp  # Combinar los paquetes

    # Enviar el paquete ARP y recibir respuestas
    resultado = srp(paquete, timeout=2, verbose=0)[0]

    dispositivos = []
    for enviado, recibido in resultado:
        ip = recibido.psrc  # IP del dispositivo
        mac = recibido.hwsrc  # MAC del dispositivo
        hostname = obtener_hostname(ip)  # Obtener el hostname
        fabricante = obtener_fabricante(mac)  # Obtener el fabricante con mac-vendor-lookup
        dispositivos.append((ip, hostname, mac, fabricante))  # Guardar los datos

    return dispositivos  # Retorna la lista de dispositivos encontrados

# Escanear la red con Nmap (comando `nmap -sn`)
def escanear_red_nmap(red):
    print(f"\n Escaneando la red {red} con Nmap...\n")
    
    # Ejecutar Nmap en modo escaneo de ping (-sn)
    comando = f"nmap -sn {red}"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)

    # Extraer IPs y hostnames de la salida de Nmap
    dispositivos = re.findall(r"Nmap scan report for (.+)", resultado.stdout)
    # Extraer direcciones MAC de la salida de Nmap
    macs = re.findall(r"MAC Address: ([\w:]+)", resultado.stdout)

    datos = []
    for i, dispositivo in enumerate(dispositivos):
        # Separar la IP y el hostname si están disponibles
        ip, hostname = (dispositivo.split(" ")[0], " ".join(dispositivo.split(" ")[1:])) if " " in dispositivo else (dispositivo, "Desconocido")
        mac = macs[i] if i < len(macs) else "No MAC"  # Si no hay MAC, colocar "No MAC"
        fabricante = obtener_fabricante(mac) if mac != "No MAC" else "No identificado"  # Obtener fabricante si hay MAC
        
        datos.append((ip, hostname, mac, fabricante))  # Guardar en la lista de dispositivos

    return datos  # Retorna la lista de dispositivos detectados por Nmap

# Función para mostrar los resultados de los escaneos
def mostrar_resultados(datos):
    if datos:
        print("Dispositivos conectados:")
        print(f"{'IP':<17}{'HOSTNAME':<30}{'MAC':<20}{'FABRICANTE'}")
        print("=" * 85)
        for dispositivo in datos:
            if len(dispositivo) == 3:  # Si viene de escanear_red_scapy (sin fabricante)
                ip, hostname, mac = dispositivo
                fabricante = "No identificado"
            else:  # Si viene de escanear_red_nmap
                ip, hostname, mac, fabricante = dispositivo
            
            print(f"{ip:<17}{hostname:<30}{mac:<20}{fabricante}")  # Imprimir formato tabla
    else:
        print(" No se encontraron dispositivos en la red.")

# Función para obtener la dirección base de la red local
def obtener_info_red():
    base_red = None
    interfaces = netifaces.interfaces()  # Obtener interfaces de red disponibles
    
    for interfaz in interfaces:
        direcciones = netifaces.ifaddresses(interfaz)
        
        if netifaces.AF_INET in direcciones:
            for direccion in direcciones[netifaces.AF_INET]:
                ip = direccion['addr']
                mascara = direccion['netmask']
                
                # Saltar interfaces loopback (127.0.0.1)
                if ip.startswith('127.'):
                    continue  

                # Calcular la dirección base de la red
                ip_bytes = list(map(int, ip.split('.')))
                mascara_bytes = list(map(int, mascara.split('.')))
                
                base_red_bytes = [ip_bytes[i] & mascara_bytes[i] for i in range(4)]
                base_red = '.'.join(map(str, base_red_bytes))
                
                print(f"Interfaz: {interfaz}")
                print(f"Dirección IP: {ip}")
                print(f"Máscara de subred: {mascara}")
                print(f"Dirección base de la red: {base_red}")
                print("-" * 40)
    
    return base_red  # Retorna la base de la red

#Escanear los dispositivos de red
def escanearRed():
    #Se obtiene la ip de la red
    ipRed = obtener_info_red()
    ipRed += "/24"
    print(ipRed)

    # Escaneo con ambos métodos
    dispositivosScapy = escanear_red_scapy(ipRed)
    dispositivosNmap = escanear_red_nmap(ipRed)

    # Diccionario para evitar duplicados basado en la IP
    dispositivos_unicos = {}

    for dispositivo in dispositivosScapy + dispositivosNmap:
        ip, hostname, mac, fabricante = dispositivo

        # Si el dispositivo ya está en el diccionario, fusionar datos
        if ip in dispositivos_unicos:
            # Si hay un hostname más detallado en otro escaneo, lo mantenemos
            if hostname == "Desconocido":
                hostname = dispositivos_unicos[ip][1]
            elif dispositivos_unicos[ip][1] == "Desconocido":
                dispositivos_unicos[ip] = (ip, hostname, mac, fabricante)

            # Si no se detectó fabricante en un escaneo, usar el del otro
            if fabricante == "No identificado":
                fabricante = dispositivos_unicos[ip][3]
            elif dispositivos_unicos[ip][3] == "No identificado":
                dispositivos_unicos[ip] = (ip, hostname, mac, fabricante)

        else:
            # Agregar el dispositivo al diccionario
            dispositivos_unicos[ip] = (ip, hostname, mac, fabricante)

    # Convertir de nuevo a lista para mostrar los resultados
    dispositivos_unicos = list(dispositivos_unicos.values())

    # Mostrar resultados
    mostrar_resultados(dispositivos_unicos)
    return dispositivos_unicos
