"""Modèles SQLAlchemy correspondant aux tables PostgreSQL."""

from sqlalchemy import String,ForeignKey,DateTime,func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum 
from app.database import Base
from datetime import datetime


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

    # Le rôle détermine les actions autorisées.
    role : Mapped[str] = mapped_column( String(20), default="viewer")


class Dataset(Base) : 

    __tablename__ = "datasets"

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(String(100))

    description : Mapped[str] = mapped_column(String(100))

    source : Mapped[str] = mapped_column(String(100))

    format : Mapped[str] = mapped_column(String(30))

    is_public: Mapped[bool] = mapped_column()



class QualityStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"



class Quality_check(Base) : 

    __tablename__ = "quality_check"

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(String(100))

    checked_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    score : Mapped[int] = mapped_column()

    status : Mapped[QualityStatus] = mapped_column(SQLEnum(QualityStatus),nullable=False)

    comment : Mapped[str] = mapped_column(String(255))

    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    
    # creator: Mapped["User"] = relationship("User")
