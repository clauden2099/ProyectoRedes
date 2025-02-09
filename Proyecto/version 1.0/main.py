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


