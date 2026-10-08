"""Fixtures partagées par les tests d'API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """Appelle FastAPI en mémoire : Uvicorn n'est pas nécessaire."""

    with TestClient(app) as test_client:
        yield test_client


def _login_and_get_token(
    client: TestClient,
    username: str,
    password: str,
) -> str:
    """Effectue un vrai login comme le ferait un client de l'API."""

    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def analyst_token(client):
    """JWT appartenant à un utilisateur analyst."""

    return _login_and_get_token(
        client,
        "alice",
        "Formation2026!",
    )


@pytest.fixture(scope="session")
def reader_token(client):
    """JWT appartenant à un utilisateur reader."""

    return _login_and_get_token(
        client,
        "bob",
        "Data2026!",
    )
