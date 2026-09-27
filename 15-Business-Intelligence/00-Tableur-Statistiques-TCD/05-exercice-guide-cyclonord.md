# 05 — Exercice guidé : faire parler les ventes Cyclo'Nord

> **Niveau 1 · IMITER.** Tu refais, sur Google Sheets, les gestes montrés le matin. Chaque étape
> te dit **où** écrire, **quoi** écrire, et **quel résultat** tu dois obtenir : tu te corriges seul,
> au fur et à mesure. Ce qui t'appartient, ce sont les réponses aux questions.

| | |
|---|---|
| **Quand** | lundi après-midi (partie A) · mardi après-midi (partie B) · mercredi après-midi (partie C) |
| **Organisation** | individuel ; entraide encouragée, chacun son classeur |
| **Fichier** | [`donnees/cyclonord_ventes_2025_fiable.xlsx`](donnees/cyclonord_ventes_2025_fiable.xlsx) — 613 commandes |
| **À rendre** | **mercredi 16 h 30**, un seul rendu pour les trois parties (voir la fin de la page) |

**Le contexte en deux lignes.** La semaine dernière, tu as audité le fichier des commandes 2025 de
Cyclo'Nord, un réseau de 8 magasins de vélos. Il a été corrigé. La responsable commerciale, Nadia
Oumejjoud, te demande : **« Dites-moi ce qu'il y a dedans. »**

---

## Mise en place (lundi, 20 min)

1. Ouvre https://sheets.new. Nomme le classeur `NOM_Prenom_cyclonord` (en haut à gauche).
2. **Fichier › Paramètres › Général › Paramètres régionaux : France** › *Enregistrer*.
   Désormais, dans les formules, les arguments se séparent par des **points-virgules** (`;`).
3. **Fichier › Importer › Importer** › glisse le fichier › **Remplacer la feuille de calcul** ›
   *Importer les données*. Tu obtiens les onglets `Ventes_2025`, `Dictionnaire` et `Journal_nettoyage`.
4. Lis l'onglet `Dictionnaire` (ce que contient chaque colonne) et `Journal_nettoyage` (ce qui a
   été corrigé).
5. **Crée les plages nommées** : *Données › Plages nommées › Ajouter une plage*. Pour chacune,
   tape le nom puis la plage, et clique sur *OK*.

| Nom | Plage |
|---|---|
| `Montant` | `Ventes_2025!K2:K614` |
| `Note` | `Ventes_2025!M2:M614` |
| `Statut` | `Ventes_2025!L2:L614` |
| `Categorie` | `Ventes_2025!E2:E614` |
| `Magasin` | `Ventes_2025!C2:C614` |

6. Crée un onglet (bouton **+** en bas) et nomme-le `Position`.

✅ **Vérification** : dans une cellule de `Position`, tape `=COUNT(Montant)` → **613**. Efface-la ensuite.

> ⚠️ **Règle d'or : on ne modifie jamais l'onglet `Ventes_2025`.** Tout ton travail se fait dans
> tes propres onglets.

---

# PARTIE A — Position *(lundi après-midi)*

Tout se passe dans l'onglet `Position`. Mets toujours **le libellé en colonne A et la formule en
colonne B**, sur la même ligne : dans une semaine, tu sauras encore relire ton classeur.

## A1 · Moyenne, médiane, mode (30 min)

| Cellule | Tape | Résultat attendu |
|---|---|---|
| A1 | `Moyenne du montant` | |
| B1 | `=AVERAGE(Montant)` *(MOYENNE)* | **1 679,77** |
| A2 | `Médiane du montant` | |
| B2 | `=MEDIAN(Montant)` *(MEDIANE)* | **177** |
| A3 | `Mode du montant` | |
| B3 | `=MODE(Montant)` | **19** |

Mets B1:B3 au format monétaire : *Format › Nombre › Devise*.

❓ **Question A1.** La moyenne vaut près de dix fois la médiane. Qu'est-ce que ça dit des commandes
de Cyclo'Nord ? (2 lignes. Indice : quelques très grosses commandes.)

## A2 · Compter avant de commenter (20 min)

| Cellule | Tape | Résultat attendu |
|---|---|---|
| A5 / B5 | `Notes renseignées` / `=COUNT(Note)` *(NB)* | **560** |
| A6 / B6 | `Notes vides` / `=COUNTBLANK(Note)` *(NB.VIDE)* | **53** |
| A7 / B7 | `Note moyenne` / `=AVERAGE(Note)` | **4,10** |

❓ **Question A2.** Nadia veut écrire : « Nos 613 commandes obtiennent une note moyenne de 4,1/5 ».
Cette phrase est-elle exacte ? Réécris-la.

## A3 · Le périmètre : commandé ou livré ? (30 min)

| Cellule | Tape | Résultat attendu |
|---|---|---|
| A9 / B9 | `Montant total commandé` / `=SUM(Montant)` *(SOMME)* | **1 029 700,50 €** |
| A10 / B10 | `Montant livré` / `=SUMIFS(Montant; Statut; "Livrée")` *(SOMME.SI.ENS)* | **343 877,45 €** |
| A11 / B11 | `Part livrée` / `=B10/B9` puis *Format › Nombre › Pourcentage* | **33,40 %** |

`SUMIFS(ce que j'additionne ; où je regarde ; ce que je cherche)` : « additionne les montants des
lignes dont le statut est Livrée ».

❓ **Question A3.** Nadia veut annoncer « 1 029 700 € de chiffre d'affaires en 2025 ». Que lui
dis-tu ?

## A4 · Un calcul par catégorie (45 min)

1. En **A13:D13**, tape les titres : `Catégorie`, `Nb commandes`, `Montant total`, `Montant moyen`.
2. En **A14 à A18**, tape les cinq catégories, **exactement** comme dans les données :
   `Accessoires`, `Atelier`, `VAE`, `VTT`, `Vélo urbain`.
3. En **B14**, **C14** et **D14**, tape :

```
=COUNTIFS(Categorie; A14)
=SUMIFS(Montant; Categorie; A14)
=AVERAGEIFS(Montant; Categorie; A14)
```

*(NB.SI.ENS, SOMME.SI.ENS, MOYENNE.SI.ENS)*

4. Sélectionne **B14:D14** et tire le petit carré bleu jusqu'à la ligne **18**.
5. En **A19**, tape `Total`, en **B19** `=SUM(B14:B18)`, en **C19** `=SUM(C14:C18)`.

✅ **Résultat attendu**

| Catégorie | Nb commandes | Montant total | Montant moyen |
|---|---|---|---|
| Accessoires | 189 | 15 730,75 € | 83,23 € |
| Atelier | 134 | 7 874,70 € | 58,77 € |
| VAE | 97 | 672 822,50 € | 6 936,31 € |
| VTT | 88 | 157 276,05 € | 1 787,23 € |
| Vélo urbain | 105 | 175 996,50 € | 1 676,16 € |
| **Total** | **613** | **1 029 700,50 €** | |

> ⚠️ Si ton total n'est pas 613, une catégorie est mal tapée (espace en trop, accent oublié).

❓ **Question A4.** Quelle part des commandes représentent les VAE ? Quelle part du montant ?
Commente l'écart en une phrase.

## A5 · La phrase pour Nadia (15 min)

En **A21**, écris **une seule phrase** qui décrit le montant d'une commande type, sans induire
Nadia en erreur. Elle doit contenir un indicateur, son chiffre, et le périmètre (quelles commandes).

---

# PARTIE B — Dispersion *(mardi après-midi)*

Crée un onglet `Dispersion`. Même règle : libellé en A, formule en B.

## B1 · L'étendue et les quartiles (45 min)

| Cellule | Libellé (colonne A) | Formule (colonne B) | Résultat attendu |
|---|---|---|---|
| ligne 1 | Minimum | `=MIN(Montant)` | **15,20 €** |
| ligne 2 | 1er quartile (Q1) | `=QUARTILE(Montant; 1)` | **50,15 €** |
| ligne 3 | Médiane | `=MEDIAN(Montant)` | **177,00 €** |
| ligne 4 | 3e quartile (Q3) | `=QUARTILE(Montant; 3)` | **1 790,00 €** |
| ligne 5 | Maximum | `=MAX(Montant)` | **379 050,00 €** |
| ligne 6 | Étendue | `=B5-B1` | **379 034,80 €** |
| ligne 7 | Écart-type | `=STDEV(Montant)` *(ECARTYPE)* | **15 504,58 €** |

❓ **Question B1.** Complète : « La moitié des commandes Cyclo'Nord se situe entre ___ € et ___ €. »

## B2 · Les commandes géantes (45 min)

1. En **A9**, tape `Les 5 plus grosses commandes`. En **A10 à A14**, tape `1`, `2`, `3`, `4`, `5`.
2. En **B10**, tape `=LARGE(Montant; A10)` *(GRANDE.VALEUR)* et tire jusqu'en **B14**.

✅ **Résultat attendu** : 379 050 · 59 415 · 7 980 · 7 980 · 7 980.

3. Qui a passé la plus grosse commande ? Sans toucher à `Ventes_2025`, affiche sa ligne complète :
   en **A15**, tape

```
=FILTER(Ventes_2025!A2:M614; Montant=MAX(Montant))
```

   « montre la ligne de `Ventes_2025` dont le montant est le maximum ». Toute la ligne s'affiche en A15:M15.

✅ **CMD-20250566** · Arras · VAE · quantité **100** · **Annulée**.

4. Que valent la moyenne et la médiane **sans** cette commande ? En **A17** et **A18** :

| Libellé | Formule | Résultat attendu |
|---|---|---|
| Moyenne sans la commande géante | `=AVERAGE(FILTER(Montant; Montant<379050))` | **1 063,15 €** |
| Médiane sans la commande géante | `=MEDIAN(FILTER(Montant; Montant<379050))` | **177,00 €** |

`FILTER(les valeurs ; la condition)` *(FILTRE)* : « garde seulement les montants inférieurs à 379 050 ».

❓ **Question B2.** Une seule commande sur 613 fait perdre 37 % à la moyenne. Et la médiane ?
Lequel des deux indicateurs donnerais-tu à Nadia, et pourquoi ?

## B3 · La médiane par magasin : le cas Arras (45 min)

1. En **A20:D20** : `Magasin`, `Montant total`, `Montant livré`, `Montant médian`.
2. En **A21 à A28**, les 8 magasins : `Amiens`, `Arras`, `Beauvais`, `Dunkerque`, `Lens`, `Lille`,
   `Roubaix`, `Valenciennes`.
3. En **B21**, **C21**, **D21** :

```
=SUMIFS(Montant; Magasin; A21)
=SUMIFS(Montant; Magasin; A21; Statut; "Livrée")
=MEDIAN(FILTER(Montant; Magasin=A21))
```

4. Sélectionne **B21:D21** et tire jusqu'à la ligne **28**.

✅ **Résultat attendu (extrait)**

| Magasin | Montant total | Montant livré | Montant médian |
|---|---|---|---|
| Arras | 442 616,80 € | **29 214,80 €** | **90,00 €** |
| Lens | 144 276,20 € | 56 878,50 € | 549,00 € |
| Dunkerque | 71 939,00 € | 53 362,40 € | 549,00 € |
| Roubaix | 59 059,35 € | 29 543,50 € | 101,05 € |

❓ **Question B3.** Arras est 1er sur une colonne et dernier sur une autre. Écris deux phrases :
une qui décrit le fait, une qui l'explique (indice : B2).

## B4 · L'histogramme (40 min)

Un histogramme montre **comment les commandes se répartissent** entre petits et gros montants.

1. Essaie d'abord : sélectionne la colonne `Montant_TTC` de `Ventes_2025`, *Insertion › Graphique*,
   type **Histogramme**. Que vois-tu ? *(Une seule barre géante : la commande de 379 050 € écrase
   l'échelle.)* Supprime ce graphique.
2. Crée un onglet `Histogramme`. En **A1**, tape `Commandes de 5 000 € ou moins`, et en **A2** :

```
=FILTER(Montant; Montant<=5000)
```

✅ La colonne A se remplit toute seule : **607 commandes** (les 6 plus grosses sont écartées).

3. Clique sur la lettre **A** (toute la colonne), puis *Insertion › Graphique* › **Histogramme**.
4. Dans l'éditeur, onglet *Personnaliser* › *Histogramme* › **Taille des segments : 250**.
5. Titre du graphique (onglet *Personnaliser* › *Titres*) : un titre qui dit ce qu'on voit.
   Écris sous le graphique : « 6 commandes de plus de 5 000 € ne sont pas représentées. »

❓ **Question B4.** Décris la forme de l'histogramme en une phrase. Où sont la plupart des commandes ?

---

# PARTIE C — Tableaux croisés dynamiques *(mercredi après-midi)*

Un **tableau croisé dynamique** (TCD) fait en quelques clics ce que tu as fait avec des formules
lundi et mardi. Cliquez dans `Ventes_2025`, puis *Insertion › Tableau croisé dynamique* ›
**Nouvelle feuille** › *Créer*. À droite s'ouvre l'**éditeur** : Lignes, Colonnes, Valeurs, Filtres.

## C1 · Le montant par magasin et par statut (30 min)

- **Lignes** : `Magasin` · **Colonnes** : `Statut` · **Valeurs** : `Montant_TTC`, résumé par **SUM**.
- Renomme l'onglet `TCD_magasins`.

✅ **Résultat attendu** : Arras, colonne *Annulée* : **392 145,75 €** ; ligne *Total général* :
**1 029 700,50 €**. La colonne *Livrée* redonne les chiffres de B3.

## C2 · La médiane dans un TCD (20 min)

Dans le même TCD, clique sur la valeur `SUM de Montant_TTC` et change **Résumer par : MEDIAN**.
Retire `Statut` des colonnes.

✅ Arras **90**, Lens **549**, Roubaix **101,05** : les mêmes médianes que ta formule de B3, en
deux clics. *(Google Sheets sait calculer la médiane directement dans un TCD.)*

## C3 · Qui achète quoi, et par quel canal ? (30 min)

Nouveau TCD : **Lignes** `Categorie` · **Colonnes** `Canal` · **Valeurs** `ID_commande` résumé par
**COUNTA** (nombre de commandes).

✅ **Résultat attendu**

| | Click & Collect | Magasin | Site web | Total |
|---|---|---|---|---|
| Accessoires | 31 | 87 | 71 | 189 |
| Atelier | | 134 | | 134 |
| VAE | 20 | 50 | 27 | 97 |
| VTT | 11 | 35 | 42 | 88 |
| Vélo urbain | 18 | 48 | 39 | 105 |
| **Total** | **80** | **354** | **179** | **613** |

Puis, dans *Valeurs*, change **Afficher en tant que : % du total de la ligne**.

❓ **Question C3.** Pourquoi la ligne *Atelier* n'a-t-elle qu'une seule case remplie ? Quelle
catégorie se vend le plus sur le site web, en proportion ?

## C4 · Le chiffre d'affaires livré mois par mois (40 min)

Nouveau TCD : **Lignes** `Date_commande` · **Valeurs** `Montant_TTC` (SUM) · **Filtres** `Statut` =
**Livrée** uniquement.

1. Le TCD affiche une ligne par jour : trop détaillé. Clic droit sur une date du TCD ›
   **Créer un groupe de dates de tableau croisé dynamique** › **Mois**.
2. Insère un graphique en **courbe** à partir du TCD (sélectionne le TCD › *Insertion › Graphique*).

✅ **Résultat attendu** : 12 lignes ; janvier **30 273,05 €**, mai **17 145,30 €** (le plus bas),
novembre **37 249,55 €** (le plus haut) ; total **343 877,45 €**.

❓ **Question C4.** Écris une phrase de lecture de la courbe pour Nadia.

---

## Le rendu (mercredi 16 h 30)

**Un seul rendu pour les parties A, B et C.**

1. **Partage le classeur** : bouton *Partager* › *Accès général* › **Tous les utilisateurs disposant
   du lien** › **Lecteur** › *Copier le lien*.
2. Sur ton dépôt GitHub (celui de la semaine 1), crée le dossier **`P2-cyclonord/`** avec :
   - `README.md` : 5 lignes — ce que contient le classeur, **le lien** vers ton Google Sheets, ta
     phrase de l'étape A5, ton nom ;
   - `cyclonord.xlsx` : *Fichier › Télécharger › Microsoft Excel*.
3. Tes réponses aux questions sont **dans le classeur**, dans une cellule à côté de chaque tableau.

## Auto-évaluation

- [ ] Mes formules donnent les résultats attendus, et l'onglet `Ventes_2025` est intact.
- [ ] Chaque résultat a un libellé en colonne A.
- [ ] Je sais dire pourquoi la médiane résume mieux ces commandes que la moyenne.
- [ ] Je sais dire ce qu'est le périmètre d'un chiffre (commandé ≠ livré ; 560 notes ≠ 613 commandes).
- [ ] Je sais construire un TCD, changer « Résumer par » et grouper des dates par mois.
