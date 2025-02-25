from flask import Blueprint, jsonify, request, render_template, current_app, send_file
from src.services.configuraciones import obtener_configuraciones,agrega,actualizar,eliminar
from src.utils.file_utils import allowed_file
import os
from io import BytesIO
from werkzeug.utils import secure_filename


configuracion_bp = Blueprint("configuracion_bp", __name__)

# Vista principal de planes (se renderiza con Jinja usando el listado actual)
@configuracion_bp.route("/configuracion")
def ver_configuraciones():
    configuraciones = obtener_configuraciones()
    return render_template("Configuracion.html", configuraciones=configuraciones)

#Controlador para agregar un nuevo ticket
@configuracion_bp.route("/agregarConfiguracion", methods=['POST'])
def agregar_configuracion():
    dispositivo = request.form.get('dispositivo')
    descripcion = request.form.get('descripcion')
    fecha = request.form.get('fecha')
    responsable = request.form.get('responsable')
    
    # Manejo del archivo
    archivo = request.files.get('archivo')
    archivo_nombre = None
    archivo_contenido = None

    if archivo and allowed_file(archivo.filename, current_app.config['ALLOWED_EXTENSIONS']):
        archivo_nombre = secure_filename(archivo.filename)
        # Si deseas guardar en la BD, lee el contenido:
        archivo_contenido = archivo.read()
        # Opcional: también puedes guardar el archivo en disco si lo necesitas
        # archivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], archivo_nombre)
        # archivo.seek(0)  # Reinicia el stream si lo vas a guardar en disco también
        # archivo.save(archivo_path)

    data = {
        "dispositivo": dispositivo,
        "descripcion": descripcion,
        "fecha": fecha,
        "responsable": responsable,
        "archivo_nombre": archivo_nombre,
        "archivo_contenido": archivo_contenido
    }
    try:
        nuevo = agrega(data)
        return jsonify({'success': True, 'configuracion': nuevo})
    except Exception as e:
        print("Error al agregar la configuracion:", e)
        return jsonify({'success': False, 'message': str(e)}), 400

#Controlador Actualizar plan
@configuracion_bp.route("/actualizarConfiguracion", methods=['POST'])
def actualizar_configuracion():
    # Se extraen los datos del formulario
    data = request.form.to_dict()
    configuracion_id = data.get('id')
    if not configuracion_id:
        return jsonify({'success': False, 'message': 'Falta el id'}), 400

    # Manejo del archivo (si se envía uno nuevo)
    archivo = request.files.get('archivo')
    if archivo and allowed_file(archivo.filename, current_app.config['ALLOWED_EXTENSIONS']):
        archivo_nombre = secure_filename(archivo.filename)
        archivo_contenido = archivo.read()
        data['archivo_nombre'] = archivo_nombre
        data['archivo_contenido'] = archivo_contenido

    actualizado = actualizar(configuracion_id, data)
    if actualizado:
        return jsonify({'success': True, 'updated': actualizado})
    else:
        return jsonify({'success': False, 'message': 'Configuracion no encontrada'}), 404


#Controlador Eliminar plan
@configuracion_bp.route("/eliminarConfiguracion", methods=['POST'])
def eliminar_configuracion():
    data = request.get_json()
    configuracion_id = data.get('id')
    if not configuracion_id:
        return jsonify({'scuess':False,'message':'Falta el id'}),400
    eliminando = eliminar(configuracion_id)
    if eliminando:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Configuracion no encontrada'}), 404
    

#Controlador Descargar Plan
@configuracion_bp.route('/descargarArchivoConfiguracion/<int:configuracion_id>')
def descargar_archivo(configuracion_id):
    # Se obtiene el plan según el id
    from src.models.configuraciones import Configuraciones  # Asegúrate de importar el modelo
    configuracion = Configuraciones.query.get(configuracion_id)
    if not configuracion or not configuracion.archivo_contenido:
        return "Archivo no encontrado", 404

    return send_file(
        BytesIO(configuracion.archivo_contenido),
        as_attachment=True,
        download_name=configuracion.archivo_nombre or "archivo",
        mimetype='application/octet-stream'
    )