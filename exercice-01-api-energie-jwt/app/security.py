"""Fonctions de sécurité à compléter pendant l'exercice."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import JWT_ALGORITHM,JWT_EXPIRE_MINUTES,JWT_SECRET

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare un mot de passe en clair avec un hash bcrypt."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(username: str) -> str:
    """Crée un JWT signé contenant l'identité de l'utilisateur."""
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        "sub" : username,
        "iat" : now,
        "exp" : expiration,
    }
    return jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Vérifie le JWT puis retourne son payload."""
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )
