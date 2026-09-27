# 03 — Tableaux croisés dynamiques dans Google Sheets

> 🎬 **Suite du fil rouge.** Nadia a aimé ton « cas Arras ». Elle en veut plus : *« Le CA par
> magasin **et** par statut. Le nombre de commandes par catégorie et par canal. Et le CA livré mois
> par mois. »* Avec `SUMIFS`, ce serait des dizaines de formules. Avec un tableau croisé dynamique,
> c'est quelques clics.

| Jour | Durée démo | Mise en pratique |
|---|---|---|
| Mercredi matin | 45 min | [Exercice guidé, partie C](05-exercice-guide-cyclonord.md) (après-midi) |

Pré-requis : [cours 01](01-statistiques-descriptives.md) et [cours 02](02-dispersion-et-pieges-de-la-moyenne.md) (`SUMIFS`, `FILTER`, plages nommées).

## Ce que tu sauras faire

- Dire en une phrase à quoi sert un tableau croisé dynamique.
- Créer un TCD dans Google Sheets et placer les champs dans Lignes, Colonnes, Valeurs et Filtres.
- Choisir le calcul : `SUM`, `COUNTA`, `AVERAGE` ou `MEDIAN`.
- Afficher un résultat en pourcentage du total.
- Regrouper des dates par mois.

---

## 1. À quoi sert un TCD

Un **tableau croisé dynamique** (TCD) est un tableau de synthèse que Sheets construit pour toi. Il
fait deux choses :

1. il **regroupe** les lignes qui ont la même valeur (toutes les commandes d'Arras ensemble) ;
2. il **calcule** un indicateur sur chaque groupe (la somme, le nombre, la médiane…).

C'est exactement ce que tu as fait lundi avec `SUMIFS` et `COUNTIFS`. La différence : tu n'écris
aucune formule, Sheets trouve tout seul la liste des magasins, et changer « somme » en « médiane »
prend deux clics.

---

## 2. Préparer les données

Un TCD a besoin d'un tableau propre. Vérifie trois choses avant de cliquer :

- **une ligne = une commande** : pas de ligne de total, pas de ligne vide au milieu ;
- **une seule ligne d'en-têtes**, en ligne 1, chaque colonne avec un nom unique ;
- **les types sont bons** : les dates sont des dates, les montants des nombres.

L'onglet `Ventes_2025` coche déjà ces cases : 613 commandes, lignes 2 à 614, en-têtes en ligne 1.

---

## 3. Créer le TCD

1. Clique dans n'importe quelle cellule du tableau `Ventes_2025`.
2. *Insertion › Tableau croisé dynamique*.
3. Vérifie la plage de données proposée : `Ventes_2025!A1:M614`.
4. Choisis d'insérer dans une **nouvelle feuille**, puis *Créer*.

Sheets ouvre une feuille vide et, à droite, le panneau **Éditeur de tableau croisé dynamique**. Il
contient quatre sections, chacune avec un bouton *Ajouter* qui liste les colonnes de ta source :

| Section | Ce qu'on y met | Exemple Cyclo'Nord |
|---|---|---|
| **Lignes** | une colonne de catégories, affichée de haut en bas | `Magasin` |
| **Colonnes** | une deuxième colonne de catégories, avec peu de valeurs différentes | `Statut` (4 valeurs) |
| **Valeurs** | ce qu'on calcule | `Montant_TTC` |
| **Filtres** | ce qu'on garde ou qu'on écarte | `Statut` = Livrée |

> ⚠️ En Colonnes, garde une colonne qui a **peu de valeurs** (3 ou 4). Un tableau de 50 colonnes ne
> se lit pas.

### Exemple 1 — CA par magasin et par statut

Lignes : `Magasin`. Colonnes : `Statut`. Valeurs : `Montant_TTC`. Résultat attendu :

| Magasin | Annulée | En cours | Livrée | Retournée | Total |
|---|---|---|---|---|---|
| Amiens | 14 760,20 | 11 402,80 | 47 930,05 | 11 091,05 | 85 184,10 |
| Arras | **392 145,75** | 7 828,85 | **29 214,80** | 13 427,40 | 442 616,80 |
| Beauvais | 3 293,00 | 14 642,05 | 42 822,10 | 11 537,35 | 72 294,50 |
| Dunkerque | 10 829,40 | 7 044,20 | 53 362,40 | 703,00 | 71 939,00 |
| Lens | 12 432,90 | 64 260,20 | 56 878,50 | 10 704,60 | 144 276,20 |
| Lille | 22 957,70 | 2 066,40 | 47 768,75 | 9 890,50 | 82 683,35 |
| Roubaix | 4 764,45 | 8 765,65 | 29 543,50 | 15 985,75 | 59 059,35 |
| Valenciennes | 12 795,75 | 4 915,20 | 36 357,35 | 17 578,90 | 71 647,20 |
| **Total** | 473 979,15 | 120 925,35 | **343 877,45** | 90 918,55 | **1 029 700,50** |

L'histoire d'hier saute aux yeux en une seule image : Arras a le plus gros CA total, mais presque
tout est dans la colonne *Annulée*. En CA livré, Arras est dernier.

---

## 4. Choisir le calcul : « Résumer par »

Dans la section Valeurs, chaque champ a une liste déroulante **Résumer par**. Pour un nombre, Sheets
choisit `SUM` par défaut. Les quatre calculs à connaître :

| Résumer par | Question à laquelle il répond |
|---|---|
| `SUM` (somme) | Combien ça pèse en euros ? |
| `COUNTA` (NBVAL : compte les cellules non vides) | Combien de commandes ? |
| `AVERAGE` (moyenne) | Combien en moyenne par commande ? |
| `MEDIAN` (médiane) | Quelle est la commande « typique » ? |

> 🚩 **Lis toujours l'en-tête de ta valeur.** Sheets l'écrit en clair, par exemple
> `SUM de Montant_TTC`. Si tu lis « SUM » alors que tu voulais un nombre de commandes, ton tableau
> est faux.

### Exemple 2 — Nombre de commandes par catégorie et par canal

Lignes : `Categorie`. Colonnes : `Canal`. Valeurs : `ID_commande`, Résumer par `COUNTA`. On compte
une colonne de texte, donc on prend `COUNTA` : chaque identifiant rempli = une commande.

| Catégorie | Click & Collect | Magasin | Site web | Total |
|---|---|---|---|---|
| Accessoires | 31 | 87 | 71 | 189 |
| Atelier | | 134 | | 134 |
| VAE | 20 | 50 | 27 | 97 |
| VTT | 11 | 35 | 42 | 88 |
| Vélo urbain | 18 | 48 | 39 | 105 |
| **Total** | 80 | 354 | 179 | **613** |

Les cases vides de l'Atelier ne sont pas une erreur : aucune réparation n'est commandée en ligne. Une
case vide dans un TCD veut dire « aucune ligne », pas « zéro euro saisi ».

### Exemple 3 — Médiane du montant par magasin

Lignes : `Magasin`. Valeurs : ajoute **deux fois** `Montant_TTC`, l'une en `AVERAGE`, l'autre en
`MEDIAN`.

| Magasin | AVERAGE de Montant_TTC | MEDIAN de Montant_TTC |
|---|---|---|
| Amiens | 1 038,83 | 507,82 |
| Arras | **4 708,69** | **90,00** |
| Beauvais | 1 112,22 | 207,00 |
| Dunkerque | 1 160,31 | 549,00 |
| Lens | 1 873,72 | 549,00 |
| Lille | 996,18 | 549,00 |
| Roubaix | 843,70 | 101,05 |
| Valenciennes | 895,59 | 92,20 |
| **Total** | 1 679,77 | 177,00 |

> ✅ **Un vrai avantage de Sheets** : il propose `MEDIAN` directement dans le TCD. Hier, tu devais
> écrire `MEDIAN(FILTER(Montant; Magasin="Arras"))` magasin par magasin ; ici, les huit médianes
> arrivent d'un coup. Arras a la plus forte moyenne et la plus faible médiane : la commande annulée
> de 379 050 € tire la moyenne vers le haut, pas la médiane.

---

## 5. Filtrer et afficher en % du total

**Filtrer.** Dans la section Filtres, ajoute `Statut`. Ouvre la liste *Statut*, décoche tout sauf
*Livrée*, puis *OK*. Le TCD ne calcule plus que sur les 360 commandes livrées.

**Afficher en %.** Dans la section Valeurs, la liste **Afficher en tant que** vaut *Par défaut*.
Choisis *% du total général* : chaque case devient sa part du total.

### Exemple 4 — Part de chaque magasin dans le CA livré

Lignes : `Magasin`. Valeurs : `Montant_TTC` en `SUM`, affiché en % du total général. Filtre :
`Statut` = Livrée.

| Magasin | Part du CA livré |
|---|---|
| Amiens | 13,9 % |
| Arras | **8,5 %** |
| Beauvais | 12,5 % |
| Dunkerque | 15,5 % |
| Lens | **16,5 %** |
| Lille | 13,9 % |
| Roubaix | 8,6 % |
| Valenciennes | 10,6 % |
| **Total** | 100 % |

Le total fait toujours 100 % : c'est ta vérification. Le même réglage existe en % du total de la
ligne ou de la colonne, pour répartir *à l'intérieur* d'un magasin ou d'un statut.

---

## 6. Grouper les dates par mois

Mettre `Date_commande` en Lignes donne une ligne par jour : illisible. Pour regrouper :

1. dans le TCD, fais un **clic droit sur une date** ;
2. *Créer un groupe de dates de tableau croisé dynamique › Mois*.

Tu n'as ajouté aucune colonne `Mois` à tes données : c'est le TCD qui regroupe.

### Exemple 5 — CA livré par mois en 2025

Lignes : `Date_commande` groupée par mois. Valeurs : `Montant_TTC` en `SUM`, et `ID_commande` en
`COUNTA`. Filtre : `Statut` = Livrée.

| Mois | Commandes livrées | CA livré |
|---|---|---|
| Janvier | 32 | 30 273,05 |
| Février | 34 | 28 189,30 |
| Mars | 31 | 31 668,40 |
| Avril | 22 | 22 178,95 |
| Mai | 26 | **17 145,30** |
| Juin | 33 | 34 781,80 |
| Juillet | 25 | 18 912,00 |
| Août | 20 | 21 964,40 |
| Septembre | 44 | 36 587,90 |
| Octobre | 29 | 32 625,50 |
| Novembre | 35 | **37 249,55** |
| Décembre | 29 | 32 301,30 |
| **Total** | **360** | **343 877,45** |

Mai est le mois le plus faible, novembre le plus fort. Septembre a le plus de commandes livrées (44).

---

## 7. Le TCD se met à jour tout seul

Quand les données de sa plage changent (par exemple quand on importe le fichier du mois suivant),
le TCD se recalcule immédiatement, sans bouton à cliquer. Seule limite : il ne lit que sa plage
(`A1:M614`). S'il y a plus de lignes, élargis la plage en haut du panneau de l'éditeur.

> 🕵️ Un chiffre te surprend ? Affiche les lignes qui sont derrière la case avec `FILTER`, sans
> toucher à `Ventes_2025` : `=FILTER(Ventes_2025!A2:M614; Magasin="Arras"; Statut="Annulée")`.
> C'est ainsi qu'on repère la commande CMD-20250566 à 379 050 €.

---

## Mémo

| Geste | Où |
|---|---|
| Créer un TCD | *Insertion › Tableau croisé dynamique* |
| Placer les champs | Panneau de l'éditeur : Lignes, Colonnes, Valeurs, Filtres › *Ajouter* |
| Changer le calcul | Valeurs › **Résumer par** : `SUM`, `COUNTA`, `AVERAGE`, `MEDIAN` |
| Afficher en % | Valeurs › **Afficher en tant que** › % du total général |
| Garder un seul statut | Filtres › `Statut` › cocher *Livrée* |
| Grouper par mois | Clic droit sur une date › *Créer un groupe de dates de tableau croisé dynamique › Mois* |

## Auto-évaluation

- [ ] Je sais dire en une phrase ce que fait un TCD : regrouper, puis calculer.
- [ ] Je sais placer un champ dans Lignes, Colonnes, Valeurs ou Filtres.
- [ ] Je lis l'en-tête de ma valeur pour vérifier `SUM`, `COUNTA`, `AVERAGE` ou `MEDIAN`.
- [ ] Je sais obtenir la médiane par magasin directement dans le TCD.
- [ ] Je sais afficher en % du total et regrouper des dates par mois.

⬅️ Retour : [02 — Dispersion et pièges de la moyenne](02-dispersion-et-pieges-de-la-moyenne.md)
· 🛠️ Mise en pratique : [exercice guidé, partie C](05-exercice-guide-cyclonord.md)

➡️ **Demain : [04 — Choisir le bon graphique](04-choisir-le-bon-graphique.md)**
