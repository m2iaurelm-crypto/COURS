"""E2E : le navigateur teste réellement Streamlit, FastAPI et PostgreSQL."""
from contextlib import asynccontextmanager
from playwright.sync_api import Page, expect
import time

URL = "http://127.0.0.1:8501"

@asynccontextmanager
async def test_connexion_et_donnees_securisees(page: Page):
    # Playwright pilote Chromium : ce n'est pas une simulation TestClient.
    page.goto(URL)
    await page.get_by_label("Connexion").wait_for(timeout=5000).check()
    page.get_by_label("Nom d'utilisateur").fill("alice")
    page.get_by_label("Mot de passe").fill("Formation2026!")
    page.get_by_role("button", name="Se connecter").click()

    #Le front s'est connecté et a conservé le JWT dans sa session.
    expect(page.get_by_text("Connecté en tant que : alice", exact=False)).to_be_visible()

    #Le KPI n'apparaît que si l'API a accepté le JWT.
    await page.get_by_label("Bilan (Privé)").check()
    expect(page.get_by_text("Bilan Analytique Métier", exact=True)).to_be_visible()
    expect(page.get_by_test_id("stMetricValue").get_by_text("24")).to_be_visible()


def test_pagination_publique(page: Page):
    # Le catalogue est visible même sans se connecter.
    page.goto(URL)
    expect(page.get_by_text("Page 1 / 5", exact=False)).to_be_visible()
    page.get_by_role("button", name="Suivant").click()
    expect(page.get_by_text("Page 2 / 5", exact=False)).to_be_visible()
