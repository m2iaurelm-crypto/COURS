"""Initialise la base avec la table users et deux comptes de démonstration."""

from sqlalchemy import select
from datetime import date
from app.database import Base, SessionLocal, engine
from app.models import User
from app.security import hash_password

from app import models
# create_all() crée les tables SQLAlchemy qui n'existent pas encore.
Base.metadata.create_all(bind=engine)

demo_users = [
    ("alice", "Formation2026!","analyst"),
    ("bob", "Data2026!","reader"),
]

with SessionLocal() as db:
    for username, plain_password,role in demo_users:

        # Évite de recréer le même compte si le script est relancé.
        existing_user = db.scalar(
            select(User).where(User.username == username)
        )

        if existing_user is not None:
            print(f"{username} existe déjà.")
            continue

        # Le mot de passe est haché AVANT son insertion en base.
        user = User(
            username=username,
            password_hash=hash_password(plain_password),
            role=role
        )

        db.add(user)
        print(f"{username} ajouté.")

    # commit() rend les insertions définitives dans PostgreSQL.
    db.commit()

    mediatheques = ["Centrale", "Jean Jaurès", "Médiathèque Sud", "Médiathèque Est"]
    observations = []
    
    for i in range(1, 25):
        m = mediatheques[i % len(mediatheques)]
        month = (i % 12) + 1
        year = 2024 if i <= 12 else 2025
        visiteurs = 800 + (i * 45) % 1200
        obs = models.Frequentation(
            mediatheque=m,
            mois=date(year, month, 1),
            visiteurs=visiteurs
        )
        observations.append(obs)

    db.add_all(observations)
    db.commit()
    db.close()
    print("Initialisation terminée : 24 observations et 2 utilisateurs créés.")
    print("Initialisation terminée.")

# python -m scripts.init_db

