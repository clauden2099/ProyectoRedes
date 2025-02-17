from src import db
from datetime import date

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispositivo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    prioridad = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")  # "Pendiente" o "Resuelto"

    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat(),  # Convertimos la fecha a string ISO
            "responsable": self.responsable,
            "prioridad": self.prioridad,
            "estado": self.estado
        }
