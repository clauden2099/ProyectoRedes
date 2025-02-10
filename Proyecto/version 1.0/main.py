#Librerías
import subprocess
import re
import os
from datetime import datetime

#Loop del programa
ejecucionAplicacion = True
#Opcion a ingresar
opcion = None

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
            # Listar las redes Wi-Fi disponibles
            listaRedes = listar_redes()
            print(type(listaRedes))
            # Comprueba si la lista de redes está vacía o no
            if listaRedes:
                print("Redes disponibles")
                # Se imprime la lista de redes
                for i, red in enumerate(listaRedes, 1):
                    print(f"{i}. {red}") 
        #Escanea los dispositivos de la red
        if opcion == "2":
            pass
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
