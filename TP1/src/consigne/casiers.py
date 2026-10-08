"""Règles métier de choix et d'utilisation des casiers."""

TAILLES = ("S", "M", "L")
CAPACITES_KG = {
    "S": 5,
    "M": 15,
    "L": 30,
}


def choisir_taille_casier(poids_kg: float) -> str:
    """Retourne le plus petit casier pouvant accueillir le colis."""
    if poids_kg is None or poids_kg <= 0:
        raise ValueError(f"Poids invalide : {poids_kg}")
    if poids_kg > CAPACITES_KG["L"]:
        raise ValueError("Poids supérieur à la capacité maximale de 30 kg")

    if poids_kg <= CAPACITES_KG["S"]:
        return "S"
    if poids_kg <= CAPACITES_KG["M"]:
        return "M"
    return "L"


def casiers_compatibles(casiers: list[dict], poids_kg: float) -> list[dict]:
    """Filtre les casiers libres capables d'accueillir le colis."""
    taille_minimale = choisir_taille_casier(poids_kg)
    index_minimal = TAILLES.index(taille_minimale)

    return [
        casier
        for casier in casiers
        if casier["libre"] and TAILLES.index(casier["taille"]) >= index_minimal
    ]
