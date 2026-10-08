"""Modèles SQLAlchemy de la démonstration."""

from sqlalchemy import String,ForeignKey,Date,CheckConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum 
from app.database import Base
from datetime import date


class User(Base):
    """Utilisateur pouvant s'authentifier."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    # Le mot de passe en clair n'est jamais enregistré.
    password_hash: Mapped[str] = mapped_column(String(100))

    # Utilisé pour illustrer le 403 dans les tests.
    role: Mapped[str] = mapped_column(String(20))


class Frequentation(Base):
    """Donnée simple utilisée pour illustrer la pagination."""

    __tablename__ = "frequentations"

    id: Mapped[int] = mapped_column(primary_key=True)
    mediatheque: Mapped[str] = mapped_column(String(50))
    mois: Mapped[date] = mapped_column(Date())
    visiteurs: Mapped[int] =mapped_column()
    
    __table_args__ = (
        CheckConstraint("visiteurs >= 0", name="check_visiteur_positif"),
    )
