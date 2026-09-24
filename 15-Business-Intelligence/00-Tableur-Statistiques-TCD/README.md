# Module 00 — Tableur : statistiques descriptives & TCD

> Sous-module du parcours [Data Analyst](../../PATH_DATA_ANALYST.md) — module Business Intelligence.
> Sommaire complet : [README du module BI](../README.md).

Semaine **P2 · S39 · 21–25 septembre 2026** · Socle · 35 h · Excel (LibreOffice Calc ou Google Sheets acceptés).

Ce module est la suite directe de la semaine « Prise en main & tableur » (P1) : tu y avais **audité** un
fichier de ventes. Ici tu le fais **parler**.

## Compétences travaillées (référentiel WCS)

| Code | Compétence | Niveau visé cette semaine |
|---|---|---|
| **C3.1** | Utiliser les statistiques descriptives pour faire émerger l'information | 1 → 3 |
| **C4.2** | Visualisations descriptives : histogrammes, boîtes à moustache, nuages de points | 1 → 3 |
| **C4.5** | Tableur et tableaux croisés dynamiques | 1 → 3 |

La semaine monte les trois niveaux : tu **imites** lundi et mardi, tu **adaptes** mercredi et jeudi,
tu **transposes** vendredi.

## Cours

- [01 — Statistiques descriptives : moyenne, médiane, mode](01-statistiques-descriptives.md) *(lundi)*
- [02 — Dispersion : écart-type, quartiles et pièges de la moyenne](02-dispersion-et-pieges-de-la-moyenne.md) *(mardi)*
- [03 — Tableaux croisés dynamiques et croisements](03-tableaux-croises-dynamiques.md) *(mercredi)*
- [04 — Choisir le bon graphique](04-choisir-le-bon-graphique.md) *(jeudi)*

## Mise en pratique

| Niveau | Support | Quand |
|---|---|---|
| **1 · Imiter** | [Brief B02-I — Les ventes Cyclo'Nord](../../99-Brief/Data-Analyst-WSC/B02-I-imiter-ventes-cyclonord.md) · [exercice guidé pas à pas](05-exercice-guide-cyclonord.md) | lundi PM + mardi PM |
| **2 · Adapter** | [Brief B02-A — Le carburant est-il plus cher chez nous ?](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md) | mercredi + jeudi |
| **3 · Transposer** | [Brief B02-T — Portrait statistique d'un territoire](../../99-Brief/Data-Analyst-WSC/B02-T-transposer-portrait-territoire.md) | vendredi (FOAD) |

## Déroulé de la semaine

| Jour | Matin | Après-midi |
|---|---|---|
| **Lun 21** | Cours 01 — position (moyenne, médiane, mode) | Exercice guidé, partie A |
| **Mar 22** | Cours 02 — dispersion et pièges de la moyenne | Exercice guidé, partie B · correction collective |
| **Mer 23** | Cours 03 — TCD | Lancement du brief **Adapter** |
| **Jeu 24** | Cours 04 — choisir le bon graphique | Production brief Adapter · revue croisée 16 h |
| **Ven 25** | FOAD — brief **Transposer** | Dépôt 17 h 30 · restitutions 16 h |

## Jeux de données

Tout est dans [`donnees/`](donnees/) — voir [`donnees/SOURCES.md`](donnees/SOURCES.md) pour l'origine,
la licence et les limites de chaque fichier.

| Fichier | Lignes | Usage |
|---|---|---|
| `cyclonord_ventes_2025_fiable.xlsx` | 613 | Cours + exercice guidé |
| `cyclonord_commandes_2025_brut.xlsx` | 627 | Rappel P1 (fichier avant nettoyage) |
| `carburants_france_releve.xlsx` | 31 277 | Brief Adapter |
| `portrait_territoire_hdf_socle.xlsx` | 3 782 communes | Brief Transposer (socle de départ) |

## Pré-requis

La semaine P1 : ouvrir un classeur, trier, filtrer, mise en forme conditionnelle, tableau structuré
(`Ctrl + L`). Aucune formule complexe n'est supposée connue.

## Ce qui vient après

- **P3 (S40)** — Python : tu recalculeras ces mêmes indicateurs en code.
- **P6 (S43)** — pandas & matplotlib : les mêmes graphiques, en Python — voir
  [04-Analyse-Exploratoire-EDA](../04-Analyse-Exploratoire-EDA/README.md).
- **P25 (S11)** — Tableur expert : TCD avancés, segments, `RECHERCHEX`, Plotly — voir
  [19-Tableur-Avance](../19-Tableur-Avance/README.md).
