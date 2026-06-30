from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.services import auth


def test_register_rejects_existing_email(monkeypatch):
    monkeypatch.setattr(
        auth,
        "get_by_email",
        lambda db, email: SimpleNamespace(id=1, email=email),
    )

    with pytest.raises(HTTPException) as exc:
        auth.register_user(db=None, email="user@example.com", password="secret")

    assert exc.value.status_code == 400


def test_register_rejects_short_password(monkeypatch):
    monkeypatch.setattr(auth, "get_by_email", lambda db, email: None)

    with pytest.raises(HTTPException) as exc:
        auth.register_user(db=None, email="user@example.com", password="short")

    assert exc.value.status_code == 400
    assert "Password must be at least" in exc.value.detail


def test_register_hashes_password(monkeypatch):
    created_user = SimpleNamespace(id=1, email="user@example.com")
    captured = {}

    monkeypatch.setattr(auth, "get_by_email", lambda db, email: None)
    monkeypatch.setattr(auth, "hash_password", lambda password: f"hashed-{password}")
    monkeypatch.setattr(auth, "create_access_token", lambda payload: "token")

    def fake_create(db, email, hashed_password):
        captured["email"] = email
        captured["hashed_password"] = hashed_password
        return created_user

    monkeypatch.setattr(auth, "create", fake_create)

    user, token = auth.register_user(
        db=None,
        email="user@example.com",
        password="strong-password",
    )

    assert user == created_user
    assert token == "token"
    assert captured == {
        "email": "user@example.com",
        "hashed_password": "hashed-strong-password",
    }


def test_login_rejects_wrong_password(monkeypatch):
    monkeypatch.setattr(
        auth,
        "get_by_email",
        lambda db, email: SimpleNamespace(id=1, hashed_password="hashed"),
    )
    monkeypatch.setattr(auth, "verify_password", lambda password, hashed: False)

    with pytest.raises(HTTPException) as exc:
        auth.login_user(db=None, email="user@example.com", password="wrong")

    assert exc.value.status_code == 401


def test_login_returns_token_for_valid_credentials(monkeypatch):
    user = SimpleNamespace(id=7, hashed_password="hashed")
    monkeypatch.setattr(auth, "get_by_email", lambda db, email: user)
    monkeypatch.setattr(auth, "verify_password", lambda password, hashed: True)
    monkeypatch.setattr(auth, "create_access_token", lambda payload: "token")

    logged_user, token = auth.login_user(
        db=None,
        email="user@example.com",
        password="correct",
    )

    assert logged_user == user
    assert token == "token"
