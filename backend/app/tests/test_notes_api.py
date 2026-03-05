def test_create_note(client):
    response = client.post(
        "/notes/",
        json={
            "title": "Nota test",
            "content": "Contenido de prueba"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Nota test"
    assert data["content"] == "Contenido de prueba"
    assert "id" in data


def test_list_notes(client):
    response = client.get("/notes/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
