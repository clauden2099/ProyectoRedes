from flask import Blueprint, jsonify, request, render_template
from src.services.inventario import obtener_inventario, agregar_dispositivo, actualizar_dispositivo, eliminar_dispositivo

inventario_bp = Blueprint("inventario", __name__)


#Regresa la vista del inventario
@inventario_bp.route("/inven")
def vista_inventario():
    print("Joto")
    print(type(obtener_inventario()))
    inventario = obtener_inventario();
    print(inventario)
    return render_template("inventario.html", inventario=inventario)


# Ruta para agregar un nuevo dispositivo
@inventario_bp.route('/agregar', methods=['POST'])
def agregar():
    data = request.get_json()
    # Asegúrate de que 'data' incluya los campos:
    # dispositivo, modelo, totales, en_uso, en_inventario, ubicacion
    try:
        nuevo = agregar_dispositivo(data)
        return jsonify({'success': True, 'id': nuevo['id']})
    except Exception as e:
        print("Error al agregar:", e)
        return jsonify({'success': False}), 400

# Ruta para actualizar un dispositivo existente
@inventario_bp.route('/actualizar', methods=['POST'])
def actualizar():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({'success': False, 'message': 'Falta el id'}), 400

    actualizado = actualizar_dispositivo(id, data)
    if actualizado:
        return jsonify({'success': True, 'updated': actualizado})
    else:
        return jsonify({'success': False, 'message': 'Dispositivo no encontrado'}), 404


@inventario_bp.route('/eliminar', methods=['POST'])
def eliminar():
    data = request.get_json()
    id = data.get('id')
    eliminado = eliminar_dispositivo(id)
    if eliminado:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Dispositivo no encontrado'}), 404

