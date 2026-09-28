# Module 00 — Tableur : statistiques descriptives et TCD, sur Google Sheets

> Sous-module du parcours [Data Analyst](../../PATH_DATA_ANALYST.md) — module Business Intelligence.
> Sommaire complet : [README du module BI](../README.md).

**Deux semaines · 9 h – 17 h · outil unique : Google Sheets.**
Cette page est ta **feuille de route** : chaque jour, elle te dit quoi ouvrir, quoi faire et quoi
rendre. Tu n'as besoin d'aucun autre document pour t'organiser.

![Infographie de synthèse du module : la médiane est plus robuste que la moyenne face aux valeurs extrêmes ; l'écart-type mesure la dispersion autour de la moyenne ; distribution symétrique (moyenne = médiane), étalée à droite (moyenne > médiane) ou à gauche (moyenne < médiane) ; toujours préciser le périmètre et l'effectif ; le TCD regroupe pour calculer ; un graphique = une intention (barres pour comparer, courbes pour l'évolution, histogrammes pour la distribution) ; éviter la 3D, les axes tronqués et les camemberts à plus de 3 parts](images/synthese-analyse-de-donnees.jpg)

*Le module en une image, avec deux réserves. Dans l'encadré rouge, le petit diagramme en barres du
milieu est lui aussi un **mauvais exemple** : ses graduations (100, 175, 110, 105) ne sont pas dans
l'ordre. Et les trois courbes de distribution ont toutes la même forme de cloche : la vraie forme
d'une distribution « étalée à droite » est dans le [cours 00](00-maths-a-la-main.md#en-une-image)
et le [cours 01](01-statistiques-descriptives.md).*

### Les vidéos du module

| Vidéo | Durée | Où elle sert |
|---|---|---|
| [La médiane robuste](videos/la-mediane-robuste.mp4) | 7 min | [cours 00](00-maths-a-la-main.md), section 3 · lundi |
| [L'écart-type : quand la moyenne vous ment](videos/ecart-type-quand-la-moyenne-ment.mp4) | 1 min | [cours 02](02-dispersion-et-pieges-de-la-moyenne.md), section 4 · mardi |
| [Le mirage du magasin numéro un](videos/le-mirage-du-magasin-numero-un.mp4) | 1 min | [cours 02](02-dispersion-et-pieges-de-la-moyenne.md), section 7 (le cas Arras) · mardi |

*Vidéos générées avec NotebookLM à partir des cours. Chacune est suivie, dans le cours, de ce
qu'elle simplifie ou invente.*

---

## Le parcours en un coup d'œil

| Niveau | Support | Du… au… | Rendu |
|---|---|---|---|
| **1 · Imiter** | cours 01 à 04 + [exercice guidé Cyclo'Nord](05-exercice-guide-cyclonord.md) | lundi → jeudi matin (semaine 1) | **jeudi 12 h 30** |
| **2 · Adapter** | [brief B02-A — Prix du gazole](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md) | jeudi après-midi → lundi (semaine 2) | **lundi 16 h 30** |
| **3 · Transposer** | [cours 06](06-joindre-deux-tableaux-xlookup.md) + [brief B02-T — Portrait d'un territoire](../../99-Brief/Data-Analyst-WSC/B02-T-transposer-portrait-territoire.md) | mardi → vendredi (semaine 2) | **vendredi 12 h 30** |

## Semaine 1

| Jour | 9 h – 10 h | 10 h 15 – 12 h 30 | 13 h 30 – 16 h 30 | 16 h 30 – 17 h |
|---|---|---|---|---|
| **Lundi** | Démo : [cours 01 — Position](01-statistiques-descriptives.md) | 10 h 15 – 11 h 15 : lecture du [cours 00, partie 1](00-maths-a-la-main.md) (à la main, sans Sheets) · puis exercice guidé : mise en place | Partie A | Correction collective A |
| **Mardi** | Démo : [cours 02 — Dispersion](02-dispersion-et-pieges-de-la-moyenne.md) | 10 h 15 – 11 h 15 : lecture du [cours 00, partie 2](00-maths-a-la-main.md) + exercices · puis partie B | Partie B (suite) | Correction collective B |
| **Mercredi** | Démo : [cours 03 — TCD](03-tableaux-croises-dynamiques.md) | Partie C | Partie C (suite) | Correction collective C |
| **Jeudi** | Démo : [cours 04 — Graphiques](04-choisir-le-bon-graphique.md) | Partie D (graphiques) · **rendu Cyclo'Nord 12 h 30** | 13 h 30 : lancement de **B02-A**, production | Point d'étape |
| **Vendredi** | B02-A : production | B02-A : production | B02-A : production | Point d'étape |

## Semaine 2

| Jour | 9 h – 10 h 30 | 10 h 45 – 12 h 30 | 13 h 30 – 16 h 30 | 16 h 30 – 17 h |
|---|---|---|---|---|
| **Lundi** | B02-A : production | B02-A : note | 14 h 30 revue croisée · 15 h 15 finitions · **rendu B02-A 16 h 30** | Retour collectif B02-A |
| **Mardi** | 9 h lancement de **B02-T** · démo : [cours 06 — Joindre deux tableaux](06-joindre-deux-tableaux-xlookup.md) | B02-T : étape 1 (import) et étape 2 (tableau `Analyse`) | B02-T : étape 2, suite | Point de contrôle |
| **Mercredi** | B02-T : étape 3 (position et dispersion) | B02-T : étapes 3 et 4 (ce qui manque) | B02-T : étape 5 (choix des critères) | Point de contrôle |
| **Jeudi** | B02-T : étape 6 (la règle) | B02-T : étape 6 | B02-T : étape 7 (graphiques) | Point de contrôle |
| **Vendredi** | Note et diapositive | Note · **rendu B02-T 12 h 30** | **Restitutions** (5 min chacun) | Retour collectif |

Pause du midi : 12 h 30 – 13 h 30. **Aucune échéance après 16 h 30.**

## Les règles, valables pendant les deux semaines

| Règle | Détail |
|---|---|
| **Un seul outil** | Google Sheets. Paramètres régionaux **France** (*Fichier › Paramètres*) : dans les formules, les arguments se séparent par des **points-virgules** (`;`). Les fonctions s'écrivent en anglais (`MEDIAN`, `FILTER`…), le nom français est donné entre parenthèses. |
| **Seul** | Tout le travail est individuel. L'entraide est encouragée : chacun son classeur. |
| **On ne touche pas aux données** | L'onglet importé (`Ventes_2025`, `Releve_prix`, `Communes_HDF`, `INSEE_…`) n'est jamais modifié. Tu travailles dans tes propres onglets. |
| **Un seul endroit pour rendre** | Ton dépôt GitHub de la semaine 1. Un dossier par rendu : **`P2-cyclonord/`**, **`P2-carburants/`** et **`P2-territoire/`**. Dans chacun : un `README.md` avec **le lien** vers ton Google Sheets partagé en *Lecteur*, et l'export `.xlsx` du classeur. |
| **Les maths à la main** | Le [cours 00 — Les maths à la main](00-maths-a-la-main.md) refait chaque calcul (moyenne, médiane, quartiles, écart-type, pourcentages, moyenne pondérée) sur quelques nombres, sans aucun prérequis. Partie 1 le lundi, partie 2 le mardi, une heure chacune dans le planning, puis à garder ouvert. |
| **Les cours sont des démos** | Le matin, le formateur montre les gestes pendant 45 min ; tu refais avec lui. Le texte du cours sert ensuite de mémo : inutile de le lire en entier avant. |

## Ce que tu sauras faire à la fin des deux semaines

- Résumer une colonne de chiffres avec une **médiane** et des **quartiles**, et dire pourquoi la
  moyenne peut tromper.
- Donner chaque chiffre avec son **périmètre** (quelles lignes ont été comptées).
- Calculer par groupe avec `COUNTIFS`, `SUMIFS`, `MEDIAN(FILTER(…))`.
- Construire un **tableau croisé dynamique** et y demander une somme, un nombre ou une médiane.
- Choisir le bon **graphique** et le rendre lisible : titre qui dit le message, axes, source.
- **Joindre** deux fichiers avec `XLOOKUP` et calculer une moyenne **pondérée**.
- **Décider** à partir de données et défendre ta décision.

## Les données

Tout est dans [`donnees/`](donnees/) — origine, licence et limites dans [`donnees/SOURCES.md`](donnees/SOURCES.md).

| Fichier | Lignes | Quand |
|---|---|---|
| `cyclonord_ventes_2025_fiable.xlsx` | 613 commandes | semaine 1, lundi → jeudi matin (exercice guidé) |
| `carburants_france_releve.xlsx` | 31 277 relevés de prix | jeudi après-midi → lundi (brief B02-A) |
| `portrait_territoire_hdf_socle.xlsx` | 3 782 communes | semaine 2, mardi → vendredi (brief B02-T) |
| `insee_revenus_population_hdf.xlsx` | 3 782 communes · 92 intercommunalités | semaine 2, mardi → vendredi (brief B02-T) |

## Compétences travaillées (référentiel WCS)

| Code | Compétence | Niveau visé |
|---|---|---|
| **C3.1** | Utiliser les statistiques descriptives pour faire émerger l'information | 1 (exercice guidé) → 2 (B02-A) → 3 (B02-T) |
| **C4.2** | Visualisations descriptives | 1 → 2 → 3 |
| **C4.5** | Tableur et tableaux croisés dynamiques | 1 → 2 → 3 |

## Avant de commencer

Il faut savoir trier, filtrer et appliquer une mise en forme conditionnelle (semaine 1), et avoir
un compte Google.

## Ce qui vient après

Les gestes de ce module ne disparaissent pas quand l'outil change : ils changent de nom.

| Dans Google Sheets | En SQL | Dans Power BI |
|---|---|---|
| un onglet de données (`Ventes_2025`) | une table | une table du modèle |
| un filtre, `FILTER(…; condition)` | `WHERE` | un filtre ou un segment |
| un TCD : regrouper, puis additionner ou compter | `GROUP BY` + `SUM`, `COUNT` | un visuel agrégé |
| `XLOOKUP` sur un code | `JOIN` | une relation entre deux tables |
| une colonne calculée par formule | une expression dans le `SELECT` | une colonne calculée ou une mesure DAX |


- **Python** : tu recalculeras ces mêmes indicateurs en code, et les chiffres devront tomber juste.
- **pandas et matplotlib** : les mêmes graphiques, en Python — voir
  [04-Analyse-Exploratoire-EDA](../04-Analyse-Exploratoire-EDA/README.md).
- **Tableur avancé** : segments, tableaux de bord — voir [19-Tableur-Avance](../19-Tableur-Avance/README.md).
