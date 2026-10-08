import pytest
from src.consigne.casiers import choisir_taille_casier,casiers_compatibles

@pytest.mark.parametrize(
    "poids,resultat_attendu",
    [   
        pytest.param(2,"S",id="nominal taille S "),
        pytest.param(5,"S",id="veille borne taille M"),
        pytest.param(6,"M",id="borne taille  M"),
        pytest.param(12,"M",id="nominal taille  M "),
        pytest.param(15,"M",id="veille borne taille L"),
        pytest.param(16,"L",id="borne taille L"),
        pytest.param(25,"L",id="nominal taille L "),
        pytest.param(30,"L",id="maximum taille L ")
    ],
)
def test_choisir_taille_casier_selon_poids(poids,resultat_attendu):
    
    assert choisir_taille_casier(poids) == resultat_attendu


@pytest.mark.parametrize(
    "poids,resultat_attendu",
    [   
        pytest.param(None,"Poids invalide : ",id="Poids absent"),
        pytest.param(-1,"Poids invalide : -1",id="Poids négatif"),
        pytest.param(0,"Poids invalide : 0",id="Poids nul"),
        pytest.param(33,"Poids supérieur à la capacité maximale de 30 kg",id="Poids supérieur à 30 kg "),
    ],
)
def test_choisir_taille_casier_erreur_poids_absent_nul_negatif_trop_grand(poids,resultat_attendu) :
    with pytest.raises(ValueError) as exc:
        choisir_taille_casier(poids)
        assert resultat_attendu in (exc.value)


def test_casiers_compatibles_immuabilite_liste_entree(parc_casiers):
        copie_initiale = [dict(c) for c in parc_casiers]
        casiers_compatibles(parc_casiers, 5.0)
        assert parc_casiers == copie_initiale


def test_isolation_fixture_parc_casiers(parc_casiers):
    parc_casiers.append({"id": 99, "taille": "L", "libre": True})
    assert len(parc_casiers) == 7