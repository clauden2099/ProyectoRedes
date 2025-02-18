from flask import Blueprint, jsonify, request, render_template
from src.services.ticket import obtener_tickets, agrega_ticket,actualizarEstado,eliminar_ticket,actualizar_ticket

ticket_bp = Blueprint("ticket", __name__)

# Vista principal de tickets (se renderiza con Jinja usando el listado actual)
@ticket_bp.route("/tickets")
def view_tickets():
    tickets = obtener_tickets()
    return render_template("tickets.html", tickets=tickets)

#Controlador para agregar un nuevo ticket
@ticket_bp.route("/agregarTicket", methods=['POST'])
def agregar():
    data = request.get_json()
    try:
        new_ticket = agrega_ticket(data)
        return jsonify({'success': True, 'ticket': new_ticket})
    except Exception as e:
        print("Error al agregar ticket:", e)
        return jsonify({'success': False, 'message': str(e)}), 400
    

#Controlador Actualizar Estado Ticket
@ticket_bp.route("/actualizarEstado", methods=['POST'])
def actualizar_estado():
    data = request.get_json()
    ticket_id = data.get('id')
    nuevo_estado = data.get('nuevoEstado')
    if not ticket_id:
        return jsonify({'scuess':False,'message':'Falta el id'}),400
    
    nuevoTicket = actualizarEstado(ticket_id,nuevo_estado)
    if nuevoTicket:
        return jsonify({'success': True, 'updated':nuevoTicket})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

#Controlador Actualizar ticket
@ticket_bp.route("/actualizarTicket", methods=['POST'])
def actualizar_Ticket():
    data = request.get_json()
    ticket_id = data.get('id')
    if not ticket_id:
        return jsonify({'scuess':False,'message':'Falta el id'}),400
    
    actualizado = actualizar_ticket(ticket_id,data)
    if actualizado:
        return jsonify({'success': True, 'updated':actualizado})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404

#Controlador Eliminar ticket
@ticket_bp.route("/eliminarTicket", methods=['POST'])
def eliminar():
    data = request.get_json()
    ticket_id = data.get('id')
    if not ticket_id:
        return jsonify({'scuess':False,'message':'Falta el id'}),400
    eliminando = eliminar_ticket(ticket_id)
    if eliminando:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404