from flask import Blueprint, render_template, jsonify, request
from src.services.MetodosRed import escanearRed

escanearDispositivos_bp = Blueprint("dispositivos", __name__)


#Controladores de escaneo de dispositivos

#Método regersar la vista de dispostivos
@escanearDispositivos_bp.route("/listaDispositivos")
def listaDispositivos():
    return render_template("listaDispositivos.html")

#Método para escanear la red
@escanearDispositivos_bp.route("/escanear_red")
def escanearDipsotivosRed():
    dispositivos = escanearRed()
    dispositivos_json = [{"ip": d[0], "hostname": d[1], "mac": d[2], "fabricante": d[3]} for d in dispositivos]
    return jsonify({"dispositivos": dispositivos_json})

