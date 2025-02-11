#Librerías
import subprocess
import re
import os
from datetime import datetime
import socket
import netifaces
import time
from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup
from datetime import datetime

#Loop del programa
ejecucionAplicacion = True
#Opcion a ingresar
opcion = None
#Lista de redes
listaRedes = None
#Credenciales de la red
ssid = None
password = None
#Conectado a alguna red
redConectada = None

#Opciones disponibles para el usuario
opciones = {
    "1": "Ver redes disponibles y conectarse a una",
    "2": "Escanear dispositivos de la red",
    "3": "Registro y seguimiento de fallas",
    "4": "Inventario",
    "5": "Planes de prevención y corrección",
    "6": "Configuraciones",
    "7": "Salir"
}

#Opciones de fallas 
opcionesFallas = {
    "1": "Mostrar lista de fallas comunes",
    "2": "Abrir archivo de falla",
    "3": "Registrar nueva falla",
    "4": "Salir",
}
#ejecución Fallas
ejecucionFallas = True


# Menu de opciones
# Definir la función para mostrar el menú, que toma un diccionario de opciones como argumento
def mostrar_menu(opciones):
    # Crear el borde superior del menú
    borde_superior = "+" + "-" * 42 + "+"
    # El borde inferior es igual al borde superior
    borde_inferior = borde_superior
    # Imprimir el borde superior
    print(borde_superior)
    # Iterar sobre los elementos del diccionario de opciones
    for clave, valor in opciones.items():
        # Crear una línea para cada opción, justificando el valor a la izquierda
        linea = f"| {clave}: {valor.ljust(37)}|"
        # Imprimir la línea del menú
        print(linea)
    # Imprimir el borde inferior
    print(borde_inferior)

# Función para listar las redes Wi-Fi disponibles
def listar_redes():
    # Ejecutar el comando netsh para mostrar las redes Wi-Fi disponibles
    resultado = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], capture_output=True, text=True)
    # Buscar y extraer los SSID de las redes encontradas
    redes = re.findall(r'SSID (\d+) : (.+)', resultado.stdout)
    # Devolver una lista con los nombres de las redes
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




#Métodos de registro de fallas
#Busca los archivos de fallas en el sistema
def mostrar_fallas():
    # Obtiene la lista de archivos que terminan en '.txt' en el directorio actual
    archivos = [f for f in os.listdir() if f.endswith('.txt')]
    print("Fallas comunes:")
    # Muestra la lista de archivos de fallas
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo[:-4]}")
    return archivos

#Abre uno de los archivo de fallas
def abrir_archivo(archivos, eleccion):
    # Obtiene el archivo seleccionado por el usuario
    archivo_seleccionado = archivos[eleccion - 1]
    # Abre y lee el contenido del archivo utilizando codificación 'utf-8' para caracteres especiales
    with open(archivo_seleccionado, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    print("\nContenido del archivo:")
    print(contenido)
    # Abre el archivo con el programa 
    os.startfile(archivo_seleccionado)

#Crea un nuevo archivo de fallas de la red
def crear_archivo():
    # Solicita al usuario ingresar los detalles de la falla
    codigo = input("Ingrese el código de la falla (ej. NET-004): ")
    descripcion = input("Ingrese la descripción de la falla: ")
    causas = input("Ingrese las causas probables (separadas por comas): ").split(',')
    acciones = input("Ingrese las acciones recomendadas (separadas por comas): ").split(',')

    # Define el nombre del archivo basado en el código de la falla
    nombre_archivo = f"{codigo}.txt"
    # Obtiene la fecha y hora actual
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Crea y escribe en el archivo utilizando codificación 'utf-8'
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"[{fecha_hora}] [ERROR] Código: {codigo}\n")
        archivo.write(f"Descripción: {descripcion}\n\n")
        archivo.write("[Causa probable]\n")
        for causa in causas:
            archivo.write(f"- {causa.strip()}\n")
        archivo.write("\n[Acciones recomendadas]\n")
        for i, accion in enumerate(acciones, 1):
            archivo.write(f"{i}. {accion.strip()}\n")

    print(f"Archivo {nombre_archivo} creado exitosamente.")




#Ciclo del programa donde se ejecutan todas las 
#funciones principales del mismo
while ejecucionAplicacion:
    print("Opciones disponibles:")
    mostrar_menu(opciones)
    opcion = input("Ingresa una opcion: ")
    if opcion in opciones:
        #Lista las redes y se conecta a alguna
        if opcion == "1":
            listaRedes = listar_redes()
            print(type(listaRedes))
            #Comprueba si la lista de redes esta vacía o no
            if listaRedes:
                print("Redes disponibles")
                #Se imprime la lista de redes
                for i, red in enumerate(listaRedes, 1):
                    print(f"{i}. {red}")
                #Selecion de red a conectar
                seleccion = int(input("\nSeleccione el número de la red a la que desea conectarse: "))
                print(seleccion)
                if seleccion <= len(listaRedes):
                    print("Red selecionada")
                    ssid = listaRedes[seleccion-1]
                    password = input(f"Ingrese la contraseña para {ssid}: ")
                    redConectada = conectar_red(ssid, password)
                    if redConectada:
                        print("Conectado a la red exitosamente")
                    else:
                        print("Error en la conexión de la red")
                else:
                    print("Esa red no existe")
            else:
                print(" No se encontraron redes disponibles.")
        #Escanea los dispositivos de la red
        if opcion == "2":
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
        #Registra y seguimiento de fallas
        if opcion == "3":
            while ejecucionFallas:
                print("Opciones disponibles")
                # Muestra el menú principal de opciones
                mostrar_menu(opcionesFallas)
                opcion = input("Ingresa una opcion: ")
                if opcion in opciones:
                    if opcion == '1':
                        # Mostrar la lista de archivos de fallas
                        archivos = mostrar_fallas()
                    if opcion == '2':
                        # Mostrar la lista de archivos de fallas y permitir la selección de un archivo para abrirlo
                        archivos = mostrar_fallas()
                        try:
                            eleccion = int(input("Seleccione una falla (número): "))
                            if 1 <= eleccion <= len(archivos):
                                abrir_archivo(archivos, eleccion)
                            else:
                                print("Selección inválida.")
                        except ValueError:
                                print("Entrada inválida. Por favor, ingrese un número.")
                    elif opcion == '3':
                        # Crear un nuevo archivo de falla
                        crear_archivo()
                    elif opcion == '4':
                        # Salir al menú principal
                        print("Saliendo al menu principal...")
                        break
        #Inventario
        if opcion == "4":
            pass
        #Planes de prevención y correción
        if opcion == "5":
            pass
        #Configuraciones
        if opcion == "6":
            pass
        #Salir
        if opcion == "7":
            ejecucionAplicacion = False
    else:
        print("Esa opción no existe")
