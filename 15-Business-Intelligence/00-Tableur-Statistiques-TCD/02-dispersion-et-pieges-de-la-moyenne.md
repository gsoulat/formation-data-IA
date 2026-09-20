# 02 — Dispersion : écart-type, quartiles et pièges de la moyenne

> 🎬 **Suite du fil rouge.**
> Hier soir, tu as envoyé à Nadia le classement des magasins par chiffre d'affaires. Arras arrive
> largement en tête : **442 617 €**, soit plus de quatre fois Lille. Ce matin, le directeur d'Arras
> t'appelle, gêné : *« Vous êtes sûr ? On a fait une année pourrie. »*
> Il a raison. Tu vas découvrir qu'Arras est à la fois **premier et dernier** du classement, selon la
> façon dont on regarde — et que ce n'est pas une contradiction, c'est une leçon de statistique.

| | |
|---|---|
| **Jour** | Mardi 22/09/2026 · matin (apport) + après-midi (exercice + correction) |
| **Durée** | ≈ 7 h |
| **Compétences** | **C3.1** (niveau 1) · **C4.2** (niveau 1) |
| **Données** | [`donnees/cyclonord_ventes_2025_fiable.xlsx`](donnees/cyclonord_ventes_2025_fiable.xlsx) |
| **Pré-requis** | [Cours 01 — moyenne, médiane, mode](01-statistiques-descriptives.md) |

---

## Objectifs pédagogiques

À la fin de la journée, tu sauras :

1. Expliquer pourquoi **deux jeux de données de même moyenne** peuvent raconter deux histoires opposées.
2. Calculer **étendue, variance, écart-type, quartiles et écart interquartile** au tableur.
3. Choisir entre `ECARTYPE.STANDARD` et `ECARTYPE.PEARSON` en sachant pourquoi.
4. Comparer la dispersion de deux groupes d'unités différentes grâce au **coefficient de variation**.
5. Repérer une **valeur atypique** par la règle des 1,5 × IQR, et décider quoi en faire.
6. Construire et **lire** une boîte à moustaches.
7. Détecter les trois pièges classiques : effet d'une valeur extrême, **paradoxe du périmètre**,
   moyenne de moyennes.

---

## 1. Le problème que la position ne voit pas

Deux équipes de vente, cinq mois, chiffre d'affaires mensuel en milliers d'euros :

| | M1 | M2 | M3 | M4 | M5 | **Moyenne** | **Médiane** |
|---|---|---|---|---|---|---|---|
| **Équipe A** | 48 | 50 | 50 | 51 | 51 | **50** | 50 |
| **Équipe B** | 5 | 12 | 50 | 88 | 95 | **50** | 50 |

Même moyenne. Même médiane. Et pourtant : l'équipe A est une horloge, l'équipe B est une roulette.
Si tu dois prévoir la trésorerie du mois prochain, ces deux équipes ne posent pas du tout le même
problème.

> 🧠 **À retenir.** Un indicateur de position **seul** ne décrit pas des données. Il faut toujours
> lui adjoindre un indicateur de **dispersion** : de combien les valeurs s'écartent-elles, en
> général, de ce point central ?

---

## 2. Les indicateurs de dispersion

### 2.1 L'étendue

La plus simple : `MAX − MIN`.

```excel
=MAX(T_Ventes[Montant_TTC]) - MIN(T_Ventes[Montant_TTC])    → 379 034,80 €
```

Elle ne repose que sur **deux valeurs** sur 613. Une seule saisie aberrante la fait exploser. On la
donne pour situer les bornes, jamais pour mesurer la dispersion.

### 2.2 Variance et écart-type

L'idée : mesurer l'écart **moyen** à la moyenne. Comme les écarts positifs et négatifs
s'annuleraient, on les met au carré — c'est la **variance**. Puis on reprend la racine carrée pour
revenir à l'unité de départ (des euros, pas des euros²) — c'est l'**écart-type**.

$$\sigma = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n}} \qquad s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n-1}}$$

```excel
=ECARTYPE.STANDARD(T_Ventes[Montant_TTC])   → 15 504,58 €   [STDEV.S]  ← échantillon
=ECARTYPE.PEARSON(T_Ventes[Montant_TTC])    → 15 491,93 €   [STDEV.P]  ← population
=VAR.S(T_Ventes[Montant_TTC])               → variance      [VAR.S]
```

**Laquelle choisir ?**

| Ta situation | Fonction | Pourquoi |
|---|---|---|
| Tes lignes **sont** tout ce qui existe (les 613 commandes de 2025) | `ECARTYPE.PEARSON` | tu décris une population complète |
| Tes lignes sont un **échantillon** d'un ensemble plus large | `ECARTYPE.STANDARD` | le `n−1` corrige un biais d'estimation |

> 💡 En pratique, au-delà de quelques centaines de lignes l'écart est négligeable (ici : 12 € sur
> 15 500, soit 0,08 %). **Mais on doit savoir pourquoi on a choisi l'une ou l'autre.** En cas de
> doute : `ECARTYPE.STANDARD`, c'est le choix conservateur et c'est celui de la plupart des outils.

**Lecture de l'écart-type sur nos données** : 15 504 € pour une moyenne de 1 680 €. L'écart-type est
**9 fois plus grand que la moyenne**. Ce n'est pas une donnée « un peu variable », c'est une donnée
dont la moyenne n'a aucun sens descriptif.

### 2.3 Le coefficient de variation (CV)

L'écart-type s'exprime dans l'unité des données. Comment comparer la variabilité des montants (en €)
à celle des notes (sur 5) ? On rapporte l'écart-type à la moyenne :

$$CV = \frac{\text{écart-type}}{\text{moyenne}}$$

```excel
=ECARTYPE.STANDARD(T_Ventes[Montant_TTC]) / MOYENNE(T_Ventes[Montant_TTC])   → 9,23  (923 %)
```

| CV | Lecture usuelle |
|---|---|
| < 0,15 | données très homogènes |
| 0,15 – 0,50 | dispersion normale |
| > 1 | données très hétérogènes — la moyenne ne résume rien |

Par catégorie de produit, le CV révèle immédiatement où sont les problèmes :

| Catégorie | Moyenne | Écart-type | **CV** | Lecture |
|---|---|---|---|---|
| VTT | 1 787 € | 977 € | **0,55** | gamme cohérente |
| Accessoires | 83 € | 53 € | **0,63** | gamme cohérente |
| Atelier | 59 € | 157 € | **2,67** | une anomalie se cache |
| Vélo urbain | 1 676 € | 5 744 € | **3,43** | idem |
| VAE | 6 936 € | 38 200 € | **5,51** | idem |

> 🔍 Le CV est un **détecteur**. Une catégorie dont le CV explose alors que son catalogue est
> homogène contient presque toujours soit une erreur de saisie, soit une vente hors norme. Ici, les
> trois catégories suspectes sont exactement celles qui portent une commande de quantité 100.

> ⚠️ Le CV n'a de sens que sur des grandeurs **positives** dont le zéro est absolu (€, kg, litres).
> Sur des températures en °C, il ne veut rien dire.

### 2.4 Quartiles, déciles, écart interquartile

On range les valeurs par ordre croissant et on découpe :

- **Q1** (1er quartile) : 25 % des valeurs sont en dessous
- **Q2** = **médiane** : 50 %
- **Q3** (3e quartile) : 75 %
- **IQR** (écart interquartile) = Q3 − Q1 : l'intervalle qui contient **la moitié centrale** des données

```excel
=QUARTILE.INCLURE(T_Ventes[Montant_TTC]; 1)   →     50,15 €     [QUARTILE.INC]
=QUARTILE.INCLURE(T_Ventes[Montant_TTC]; 3)   →  1 790,00 €
=CENTILE.INCLURE(T_Ventes[Montant_TTC]; 0,9)  →  2 590,00 €     [PERCENTILE.INC]
```

**Lecture Cyclo'Nord** : la moitié des commandes est comprise entre **50 € et 1 790 €**. L'IQR vaut
**1 740 €**. C'est une mesure de dispersion **robuste** : la commande à 379 050 € ne la modifie pas
d'un centime, alors qu'elle multiplie l'écart-type par douze.

| Mesure | Avec la flotte à 379 050 € | Sans elle (612 lignes) | Variation |
|---|---|---|---|
| Moyenne | 1 679,77 € | 1 063,15 € | **−37 %** |
| Médiane | 177,00 € | 177,00 € | **0 %** |
| Écart-type | 15 504,58 € | 2 707,51 € | **−83 %** |
| IQR | 1 739,85 € | 1 673,10 € | −4 % |

> 🚩 **La leçon.** Moyenne et écart-type sont **sensibles** ; médiane et IQR sont **robustes**.
> Sur une donnée économique (prix, salaires, montants), on communique presque toujours
> **médiane + IQR**.

---

## 3. Valeurs atypiques : les repérer, puis décider

### La règle des 1,5 × IQR (Tukey)

Une valeur est dite **atypique** (*outlier*) si elle sort de l'intervalle :

$$[\; Q1 - 1{,}5 \times IQR \;;\; Q3 + 1{,}5 \times IQR \;]$$

```excel
Q1       =QUARTILE.INCLURE(T_Ventes[Montant_TTC];1)          →     50,15
Q3       =QUARTILE.INCLURE(T_Ventes[Montant_TTC];3)          →  1 790,00
IQR      =Q3-Q1                                              →  1 739,85
Seuil_haut =Q3 + 1,5*IQR                                     →  4 399,77
Nb       =NB.SI.ENS(T_Ventes[Montant_TTC];">"&Seuil_haut)    →         14
```

**14 commandes sur 613** dépassent le seuil haut (2,3 %). Aucune ne passe sous le seuil bas — ce qui
confirme l'étalement vers la droite vu hier.

### Atypique ≠ faux

C'est le point le plus important de la journée, et celui qu'on rate le plus souvent en entreprise.

| Commande | Quantité | Montant | Statut | Diagnostic |
|---|---|---|---|---|
| CMD-20250566 (Arras) | 100 | 379 050 € | **Annulée** | Vente de flotte négociée puis perdue — ou faute de frappe ? **Non tranché.** |
| CMD-20250284 (Lens) | 100 | 59 415 € | En cours | Même question |
| CMD-20250156 (Arras) | 100 | 1 805 € | Livrée | 100 chambres à air : **parfaitement crédible** |
| 11 autres | 2 | 4 980 – 7 980 € | divers | VAE et VTT haut de gamme : **normal** |

Tu n'as pas le droit de supprimer une ligne parce qu'elle te gêne. Les trois attitudes légitimes :

1. **Garder et signaler** — l'analyse porte sur tout, tu mentionnes l'effet des extrêmes.
2. **Exclure en le disant** — « hors commandes de flotte (3 lignes) », et tu donnes les deux chiffres.
3. **Analyser à part** — les ventes B2B forment un segment distinct, tu les traites séparément.

> ❌ **Ce qui n'est jamais acceptable** : supprimer sans trace, ou publier un chiffre nettoyé sans
> dire qu'il l'est. Le [journal de nettoyage](donnees/cyclonord_ventes_2025_fiable.xlsx) du fichier
> laisse ces trois lignes **en suspens** exprès : c'est à toi de trancher et de l'écrire.

---

## 4. La boîte à moustaches

C'est la traduction graphique de tout ce qui précède, en une seule figure.

```
          Q1          médiane        Q3
  |────────┤━━━━━━━━━━━━┃━━━━━━━━━━━━├────────|        ● ●    ●
  │                                           │      valeurs atypiques
 moustache basse                    moustache haute
 (min au-dessus de Q1−1,5·IQR)      (max en dessous de Q3+1,5·IQR)
```

| Ce que tu vois | Ce que ça veut dire |
|---|---|
| La boîte | la **moitié centrale** des données (de Q1 à Q3) |
| Le trait dans la boîte | la **médiane** |
| Boîte large | données dispersées |
| Médiane décentrée dans la boîte | distribution **asymétrique** |
| Points isolés au-delà des moustaches | valeurs **atypiques** |

**Dans Excel** : sélectionne tes valeurs → *Insertion › Graphiques › Boîte à moustaches*
(Excel 2016 et suivants ; dans LibreOffice Calc, *Insertion › Diagramme › Boîte à moustaches*).

> 🎯 **Le vrai pouvoir de la boîte à moustaches, c'est la comparaison.** Une boîte par catégorie,
> côte à côte, et tu vois d'un coup d'œil laquelle est chère, laquelle est régulière, laquelle
> déraille. Tu en produiras une demain.

---

## 5. Les trois pièges de la moyenne

### Piège 1 — Une seule valeur suffit à renverser un classement

C'est l'histoire d'Arras, ce matin.

| Magasin | CA **toutes commandes** | Rang | CA **livré uniquement** | Rang |
|---|---|---|---|---|
| **Arras** | **442 617 €** | **1er** | **29 215 €** | **8e** |
| Lens | 144 276 € | 2e | 56 878 € | 1er |
| Dunkerque | 71 939 € | 6e | 53 362 € | 2e |
| Amiens | 85 184 € | 4e | 47 930 € | 3e |

Arras passe de **premier à dernier**. Une seule commande de 379 050 €, **annulée**, portait 86 % de
son « chiffre d'affaires ». Son panier médian (90 €) était d'ailleurs l'un des plus faibles du réseau
dès le départ : la médiane, elle, n'avait jamais menti.

### Piège 2 — Le paradoxe du périmètre

Les deux phrases suivantes sont vraies en même temps :

> « Cyclo'Nord a réalisé **1 029 700 €** de commandes en 2025. »
> « Cyclo'Nord a encaissé **343 877 €** en 2025. »

Elles portent sur des périmètres différents (toutes commandes vs. commandes livrées). Ni l'une ni
l'autre n'est fausse. Publier la première en l'appelant « chiffre d'affaires » est une **erreur
professionnelle** : 67 % du montant correspond à des commandes annulées, retournées ou en cours.

> 📌 **Règle absolue** : tout indicateur se publie avec sa **définition** et son **périmètre**.
> « CA = somme des Montant_TTC des commandes au statut *Livrée*, du 01/01 au 31/12/2025, 360 lignes. »

### Piège 3 — La moyenne de moyennes

Trois magasins, note moyenne 4,5 / 4,0 / 3,0. La note moyenne du réseau est-elle 3,83 ?

**Non** — sauf si les trois magasins ont exactement le même nombre d'avis. Une moyenne de moyennes
donne le même poids à un magasin qui a 5 avis et à un magasin qui en a 500. Il faut **repartir des
données de base**, ou pondérer :

```excel
✅  =MOYENNE(T_Ventes[Note_client])                                        ← sur toutes les lignes
✅  =SOMMEPROD(moyennes; effectifs) / SOMME(effectifs)                     ← pondérée
❌  =MOYENNE(cellule_moyenne_magasin_1; cellule_moyenne_magasin_2; ...)    ← faux
```

Tu retrouveras ce piège vendredi, en version « revenu moyen des communes » : une commune de
300 habitants n'a pas à peser autant qu'une ville de 230 000.

---

## 6. Le résumé à cinq nombres

Quand on te demande de décrire une variable quantitative, la réponse professionnelle standard tient
en cinq nombres (plus l'effectif) :

| | Formule | Cyclo'Nord `Montant_TTC` |
|---|---|---|
| Effectif | `=NB(...)` | 613 |
| Minimum | `=MIN(...)` | 15,20 € |
| Q1 | `=QUARTILE.INCLURE(...;1)` | 50,15 € |
| **Médiane** | `=MEDIANE(...)` | **177,00 €** |
| Q3 | `=QUARTILE.INCLURE(...;3)` | 1 790,00 € |
| Maximum | `=MAX(...)` | 379 050,00 € |

> 🧰 **Raccourci Excel** : *Données › Utilitaire d'analyse › Statistiques descriptives* produit
> l'ensemble d'un coup. Pratique pour explorer — mais le résultat est **figé** : il ne se recalcule
> pas si les données changent. Pour un livrable, écris les formules.

---

## 7. Mémo des fonctions du jour

| Besoin | Excel (FR) | Excel (EN) |
|---|---|---|
| Écart-type (échantillon) | `ECARTYPE.STANDARD` | `STDEV.S` |
| Écart-type (population) | `ECARTYPE.PEARSON` | `STDEV.P` |
| Variance (échantillon) | `VAR.S` | `VAR.S` |
| Quartile | `QUARTILE.INCLURE` | `QUARTILE.INC` |
| Centile / décile | `CENTILE.INCLURE` | `PERCENTILE.INC` |
| Rang d'une valeur en % | `RANG.POURCENTAGE.INCLURE` | `PERCENTRANK.INC` |
| n-ième plus grande valeur | `GRANDE.VALEUR` | `LARGE` |
| n-ième plus petite valeur | `PETITE.VALEUR` | `SMALL` |
| Moyenne en excluant les extrêmes | `MOYENNE.REDUITE` | `TRIMMEAN` |
| Comptage des valeurs par tranche | `FREQUENCE` | `FREQUENCY` |

---

## 8. À toi de jouer

➡️ **[Exercice guidé — Faire parler les ventes Cyclo'Nord](05-exercice-guide-cyclonord.md), partie B**
*(cet après-midi, niveau 1 · imiter — correction collective à 16 h)*

---

## 9. Auto-évaluation

- [ ] Je sais construire deux séries de même moyenne et de dispersions opposées.
- [ ] Je sais expliquer la différence entre `ECARTYPE.STANDARD` et `ECARTYPE.PEARSON`.
- [ ] Je sais dire pourquoi la médiane et l'IQR sont « robustes » et la moyenne ne l'est pas.
- [ ] Je sais calculer le seuil des valeurs atypiques et le justifier.
- [ ] Je sais qu'une valeur atypique ne se supprime pas sans trace.
- [ ] Je sais lire une boîte à moustaches et dire où est la médiane.
- [ ] Je sais pourquoi Arras est à la fois premier et dernier — et laquelle des deux réponses je
      donnerais à la direction.
- [ ] Je ne fais jamais la moyenne de moyennes sans pondérer.

---

## 10. Pour aller plus loin

- INSEE — [définition : quantile](https://www.insee.fr/fr/metadonnees/definition/c1276), [écart-type](https://www.insee.fr/fr/metadonnees/definition/c1439)
- Microsoft — [créer une boîte à moustaches](https://support.microsoft.com/fr-fr/office/cr%C3%A9er-un-graphique-en-zone-et-en-moustaches-62f4219f-db4b-4754-aca8-4743f6190f0d)
- Microsoft — [ECARTYPE.STANDARD](https://support.microsoft.com/fr-fr/office/ecartype-standard-fonction-ecartype-standard-7d69cf97-0c1f-4acf-be27-f3e83904cc23)

➡️ **Demain : [03 — Tableaux croisés dynamiques et croisements](03-tableaux-croises-dynamiques.md)**
