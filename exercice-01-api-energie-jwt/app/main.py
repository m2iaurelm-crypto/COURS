"""Point d'entrée de l'API."""

from fastapi import FastAPI

from app.routers import analytics, auth, public

app = FastAPI(
    title="Energy Analytics API",
    description="Exercice de sécurisation JWT d'une API orientée Data Analyst.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(analytics.router)


@app.get("/", tags=["Accueil"])
def root():
    """Endpoint public permettant de vérifier que l'API fonctionne."""
    return {
        "message": "Energy Analytics API",
        "documentation": "/docs",
    }
