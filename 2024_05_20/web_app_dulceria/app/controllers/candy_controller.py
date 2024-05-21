from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.candy_model import Candy
from views import candy_view
from utils.decorators import role_required

candy_bp = Blueprint("candy", __name__)


@candy_bp.route("/candies")
@login_required
def list_candies():
    candies = Candy.get_all()
    return candy_view.list_candies(candies)


@candy_bp.route("/candies/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_candy():
    if request.method == "POST":
        marca = request.form["marca"]
        peso = float(request.form["peso"])
        origen = request.form["origen"]
        sabor = request.form["sabor"]
        candy = Candy(marca=marca, peso=peso, origen=origen, sabor=sabor)
        candy.save()
        flash("Dulce creado exitosamente", "success")
        return redirect(url_for("candy.list_candies"))
    return candy_view.create_candy()


@candy_bp.route("/candies/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_candy(id):
    candy = Candy.get_by_id(id)
    if not candy:
        return "Dulce no encontrado", 404
    if request.method == "POST":
        marca = request.form["marca"]
        peso = float(request.form["peso"])
        origen = request.form["origen"]
        sabor = request.form["sabor"]

        candy.update(marca=marca, peso=peso, origen=origen, sabor=sabor)
        flash("Dulce actualizado exitosamente", "success")
        return redirect(url_for("candy.list_candies"))
    return candy_view.update_candy(candy)


@candy_bp.route("/candies/<int:id>/delete")
@login_required
@role_required("admin")
def delete_candy(id):
    candy = Candy.get_by_id(id)
    if not candy:
        return "Dulce no encontrado", 404
    candy.delete()
    flash("Dulce eliminado exitosamente", "success")
    return redirect(url_for("candy.list_candies"))
  