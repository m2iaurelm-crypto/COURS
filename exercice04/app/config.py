"""Chargement de la configuration du backend."""

import os

from dotenv import load_dotenv

# Charge les variables du fichier .env.
load_dotenv()
POSTGRES_URL = os.environ["POSTGRES_URL"] 
DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_NAME = DATABASE_URL.split("/")[-1]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "15"))
