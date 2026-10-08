import pytest
from consigne.retrait import retrait_autorise



@pytest.mark.securite
def test_retrait_autorise_code_correct():   
    autorise = retrait_autorise("123456", "123456", 0)      
    assert autorise is True

@pytest.mark.securite
def test_retrait_refuse_code_incorrect(): 
    autorise = retrait_autorise("654321", "123456", 1)
    assert autorise is False


@pytest.mark.securite
@pytest.mark.parametrize(
    "tentatives, attendu",
    [
            (0, True),
            (1, True),
            (2, True),
            (3, False),  
            (4, False), 
    ],
        ids=["0_tentatives", "1_tentative", "2_tentatives", "3_tentatives_bloque", "4_tentatives_bloque"]
    )
def test_retrait_blocage_tentatives_echouees(tentatives, attendu):
    autorise = retrait_autorise("123456", "123456", tentatives)
    assert autorise is attendu


@pytest.mark.securite
@pytest.mark.parametrize(
    "code_invalide",
    ["12345", "1234567", "ABCDEF", "123A56", "", None],
    ids=["trop_court", "trop_long", "lettres", "alphanumerique", "vide", "none"]
)
def test_retrait_code_format_invalide(code_invalide):
    with pytest.raises(ValueError) as exc:
        retrait_autorise(code_invalide, "123456", 0)
        assert "Le code saisi doit contenir exactement 6 chiffres" in (exc.value)


@pytest.mark.securite
def test_retrait_tentatives_negatives_refusees():
    with pytest.raises(ValueError) as exc:
        retrait_autorise("123456", "123456", -1)
        assert "Le nombre de tentatives échouées est invalide" in (exc.value)
