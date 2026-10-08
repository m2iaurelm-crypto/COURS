"""Endpoint de connexion."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """Vérifie les identifiants puis délivre un JWT."""

    user = db.scalar(
        select(User).where(User.username == data.username)
    )

    # Même message si le compte n'existe pas ou si le mot de passe est faux.
    if user is None or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    token = create_access_token(
        username=user.username,
        role=user.role,
    )

    return TokenResponse(
        access_token=token,
        role=user.role,
    )
