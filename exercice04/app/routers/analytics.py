"""Endpoint protégé consommé par le front Streamlit."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.dependencies import require_roles
from app.models import User,Frequentation

router = APIRouter(
    prefix="/analytics/bilan",
    tags=["Analytics"],
)


@router.get("")
def analyse_bilan(
    db : Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("analyst")
    ),
):
    nb_obs = db.query(Frequentation).count()
    if nb_obs == 0:
        return {"nb_observations": 0, "total_visiteurs": 0, "moyenne_visiteurs": 0.0}
    
    total_visiteurs = db.query(func.sum(Frequentation.visiteurs)).scalar() or 0
    moyenne = total_visiteurs / nb_obs
    return {"nb_observations": nb_obs, "total_visiteurs": total_visiteurs, "moyenne_visiteurs": moyenne}
