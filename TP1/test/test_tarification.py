import pytest
from src.consigne.tarification import calculer_prix_occupation

# from calcul import additionner, soustraire, diviser,est_pair,multiplier

@pytest.mark.parametrize(
    "duree_jours,resultat_attendu",
    [
        pytest.param(1,4, id="Check prix premier jour 4 EUR"),
        pytest.param(3,9, id="Check jour supplémentaire 2.5 EUR(2 jours sup = 9 EUR)"),
        pytest.param(6,16.5, id="Check plafond à 16.5 EUR borne"),
        pytest.param(9,16.5, id="Check plafond à 16.5 EUR nominal"),
    ],
)
def test_calculer_prix_occupation_différents_prix(duree_jours,resultat_attendu):
    assert calculer_prix_occupation(duree_jours) == resultat_attendu

@pytest.mark.parametrize(
    "duree_jours,resultat_attendu",
    [
        pytest.param(0,f"Durée invalide : 0", id="Check error durée nulle"),
        pytest.param(-1,f"Durée invalide : -1", id="Check error durée négative"),
    ],
)
def test_calculer_prix_occupation_durée_nulle_négative(duree_jours,resultat_attendu):
    with pytest.raises(ValueError) as exc:
        calculer_prix_occupation(duree_jours)
        assert resultat_attendu in (exc.value)







