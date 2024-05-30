from flask import Blueprint, request, jsonify

from app.models.book_model import Book
from app.views.book_view import render_book_list, render_book_detail
from app.utils.decorators import jwt_required, roles_required

 
# Crear un blueprint para el controlador de libros
book_bp = Blueprint("book", __name__)






# Ruta para obtener la lista de bookes
@book_bp.route("/books", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_books():
    books = Book.get_all()
    return jsonify(render_book_list(books))


# Ruta para obtener un book específico por su ID
@book_bp.route("/books/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_book(id):
    book = Book.get_by_id(id)
    if book:
        return jsonify(render_book_detail(book))
    return jsonify({"error": "Book no encontrado"}), 404


# Ruta para crear un nuevo book
@book_bp.route("/books", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    edition = data.get("edition")
    disponibility = data.get("disponibility")

    # Validación simple de datos de entrada
    
    if not title or not author or not edition or not disponibility:

        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo book y guardarlo en la base de datos
    book = Book(title=title, author=author, edition=edition, disponibility=disponibility)
    book.save()

    return jsonify(render_book_detail(book)), 201


# Ruta para actualizar un book existente
@book_bp.route("/books/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_book(id):
    book = Book.get_by_id(id)

    if not book:
        return jsonify({"error": "Book no encontrado"}), 404

    data = request.json
    title = data.get("title")
    author = data.get("author")
    edition = data.get("edition")
    disponibility = data.get("disponibility")
    # Actualizar los datos del book
    book.update(title=title, author=author, edition=edition, disponibility=disponibility)

    return jsonify(render_book_detail(book))


# Ruta para eliminar un book existente
@book_bp.route("/books/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_book(id):
    book = Book.get_by_id(id)

    if not book:
        return jsonify({"error": "Book no encontrado"}), 404

    # Eliminar el book de la base de datos
    book.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204