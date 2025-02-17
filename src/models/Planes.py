from src import db
from datetime import date

class Planes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispositivo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    tipo_plan = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat(),  # Convertimos la fecha a string ISO
            "responsable": self.responsable,
            "tipo_plan": self.tipo_plan,
        }