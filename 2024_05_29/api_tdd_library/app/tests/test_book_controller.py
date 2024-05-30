def test_get_books(test_client, auth_headers_user):
    response = test_client.get("/api/books", headers=auth_headers_user)
    assert response.status_code == 200
    assert response.json == []

 
def test_create_book(test_client, auth_headers_user):
    data = {"title": "Lion", "author": "Panthera leo", "edition": 5, "diponibility": True}
    response = test_client.post("/api/books", json=data, headers=auth_headers_user)
    assert response.status_code == 201
    assert response.json["title"] == "Lion"


def test_get_book(test_client, auth_headers_user):
    # Primero crea un book
    data = {"title": "Tiger", "author": "Panthera tigris", "edition": 3, "diponibility": True}
    response = test_client.post("/api/books", json=data, headers=auth_headers_user)
    assert response.status_code == 201
    book_id = response.json["id"]

    # Ahora obtén el book
    response = test_client.get(f"/api/books/{book_id}", headers=auth_headers_user)
    assert response.status_code == 200
    assert response.json["title"] == "Tiger"


def test_update_book(test_client, auth_headers_user):
    # Primero crea un book
    data = {"title": "Elephant", "author": "Loxodonta", "edition": 10, "diponibility": True}
    response = test_client.post("/api/books", json=data, headers=auth_headers_user)
    assert response.status_code == 201
    book_id = response.json["id"]

    # Ahora actualiza el book
    update_data = {"title": "Elephant", "author": "Loxodonta africana", "edition": 12, "diponibility": True}
    response = test_client.put(
        f"/api/books/{book_id}", json=update_data, headers=auth_headers_user
    )
    assert response.status_code == 200
    assert response.json["author"] == "Loxodonta africana"
    assert response.json["edition"] == 12


def test_delete_book(test_client, auth_headers_user):
    # Primero crea un book
    data = {"title": "Giraffe", "author": "Giraffa camelopardalis", "edition": 7, "diponibility": True}
    response = test_client.post("/api/books", json=data, headers=auth_headers_user)
    assert response.status_code == 201
    book_id = response.json["id"]

    # Ahora elimina el book
    response = test_client.delete(f"/api/books/{book_id}", headers=auth_headers_user)
    assert response.status_code == 204

    # Verifica que el book ha sido eliminado
    response = test_client.get(f"/api/books/{book_id}", headers=auth_headers_user)
    assert response.status_code == 404
