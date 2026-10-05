"""Route d'authentification à compléter."""

from fastapi import APIRouter,HTTPException,status

from app.config import EXERCICE_PASSWORD_HASH,EXERCICE_USERNAME
from app.schemas import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest) -> TokenResponse:
    """Authentifie l'utilisateur puis retourne un JWT."""
    valid_username = data.username == EXERCICE_USERNAME
    valid_password = verify_password(data.password,EXERCICE_PASSWORD_HASH)
    if not valid_username or not valid_password : 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )
    token = create_access_token(data.username)
    return TokenResponse(access_token=token)