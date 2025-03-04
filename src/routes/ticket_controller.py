# Importamos los módulos necesarios de Flask y los servicios de tickets
from flask import Blueprint, jsonify, request, render_template
from src.services.ticket import obtener_tickets, agrega_ticket, actualizarEstado, eliminar_ticket, actualizar_ticket

# Definimos un Blueprint para manejar las rutas relacionadas con los tickets
ticket_bp = Blueprint("ticket", __name__)

# Vista principal de tickets (se renderiza con Jinja usando el listado actual)
@ticket_bp.route("/tickets")
def view_tickets():
    # Obtiene la lista de tickets desde la base de datos
    tickets = obtener_tickets()
    # Renderiza la plantilla de tickets con los datos obtenidos
    return render_template("tickets.html", tickets=tickets)

# Controlador para agregar un nuevo ticket
@ticket_bp.route("/agregarTicket", methods=['POST'])
def agregar():
    data = request.get_json()  # Obtiene los datos enviados en formato JSON
    try:
        # Llama al servicio para agregar un nuevo ticket
        new_ticket = agrega_ticket(data)
        return jsonify({'success': True, 'ticket': new_ticket})
    except Exception as e:
        print("Error al agregar ticket:", e)  # Imprime el error en la consola del servidor
        return jsonify({'success': False, 'message': str(e)}), 400  # Devuelve un error en la respuesta JSON

# Controlador para actualizar el estado de un ticket
@ticket_bp.route("/actualizarEstado", methods=['POST'])
def actualizar_estado():
    data = request.get_json()  # Obtiene los datos enviados en JSON
    ticket_id = data.get('id')  # Extrae el ID del ticket
    nuevo_estado = data.get('nuevoEstado')  # Extrae el nuevo estado

    # Verifica si se proporcionó el ID
    if not ticket_id:
        return jsonify({'success': False, 'message': 'Falta el id'}), 400

    # Llama al servicio para actualizar el estado del ticket
    nuevoTicket = actualizarEstado(ticket_id, nuevo_estado)

    if nuevoTicket:
        return jsonify({'success': True, 'updated': nuevoTicket})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

# Controlador para actualizar un ticket completo
@ticket_bp.route("/actualizarTicket", methods=['POST'])
def actualizar_Ticket():
    data = request.get_json()  # Obtiene los datos enviados en JSON
    ticket_id = data.get('id')  # Extrae el ID del ticket

    # Verifica si se proporcionó el ID
    if not ticket_id:
        return jsonify({'success': False, 'message': 'Falta el id'}), 400

    # Llama al servicio para actualizar el ticket con los datos proporcionados
    actualizado = actualizar_ticket(ticket_id, data)

    if actualizado:
        return jsonify({'success': True, 'updated': actualizado})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

# Controlador para eliminar un ticket
@ticket_bp.route("/eliminarTicket", methods=['POST'])
def eliminar():
    data = request.get_json()  # Obtiene los datos enviados en JSON
    ticket_id = data.get('id')  # Extrae el ID del ticket

    # Verifica si se proporcionó el ID
    if not ticket_id:
        return jsonify({'success': False, 'message': 'Falta el id'}), 400

    # Llama al servicio para eliminar el ticket
    eliminando = eliminar_ticket(ticket_id)

    if eliminando:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404
