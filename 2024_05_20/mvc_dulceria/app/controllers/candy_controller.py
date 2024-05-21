from flask import Blueprint, request, jsonify
from models.candy_model import Candy
from views.candy_view import render_candy_list, render_candy_detail
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from utils.decorators import jwt_required, roles_required

candy_bp = Blueprint("candy", __name__)




@candy_bp.route("/candys", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_candys():
    candys = Candy.get_all()
    return jsonify(render_candy_list(candys))



@candy_bp.route("/candys/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_candy(id):
    candy = Candy.get_by_id(id)
    if candy:
        return jsonify(render_candy_detail(candy))
    return jsonify({"error": "Dulce no encontrado"}), 404


@candy_bp.route("/candys", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_candy():
    data = request.json
    marca = data.get("marca")
    peso = data.get("peso")
    sabor = data.get("sabor")
    origen = data.get("origen")

    if not marca or not peso or not sabor or not origen:

        return jsonify({"error": "Faltan datos requeridos"}), 400
    candy = Candy(marca=marca, peso=peso, sabor=sabor, origen=origen)
    candy.save()

    return jsonify(render_candy_detail(candy)), 201


@candy_bp.route("/candys/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_candy(id):
    candy = Candy.get_by_id(id)

    if not candy:
        return jsonify({"error": "Dulce no encontrado"}), 404

    data = request.json
    data = request.json
    marca = data.get("marca")
    peso = data.get("peso")
    sabor = data.get("sabor")
    origen = data.get("origen")

    candy.update(marca=marca, peso=peso, origen=origen, sabor=sabor)

    return jsonify(render_candy_detail(candy))


@candy_bp.route("/candys/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_candy(id):
    candy = Candy.get_by_id(id)
    if not candy:
        return jsonify({"error": "Dulce no encontrado"}), 404
    candy.delete()
    return "", 204