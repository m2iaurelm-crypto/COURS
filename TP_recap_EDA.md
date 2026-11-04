# récap + TP final : Module EDA (Analyse Exploratoire de Données)

## 1. Fiche mémo — ce qu'il faut retenir du module

### 1.1 Les étapes d'une EDA, dans l'ordre

| #   | Étape                                                                            | Pourquoi                                              |
| --- | -------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1   | Premier coup d'œil (`shape`, `head`, `sample`, `info`)                           | Comprendre la taille et la structure brute            |
| 2   | Dictionnaire de données                                                          | Comprendre le sens métier de chaque colonne           |
| 3   | Valeurs manquantes (`isna`, `msno.matrix`, `msno.bar`)                           | Savoir où et combien de données manquent              |
| 4   | Doublons (`duplicated`)                                                          | Éviter de biaiser les statistiques                    |
| 5   | Typage des variables (quanti continue/discrète, quali nominale/ordinale)         | Choisir les bons outils statistiques/graphiques       |
| 6   | Stats univariées (`describe`, skew, kurtosis, `value_counts`)                    | Résumer chaque variable isolément                     |
| 7   | Visualisation univariée (histogramme, boxplot, countplot)                        | Voir la distribution, repérer l'asymétrie             |
| 8   | Détection des outliers (IQR, z-score)                                            | Repérer les valeurs extrêmes, comprendre leur origine |
| 9   | Analyse bivariée (scatterplot, heatmap de corrélation, crosstab, boxplot groupé) | Comprendre les relations entre variables              |
| 10  | Analyse multivariée (FacetGrid, pivot_table + heatmap)                           | Détecter des interactions entre plusieurs variables   |
| 11  | Analyse de la variable cible                                                     | Vérifier l'équilibre des classes avant le ML          |
| 12  | Synthèse / checklist de préprocessing                                            | Transition propre vers le Machine Learning            |

### 1.2 Lire le skewness et le kurtosis

| Indicateur               | Valeur            | Interprétation                                                |
| ------------------------ | ----------------- | ------------------------------------------------------------- |
| Skewness (asymétrie)     | ≈ 0               | Distribution quasi symétrique                                 |
| Skewness                 | `\|skew\| < 0.5`  | Asymétrie faible / négligeable                                |
| Skewness                 | `0.5` à `1`       | Asymétrie modérée                                             |
| Skewness                 | `> 1` (ou `< -1`) | Asymétrie forte → moyenne peu fiable, préférer la médiane     |
| Skewness                 | `> 0`             | Étalée à droite (queue de valeurs hautes)                     |
| Skewness                 | `< 0`             | Étalée à gauche (queue de valeurs basses)                     |
| Kurtosis (aplatissement) | ≈ 0               | Comportement proche d'une distribution normale (mésokurtique) |
| Kurtosis                 | `> 0`             | Queues lourdes, plus de valeurs extrêmes (leptokurtique)      |
| Kurtosis                 | `< 0`             | Distribution plus plate, moins d'extrêmes (platykurtique)     |

### 1.3 Quel graphique pour quel usage ?

| Graphique                  | Pour quelle variable ?                        | Ce qu'il montre                        | Limite principale                             |
| -------------------------- | --------------------------------------------- | -------------------------------------- | --------------------------------------------- |
| Histogramme                | 1 numérique                                   | Forme de la distribution               | Peu lisible si trop peu de valeurs distinctes |
| Boxplot                    | 1 numérique (ou 1 numérique x 1 catégorielle) | Médiane, quartiles, outliers           | Cache la forme fine (bimodalité)              |
| Violinplot                 | 1 numérique x 1 catégorielle                  | Boxplot + forme de la distribution     | Moins lisible pour un public non-technique    |
| Countplot                  | 1 catégorielle                                | Fréquence de chaque catégorie          | Illisible si trop de catégories               |
| Scatterplot                | 2 numériques                                  | Relation / nuage de points             | Illisible avec trop de points                 |
| Heatmap de corrélation     | n numériques                                  | Force des relations linéaires 2 à 2    | Ne capte pas les relations non-linéaires      |
| Pairplot                   | 3-8 numériques                                | Toutes les relations 2 à 2 en une fois | Très lourd au-delà de 8-10 variables          |
| Crosstab / barres empilées | 2 catégorielles                               | Répartition croisée                    | Illisible avec trop de catégories             |
| FacetGrid                  | 1 graphique x 1 variable de découpage         | Comparer un pattern entre sous-groupes | Surchargé si trop de sous-groupes             |

### 1.4 Pièges classiques à éviter

- Confondre une variable **numérique de façade** (ex : `pclass` = 1, 2, 3) avec une vraie variable
  continue : ici c'est une catégorielle **ordinale**.
- Utiliser la **moyenne** sur une distribution très asymétrique : préférer la **médiane**.
- Supprimer des outliers sans comprendre leur origine (erreur de saisie vs valeur rare mais réelle).
- Conclure à une causalité à partir d'une simple corrélation.
- Juger l'équilibre des classes uniquement "à l'œil" sans calculer les pourcentages exacts.

---

## 2. TP final —: Analyse exploratoire du dataset Palmer Penguins

**Chargement du dataset :**

```python
import seaborn as sns
df = sns.load_dataset("penguins")
```

**Colonnes du dataset :**

| Colonne             | Description                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| `species`           | Espèce du manchot (Adelie, Chinstrap, Gentoo) — **variable cible** pour un futur ML |
| `island`            | Île d'observation (Torgersen, Biscoe, Dream)                                        |
| `bill_length_mm`    | Longueur du bec (mm)                                                                |
| `bill_depth_mm`     | Profondeur du bec (mm)                                                              |
| `flipper_length_mm` | Longueur de la nageoire (mm)                                                        |
| `body_mass_g`       | Masse corporelle (g)                                                                |
| `sex`               | Sexe du manchot                                                                     |

### Objectifs

Produire un notebook (`TP_penguins.ipynb`) qui reproduit **toutes les étapes** de l'EDA (à l'aide du memo)

### Consignes étape par étape

1. **Premier coup d'œil** : affiche la forme du dataset, les 5 premières lignes, les types de colonnes.
2. **Valeurs manquantes** : ce dataset en contient (contrairement à ce qu'on pourrait croire au
   premier regard). Quantifie-les et visualise-les avec `missingno`. Quelle(s) colonne(s) sont concernées ?
3. **Doublons** : vérifie s'il y en a.
4. **Typage des variables** : classe chaque colonne (numérique continue/discrète, catégorielle
   nominale/ordinale).
5. **Statistiques univariées** : calcule `describe()`, le skewness et le kurtosis des 4 variables
   numériques. Laquelle est la plus asymétrique ?
6. **Visualisation univariée** :
   - Histogrammes des 4 variables numériques.
   - Countplot de `species` et de `island`.
7. **Outliers** : applique la méthode de l'IQR sur `body_mass_g`. Trouve-t-on des outliers ?
8. **Analyse bivariée** :
   - Heatmap de corrélation entre les 4 variables numériques.
   - Scatterplot `bill_length_mm` vs `bill_depth_mm`, coloré par `species`. Que remarques-tu de
     particulier sur la séparation des groupes ?
   - Boxplot de `body_mass_g` par `species`.
9. **Analyse multivariée** : un pairplot des 4 variables numériques avec `hue="species"`.
10. **Variable cible** : analyse la répartition de `species`. Les 3 classes sont-elles équilibrées ?
    Et la répartition par `island` — toutes les espèces vivent-elles sur toutes les îles ?
11. **Synthèse finale** : rédige, en 10 lignes maximum (dans une cellule Markdown), ce que tu
    retiens de cette exploration et ce qu'il faudrait faire avant d'entraîner un modèle de
    classification sur ce dataset.

### Grille d'auto-évaluation

Coche chaque case une fois le point traité dans ton notebook :

- [ ] Forme et structure du dataset identifiées
- [ ] Valeurs manquantes quantifiées ET visualisées
- [ ] Doublons vérifiés
- [ ] Chaque variable correctement typée
- [ ] Stats univariées calculées et commentées (moyenne vs médiane, skew)
- [ ] Au moins 1 histogramme + 1 countplot, avec interprétation
- [ ] Outliers détectés avec une méthode justifiée (IQR ou z-score)
- [ ] Au moins 1 scatterplot + 1 heatmap de corrélation, avec interprétation
- [ ] Au moins 1 boxplot catégorie x numérique, avec interprétation
- [ ] Répartition de la variable cible analysée (équilibre des classes)
- [ ] Synthèse finale rédigée
