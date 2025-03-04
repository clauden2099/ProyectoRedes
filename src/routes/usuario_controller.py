# Importamos los módulos necesarios de Flask y servicios relacionados con usuarios
from flask import Blueprint, jsonify, request, render_template, flash
from src.services.usuario import obtenerUsuario  # (No se usa en el código actual)
from src.services.usuario import Usuario  # Importamos el modelo de usuario

# Creamos un Blueprint para definir las rutas relacionadas con los usuarios
usuario_bp = Blueprint("usuario", __name__)

# Ruta para el inicio de sesión de usuarios
@usuario_bp.route("/login", methods=['GET', 'POST'])
def view_tickets():
    if request.method == 'POST':  # Si la solicitud es POST, procesamos el formulario
        nombre = request.form['nombre']  # Obtenemos el nombre de usuario ingresado
        password = request.form['password']  # Obtenemos la contraseña ingresada

        # Buscamos en la base de datos un usuario con el nombre proporcionado
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        # Si el usuario existe y la contraseña es correcta, redirigimos a la página de redes
        if usuario and usuario.password == password:
            return render_template("listaRedes.html")
        else:
            # Si la autenticación falla, mostramos un mensaje de error en la pantalla de login
            flash('Correo o contraseña inválidos')

    # Si la solicitud es GET o la autenticación falla, renderizamos el formulario de login
    return render_template('login.html')
