from flask import Blueprint, render_template, jsonify, request
from src.services.MetodosRed import listar_redes, conectar_red

listaRedes_bp = Blueprint("redes", __name__)

#Controladoresd de Listar redes

#Regresa la vista de la lista de redes
@listaRedes_bp.route("/listaRedes")
def listaRedes():
    return render_template("listaRedes.html")

#Método para listar las redes disponibles
@listaRedes_bp.route("/listarRedes")
def listarRedes():
    print("Redes disponibles")
    lista = listar_redes()
    print(lista)
    return jsonify(lista)  # Devolvemos los datos en formato JSON

#Método para conectar a la red
@listaRedes_bp.route("/conectar", methods=['POST'])
def conectarRed():
    data = request.json
    ssid = data.get("ssid")
    password = data.get("password")
    if conectar_red(ssid,password):
        return jsonify({"Mensaje":f"conectado a {ssid}"}),200
    return jsonify({"Error":"No se pudo conectar a la red"}),400
