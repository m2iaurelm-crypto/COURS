"""Endpoints analytiques à sécuriser."""

from fastapi import APIRouter,Depends

from app.data.energy import CONSUMPTION_DATA
from app.schemas import CurrentUser
from app.dependencies import get_current_user
router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/resume")
def analytics_summary(current_user: CurrentUser = Depends(get_current_user)):
    """Retourne quelques indicateurs globaux.

    TODO :
    protéger cet endpoint avec get_current_user.
    """
    values = [row["consumption_gwh"] for row in CONSUMPTION_DATA]

    return {
        "year": 2024,
        "regions_count": len(values),
        "total_consumption_gwh": round(sum(values), 2),
        "average_consumption_gwh": round(sum(values) / len(values), 2),
    }


@router.get("/top-regions")
def top_regions(limit: int = 3, current_user: CurrentUser = Depends(get_current_user)):
    """Retourne les régions les plus consommatrices.
    """
    ordered = sorted(
        CONSUMPTION_DATA,
        key=lambda row: row["consumption_gwh"],
        reverse=True,
    )

    return ordered[:limit]
