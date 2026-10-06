"""Schémas Pydantic utilisés pour les entrées et sorties de l'API."""

from pydantic import BaseModel, ConfigDict,Field


class LoginRequest(BaseModel) : 
    """Données envoyées par le client lors de la connexion"""

    username : str
    password : str

class TokenResponse(BaseModel) : 
    """Réponse renvoyée après une authentification réussie"""

    access_token : str
    token_type : str = "bearer"


class UserResponse(BaseModel) : 
    """Utilisateur exposé par l'API sans jamais révéler le password_hash"""

    model_config = ConfigDict(from_attributes=True)

    id: int 
    username : str 

class RegisterRequest(BaseModel) : 
    username : str 
    password : str 


class ObservationCreate(BaseModel) : 
    indicator : str = Field(max_length=100)
    region : str = Field(max_length=100)
    year : int
    value : float
    unit : str = Field(max_length=30)

class ObservationOut(ObservationCreate) : 
    id : int 