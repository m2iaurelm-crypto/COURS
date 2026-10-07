"""Point d'entrée principal de l'API."""

from fastapi import FastAPI

from app.routers import auth, dataset,quality_check,admin

app = FastAPI(
    title="Exercice 03 - JWT et roles avec PostgreSQL",
    description="Authentification JWT avec utilisateurs stockés dans PostgreSQL et filtre de l'accès au endpoint via leur rôle respectif.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(dataset.router)
app.include_router(quality_check.router)
app.include_router(admin.router)


@app.get("/", tags=["Accueil"])
def root():
    """Confirme simplement que l'API fonctionne."""
    return {
        "message": "API démarrée",
        "documentation": "/docs",
    }

