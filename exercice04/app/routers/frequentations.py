"""Endpoint public illustrant la pagination."""

import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Frequentation
from app.schemas import FrequentationPage

router = APIRouter(
    prefix="/frequentations",
    tags=["Frequentations"],
)


@router.get("", response_model=FrequentationPage)
def list_frequentation(
    # Query() permet aussi de valider directement les paramètres.
    # page ne peut jamais être inférieur à 1.
    page: int = Query(default=1, ge=1),

    # La taille de page est limitée pour éviter des réponses trop volumineuses.
    page_size: int = Query(default=5, ge=1, le=50),

    db: Session = Depends(get_db),
):
    """Retourne une page de données.

    Aucun Depends(get_current_user) :
    cet endpoint est public.
    """

    # COUNT(*) permet de connaître le nombre TOTAL de lignes,
    # indépendamment de la page actuellement demandée.
    total = db.scalar(
        select(func.count()).select_from(Frequentation)
    ) or 0

    # Exemple :
    # page=1, page_size=5 -> offset=0
    # page=2, page_size=5 -> offset=5
    # page=3, page_size=5 -> offset=10
    offset = (page - 1) * page_size

    # offset() ignore les lignes des pages précédentes.
    # limit() limite le nombre de lignes retournées à la taille de page.
    freq_items = db.execute(
        select(Frequentation.mediatheque,Frequentation.visiteurs,Frequentation.mois)
        .order_by(Frequentation.mois)
        .offset(offset)
        .limit(page_size)
    ).all()
    items = [dict(row._mapping) for row in freq_items]
    # ceil() arrondit au nombre de pages supérieur.
    # Exemple : 21 éléments avec 5 éléments/page -> 5 pages.
    pages = math.ceil(total / page_size) if total else 0

    return FrequentationPage(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    )
