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


#Ciclo del programa donde se ejecutan todas las 
#funciones principales del mismo
while ejecucionAplicacion:
    print("Opciones disponibles:")
    mostrar_menu(opciones)
    opcion = input("Ingresa una opcion: ")
    if opcion in opciones:
        #Lista las redes y se conecta a alguna
        if opcion == "1":
            pass
        #Escanea los dispositivos de la red
        if opcion == "2":
            pass
        #Registra y seguimiento de fallas
        if opcion == "3":
            pass
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
