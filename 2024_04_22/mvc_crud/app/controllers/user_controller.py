from flask import Blueprint, request, redirect, url_for

# Importamos la vista de usuarios
from views import user_view

# Importamos el modelo de usuario
from models.user_model import User

from datetime import datetime
# Un Blueprint es un objeto que agrupa
# rutas y vistas
user_bp = Blueprint("user", __name__)


# Definimos las rutas "/" asociada a la funcion usuarios
# que nos devuelve la vista de usuarios
@user_bp.route("/")
def usuarios():
    # Obtenemos todos los usuarios
    users = User.get_all()
    # Llamamos a la vista de usuarios
    return user_view.usuarios(users)


# Definimos la ruta "/users" asociada a la función registro
# que nos devuelve la vista de registro
@user_bp.route("/users", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        # Obtenemos los datos del formulario
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        # Creamos un nuevo usuario
        email = request.form['email']
        password = request.form['password']
        birthdate = request.form['birthdate']
        # Crear nuevo usuario
        user = User(first_name, last_name, email, password, datetime.strptime(birthdate, "%Y-%m-%d").date())
        # Guardamos el usuario
        user.save()
        # Redirigimos a la vista de usuarios
        # llamamos al blue print "user" y a la función usuarios
        return redirect(url_for("user.usuarios"))
    # Llamamos a la vista de registro
    return user_view.registro()


# Actualizar la información de un usuario por su id
# primero recuperamos la información del usuario
@user_bp.route("/users/<int:id>", methods=["GET"])
def obtener_usuario(id):
    # Obtenemos el usuario por su id
    user = User.get_by_id(id)
    if not user:
        return "Usuario no encontrado", 404
    return user_view.actualizar(user)


# Actualizamos la información del usuario por su id
# Ya estamos en la vista de actualizar
# por lo que obtenemos los datos del formulario
# y actualizamos la información del usuario
@user_bp.route("/users/<int:id>", methods=["POST"])
def actualizar(id):
    user = User.get_by_id(id)
    if not user:
        return "Usuario no encontrado", 404
    # Obtenemos los datos del formulario
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form['email']
    password = request.form['password']
    birthdate = request.form['birthdate']

    # Actualizamos los datos del usuario
    user.first_name = first_name
    user.last_name = last_name
    user.email =email
    user.password= password
    user.birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
    # Guardamos los cambios
    user.update()
    return redirect(url_for("user.usuarios"))


#Creamos el metodo delete
@user_bp.route("/usersd/<int:id>", methods=["GET"])
def eliminar(id):

    user =User.delete_by_id(id)
    if not user:
        return "Usuario no encontrado", 404
    return redirect(url_for("user.usuarios"))