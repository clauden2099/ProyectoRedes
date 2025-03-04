from src import db  # Importa la instancia de la base de datos desde el módulo src

# Define el modelo Inventario para gestionar los dispositivos en la base de datos
class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de cada dispositivo en el inventario
    dispositivo = db.Column(db.String(50), nullable=False)  # Nombre o tipo del dispositivo
    modelo = db.Column(db.String(50), nullable=False)  # Modelo específico del dispositivo
    totales = db.Column(db.Integer, nullable=False)  # Cantidad total de dispositivos registrados
    en_uso = db.Column(db.Integer, nullable=False)  # Cantidad de dispositivos actualmente en uso
    en_inventario = db.Column(db.Integer, nullable=False)  # Cantidad de dispositivos disponibles en inventario
    ubicacion = db.Column(db.String(100), nullable=False)  # Ubicación donde se encuentra el dispositivo

    # Método para convertir la instancia del modelo a un diccionario, útil para respuestas JSON
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
