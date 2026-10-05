"""Configuration de l'application.

TODO :
- charger le fichier .env ;
- récupérer les informations utilisateur ;
- récupérer les paramètres JWT.
"""

import os

from dotenv import load_dotenv

load_dotenv()


# Utilisateur unique de cette première démonstration.
EXERCICE_USERNAME = os.environ["ENERGY_USERNAME"]
EXERCICE_PASSWORD_HASH = os.environ["ENERGY_PASSWORD_HASH"]

# Paramètres utilisés pour signer les JWT.
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "5"))
