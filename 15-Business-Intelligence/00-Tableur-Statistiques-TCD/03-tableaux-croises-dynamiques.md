# 03 — Tableaux croisés dynamiques et croisements

> 🎬 **Suite du fil rouge.**
> Mardi soir, Nadia a lu ton analyse. Elle est convaincue — et elle en veut plus :
> *« Le CA par magasin, très bien. Mais je voudrais le CA par magasin **et** par catégorie.
> Et par canal. Et par mois. Et le taux d'annulation par magasin. Pour jeudi. »*
> Avec les fonctions d'hier, cela ferait environ **trois cents formules `SOMME.SI.ENS`**.
> Tu vas apprendre à produire la même chose en quarante secondes — et à la modifier en cinq.

| | |
|---|---|
| **Jour** | Mercredi 23/09/2026 · matin (apport) + après-midi (lancement du brief Adapter) |
| **Durée** | ≈ 7 h |
| **Compétences** | **C4.5** (niveau 1 → 2) · **C3.1** (niveau 2) |
| **Données** | [`donnees/cyclonord_ventes_2025_fiable.xlsx`](donnees/cyclonord_ventes_2025_fiable.xlsx) |
| **Pré-requis** | Cours [01](01-statistiques-descriptives.md) et [02](02-dispersion-et-pieges-de-la-moyenne.md) |

---

## Objectifs pédagogiques

À la fin de la journée, tu sauras :

1. Expliquer ce qu'est un TCD : **regrouper, puis agréger**.
2. Construire un TCD et placer correctement les champs dans les quatre zones.
3. Changer la **fonction d'agrégation** (somme, moyenne, nombre, max…) en connaissant le piège du
   `Nombre` par défaut.
4. Afficher les valeurs en **pourcentage** (du total, de la ligne, de la colonne).
5. **Grouper** des dates par mois / trimestre et des nombres par tranches.
6. Filtrer un TCD avec les **segments** et lire un **graphique croisé dynamique**.
7. Connaître les **limites** du TCD — notamment l'absence de médiane — et savoir les contourner.

---

## 1. Ce qu'est un TCD, en une phrase

> Un tableau croisé dynamique **regroupe** les lignes qui se ressemblent, puis **calcule un
> indicateur** sur chaque groupe.

C'est exactement ce que tu faisais hier avec `SOMME.SI.ENS`, mais :

| Avec des formules | Avec un TCD |
|---|---|
| Une formule par case | Un glisser-déposer pour tout le tableau |
| Tu dois connaître les valeurs à l'avance (« Lille », « Arras »…) | Il découvre les modalités tout seul |
| Ajouter un magasin = réécrire | Ajouter un magasin = actualiser |
| Changer somme → moyenne = tout réécrire | Deux clics |

> 🧠 **L'idée à retenir** : un TCD transforme des **lignes de détail** en **tableau de synthèse**.
> C'est le geste le plus rentable de toute la bureautique d'analyse.

---

## 2. Préparer les données (l'étape que tout le monde saute)

Un TCD exige une **table plate** : une ligne = une observation, une colonne = une variable, une
seule ligne d'en-tête, aucune cellule fusionnée, aucune ligne vide, aucun total intercalé.

**Check-list avant de cliquer :**

- [ ] Une seule ligne d'en-tête, en ligne 1
- [ ] Aucun en-tête vide ni en double
- [ ] Aucune ligne ni colonne entièrement vide au milieu de la plage
- [ ] Aucune cellule fusionnée
- [ ] Les dates sont des **dates** (alignées à droite), pas du texte
- [ ] Les nombres sont des **nombres** (pas de `1 250 €` saisi en texte)
- [ ] La plage est convertie en **tableau structuré** (`Ctrl + L`), nommée `T_Ventes`

> 🧰 **Pourquoi le tableau structuré ?** Parce que la source du TCD devient `T_Ventes` au lieu de
> `A1:M614`. Si le mois prochain le fichier passe à 900 lignes, tu fais *Actualiser* et c'est fini.
> Sinon, tu dois retoucher la plage à la main — et neuf fois sur dix, on oublie.

---

## 3. Créer son premier TCD

**Insertion › Tableau croisé dynamique › Nouvelle feuille de calcul.**

Le volet de droite propose la liste des champs et **quatre zones** :

```
┌─────────────────────────────┬───────────────────────────────┐
│  FILTRES                    │  COLONNES                     │
│  (un filtre global au-dessus│  (les modalités se déploient  │
│   du tableau)               │   horizontalement)            │
├─────────────────────────────┼───────────────────────────────┤
│  LIGNES                     │  VALEURS                      │
│  (les modalités se déploient│  (le calcul : somme, moyenne, │
│   verticalement)            │   nombre…)                    │
└─────────────────────────────┴───────────────────────────────┘
```

| Zone | Ce qu'on y met | Exemple Cyclo'Nord |
|---|---|---|
| **Lignes** | une variable **qualitative** | `Magasin`, `Categorie` |
| **Colonnes** | une deuxième variable qualitative, peu de modalités | `Canal` (3 modalités) |
| **Valeurs** | une variable **quantitative** à agréger | `Montant_TTC` |
| **Filtres** | ce qui restreint le périmètre | `Statut` |

> ⚠️ **Règle de lisibilité** : en colonnes, **jamais plus de 6 à 8 modalités**. Un TCD de 40 colonnes
> ne se lit pas. Si tu as beaucoup de modalités, mets-les en lignes.

### Le premier résultat : `Categorie` × `Canal`, somme des montants

| Catégorie | Click & Collect | Magasin | Site web | **Total** |
|---|---|---|---|---|
| Accessoires | 2 506 € | 7 292 € | 5 932 € | 15 731 € |
| Atelier | — | 7 875 € | — | 7 875 € |
| VAE | 52 088 € | 526 876 € | 93 858 € | 672 822 € |
| VTT | 21 787 € | 68 396 € | 67 093 € | 157 276 € |
| Vélo urbain | 16 299 € | 56 346 € | 103 352 € | 175 996 € |
| **Total** | **92 680 €** | **666 785 €** | **270 235 €** | **1 029 700 €** |

Deux informations sautent aux yeux, qu'aucun tri ni filtre ne t'aurait données aussi vite :

1. **L'Atelier est à 100 % en magasin.** Zéro en ligne, zéro en Click & Collect. Structurellement
   logique (on ne répare pas un vélo à distance) — mais c'est un angle mort : aucune prise de
   rendez-vous en ligne n'existe.
2. **Le VAE pèse 65 % du montant total** alors qu'il ne représente que 97 commandes sur 613 (16 %).
   Le chiffre d'affaires de l'enseigne tient à une catégorie minoritaire en volume.

---

## 4. Changer le calcul : la zone Valeurs

**Clic droit sur une valeur › Paramètres des champs de valeurs** (ou double-clic sur l'en-tête de
la valeur).

| Fonction | Question à laquelle elle répond |
|---|---|
| **Somme** | « combien ça pèse ? » |
| **Nombre** | « combien de fois ? » |
| **Moyenne** | « combien en moyenne par commande ? » |
| **Max / Min** | « quelle est la plus grosse / petite ? » |
| **Écart-type** | « est-ce régulier ? » |

> 🚩 **Le piège numéro un du TCD.** Quand tu glisses un champ dans *Valeurs*, Excel choisit
> **Somme** si la colonne ne contient que des nombres, et **Nombre** dès qu'elle contient **une
> seule** cellule vide ou textuelle. Sur `Note_client` (53 cellules vides), tu obtiendras un
> « Nombre de Note_client » par défaut. Beaucoup de rapports faux naissent exactement là.
> **Vérifie systématiquement l'intitulé de ta valeur.**

### Le même croisement, en moyenne

| Catégorie | Click & Collect | Magasin | Site web |
|---|---|---|---|
| Accessoires | 81 € | 84 € | 84 € |
| VAE | 2 604 € | **10 538 €** | 3 476 € |
| VTT | 1 981 € | 1 954 € | 1 597 € |
| Vélo urbain | 905 € | 1 174 € | 2 650 € |

Le 10 538 € du VAE en magasin doit te faire tiquer immédiatement : c'est la commande de flotte
annulée à 379 050 € qui gonfle la case. **Un TCD ne protège de rien** — les pièges d'hier
s'appliquent case par case.

### Afficher en pourcentage

*Paramètres des champs de valeurs › onglet « Afficher les valeurs »* :

| Option | Utilité |
|---|---|
| **% du total général** | poids de chaque case dans l'ensemble |
| **% du total de la ligne** | répartition **au sein** de chaque catégorie |
| **% du total de la colonne** | répartition au sein de chaque canal |
| **% de** (valeur de référence) | tout comparer à une modalité choisie |
| **Différence par rapport à** | écart au mois précédent, par exemple |

C'est le moyen le plus rapide de produire un taux. Exemple : `Magasin` en lignes, `Statut` en
colonnes, `ID_commande` en valeurs (Nombre), affichage **% du total de la ligne** :

| Magasin | Annulée | En cours | **Livrée** | Retournée | **Annulée + Retournée** |
|---|---|---|---|---|---|
| Lens | 11,7 % | 11,7 % | **68,8 %** | 7,8 % | 19,5 % |
| Dunkerque | 16,1 % | 11,3 % | 67,7 % | 4,8 % | 21,0 % |
| Lille | 12,0 % | 9,6 % | 63,9 % | 14,5 % | 26,5 % |
| Amiens | 15,9 % | 15,9 % | 57,3 % | 11,0 % | 26,8 % |
| Beauvais | 6,2 % | 15,4 % | 56,9 % | 21,5 % | 27,7 % |
| Roubaix | 12,9 % | 18,6 % | 50,0 % | 18,6 % | 31,4 % |
| Valenciennes | 13,8 % | 6,2 % | 58,8 % | 21,2 % | 35,0 % |
| **Arras** | **20,2 %** | 16,0 % | 48,9 % | 14,9 % | **35,1 %** |

Arras cumule le plus fort taux d'annulation **et** le plus faible taux de livraison. L'histoire des
deux jours précédents se confirme sous un troisième angle.

---

## 5. Grouper

### Grouper des dates

C'est la fonction la plus utile du TCD et la moins connue. Mets `Date_commande` en lignes →
**clic droit › Grouper** → coche *Mois*, *Trimestres*, *Années*.

Excel crée les niveaux tout seuls. Tu n'as **pas besoin** d'ajouter une colonne `Mois` au fichier
source.

| Mois | Nb commandes livrées | CA livré |
|---|---|---|
| Janvier | 32 | 30 273 € |
| … | … | … |
| Septembre | 44 | **36 588 €** |
| Novembre | 35 | 37 250 € |

> ⚠️ Si *Grouper* est grisé, c'est que ta colonne de dates contient **du texte** ou **une cellule
> vide**. Retour au nettoyage.

### Grouper des nombres par tranches

Même geste sur une colonne numérique : *clic droit › Grouper*, puis pas de 500. Tu obtiens en trois
clics la **table des effectifs** dont tu auras besoin demain pour l'histogramme.

---

## 6. Segments et graphiques croisés

**Segments** (*Analyse du TCD › Insérer un segment*) : des boutons de filtre visuels. Bien plus
lisibles que la liste déroulante, et un même segment peut piloter **plusieurs TCD** à la fois
(*Connexions de rapport*) — c'est l'embryon d'un tableau de bord.

**Chronologie** (*Insérer une chronologie*) : le même principe sur un champ de type date, avec un
curseur mois / trimestre / année.

**Graphique croisé dynamique** (*Analyse du TCD › Graphique croisé dynamique*) : il se met à jour en
même temps que le TCD et hérite de ses filtres. C'est le pont vers le cours de demain.

---

## 7. Les limites du TCD (à connaître avant de se faire piéger)

| Limite | Contournement |
|---|---|
| **Pas de médiane** dans les fonctions d'agrégation | Passer par un filtre + `MEDIANE`, ou une formule matricielle, ou Python (semaine P6) |
| Le TCD **ne se recalcule pas tout seul** quand la source change | *Données › Actualiser tout* — à faire **avant** toute capture d'écran |
| Une source en plage figée (`A1:M614`) ignore les lignes ajoutées | Toujours partir d'un **tableau structuré** |
| Les **cellules vides** deviennent des blancs ambigus | *Options du TCD › « Pour les cellules vides, afficher : » 0* — et dire dans la note si 0 signifie « zéro » ou « pas de donnée » |
| Les **totaux de moyennes** ne sont pas la moyenne des moyennes | Le total général est recalculé sur toutes les lignes : c'est correct, mais ne colle pas à la somme de la colonne |
| Une modalité mal orthographiée crée une **ligne en double** | C'est le travail de la semaine P1 : nettoyer avant |

> 🚩 **L'absence de médiane n'est pas un détail.** Sur des données asymétriques — c'est-à-dire la
> plupart des données économiques — le TCD te pousse structurellement vers la moyenne, donc vers le
> chiffre le plus trompeur. Sache-le, et compense.

---

## 8. Les quatre croisements qui valent toujours le coup

Face à un fichier inconnu, ces quatre TCD donnent 80 % de la compréhension en dix minutes :

1. **Volume** — une dimension en lignes, `Nombre` en valeurs. *Qui est gros, qui est petit ?*
2. **Poids** — même chose en `Somme`. *Où est l'argent (ou le volume) ?*
3. **Intensité** — même chose en `Moyenne`. *Qui a le plus gros ticket ?*
4. **Temps** — la date en lignes, groupée par mois. *Est-ce que ça monte ou ça descend ?*

Les trois premiers ne disent pas la même chose, et **l'écart entre eux est souvent l'information
principale** : le VAE, c'est 16 % des commandes (volume), 65 % du montant (poids) et le plus gros
ticket (intensité). Trois réponses, un seul fichier.

---

## 9. Mémo des gestes du jour

| Geste | Où |
|---|---|
| Créer un TCD | *Insertion › Tableau croisé dynamique* |
| Changer somme / moyenne / nombre | Clic droit sur une valeur › *Paramètres des champs de valeurs* |
| Afficher en % | idem › onglet *Afficher les valeurs* |
| Grouper des dates ou des tranches | Clic droit sur une étiquette de ligne › *Grouper* |
| Actualiser après modification de la source | *Données › Actualiser tout* (`Ctrl + Alt + F5`) |
| Insérer un segment | *Analyse du TCD › Insérer un segment* |
| Graphique croisé | *Analyse du TCD › Graphique croisé dynamique* |
| Aller voir les lignes derrière une case | **Double-clic sur la case** → Excel extrait le détail |

> 🕵️ Le **double-clic sur une case** est le meilleur outil de vérification qui existe. Un chiffre te
> surprend ? Double-clique : Excel crée une feuille avec les lignes exactes qui le composent. C'est
> comme ça qu'on trouve la commande à 379 050 € en quinze secondes.

---

## 10. À toi de jouer

➡️ **Lancement cet après-midi : [Brief B02-A — Le carburant est-il plus cher chez nous ?](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md)**
*(niveau 2 · adapter — 31 277 lignes de données réelles, en binôme, rendu jeudi 17 h 30)*

---

## 11. Auto-évaluation

- [ ] Je sais dire en une phrase ce que fait un TCD.
- [ ] Je connais la check-list de préparation d'une table plate.
- [ ] Je sais placer un champ dans la bonne zone, et pourquoi pas plus de 8 modalités en colonnes.
- [ ] Je vérifie toujours si ma valeur est en *Somme* ou en *Nombre*.
- [ ] Je sais afficher un pourcentage de ligne, de colonne et du total général.
- [ ] Je sais grouper des dates par mois sans ajouter de colonne au fichier source.
- [ ] Je sais que le TCD ne propose pas la médiane, et ce que je fais à la place.
- [ ] Je pense à *Actualiser* avant de lire ou de capturer un TCD.
- [ ] Je sais retrouver les lignes derrière n'importe quelle case.

---

## 12. Pour aller plus loin

- Microsoft — [créer un tableau croisé dynamique](https://support.microsoft.com/fr-fr/office/cr%C3%A9er-un-tableau-crois%C3%A9-dynamique-pour-analyser-des-donn%C3%A9es-de-feuille-de-calcul-a9a84538-bfe9-40a9-a8e9-f99134456576)
- Microsoft — [afficher des calculs dans un TCD](https://support.microsoft.com/fr-fr/office/afficher-diff%C3%A9rents-calculs-dans-les-champs-de-valeurs-d-un-tableau-crois%C3%A9-dynamique-011bf0e6-2db8-4dd1-9b2e-4be2b6dd6ea1)
- Microsoft — [grouper ou dissocier des données dans un TCD](https://support.microsoft.com/fr-fr/office/grouper-ou-dissocier-des-donn%C3%A9es-dans-un-tableau-crois%C3%A9-dynamique-c9d1ddd0-6580-47d1-82bc-c84a5a340725)
- Google — [créer des tableaux croisés dynamiques dans Sheets](https://support.google.com/docs/answer/1272900)

➡️ **Demain : [04 — Choisir le bon graphique](04-choisir-le-bon-graphique.md)**
