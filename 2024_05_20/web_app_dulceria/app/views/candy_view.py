from flask import render_template
from flask_login import current_user


def list_candies(candies):
    return render_template(
        "candies.html",
        candies=candies,
        title="Lista de dulces",
        current_user=current_user,
    )


def create_candy():
    return render_template(
        "create_candy.html", title="Crear Dulce", current_user=current_user
    )

def update_candy(candy):
    return render_template(
        "update_candy.html",
        title="Editar Dulce",
        candy=candy,
        current_user=current_user,
    )