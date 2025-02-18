from flask import Blueprint, jsonify, request, render_template
from src.services.planes import obtener_planes,agrega,actualizar,eliminar

plan_bp = Blueprint("plan", __name__)

# Vista principal de planes (se renderiza con Jinja usando el listado actual)
@plan_bp.route("/planes")
def ver_planes():
    planes = obtener_planes()
    return render_template("PlanesCorrecionPrevencion.html", planes=planes)

#Controlador para agregar un nuevo ticket
@plan_bp.route("/agregarPlan", methods=['POST'])
def agregar():
    data = request.get_json()
    try:
        nuevo = agrega(data)
        return jsonify({'success': True, 'plan': nuevo})
    except Exception as e:
        print("Error al agregar ticket:", e)
        return jsonify({'success': False, 'message': str(e)}), 400

#Controlador Actualizar plan
@plan_bp.route("/actualizarPlan", methods=['POST'])
def actualizar_plan():
    data = request.get_json()
    plan_id = data.get('id')
    if not plan_id:
        return jsonify({'scuess':False,'message':'Falta el id'}),400
    
    actualizado = actualizar(plan_id,data)
    if actualizado:
        return jsonify({'success': True, 'updated':actualizado})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404


#Controlador Eliminar plan
@plan_bp.route("/eliminarPlan", methods=['POST'])
def eliminar_plan():
    data = request.get_json()
    plan_id = data.get('id')
    if not plan_id:
        return jsonify({'scuess':False,'message':'Falta el id'}),400
    eliminando = eliminar(plan_id)
    if eliminando:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404