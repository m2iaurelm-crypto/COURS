"""Tarification de la durée d'occupation d'un casier."""

from decimal import Decimal

TARIF_PREMIERE_JOURNEE = Decimal("4.00")
TARIF_JOUR_SUPPLEMENTAIRE = Decimal("2.50")
PLAFOND_FACTURATION = Decimal("16.50")


def calculer_prix_occupation(duree_jours: int) -> Decimal:
    """Calcule le prix d'une occupation en nombre de jours entamés."""
    if duree_jours is None or duree_jours <= 0:
        raise ValueError(f"Durée invalide : {duree_jours}")

    total = TARIF_PREMIERE_JOURNEE
    if duree_jours > 1:
        total += (duree_jours - 1) * TARIF_JOUR_SUPPLEMENTAIRE

    return min(total, PLAFOND_FACTURATION)
