def auth_headers(client, email="user@example.com", password="strong-password"):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_notes_crud_flow(client):
    headers = auth_headers(client)

    create_response = client.post(
        "/api/v1/notes",
        json={
            "title": "Test note",
            "content": "Relevant content",
            "category_ids": [],
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Test note"
    assert created["content"] == "Relevant content"
    assert created["is_archived"] is False

    note_id = created["id"]

    list_response = client.get("/api/v1/notes", headers=headers)
    assert list_response.status_code == 200
    assert [note["id"] for note in list_response.json()] == [note_id]

    update_response = client.put(
        f"/api/v1/notes/{note_id}",
        json={"title": "Updated note", "content": "Updated content"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated note"

    archive_response = client.patch(
        f"/api/v1/notes/{note_id}/archive",
        headers=headers,
    )
    assert archive_response.status_code == 200
    assert archive_response.json()["is_archived"] is True

    active_response = client.get("/api/v1/notes", headers=headers)
    assert active_response.status_code == 200
    assert active_response.json() == []

    delete_response = client.delete(
        f"/api/v1/notes/{note_id}",
        headers=headers,
    )
    assert delete_response.status_code == 204


def test_notes_require_authentication(client):
    response = client.get("/api/v1/notes")

    assert response.status_code == 401
