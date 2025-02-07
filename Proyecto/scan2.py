import subprocess
import nmap
import socket
import ipaddress
import wifi

def listar_redes_wifi():
    try:
        redes = wifi.scan()
        nombres_redes = [red.ssid for red in redes]
        return nombres_redes
    except Exception as e:
        print(f"Error al listar redes Wi-Fi: {e}")
        return []

def conectar_a_wifi(nombre_red, contrasena):
    try:
        # Comando para conectar a la red Wi-Fi (adaptar según tu configuración)
        comando = f'netsh wlan connect name="{nombre_red}" ssid="{nombre_red}" keyMaterial="{contrasena}"'
        resultado = subprocess.run(comando, capture_output=True, text=True)
        print(resultado.stdout)
        return True
    except Exception as e:
        print(f"Error al conectar a Wi-Fi: {e}")
        return False

def obtener_direccion_de_red():
    try:
        # Obtener el nombre del host local
        nombre_host = socket.gethostname()
        # Obtener la dirección IP del host local
        direccion_ip = socket.gethostbyname(nombre_host)

        # Obtener la máscara de subred (esto es específico del sistema operativo)
        # Windows:
        resultado = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lineas = resultado.stdout.splitlines()
        for linea in lineas:
            if "Máscara de subred" in linea and direccion_ip in linea:
                mascara_subred = linea.split(":")[1].strip()
                break
        else:
            mascara_subred = "255.255.255.0"  # Valor por defecto si no se encuentra

        # Calcular la dirección de red
        direccion_red = ipaddress.IPv4Network(f"{direccion_ip}/{mascara_subred}", strict=False)
        return str(direccion_red.network_address) + "/" + str(direccion_red.prefixlen)

    except Exception as e:
        print(f"Error al obtener la dirección de red: {e}")
        return None

def escanear_dispositivos(red):
    escaner = nmap.PortScanner()

    # Escaneo de ping para descubrir hosts activos
    print(f"Escaneando la red {red}...")
    escaner.scan(hosts=red, arguments='-sn')

    # Obtener la puerta de enlace y la máscara de subred
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

# Listar redes Wi-Fi disponibles
redes_disponibles = listar_redes_wifi()

if redes_disponibles:
    print("Redes Wi-Fi disponibles:")
    for i, red in enumerate(redes_disponibles):
        print(f"{i + 1}. {red}")

    # Seleccionar red
    seleccion = int(input("Seleccione el número de la red a la que desea conectarse: ")) - 1
    nombre_red_seleccionada = redes_disponibles[seleccion]

    # Ingresar contraseña
    contrasena = input(f"Ingrese la contraseña para la red {nombre_red_seleccionada}: ")

    # Conectar a la red Wi-Fi
    if conectar_a_wifi(nombre_red_seleccionada, contrasena):
        # Obtener la dirección de red
        direccion_red = obtener_direccion_de_red()

        if direccion_red:
            # Escanear dispositivos
            dispositivos, puerta_enlace, mascara_subred = escanear_dispositivos(direccion_red)

            print(f"Puerta de enlace: {puerta_enlace}")
            print(f"Máscara de subred: {mascara_subred}")

            print("\nDispositivos conectados en la red:")
            for nombre, ip, mac in dispositivos:
                print(f"IP: {ip}, Nombre: {nombre}, MAC: {mac}")
        else:
            print("No se pudo obtener la dirección de red.")
    else:
        print("No se pudo conectar a la red Wi-Fi.")
else:
    print("No se encontraron redes Wi-Fi disponibles.")