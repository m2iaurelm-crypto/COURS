"""Tests d'intégration de la sécurité JWT et des rôles."""


def test_secure_sans_token(client):
    """Aucune identité connue : 401."""

    response = client.get(
        "/analytics/bilan"
    )

    assert response.status_code == 401


def test_secure_avec_token_invalide(client):
    """Un faux JWT doit également produire 401."""

    response = client.get(
        "/analytics/bilan",
        headers={
            "Authorization": "Bearer faux-token"
        },
    )

    assert response.status_code == 401


def test_secure_reader_interdit(
    client,
    reader_token,
):
    """Le reader est authentifié mais n'a pas le bon rôle : 403."""

    response = client.get(
        "/analytics/bilan",
        headers={
            "Authorization": f"Bearer {reader_token}"
        },
    )

    assert response.status_code == 403


def test_secure_analyst_autorise(
    client,
    analyst_token,
):
    """L'analyst possède le rôle attendu : 200."""

    response = client.get(
        "/analytics/bilan",
        headers={
            "Authorization": f"Bearer {analyst_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["nb_observations"] == 24
    assert data["total_visiteurs"] == 32700
