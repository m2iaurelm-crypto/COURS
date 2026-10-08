"""Génère un secret aléatoire adapté à la signature JWT HS256."""

import secrets

print(secrets.token_hex(32))
