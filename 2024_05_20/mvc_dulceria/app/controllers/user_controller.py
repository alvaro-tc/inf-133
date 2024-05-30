from flask import Blueprint, request, jsonify
from models.user_model import User
from views.user_view import render_users_list, render_user_detail
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from utils.decorators import jwt_required, roles_required

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_users():
    users = User.get_all()
    return jsonify(render_users_list(users))

@user_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_user(id):
    user = User.get_by_id(id)
    if user:
        return jsonify(render_user_detail(user))
    return jsonify({"error": "Usuario no encontrado"}), 404



@user_bp.route("/users", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def register():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    password = data.get("password")
    roles = data.get("roles")
    if not username or not password or not first_name or not last_name:
        return jsonify({"error": "Se requieren primer nombre, apellido, nombre de usuario y contraseña"}), 400
    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400
    new_user = User(first_name,last_name,username, password, roles)
    new_user.save()
    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/users/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(
            identity={"username": username, "roles": user.roles}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    
    
@user_bp.route("/users/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update():
    user = User.get_by_id(id)
    if not user:
        return "Usuario no encontrado", 404 
    data = request.json  
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    roles = data.get("roles")
    user = User.find_by_username(username)
    user.update(first_name=first_name, last_name=last_name, username=username, roles=roles)
    return jsonify(render_user_detail(user))

@user_bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete():
    user = User.get_by_id(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    user.delete()
    return "", 204

