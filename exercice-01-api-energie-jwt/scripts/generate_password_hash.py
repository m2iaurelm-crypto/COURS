"""Utilitaire pour générer le hash bcrypt utilisé dans .env."""

import getpass

import bcrypt

password = getpass.getpass("Mot de passe à hacher : ")
hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

print("\nHash bcrypt à copier dans .env :")
print(hashed.decode("utf-8"))
