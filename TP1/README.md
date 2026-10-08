# TP 1 — Tests unitaires d'une consigne automatique


Vous travaillez sur les règles métier d'un réseau de consignes automatiques.
Le projet est autonome : aucune base de données, API ou connexion réseau n'est nécessaire.

## Mise en place

Installez les dépendances puis exécutez la suite avec :

```text
python -m pip install -r requirements.txt
python -m pytest -v
```

## Travail demandé

Construisez une suite de tests unitaires fiable pour les trois modules du dossier
`src/consigne/`. Utilisez les techniques vues pendant le module : structure AAA,
noms explicites, cas nominaux, limites, erreurs, `pytest.raises`, fixtures,
`conftest.py` et paramétrage.

### 1. Tarification d'occupation

La fonction `calculer_prix_occupation(duree_jours)` doit respecter les règles suivantes :

- le premier jour coûte **4,00 €** ;
- chaque jour supplémentaire coûte **2,50 €** ;
- le prix total est plafonné à **16,50 €** ;
- une durée absente, nulle ou négative est refusée.

Testez notamment les frontières du plafond et les entrées invalides.

### 2. Choix des casiers

La fonction `choisir_taille_casier(poids_kg)` doit sélectionner le plus petit casier
compatible :

| Taille | Capacité maximale |
|---|---:|
| S | 5 kg |
| M | 15 kg |
| L | 30 kg |

Un poids absent, nul, négatif ou supérieur à 30 kg est refusé.

La fonction `casiers_compatibles(casiers, poids_kg)` doit retourner, dans le même ordre,
uniquement les casiers **libres** suffisamment grands. Elle ne doit pas modifier la liste
reçue.

Utilisez au moins une fixture métier, une fixture dépendant d'une autre fixture et un test
combinant **fixture + paramétrage**.

### 3. Validation d'un retrait

La fonction `retrait_autorise(code_saisi, code_attendu, tentatives_echouees)` applique ces règles :

- les codes contiennent exactement **6 chiffres** ;
- le retrait est autorisé uniquement si le code saisi correspond au code attendu ;
- après **3 tentatives échouées**, le casier est bloqué, même si le code devient correct ;
- un nombre de tentatives négatif est refusé.

Commencez par écrire les tests décrivant ces règles. Si un test révèle un défaut dans le
code fourni, conservez ce test, corrigez le code puis relancez toute la suite : ce test
devient un test de non-régression.

## Contraintes de réalisation

Votre solution doit comporter :

- un `conftest.py` avec plusieurs fixtures métier ;
- au moins une fixture dépendant d'une autre ;
- au moins **deux tests paramétrés**, avec des identifiants lisibles ;
- au moins un test combinant fixture et paramétrage ;
- des tests de cas nominaux, de frontières et d'erreurs ;
- au moins une vérification de message d'exception ;
- une suite entièrement verte à la fin.

Les valeurs attendues doivent être déterminées à partir des règles ci-dessus, pas calculées
en appelant le code testé.

## Bonus

1. Ajoutez un marqueur `securite` aux tests concernant le retrait et déclarez-le dans
   `pytest.ini`. Vérifiez `python -m pytest -m securite -v`.
2. Ajoutez un test démontrant que deux utilisations successives de la fixture `parc_casiers`
   ne partagent pas leurs modifications.
3. Utilisez `python -m pytest -k "casier" -v` pour exécuter uniquement les tests liés aux casiers.
