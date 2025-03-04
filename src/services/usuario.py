from src.models.usuario import Usuario
from src import db

def obtenerUsuario(id):
    return Usuario.query.get(id);