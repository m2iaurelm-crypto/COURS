"""Endpoints publics de l'API énergétique."""

from fastapi import APIRouter

from app.data.energy import CONSUMPTION_DATA

router = APIRouter(tags=["Données publiques"])


@router.get("/dataset/info")
def dataset_info():
    """Informations générales sur le jeu de données."""
    return {
        "name": "Consommation électrique régionale",
        "year": 2024,
        "unit": "GWh",
        "rows": len(CONSUMPTION_DATA),
    }


@router.get("/regions")
def list_regions():
    """Liste des régions disponibles.

    Aucun Depends(get_current_user) :
    cet endpoint doit rester public.
    """
    return [row["region"] for row in CONSUMPTION_DATA]
