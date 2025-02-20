from src.models.ticket import Ticket
from src import db
from datetime import datetime

def obtener_tickets():
    return [ticket.to_dict() for ticket in Ticket.query.all()]

#Agregar ticket a la BD
def agrega_ticket(data):
    if "fecha" in data:
        data["fecha"] = datetime.fromisoformat(data["fecha"]).date()
    nuevoTicket = Ticket(**data)
    db.session.add(nuevoTicket)
    db.session.commit()
    return nuevoTicket.to_dict()


def actualizarEstado(id, estado):
    # Buscar el ticket por id
    ticket = Ticket.query.get(id)
    if ticket:
        ticket.estado = estado
        db.session.commit()
        return ticket.to_dict()
    return None

def actualizar_ticket(id, data):
    ticket = Ticket.query.get(id)
    if ticket:
        data.pop('id', None)  # Evita actualizar el campo id
        for key, value in data.items():
            if key == 'fecha' and isinstance(value,str):
                #Convierte la cadena a objeto date
                try:
                    value = datetime.fromisoformat(value).date()
                except ValueError:
                    continue
            setattr(ticket, key, value)
        db.session.commit()
        return ticket.to_dict()  # Retorna el objeto actualizado como diccionario
    return None


def eliminar_ticket(id):
    ticket = Ticket.query.get(id)
    if ticket:
        db.session.delete(ticket)
        db.session.commit()
        return ticket.to_dict()
    return None
