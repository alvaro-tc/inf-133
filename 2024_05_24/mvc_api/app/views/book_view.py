def render_book_list(books):
    # Representa una lista de bookes como una lista de diccionarios
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "edition": book.edition,
            "disponibility": book.disponibility
        }
        for book in books
    ]


def render_book_detail(book):
    # Representa los detalles de un book como un diccionario
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "edition": book.edition,
        "disponibility": book.disponibility
    }