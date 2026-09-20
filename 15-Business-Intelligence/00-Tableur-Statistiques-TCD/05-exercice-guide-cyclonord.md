# 05 — Exercice guidé : faire parler les ventes Cyclo'Nord

> **Niveau 1 · IMITER** — tu reproduis, sur un jeu de données fourni, les manipulations montrées en
> cours. Toutes les valeurs attendues sont données : tu peux te corriger seul, au fur et à mesure.

| | |
|---|---|
| **Quand** | Lundi 21/09 après-midi (partie A) · Mardi 22/09 après-midi (partie B) |
| **Durée** | 2 × 3 h · correction collective mardi 16 h |
| **Modalité** | **Individuel** · formatif, non noté |
| **Compétences** | **C3.1** (niveau 1) · **C4.2** (niveau 1) · **C4.5** (niveau 1) |
| **Fichier** | [`donnees/cyclonord_ventes_2025_fiable.xlsx`](donnees/cyclonord_ventes_2025_fiable.xlsx) |
| **Livrable** | `NOM_Prenom_cyclonord_stats.xlsx` + 10 lignes de conclusion, sur Simplonline mardi 17 h 30 |

---

## Contexte

C'est le même fichier que la semaine dernière — **corrigé**. Les 14 lignes que ton audit avait
signalées comme inexploitables ont été retirées, les villes normalisées, les montants recalculés.
Il reste **613 commandes**. L'onglet `Journal_nettoyage` documente chaque correction : lis-le, il
fait partie de l'exercice.

Nadia Oumejjoud, responsable commerciale, te demande une chose : **« Dites-moi ce qu'il y a
dedans. »**

---

## Étape 0 — Préparer le classeur (10 min)

1. Ouvre `cyclonord_ventes_2025_fiable.xlsx` et **enregistre-le immédiatement** sous
   `NOM_Prenom_cyclonord_stats.xlsx`.
2. Lis l'onglet `Dictionnaire` **et** l'onglet `Journal_nettoyage`.
3. Sur l'onglet `Ventes_2025`, place-toi dans les données et fais `Ctrl + L` (`⌘ + T` sur Mac) pour
   convertir en **tableau structuré**. Dans *Création de tableau › Nom du tableau*, saisis
   **`T_Ventes`**.
4. Crée un nouvel onglet nommé **`Position`**. Tout ton travail de la partie A s'y fera.

> 🧰 Grâce au tableau structuré, tu écriras `T_Ventes[Montant_TTC]` au lieu de `Ventes_2025!K2:K614`.
> Si tu vois apparaître `K2:K614` dans tes formules, c'est que l'étape 3 a échoué : recommence.

---

# PARTIE A — Position *(lundi après-midi)*

## A1 · Typer les colonnes (20 min)

Dans l'onglet `Position`, recopie ce tableau et **complète les deux dernières colonnes** :

| Colonne | Type (quantitative continue / discrète / qualitative nominale / ordinale / date / identifiant) | Moyenne possible ? (oui/non) |
|---|---|---|
| `ID_commande` | | |
| `Date_commande` | | |
| `Magasin` | | |
| `Categorie` | | |
| `Canal` | | |
| `Quantite` | | |
| `Prix_unitaire_TTC` | | |
| `Remise` | | |
| `Montant_TTC` | | |
| `Statut` | | |
| `Note_client` | | |

> ❓ Pour `Note_client`, justifie ta réponse en une phrase : la moyenne est-elle **interdite**, ou
> seulement **discutable** ?

## A2 · Les trois indicateurs de position (30 min)

**Exemple montré en cours**, à reproduire tel quel dans `Position` :

```excel
=MOYENNE(T_Ventes[Montant_TTC])
=MEDIANE(T_Ventes[Montant_TTC])
=MODE.SIMPLE(T_Ventes[Montant_TTC])
```

✅ **Valeurs attendues :** 1 679,77 € · 177,00 € · 19,00 €

Puis **reproduis les trois mêmes formules** sur `Prix_unitaire_TTC` et sur `Note_client`.

✅ `Prix_unitaire_TTC` : moyenne **892,28 €** · médiane **89,00 €** · mode **19,00 €**
✅ `Note_client` : moyenne **4,10** · médiane **4** · mode **5**

**Question A2.** L'écart entre moyenne et médiane est énorme sur `Montant_TTC` et
`Prix_unitaire_TTC`, presque nul sur `Note_client`. Qu'est-ce que cela t'apprend sur la **forme**
de chacune de ces trois distributions ? *(3 lignes)*

## A3 · Compter avant de commenter (20 min)

```excel
=NB(T_Ventes[Montant_TTC])       → ?
=NB(T_Ventes[Note_client])       → ?
=NB.VIDE(T_Ventes[Note_client])  → ?
```

✅ 613 · 560 · 53

**Question A3.** Nadia veut écrire dans sa présentation : *« Nos 613 commandes obtiennent une note
moyenne de 4,1/5. »* Cette phrase est-elle exacte ? Réécris-la correctement.

## A4 · Le périmètre (30 min)

```excel
=SOMME(T_Ventes[Montant_TTC])                                      → ?
=SOMME.SI.ENS(T_Ventes[Montant_TTC]; T_Ventes[Statut]; "Livrée")   → ?
=NB.SI.ENS(T_Ventes[Statut]; "Livrée")                             → ?
```

✅ 1 029 700,50 € · 343 877,45 € · 360

**Question A4.** Calcule la part du montant total qui correspond à des commandes **livrées**
(une formule, en %). Que dirais-tu à Nadia si elle voulait annoncer « 1 029 700 € de chiffre
d'affaires 2025 » ?

✅ Part attendue : **33,4 %**

## A5 · Calculer par sous-ensemble (45 min)

Construis, **avec des formules** (pas de TCD, pas de filtre manuel), le tableau suivant :

| Catégorie | Nb commandes | CA total | Montant moyen |
|---|---|---|---|
| Accessoires | | | |
| Atelier | | | |
| VAE | | | |
| VTT | | | |
| Vélo urbain | | | |
| **Total** | | | |

Formules à utiliser : `NB.SI.ENS`, `SOMME.SI.ENS`, `MOYENNE.SI.ENS`.

✅ **Contrôle** : la colonne « Nb commandes » doit totaliser **613** et le CA total
**1 029 700,50 €**. Si ce n'est pas le cas, une modalité t'échappe.

✅ VAE : 97 commandes · 672 822,50 € · 6 936,31 €

**Question A5.** Le VAE représente quel pourcentage des **commandes** ? Quel pourcentage du
**montant** ? Commente l'écart en une phrase.

✅ 15,8 % des commandes · 65,3 % du montant

## A6 · Moyenne simple contre moyenne pondérée (30 min)

Calcule la note moyenne de deux façons :

```excel
Moyenne simple    =MOYENNE(T_Ventes[Note_client])
Moyenne pondérée  =SOMMEPROD(T_Ventes[Note_client]; T_Ventes[Montant_TTC])
                   / SOMME(T_Ventes[Montant_TTC])
```

**Question A6.** Les deux résultats diffèrent. Lequel utiliserais-tu, et pour dire quoi ?
Attention : la formule pondérée traite les 53 notes vides comme des zéros. En quoi cela fausse-t-il
le résultat, et comment le corrigerais-tu ?

## A7 · La phrase de restitution (15 min)

Écris, dans une cellule de l'onglet `Position`, **une seule phrase** décrivant le montant typique
d'une commande Cyclo'Nord. Elle doit contenir un indicateur de position, son périmètre, et ne pas
induire Nadia en erreur.

---

# PARTIE B — Dispersion *(mardi après-midi)*

Crée un onglet **`Dispersion`**.

## B1 · Étendue, écart-type, coefficient de variation (30 min)

```excel
=MIN(T_Ventes[Montant_TTC])                  → ?
=MAX(T_Ventes[Montant_TTC])                  → ?
=MAX(...) - MIN(...)                         → ?
=ECARTYPE.STANDARD(T_Ventes[Montant_TTC])    → ?
=ECARTYPE.PEARSON(T_Ventes[Montant_TTC])     → ?
```

✅ 15,20 € · 379 050,00 € · 379 034,80 € · 15 504,58 € · 15 491,93 €

Calcule le **coefficient de variation** (écart-type ÷ moyenne).

✅ **9,23** soit **923 %**

**Question B1.** Les deux écarts-types diffèrent de 12 € sur 15 500. Explique en deux lignes
laquelle des deux fonctions convient ici, et pourquoi la différence est si faible.

## B2 · Le résumé à cinq nombres (30 min)

| | Formule | Valeur |
|---|---|---|
| Effectif | `=NB(...)` | |
| Minimum | `=MIN(...)` | |
| Q1 | `=QUARTILE.INCLURE(...;1)` | |
| Médiane | `=MEDIANE(...)` | |
| Q3 | `=QUARTILE.INCLURE(...;3)` | |
| Maximum | `=MAX(...)` | |
| IQR | `=Q3-Q1` | |

✅ 613 · 15,20 € · 50,15 € · 177,00 € · 1 790,00 € · 379 050,00 € · 1 739,85 €

**Question B2.** Complète la phrase : « La moitié des commandes Cyclo'Nord se situe entre ____ € et
____ €. »

## B3 · Repérer les valeurs atypiques (40 min)

Reproduis la règle vue en cours :

```excel
Seuil_bas   = Q1 - 1,5*IQR       → ?
Seuil_haut  = Q3 + 1,5*IQR       → ?
Nb au-dessus du seuil haut  =NB.SI.ENS(T_Ventes[Montant_TTC]; ">"&Seuil_haut)   → ?
Nb en dessous du seuil bas  =NB.SI.ENS(T_Ventes[Montant_TTC]; "<"&Seuil_bas)    → ?
```

✅ −2 559,62 € · 4 399,77 € · **14** · **0**

Utilise ensuite `GRANDE.VALEUR` pour afficher les **cinq plus gros montants**, puis retrouve les
lignes correspondantes (tri décroissant sur `Montant_TTC`, ou double-clic dans un TCD demain).

✅ Top 3 : **379 050 €** (CMD-20250566, Arras, VAE, quantité 100, **Annulée**) ·
**59 415 €** (CMD-20250284, Lens, Vélo urbain, quantité 100, En cours) · **7 980 €** (4 ex æquo)

**Question B3.** Le seuil bas est négatif. Est-ce un bug ? Que faut-il en conclure sur la forme de
la distribution ?

**Question B4.** Pour chacune des trois commandes de quantité 100, dis si tu la gardes, si tu
l'écartes ou si tu l'analyses à part — et **justifie**. Aucune des trois réponses n'est
automatiquement fausse ; c'est la justification qui compte.

## B4 · Mesurer l'effet d'une seule ligne (30 min)

Recalcule moyenne, médiane, écart-type et IQR **en excluant la seule commande CMD-20250566**
(filtre ou `MOYENNE.SI.ENS` avec le critère `<>CMD-20250566`), et remplis :

| Mesure | Avec | Sans | Variation en % |
|---|---|---|---|
| Moyenne | 1 679,77 € | | |
| Médiane | 177,00 € | | |
| Écart-type | 15 504,58 € | | |
| IQR | 1 739,85 € | | |

✅ Sans : 1 063,15 € (−37 %) · 177,00 € (0 %) · 2 707,51 € (−83 %) · 1 673,10 € (−4 %)

**Question B5.** Classe ces quatre indicateurs du plus **robuste** au plus **sensible**.

## B5 · La boîte à moustaches (30 min)

Insère une boîte à moustaches de `Montant_TTC` **par catégorie** :
*Insertion › Graphiques statistiques › Boîte à moustaches*.

Habille-la : titre porteur de message, axe des ordonnées nommé « Montant TTC (€) », note de source.

**Question B6.** Deux catégories ont une boîte écrasée près de zéro. Lesquelles, et pourquoi ?
Que proposerais-tu pour les rendre lisibles ?

## B6 · Le cas Arras (30 min)

Construis, avec des formules, le tableau suivant :

| Magasin | CA **toutes commandes** | CA **livré** | Panier **médian** |
|---|---|---|---|

*(Pour le panier médian par magasin, tu devras filtrer : il n'existe pas de `MEDIANE.SI.ENS`.
Note cette limite dans ton classeur — c'est une vraie contrainte du tableur.)*

✅ Arras : 442 616,80 € · 29 214,80 € · 90,00 €
✅ Lens : 144 276,20 € · 56 878,50 € · 549,00 €

**Question B7.** Arras est premier sur une colonne et dernier sur une autre. Rédige les **deux
phrases** que tu mettrais dans un rapport : celle qui décrit le fait, et celle qui l'explique.

---

## Livrable

À déposer sur Simplonline **mardi 22/09 avant 17 h 30** :

**`NOM_Prenom_cyclonord_stats.xlsx`** contenant :

| Onglet | Contenu |
|---|---|
| `Ventes_2025` | **intact** — aucune modification de la donnée source |
| `Dictionnaire`, `Journal_nettoyage` | conservés tels quels |
| `Position` | A1 à A7, formules apparentes |
| `Dispersion` | B1 à B6, formules apparentes, + la boîte à moustaches |
| `Conclusion` | **10 lignes maximum** répondant à : *« que faut-il retenir de ces 613 commandes, et quel chiffre unique donneriez-vous à la direction ? »* |

> 📌 Les indicateurs doivent être **calculés par formule**, jamais saisis en dur. Un correcteur qui
> clique sur une cellule doit voir la formule.

---

## Critères de réussite (auto-évaluation)

| | Critère | Compétence |
|---|---|---|
| ☐ | La donnée source est intacte | C4.5 |
| ☐ | Toutes les valeurs attendues sont retrouvées | C3.1 |
| ☐ | Les indicateurs sont obtenus par formule, avec références structurées | C4.5 |
| ☐ | Chaque calcul indique son **périmètre** | C3.1 |
| ☐ | L'écart moyenne / médiane est commenté en termes de forme | C3.1 |
| ☐ | Les valeurs atypiques sont identifiées **et** une décision est justifiée | C3.1 |
| ☐ | La boîte à moustaches est titrée, légendée, avec unité | C4.2 |
| ☐ | La conclusion propose un chiffre unique **et** le défend | C3.1 |

**Positionnement** : ● Acquis · ◐ En cours d'acquisition · ○ Non acquis

---

## Pour aller plus loin (facultatif)

- Recalcule tout le résumé à cinq nombres **par magasin**, et repère celui dont la distribution est
  la plus régulière (CV le plus faible).
- Utilise `MOYENNE.REDUITE(T_Ventes[Montant_TTC]; 0,1)` (`TRIMMEAN`) : la moyenne après exclusion
  des 5 % extrêmes de chaque côté. Compare-la à la moyenne et à la médiane. Dans quel cas
  l'utiliserais-tu ?
- Construis la table des effectifs par tranche de 250 € avec `FREQUENCE`, puis l'histogramme.
  Combien de bosses vois-tu ?
- Refais trois calculs dans **Google Sheets** et note les différences de nom de fonction.
