"""Validation d'un code de retrait."""

LONGUEUR_CODE = 6
TENTATIVES_MAX = 3


def retrait_autorise(code_saisi: str, code_attendu: str, tentatives_echouees: int) -> bool:
    """Indique si le retrait peut être autorisé."""
    if code_saisi is None or code_attendu is None:
        raise ValueError("Les codes sont obligatoires")
    if len(code_attendu) != LONGUEUR_CODE or not code_attendu.isdigit():
        raise ValueError("Le code attendu doit contenir exactement 6 chiffres")
    if len(code_saisi) != LONGUEUR_CODE or not code_saisi.isdigit():
        raise ValueError("Le code saisi doit contenir exactement 6 chiffres")
    if tentatives_echouees is None or tentatives_echouees < 0:
        raise ValueError("Le nombre de tentatives échouées est invalide")

    # DÉFAUT VOLONTAIRE : après 3 échecs, le casier doit être bloqué.
    if tentatives_echouees >= TENTATIVES_MAX:
        return False

    return code_saisi == code_attendu
