"""Dépendances FastAPI utilisées pour protéger les endpoints."""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token

# HTTPBearer indique à FastAPI et Swagger que l'on attend :
# Authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Vérifie le JWT puis retourne l'utilisateur correspondant en base."""

    # Sans en-tête Authorization, l'utilisateur n'est pas authentifié.
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # credentials.credentials contient uniquement la valeur du token,
        # sans le mot "Bearer".
        payload = decode_access_token(credentials.credentials)

        # sub contient le username placé dans le JWT lors du login.
        username = payload.get("sub")

    except jwt.ExpiredSignatureError:
        # Token correctement signé mais arrivé après sa date exp.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    except jwt.InvalidTokenError:
        # Token modifié, mal signé ou simplement invalide.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    if not username:
        # Un token sans identité exploitable ne peut pas authentifier quelqu'un.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Le JWT donne l'identité, puis on recharge l'utilisateur depuis PostgreSQL.
    user = db.scalar(
        select(User).where(User.username == username)
    )

    # Le compte peut avoir été supprimé après la création du token.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur inconnu",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Si cette fonction arrive jusqu'ici, l'appelant est authentifié.
    return user


def require_roles(*allowed_roles : str) : 
    """Fabrique une dépendance limitée à certains rôles"""
    def check_roles(
            # Authentification d'abord
            current_user : User = Depends(get_current_user)
    ) -> User : 
        
    # Ici l'utilisateur est connu : un refus devient donc un 403
        if current_user.role not in allowed_roles : 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rôle non autorisé pour cette action"
            )
        return current_user

    return check_roles