from src import db

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispositivo = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    totales = db.Column(db.Integer, nullable=False)
    en_uso = db.Column(db.Integer, nullable=False)
    en_inventario = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "dispositivo": self.dispositivo,
            "modelo": self.modelo,
            "totales": self.totales,
            "en_uso": self.en_uso,
            "en_inventario": self.en_inventario,
            "ubicacion": self.ubicacion
        }
