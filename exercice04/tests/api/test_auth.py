"""Tests simples de la route de connexion."""


def test_login_ok(client):
    """Des identifiants valides doivent retourner un JWT."""

    response = client.post(
        "/auth/login",
        json={
            "username": "alice",
            "password": "Formation2026!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["role"] == "analyst"
    assert data["access_token"]


def test_login_incorrect(client):
    """Un mauvais mot de passe doit produire 401."""

    response = client.post(
        "/auth/login",
        json={
            "username": "analyst01",
            "password": "mauvais-mot-de-passe",
        },
    )

    assert response.status_code == 401
