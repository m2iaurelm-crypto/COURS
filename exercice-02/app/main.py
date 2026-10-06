"""Point d'entrée principal de l'API."""

from fastapi import FastAPI

from app.routers import auth, observations

app = FastAPI(
    title="Exercice 02 - JWT avec PostgreSQL",
    description="Authentification JWT avec utilisateurs stockés dans PostgreSQL.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(observations.router)


@app.get("/", tags=["Accueil"])
def root():
    """Confirme simplement que l'API fonctionne."""
    return {
        "message": "API démarrée",
        "documentation": "/docs",
    }

