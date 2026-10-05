"""Dépendance chargée de protéger les endpoints analytiques."""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import EXERCICE_USERNAME
from app.schemas import CurrentUser
from app.security import decode_access_token

# Déclare dans Swagger que l'API utilise un Bearer Token.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
        
) -> CurrentUser:
    """Retourne l'utilisateur si le Bearer Token est valide."""

    if credentials is None : 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate" : "Bearer"},
        )

    try: 
         # jwt.decode() contrôle également l'expiration.
         payload = decode_access_token(credentials.credentials)
         username = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate" : "Bearer"}, 
        ) from None
    except jwt.InvalidTokenError : 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate" : "Bearer"}, 
        ) from None

    if username != EXERCICE_USERNAME : 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate" : "Bearer"}, 
        ) 
    
    return CurrentUser(username=username)
