# Module 00 — Tableur : statistiques descriptives et TCD, sur Google Sheets

> Sous-module du parcours [Data Analyst](../../PATH_DATA_ANALYST.md) — module Business Intelligence.
> Sommaire complet : [README du module BI](../README.md).

**Une semaine · 9 h – 17 h · outil unique : Google Sheets.**
Cette page est ta **feuille de route** : chaque jour, elle te dit quoi ouvrir, quoi faire et quoi
rendre. Tu n'as besoin d'aucun autre document pour t'organiser.

---

## La semaine en un coup d'œil

| Jour | 9 h – 10 h | 10 h 15 – 12 h 30 | 13 h 30 – 16 h 30 | 16 h 30 – 17 h | À rendre |
|---|---|---|---|---|---|
| **Lundi** | Démo : [cours 01 — Position](01-statistiques-descriptives.md) | [Exercice guidé](05-exercice-guide-cyclonord.md) : mise en place + partie A | Exercice guidé, partie A (suite) | Correction collective de la partie A | rien |
| **Mardi** | Démo : [cours 02 — Dispersion](02-dispersion-et-pieges-de-la-moyenne.md) | Exercice guidé, partie B | Exercice guidé, partie B (suite) | Correction collective de la partie B | rien |
| **Mercredi** | Démo : [cours 03 — TCD](03-tableaux-croises-dynamiques.md) | Exercice guidé, partie C | Partie C (suite), rendu à **16 h 30** | Correction collective de la partie C | **Cyclo'Nord**, 16 h 30 |
| **Jeudi** | Démo : [cours 04 — Graphiques](04-choisir-le-bon-graphique.md) | Exercice express du cours 04 (20 min), puis, dans ton classeur Cyclo'Nord, les graphiques des questions 1 et 2 (barres du CA livré par magasin, courbe du CA livré par mois) | 13 h 30 : lancement du [brief B02-A](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md), puis production | Point d'étape | rien |
| **Vendredi** | Brief B02-A : production | Brief B02-A : production | 14 h 30 revue croisée · 15 h 15 note et dépôt | **16 h 30** : retour collectif | **B02-A**, 16 h 30 |

Pause du midi : 12 h 30 – 13 h 30. **Aucune échéance après 16 h 30.**

## Les règles, valables toute la semaine

| Règle | Détail |
|---|---|
| **Un seul outil** | Google Sheets. Paramètres régionaux **France** (*Fichier › Paramètres*) : dans les formules, les arguments se séparent par des **points-virgules** (`;`). Les fonctions s'écrivent en anglais (`MEDIAN`, `FILTER`…), le nom français est donné entre parenthèses. |
| **Seul** | Tout le travail de la semaine est individuel. L'entraide est encouragée : chacun son classeur. |
| **On ne touche pas aux données** | L'onglet importé (`Ventes_2025`, `Releve_prix`) n'est jamais modifié. Tu travailles dans tes propres onglets. |
| **Un seul endroit pour rendre** | Ton dépôt GitHub de la semaine 1. Un dossier par rendu : **`P2-cyclonord/`** (mercredi) et **`P2-carburants/`** (vendredi). Dans chacun : un `README.md` avec **le lien** vers ton Google Sheets partagé en *Lecteur*, et l'export `.xlsx` du classeur. |
| **Les cours sont des démos** | Le matin, le formateur montre les gestes pendant 45 min ; tu refais avec lui. Le texte du cours sert ensuite de mémo : inutile de le lire en entier avant. |

## Ce que tu sauras faire vendredi soir

- Résumer une colonne de chiffres avec une **médiane** et des **quartiles**, et dire pourquoi la
  moyenne peut tromper.
- Donner chaque chiffre avec son **périmètre** (quelles lignes ont été comptées).
- Calculer par groupe avec `COUNTIFS`, `SUMIFS`, `MEDIAN(FILTER(…))`.
- Construire un **tableau croisé dynamique** et y demander une somme, un nombre ou une médiane.
- Choisir le bon **graphique** et le rendre lisible : titre qui dit le message, axes, source.

## Les données

Tout est dans [`donnees/`](donnees/) — origine, licence et limites dans [`donnees/SOURCES.md`](donnees/SOURCES.md).

| Fichier | Lignes | Quand |
|---|---|---|
| `cyclonord_ventes_2025_fiable.xlsx` | 613 commandes | lundi → jeudi matin (exercice guidé) |
| `carburants_france_releve.xlsx` | 31 277 relevés de prix | jeudi après-midi → vendredi (brief B02-A) |

## Compétences travaillées (référentiel WCS)

| Code | Compétence | Niveau visé |
|---|---|---|
| **C3.1** | Utiliser les statistiques descriptives pour faire émerger l'information | 1 (exercice guidé) → 2 (B02-A) |
| **C4.2** | Visualisations descriptives | 1 → 2 |
| **C4.5** | Tableur et tableaux croisés dynamiques | 1 → 2 |

> Le niveau 3 (« transposer » : portrait statistique d'un territoire, brief B02-T) est **reporté** à
> plus tard dans la formation, après l'apprentissage de la recherche entre deux fichiers
> (`XLOOKUP`), dont il a besoin.

## Avant de commencer

Il faut savoir trier, filtrer et appliquer une mise en forme conditionnelle (semaine 1), et avoir
un compte Google.

## Ce qui vient après

- **Python** : tu recalculeras ces mêmes indicateurs en code, et les chiffres devront tomber juste.
- **pandas et matplotlib** : les mêmes graphiques, en Python — voir
  [04-Analyse-Exploratoire-EDA](../04-Analyse-Exploratoire-EDA/README.md).
- **Tableur avancé** : `XLOOKUP`, segments, tableaux de bord — voir [19-Tableur-Avance](../19-Tableur-Avance/README.md).
