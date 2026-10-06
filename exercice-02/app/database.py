"""Configuration de la connexion PostgreSQL avec SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL



# L'engine représente la connexion générale entre SQLAlchemy et PostgreSQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,# Vérifie qu'une connexion du pool est encore valide avant usage.

)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase) : 
    """Classe de base dont héritent les modèles SQLAlchemy"""
    pass

def get_db() : 
    """Fournit une session SQLAlchemy à FastAPI puis la ferme proprement."""

    db = SessionLocal()

    try : 
        #yield permet à FastAPI d'injecter la sesson dans l'endpoint.
        yield db
    finally : 
        # La session est fermée même si l'endpoint provoque une erreur. 
        db.close()

