"""Tests classiques de l'endpoint public."""


def test_items_publics_sans_token(client):
    """Un endpoint public se teste sans authentification particulière."""

    response = client.get(
        "/frequentations",
        params={
            "page": 1,
            "page_size": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 5
    assert data["total"] == 24
    assert data["pages"] == 5
    assert len(data["items"]) == 5


def test_pagination_page_2(client):
    """La page 2 doit commencer après les 5 premiers éléments."""

    response = client.get(
        "/frequentations",
        params={
            "page": 2,
            "page_size": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["items"][0]["mois"] == "2024-06"


def test_pagination_refuse_page_zero(client):
    """Query(ge=1) fait refuser automatiquement une page invalide."""

    response = client.get(
        "/frequentations",
        params={
            "page": 0,
            "page_size": 5,
        },
    )

    assert response.status_code == 422
