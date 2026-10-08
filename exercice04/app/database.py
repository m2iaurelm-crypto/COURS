"""Connexion PostgreSQL avec SQLAlchemy."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL,POSTGRES_URL,DATABASE_NAME

# L'engine représente la connexion générale entre SQLAlchemy et PostgreSQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


engine_admin = create_engine(POSTGRES_URL, isolation_level="AUTOCOMMIT")

with engine_admin.connect() as connection:
    # Vérifier si la base existe
    result = connection.execute(
        text(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'")
    ).scalar()
    
    if not result:
        connection.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
        print("Base de données créée avec succès !")

# Fabrique une Session SQLAlchemy pour chaque requête qui en a besoin.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Classe de base commune aux modèles SQLAlchemy."""
    pass


def get_db():
    """Injecte une session puis la ferme après la requête."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
