"""Schémas Pydantic utilisés pour les entrées et sorties de l'API."""

from pydantic import BaseModel, ConfigDict,Field,field_serializer
from typing import Literal,List
from datetime import date

class LoginRequest(BaseModel) : 
    """Données envoyées par le client lors de la connexion"""

    username : str
    password : str

class TokenResponse(BaseModel) : 
    """Réponse renvoyée après une authentification réussie"""

    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel) : 
    """Utilisateur exposé par l'API sans jamais révéler le password_hash"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str

class RegisterRequest(BaseModel) : 
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    username: str

    class Config:
        from_attributes = True

class RoleUpdateRequest(BaseModel):
    """Liste fermée des rôles acceptés."""

    role: Literal["reader", "analyst"]




class FrequentationCreate(BaseModel) : 
    mediatheque: str
    mois: date
    visiteurs: int

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("mois")
    def serialize_mois(self, mois: date) -> str:
        """Formate la date au format AAAA-MM pour l'API."""
        return mois.strftime("%Y-%m")


class FrequentationOut(FrequentationCreate) : 
    pass


class FrequentationPage(BaseModel):
    items: List[FrequentationOut]
    page: int
    page_size: int
    total: int
    pages: int
