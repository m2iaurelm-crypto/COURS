"""Modèles SQLAlchemy correspondant aux tables PostgreSQL."""

from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base) : 
    """Utilisateur pouvant s'authentifier auprès de l'API"""

    __tablename__ = "users"

    # Identifiant technique unique généré automatiquement.
    id : Mapped[int] = mapped_column(primary_key=True)

    # Nom utilisé lors du login 
    # unique=True empêche deux utilisateurs d'avoir le même username 
    username : Mapped[str] = mapped_column(String(50), unique=True , index= True)

    # On stocke unique le hash bcrypt, jamais le mot de passe en clair 
    password_hash : Mapped[str] = mapped_column(String(100))

class Observation(Base) : 

    __tablename__ = "observations"

    id : Mapped[int] = mapped_column(primary_key=True)

    indicator : Mapped[str] = mapped_column(String(100))

    region : Mapped[str] = mapped_column(String(100))

    year: Mapped[int] = mapped_column()

    value: Mapped[float] = mapped_column()

    unit : Mapped[str] = mapped_column(String(30))


    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    

    creator: Mapped["User"] = relationship("User")
# CREATE TABLE observations (
#     id SERIAL PRIMARY KEY,
#     indicator VARCHAR(100) NOT NULL,
#     region VARCHAR(100) NOT NULL,
#     year INTEGER NOT NULL,
#     value DOUBLE PRECISION NOT NULL,
#     unit VARCHAR(30) NOT NULL
# );