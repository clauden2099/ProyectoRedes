from src.models.Planes import Planes
from src import db
from datetime import datetime

def obtener_planes():
    return [ticket.to_dict() for ticket in Planes.query.all()]

#Agregar plan a la BD
def agrega(data):
    if "fecha" in data:
        data["fecha"] = datetime.fromisoformat(data["fecha"]).date()
    nuevoPlan = Planes(**data)
    db.session.add(nuevoPlan)
    db.session.commit()
    return nuevoPlan.to_dict()

#Actualizar plan BD
def actualizar(id, data):
    plan = Planes.query.get(id)
    if plan:
        data.pop('id', None)  # Evita actualizar el campo id
        for key, value in data.items():
            if key == 'fecha' and isinstance(value,str):
                #Convierte la cadena a objeto date
                try:
                    value = datetime.fromisoformat(value).date()
                except ValueError:
                    continue
            setattr(plan, key, value)
        db.session.commit()
        return plan.to_dict()  # Retorna el objeto actualizado como diccionario
    return None

#Eliminar Plan BD
def eliminar(id):
    plan = Planes.query.get(id)
    if plan:
        db.session.delete(plan)
        db.session.commit()
        return plan.to_dict()
    return None

