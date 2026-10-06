# Exercice 02 — API d'indicateurs territoriaux sécurisée

## Contexte

Vous devez développer une API REST destinée à exposer et administrer des **indicateurs territoriaux** utilisés par une équipe de Data Analysts.

L'API doit permettre à n'importe quel client de **consulter les données publiquement**, mais toute modification des données doit nécessiter une authentification JWT valide.

Technologies imposées :

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **bcrypt**
- **JWT**
- configuration sensible dans un fichier `.env`

## Authentification

L'API doit proposer :

```text
POST /auth/register
POST /auth/login
```

L'inscription est publique.

Un utilisateur contient au minimum :

```text
id
username
password_hash
```

Le mot de passe ne doit jamais être stocké en clair.

Le JWT doit contenir au minimum :

```text
sub
iat
exp
```

## Données métier

L'API gère des observations d'indicateurs territoriaux.

Une observation contient au minimum :

```text
id
indicator
region
year
value
unit
```

Exemple :

```json
{
  "indicator": "Taux de chômage",
  "region": "Hauts-de-France",
  "year": 2025,
  "value": 8.7,
  "unit": "%"
}
```

## Endpoints à réaliser

### Consultation publique

Ces endpoints doivent fonctionner **sans JWT** :

```text
GET /observations
GET /observations/{id}
```

### Modification sécurisée

Ces endpoints doivent nécessiter un JWT valide :

```text
POST   /observations
PUT    /observations/{id}
DELETE /observations/{id}
```

Un token absent, invalide ou expiré doit empêcher l'opération.

## Comportements attendus

- `POST /auth/register`
  - crée un utilisateur ;
  - refuse un `username` déjà utilisé ;
  - hache le mot de passe avant insertion.

- `POST /auth/login`
  - recherche l'utilisateur en base ;
  - vérifie le mot de passe avec bcrypt ;
  - retourne un JWT si les identifiants sont corrects.

- `GET /observations`
  - public.

- `GET /observations/{id}`
  - public ;
  - retourne `404` si l'observation n'existe pas.

- `POST /observations`
  - authentification obligatoire ;
  - crée une observation.

- `PUT /observations/{id}`
  - authentification obligatoire ;
  - modifie une observation existante ;
  - retourne `404` si elle n'existe pas.

- `DELETE /observations/{id}`
  - authentification obligatoire ;
  - supprime une observation ;
  - retourne `404` si elle n'existe pas.

## Base PostgreSQL

Créer une base nommée :

```text
data_indicators
```

Le schéma attendu est fourni dans :

```text
sql/schema_reference.sql
```

Ce fichier sert uniquement de **référence de structure**. Les tables peuvent être créées avec SQLAlchemy.

## Configuration

Les valeurs suivantes doivent être placées dans `.env` :

```text
DATABASE_URL
JWT_SECRET
JWT_ALGORITHM
JWT_EXPIRE_MINUTES
```

## Contraintes

- utiliser SQLAlchemy pour PostgreSQL ;
- utiliser Pydantic pour les entrées/sorties ;
- ne jamais exposer `password_hash` ;
- ne jamais stocker le mot de passe en clair ;
- ne jamais écrire le secret JWT en dur dans le code ;
- séparer configuration, base, modèles, sécurité, dépendances et routers ;
- protéger les routes d'écriture avec `Depends(get_current_user)` ou un mécanisme équivalent ;
- ne pas ajouter de rôles : ils seront étudiés plus tard.

## Vérifications minimales dans Swagger

1. créer un utilisateur ;
2. se connecter ;
3. vérifier que `GET /observations` fonctionne sans authentification ;
4. vérifier que `POST /observations` retourne `401` sans token ;
5. utiliser **Authorize** avec le JWT ;
6. créer une observation ;
7. la consulter sans authentification ;
8. la modifier avec authentification ;
9. la supprimer avec authentification ;
10. vérifier qu'un token invalide ou expiré est refusé.
