from flask import Blueprint, jsonify, request, render_template
from src.services.inventario import obtener_inventario, agregar_dispositivo, actualizar_dispositivo, eliminar_dispositivo

# Definir un Blueprint para manejar las rutas relacionadas con el inventario
inventario_bp = Blueprint("inventario", __name__)

# Ruta para mostrar la vista del inventario en la interfaz web
@inventario_bp.route("/inven")
def vista_inventario():
    print(type(obtener_inventario()))  # Imprime el tipo de dato del inventario para depuración
    inventario = obtener_inventario()  # Obtiene la lista de dispositivos en inventario
    print(inventario)  # Muestra el inventario en la consola (puede eliminarse en producción)
    return render_template("inventario.html", inventario=inventario)  # Renderiza la vista con los datos

# Ruta para agregar un nuevo dispositivo al inventario
@inventario_bp.route('/agregar', methods=['POST'])
def agregar():
    data = request.get_json()  # Obtiene los datos enviados en formato JSON
    # Se espera que 'data' incluya: dispositivo, modelo, totales, en_uso, en_inventario, ubicación
    try:
        nuevo = agregar_dispositivo(data)  # Llama a la función de servicio para agregar el dispositivo
        return jsonify({'success': True, 'id': nuevo['id']})  # Devuelve el ID del nuevo dispositivo
    except Exception as e:
        print("Error al agregar:", e)  # Registra el error en la consola
        return jsonify({'success': False}), 400  # Devuelve un error HTTP 400 si falla

# Ruta para actualizar un dispositivo existente en el inventario
@inventario_bp.route('/actualizar', methods=['POST'])
def actualizar():
    data = request.get_json()  # Obtiene los datos enviados en formato JSON
    id = data.get('id')  # Obtiene el ID del dispositivo a actualizar
    if not id:
        return jsonify({'success': False, 'message': 'Falta el id'}), 400  # Devuelve error si no hay ID

    actualizado = actualizar_dispositivo(id, data)  # Llama a la función para actualizar el dispositivo
    if actualizado:
        return jsonify({'success': True, 'updated': actualizado})  # Responde con éxito si se actualizó
    else:
        return jsonify({'success': False, 'message': 'Dispositivo no encontrado'}), 404  # Error si no existe

# Ruta para eliminar un dispositivo del inventario
@inventario_bp.route('/eliminar', methods=['POST'])
def eliminar():
    data = request.get_json()  # Obtiene los datos en formato JSON
    id = data.get('id')  # Obtiene el ID del dispositivo a eliminar
    eliminado = eliminar_dispositivo(id)  # Llama a la función de eliminación
    if eliminado:
        return jsonify({'success': True})  # Responde con éxito si se eliminó
    else:
        return jsonify({'success': False, 'message': 'Dispositivo no encontrado'}), 404  # Error si no existe
