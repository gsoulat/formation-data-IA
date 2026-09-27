# 02 — Dispersion : quand la moyenne ment

> 🎬 **Fil rouge.** Hier, Arras est sorti premier magasin avec **442 616,80 €** de commandes.
> Ce matin, son directeur appelle, gêné : *« Vous êtes sûr ? On a fait une année pourrie. »*
> Il a raison. Aujourd'hui, tu vas comprendre pourquoi Arras est à la fois premier et dernier.

| Jour | Durée démo | Mise en pratique |
|---|---|---|
| Mardi matin | 45 min | [Exercice guidé, partie B](05-exercice-guide-cyclonord.md) (après-midi) |

Pré-requis : [cours 01 — Position](01-statistiques-descriptives.md) (moyenne, médiane, plages nommées).

---

## Ce que tu sauras faire

- Calculer le minimum, le maximum, l'étendue et les quartiles d'une colonne.
- Dire en une phrase ce que mesure l'écart-type.
- Trouver les plus grosses valeurs avec `LARGE` et mesurer leur effet sur la moyenne.
- Calculer une médiane pour un seul magasin avec `MEDIAN(FILTER(...))`.
- Faire un histogramme dans Google Sheets et lire la forme des données.

---

## 1. Pourquoi la position ne suffit pas

Hier, tu as calculé la moyenne (1 679,77 €) et la médiane (177,00 €) de `Montant`. Ce sont des
indicateurs de **position** : ils disent où se trouve le « centre » des données.

Mais deux séries peuvent avoir le même centre et être très différentes. Une équipe qui vend 50 000 €
tous les mois et une équipe qui vend 5 000 € un mois puis 95 000 € le suivant ont la même moyenne.
La deuxième est bien plus difficile à prévoir.

La **dispersion**, c'est ça : à quel point les valeurs sont **étalées** autour du centre. Un résumé
honnête donne toujours les deux, la position et la dispersion.

Dans la démo, crée un onglet `Dispersion` : colonne A pour le nom de l'indicateur, colonne B pour la formule.

---

## 2. Minimum, maximum, étendue

Le plus simple : la plus petite valeur, la plus grande, et l'écart entre les deux. Cet écart
s'appelle l'**étendue**.

```
B2  =MIN(Montant)                    → 15,20 €
B3  =MAX(Montant)                    → 379 050,00 €
B4  =MAX(Montant)-MIN(Montant)       → 379 034,80 €
```

L'étendue ne regarde que **deux** commandes sur 613. Une seule valeur extrême suffit à la faire
exploser. Elle sert à situer les bornes, pas à décrire l'ensemble.

---

## 3. Les quartiles

Range mentalement les 613 montants du plus petit au plus grand, puis coupe la liste en quatre
paquets de même taille. Les trois points de coupe sont les **quartiles** :

- **Q1** (1er quartile) : 25 % des commandes sont en dessous ;
- **Q2** : 50 % en dessous, c'est la **médiane** ;
- **Q3** (3e quartile) : 75 % en dessous.

La fonction `QUARTILE` (QUARTILE) prend la plage et le numéro du quartile :

```
B5  =QUARTILE(Montant;1)             → 50,15 €
B6  =QUARTILE(Montant;2)             → 177,00 €      (= MEDIAN(Montant))
B7  =QUARTILE(Montant;3)             → 1 790,00 €
B8  =B7-B5                           → 1 739,85 €
```

La phrase à savoir dire : **« La moitié des commandes est comprise entre 50 € et 1 790 €. »**
C'est la moitié « du milieu », entre Q1 et Q3. L'écart Q3 − Q1 (1 739,85 €) s'appelle l'**écart
interquartile**.

Regarde aussi les distances : de Q1 à la médiane, il y a 127 €. De la médiane à Q3, plus de 1 600 €.
Les petites commandes sont serrées, les grosses sont très étalées. On dit que la distribution est
**étalée à droite**, comme on l'a vu hier avec l'écart entre moyenne et médiane.

---

## 4. L'écart-type, en une phrase

L'**écart-type** mesure la distance **typique** entre une valeur et la moyenne. Petit écart-type :
les valeurs sont proches de la moyenne. Grand écart-type : elles en sont loin. Il s'exprime dans la
même unité que les données, ici en euros.

La fonction est `STDEV` (ECARTYPE) :

```
B9  =STDEV(Montant)                  → 15 504,58 €
```

Comment le lire ? La moyenne est de 1 679,77 €, et l'écart-type est **neuf fois plus grand**. Les
commandes ne sont pas « un peu » autour de la moyenne : elles en sont très loin. Dans ce cas, la
moyenne ne décrit pas une commande « normale ».

Retiens juste ceci : comme la moyenne, l'écart-type est **sensible** aux valeurs extrêmes.

---

## 5. Les valeurs extrêmes

### Voir les plus grosses commandes avec `LARGE`

`LARGE` (GRANDE.VALEUR) donne la n-ième plus grande valeur d'une plage, sans trier ton tableau :

```
D2  =LARGE(Montant;1)                → 379 050,00 €
D3  =LARGE(Montant;2)                → 59 415,00 €
D4  =LARGE(Montant;3)                → 7 980,00 €
D5  =LARGE(Montant;4)                → 7 980,00 €
D6  =LARGE(Montant;5)                → 7 980,00 €
```

La troisième commande pèse 7 980 € (quatre commandes de 2 VAE à ce prix). Les deux premières sont
hors norme. Pour savoir de quelles lignes il s'agit **sans toucher à `Ventes_2025`**, affiche-les
avec `FILTER` : `=FILTER(Ventes_2025!A2:M614; Montant>=59415)` renvoie les deux lignes complètes.

| Commande | Magasin | Quantité | Montant | Statut |
|---|---|---|---|---|
| CMD-20250566 | Arras | 100 VAE | 379 050,00 € | **Annulée** |
| CMD-20250284 | Lens | 100 vélos urbains | 59 415,00 € | En cours |

### Et sans la commande de 379 050 € ?

`FILTER` (FILTRE) garde seulement les valeurs qui respectent une condition. Ici : tous les montants
différents de 379 050 (`<>` veut dire « différent de »). On l'emboîte dans les autres fonctions :

```
B11  =AVERAGE(FILTER(Montant;Montant<>379050))     → 1 063,15 €
B12  =MEDIAN(FILTER(Montant;Montant<>379050))      → 177,00 €
B13  =STDEV(FILTER(Montant;Montant<>379050))       → 2 707,51 €
B14  =MAX(FILTER(Montant;Montant<>379050))         → 59 415,00 €
```

| Indicateur | 613 commandes | Sans la commande de 379 050 € |
|---|---|---|
| Moyenne | 1 679,77 € | 1 063,15 € (−37 %) |
| Médiane | 177,00 € | 177,00 € (inchangée) |
| Écart-type | 15 504,58 € | 2 707,51 € (−83 %) |

**Une seule ligne sur 613** fait perdre plus d'un tiers à la moyenne. La médiane, elle, ne bouge pas
d'un centime. On dit que la médiane est **robuste** : elle résiste aux valeurs extrêmes. La moyenne
et l'écart-type ne le sont pas.

> ⚠️ **Extrême ne veut pas dire faux.** Tu n'as pas le droit de supprimer une ligne parce qu'elle
> te gêne. Tu peux la garder et signaler son effet, ou l'exclure **en le disant** et donner les deux
> chiffres. Supprimer sans trace, jamais.

---

## 6. La médiane d'un seul magasin : `MEDIAN(FILTER(...))`

Hier, `AVERAGEIFS` calculait une moyenne par groupe. Il n'existe pas de « MEDIANIFS ». On combine
donc `FILTER` et `MEDIAN` : `FILTER` garde les montants d'Arras, `MEDIAN` calcule leur médiane.

```
B16  =MEDIAN(FILTER(Montant;Magasin="Arras"))      → 90,00 €
B17  =MEDIAN(FILTER(Montant;Magasin="Lens"))       → 549,00 €
```

Arras a l'un des paniers médians les plus faibles du réseau (90 €), avec Valenciennes (92,20 €).

---

## 7. Le cas Arras

Trois chiffres, trois histoires :

```
B19  =SUMIFS(Montant;Magasin;"Arras")                        → 442 616,80 €
B20  =SUMIFS(Montant;Magasin;"Arras";Statut;"Livrée")        → 29 214,80 €
B21  =MEDIAN(FILTER(Montant;Magasin="Arras"))                → 90,00 €
```

- En **commandes passées**, Arras est **premier**, loin devant Lens (144 276,20 €).
- En **commandes livrées**, Arras est **dernier** des huit magasins.
- Son **panier médian** est parmi les plus faibles.

L'explication : la commande CMD-20250566 (100 VAE, 379 050 €, **annulée**) représente 86 % du
montant commandé à Arras. Elle gonfle le total, mais n'a jamais rapporté un euro. La médiane, elle, n'a
jamais menti : Arras vend surtout de petites commandes.

Ce que tu réponds au directeur : *« En chiffre livré, Arras est dernier avec 29 214,80 €. Le total
de 442 616,80 € vient d'une commande de flotte annulée. »*

---

## 8. Voir la forme : l'histogramme

Un **histogramme** découpe les montants en tranches (0 à 100 €, 100 à 200 €…) et dessine une barre
par tranche : plus la barre est haute, plus il y a de commandes dans cette tranche.

**Geste de démo :**

1. Dans `Ventes_2025`, sélectionne la colonne K (`Montant_TTC`).
2. *Insertion › Graphique*.
3. Dans l'éditeur, onglet *Configurer*, *Type de graphique* : choisis **Histogramme**.

Résultat attendu : presque toutes les barres sont vides, et une barre écrasée à gauche contient
presque tout. La commande de 379 050 € étire l'axe jusqu'à 380 000 € : on ne voit rien.

Pour lire la forme, regarde les commandes jusqu'à 5 000 €. Dans une colonne vide de `Dispersion`
(avec assez de cellules libres en dessous, 607 lignes) :

```
F1  =FILTER(Montant;Montant<=5000)               → 607 montants
```

Fais l'histogramme de cette colonne F. Les barres hautes sont à gauche (259 commandes font moins de
100 €), puis une longue traîne de barres basses vers la droite. C'est l'**étalement à droite** que
les quartiles annonçaient.

Précise toujours le périmètre : « commandes jusqu'à 5 000 € (607 sur 613) ».

---

## Mémo

| Besoin | Fonction ou geste | Exemple Cyclo'Nord |
|---|---|---|
| Bornes et étendue | `MIN`, `MAX`, `MAX-MIN` | 15,20 € → 379 050 € |
| Quartiles | `QUARTILE(plage;1)` / `;3` | Q1 50,15 € · Q3 1 790 € |
| Écart-type | `STDEV` (ECARTYPE) | 15 504,58 € |
| n-ième plus grande valeur | `LARGE(plage;n)` (GRANDE.VALEUR) | 379 050 € puis 59 415 € |
| Calcul sur un sous-ensemble | `MEDIAN(FILTER(plage;condition))` | Arras : 90,00 € |
| Voir la forme | *Insertion › Graphique* › Histogramme | étalé à droite |

---

## Auto-évaluation

- [ ] Je sais dire « la moitié des commandes est entre … et … » à partir de Q1 et Q3.
- [ ] Je sais expliquer l'écart-type en une phrase, sans formule.
- [ ] Je sais montrer qu'une seule commande change la moyenne mais pas la médiane.
- [ ] Je sais calculer la médiane d'un seul magasin avec `MEDIAN(FILTER(...))`.
- [ ] Je sais expliquer pourquoi Arras est à la fois premier et dernier.

---

➡️ **Cours suivant : [03 — Tableaux croisés dynamiques dans Sheets](03-tableaux-croises-dynamiques.md)**
