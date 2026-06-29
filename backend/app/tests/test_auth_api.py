def test_register_and_login(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "strong-password"},
    )

    assert register_response.status_code == 200
    assert register_response.json()["email"] == "user@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "user@example.com", "password": "strong-password"},
    )

    assert login_response.status_code == 200
    body = login_response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_rejects_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "missing@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
