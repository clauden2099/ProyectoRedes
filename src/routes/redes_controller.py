# Importamos los módulos necesarios de Flask y los servicios de redes
from flask import Blueprint, render_template, jsonify, request
from src.services.MetodosRed import listar_redes, conectar_red

# Definimos un Blueprint para manejar las rutas relacionadas con redes
listaRedes_bp = Blueprint("redes", __name__)

# Controlador para mostrar la vista de la lista de redes
@listaRedes_bp.route("/listaRedes")
def listaRedes():
    # Renderiza la plantilla que muestra las redes disponibles
    return render_template("listaRedes.html")

# Controlador para obtener la lista de redes disponibles
@listaRedes_bp.route("/listarRedes")
def listarRedes():
    print("Redes disponibles")  # Mensaje en la consola del servidor
    lista = listar_redes()  # Llama al servicio que obtiene las redes disponibles
    print(lista)  # Muestra la lista en la consola del servidor
    return jsonify(lista)  # Devuelve la lista en formato JSON

# Controlador para conectarse a una red Wi-Fi
@listaRedes_bp.route("/conectar", methods=['POST'])
def conectarRed():
    data = request.json  # Obtiene los datos enviados en JSON
    ssid = data.get("ssid")  # Extrae el nombre de la red Wi-Fi
    password = data.get("password")  # Extrae la contraseña

    # Intenta conectar a la red con los datos proporcionados
    if conectar_red(ssid, password):
        return jsonify({"mensaje": f"Conectado a {ssid}"}), 200

    # Si la conexión falla, devuelve un error con código 400
    return jsonify({"error": "No se pudo conectar a la red"}), 400
