from src import db
from datetime import date

class Configuraciones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispositivo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    archivo_nombre = db.Column(db.String(255))  # Opcional, para guardar el nombre
    archivo_contenido = db.Column(db.LargeBinary)  # Para guardar el contenido

    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.isoformat(),
            "responsable": self.responsable,
            "archivo_nombre": self.archivo_nombre,
            # Usualmente no se incluye el contenido en la respuesta JSON
        }
