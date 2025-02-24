from flask import Blueprint, jsonify, request, render_template, flash
from src.services.usuario import obtenerUsuario
from src.services.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__)

# Vista principal de tickets (se renderiza con Jinja usando el listado actual)
@usuario_bp.route("/login", methods=['GET', 'POST'])
def view_tickets():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        usuario = Usuario.query.filter_by(nombre=nombre).first()
        if usuario and usuario.password == password:
            return render_template("listaRedes.html")
        else:
            flash('Correo o contraseña invalidos')
    return render_template('login.html')



