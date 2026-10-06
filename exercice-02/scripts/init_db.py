"""Initialise la base avec la table users et deux comptes de démonstration."""

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import User
from app.security import hash_password

# create_all() crée les tables SQLAlchemy qui n'existent pas encore.
Base.metadata.create_all(bind=engine)

demo_users = [
    ("alice", "Formation2026!"),
    ("bob", "Data2026!"),
]

with SessionLocal() as db:
    for username, plain_password in demo_users:

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
        )

        db.add(user)
        print(f"{username} ajouté.")

    # commit() rend les insertions définitives dans PostgreSQL.
    db.commit()

print("Initialisation terminée.")

# python -m scripts.init_db

