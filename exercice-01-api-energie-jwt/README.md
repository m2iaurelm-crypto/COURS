# Exercice 01 — Sécuriser une API d'analyse énergétique

## Contexte

Vous travaillez sur une API FastAPI exposant des indicateurs de consommation électrique régionale.

Les données métier et les endpoints existent déjà.  
Votre mission est d'ajouter l'authentification JWT vue dans la **démo 01**.

Aucune base de données ni gestion de rôles n'est demandée.

## Objectifs

- conserver certains endpoints publics ;
- authentifier un utilisateur avec un mot de passe haché en bcrypt ;
- générer un JWT signé avec expiration ;
- protéger les endpoints analytiques avec un Bearer Token ;
- retourner `401` si le token est absent, invalide ou expiré.

## 1. Installation

Dans PowerShell, à la racine du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Préparer le hash du mot de passe

Compte utilisé pour l'exercice :

```text
Utilisateur : data_analyst
Mot de passe : Data2026!
```

Générer le hash bcrypt :

```powershell
python scripts/generate_password_hash.py
```

Saisir `Data2026!`, puis copier le hash obtenu dans :

```text
ENERGY_PASSWORD_HASH=...
```

du fichier `.env`.

## 3. Lancer l'API

```powershell
python -m uvicorn app.main:app --reload
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

## 4. Travail demandé

### Étape 1 — Configuration

Compléter `app/config.py` pour charger les variables du `.env`.

### Étape 2 — Mot de passe

Dans `app/security.py`, compléter `verify_password()`.

### Étape 3 — JWT

Dans `app/security.py` :

- compléter `create_access_token()` ;
- placer `sub`, `iat` et `exp` dans le payload ;
- compléter `decode_access_token()`.

### Étape 4 — Login

Compléter `POST /auth/login` dans `app/routers/auth.py`.

Identifiants incorrects :

```text
401 - Identifiants invalides
```

### Étape 5 — Protéger les analytics

Compléter `get_current_user()` dans `app/dependencies.py`.

Puis protéger :

```text
GET /analytics/resume
GET /analytics/top-regions
```

Doivent rester publics :

```text
GET /
GET /dataset/info
GET /regions
```

## 5. Vérifications dans Swagger

1. `/regions` fonctionne sans token.
2. `/analytics/resume` retourne `401` sans token.
3. `/auth/login` retourne un JWT avec les bons identifiants.
4. Après **Authorize**, `/analytics/resume` fonctionne.
5. `/analytics/top-regions` fonctionne avec le même token.
6. Un token modifié retourne `401`.
7. Après expiration du token, l'accès retourne `401`.

> Le token expire après 5 minutes pour faciliter la démonstration.

## Infos :

Les `TODO` indiquent les principales zones à compléter.
