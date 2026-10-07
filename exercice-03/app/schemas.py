"""Schémas Pydantic utilisés pour les entrées et sorties de l'API."""

from pydantic import BaseModel, ConfigDict,Field
from typing import Literal
from datetime import datetime

from app.models import QualityStatus
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

    role: Literal["viewer", "analyst", "manager"]




class DatasetCreate(BaseModel) : 
    name : str = Field(max_length=100)
    description : str = Field(max_length=100)
    source : str = Field(max_length=100)
    format : str = Field(max_length=30)
    is_public : bool 


class DatasetOut(DatasetCreate) : 
    id : int 
    name : str = Field(max_length=100)
    description : str = Field(max_length=100)
    source : str = Field(max_length=100)
    format : str = Field(max_length=30)
    is_public : bool 

    class Config:
            from_attributes = True




class Quality_checkCreate(BaseModel) : 
    name : str = Field(max_length=100)
    checked_at : datetime = Field(default_factory=datetime.now())
    score : int = Field(ge=0 , le=100)
    status : QualityStatus
    comment : str = Field(max_length=255) 
    dataset_id : int

class Quality_checkOut(BaseModel) :
    id : int 
    name : str = Field(max_length=100)
    checked_at : datetime = Field(default_factory=datetime.now())
    score : int = Field(ge=0 , le=100)
    status : QualityStatus
    comment : str = Field(max_length=255) 
    dataset_id : int 

