"""Point d'entrée de l'API FastAPI."""

from fastapi import FastAPI

from app.routers import auth, frequentations,analytics


app = FastAPI(
    title="Démo 04 - Pagination, tests et Streamlit",
    description="API utilisée pour illustrer pagination, tests et front sécurisé.",
    version="2.0.0",
)


app.include_router(auth.router)
app.include_router(frequentations.router)
app.include_router(analytics.router)


@app.get("/", tags=["Accueil"])
def root():
    return {
        "message": "API démarrée",
        "documentation": "/docs",
    }
