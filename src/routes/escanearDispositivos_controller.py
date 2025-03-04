from flask import Blueprint, render_template, jsonify, request
# Importamos la función que escanea la red para obtener los dispositivos conectados
from src.services.MetodosRed import escanearRed

# Se crea un Blueprint para manejar las rutas relacionadas con el escaneo de dispositivos
escanearDispositivos_bp = Blueprint("dispositivos", __name__)

# Controladores para el escaneo de dispositivos

# Ruta para renderizar la vista de la lista de dispositivos
@escanearDispositivos_bp.route("/listaDispositivos")
def listaDispositivos():
    return render_template("listaDispositivos.html")  # Muestra la interfaz con la lista de dispositivos

# Ruta para escanear la red y obtener los dispositivos conectados
@escanearDispositivos_bp.route("/escanear_red")
def escanearDipsotivosRed():
    dispositivos = escanearRed()  # Llama a la función que escanea la red
    # Convierte la lista de dispositivos en un formato JSON adecuado
    dispositivos_json = [{"ip": d[0], "hostname": d[1], "mac": d[2], "fabricante": d[3]} for d in dispositivos]
    return jsonify({"dispositivos": dispositivos_json})  # Devuelve la información en formato JSON
