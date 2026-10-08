import pytest


@pytest.fixture
def parc_casiers():
    """
    Fixture fournissant un ensemble de casiers de différentes tailles et états.
    """
    return [
        {"id": 1, "taille": "S", "libre": True},
        {"id": 2, "taille": "S", "libre": False},
        {"id": 3, "taille": "M", "libre": True},
        {"id": 4, "taille": "M", "libre": False},
        {"id": 5, "taille": "L", "libre": True},
        {"id": 6, "taille": "L", "libre": False},
    ]


@pytest.fixture
def casiers_libres(parc_casiers):
    """
    Fixture dépendant de 'parc_casiers' retournant uniquement les casiers non occupés.
    """
    return [casier for casier in parc_casiers if casier["libre"]]

