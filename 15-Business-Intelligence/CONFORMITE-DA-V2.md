# ✅ Conformité — Parcours Data Analyst V2

> Traçabilité **compétence → cours & brief** pour le parcours [Data Analyst V2](../PATH_DATA_ANALYST_V2.md),
> organisé en 4 blocs. Ce document centralise la correspondance ; les cours eux-mêmes restent
> neutres (pas de codes de compétence dans le corps public).

**Légende** : ✅ couvert · ✅✅ couvert au-delà du niveau attendu.

---

## Bloc n°1 — Collecte des données

| Comp. | Compétence | Statut | Cours support | Brief |
|:---:|:---|:---:|:---|:---:|
| C1.1 | Explorer, évaluer la qualité, interpréter | ✅ | [15-BI/01](01-Metier-Data-Analyst/), [03](03-Analyse-Besoin-Metier/), [04](04-Analyse-Exploratoire-EDA/) · [SQL/09](../01-Fondamentaux/SQL/09-Extraction-Analyse/) | Bloc 1 |
| C1.2 | Stratégie de décision par les données | ✅ | [15-BI/01](01-Metier-Data-Analyst/), [06](06-KPI-Indicateurs/) | Bloc 1 |
| C1.3 | Modéliser une base relationnelle (SQL) | ✅ | [SQL/04](../01-Fondamentaux/SQL/04-Conception-DDL-DML/) · [DataWarehouse](../05-Databases/DataWarehouse/) | Bloc 1 |
| C1.4 | Requêtes avancées (agrégations, jointures, vues, sous-requêtes) | ✅✅ | [SQL/02](../01-Fondamentaux/SQL/02-Agregations-Groupby/), [03](../01-Fondamentaux/SQL/03-Jointures/), [05](../01-Fondamentaux/SQL/05-Fonctions-Avancees/) | Bloc 1 |
| C1.5 | Automatiser une collecte (web scraping) | ✅ | [15-BI/14 · 02-web-scraping](14-Collecte-Donnees/02-web-scraping.md) | Bloc 1 |
| C1.6 | Interface de partage automatique (API REST) | ✅ | [Python/06](../01-Fondamentaux/Python/06-Data-Engineering/) · [Python/08-FastAPI](../01-Fondamentaux/Python/08-FastAPI/) | Bloc 1 |
| C1.7 | Contrôle collecte/usage, RGPD | ✅✅ | [RGPD-Gouvernance](../01-Fondamentaux/RGPD-Gouvernance/) · [15-BI/12](12-Ethique-Biais-RGPD/) | Bloc 1 |

## Bloc n°2 — Automatisation du traitement

| Comp. | Compétence | Statut | Cours support | Brief |
|:---:|:---|:---:|:---|:---:|
| C2.1 | Choix méthodologiques documentés | ✅ | [Python/05](../01-Fondamentaux/Python/05-Qualite-Tests/) · [Bonne pratique](../01-Fondamentaux/Bonne%20pratique/) | Bloc 2 |
| C2.2 | Outils/méthodes modernes (agile, suivi, IDE) | ✅ | [11-Gestion-Projet](../11-Gestion-Projet/) · [Git](../01-Fondamentaux/Git/) | Bloc 2 |
| C2.3 | Structures de données & algorithmie | ✅✅ | [Python/01-Syntaxe](../01-Fondamentaux/Python/01-Syntaxe/) · [Algorithmie](../01-Fondamentaux/Algorithmie/) | Bloc 2 |
| C2.4 | Bonnes pratiques (clean code, PEP8) | ✅ | [Python/05](../01-Fondamentaux/Python/05-Qualite-Tests/) · [Bonne pratique/03](../01-Fondamentaux/Bonne%20pratique/03-code-propre.md) | Bloc 2 |
| C2.5 | DataFrames (pandas) | ✅✅ | [Python/06](../01-Fondamentaux/Python/06-Data-Engineering/) · [15-BI/04](04-Analyse-Exploratoire-EDA/) | Bloc 2 |
| C2.6 | Nettoyage : outliers, valeurs manquantes | ✅ | [15-BI/16](16-Nettoyage-Donnees/) | Bloc 2 |
| C2.7 | RegEx + anonymisation RGPD | ✅ | [Python/04](../01-Fondamentaux/Python/04-Bibliotheque-Standard/) · [RGPD/05](../01-Fondamentaux/RGPD-Gouvernance/05-anonymisation-pseudonymisation.md) | Bloc 2 |

## Bloc n°3 — Modélisation des données structurées

| Comp. | Compétence | Statut | Cours support | Brief |
|:---:|:---|:---:|:---|:---:|
| C3.1 | Statistiques descriptives (variance, quantiles, corrélation) | ✅ | [Maths/03](../01-Fondamentaux/Mathematiques/03-Statistiques-Descriptives/) · [15-BI/04](04-Analyse-Exploratoire-EDA/) | Bloc 3 |
| C3.2 | Process ML (split, entraînement, prédiction, mesure) | ✅ | [08-ML/01,02,06,07,13](../08-Machine-Learning/) | Bloc 3 |
| C3.3 | Régressions + métriques | ✅ | [08-ML/09](../08-Machine-Learning/cours/09-modeles-lineaires.md) | Bloc 3 |
| C3.4 | Classifications + métriques | ✅ | [08-ML/10,12](../08-Machine-Learning/cours/12-metriques-classification.md) | Bloc 3 |
| C3.5 | NLP — analyse de sentiments | ✅ | [09-DL/NLP](../09-Deep-Learning/NLP/) | Bloc 3 |
| C3.6 | Contrôler & documenter les biais | ✅ | [08-ML/14](../08-Machine-Learning/cours/14-interpretabilite-ethique.md) · [15-BI/12](12-Ethique-Biais-RGPD/) | Bloc 3 |
| C3.7 | Vulgariser un algorithme (éviter la boîte noire) | ✅ | [08-ML/14](../08-Machine-Learning/cours/14-interpretabilite-ethique.md) · [15-BI/08](08-Restitution-Storytelling/) | Bloc 3 |

## Bloc n°4 — Visualisation des données

| Comp. | Compétence | Statut | Cours support | Brief |
|:---:|:---|:---:|:---|:---:|
| C4.1 | Identifier/prioriser, structurer | ✅ | [15-BI/06](06-KPI-Indicateurs/), [07](07-Dashboards-Fondamentaux/), [03](03-Analyse-Besoin-Metier/) | Bloc 4 |
| C4.2 | Visualisations descriptives (nuages, boîtes, histogrammes) | ✅ | [15-BI/04](04-Analyse-Exploratoire-EDA/) · [Maths/06](../01-Fondamentaux/Mathematiques/06-Mathematiques-Dataviz/) | Bloc 4 |
| C4.3 | Dataviz interactive (Plotly/Bokeh) | ✅ | [15-BI/11 · 02](11-Visualisations-Avancees/02-dataviz-interactive-python.md) | Bloc 4 |
| C4.4 | Cartographie (Folium) | ✅ | [15-BI/11 · 03](11-Visualisations-Avancees/03-cartographie-folium.md) | Bloc 4 |
| C4.5 | Tableur : TCD, recherches inter-fichiers | ✅ | [15-BI/19](19-Tableur-Avance/01-tableur-tcd.md) | Bloc 4 |
| C4.6 | Tableaux de bord BI (Power BI ou Tableau) | ✅✅ | [15-BI/07](07-Dashboards-Fondamentaux/), [09](09-Modelisation-Etoile-PowerQuery/), [10](10-DAX/), [11](11-Visualisations-Avancees/), [17](17-Dashboard-Expert/) | Bloc 4 |
| C4.7 | Accessibilité (handicaps visuels, WCAG) | ✅ | [15-BI/11](11-Visualisations-Avancees/), [17](17-Dashboard-Expert/) · [11-Gestion-Projet/07](../11-Gestion-Projet/07-accessibilite-eco-conception.md) | Bloc 4 |
| C4.8 | Présenter à l'oral & à l'écrit | ✅ | [15-BI/08](08-Restitution-Storytelling/) | Bloc 4 |

---

## Synthèse

- **28 compétences** au référentiel, réparties en **4 blocs**.
- Toutes couvertes par les modules du dépôt ; **4 cours** ont été créés spécifiquement pour ce
  parcours : web scraping (C1.5), dataviz interactive Plotly/Bokeh (C4.3), cartographie Folium
  (C4.4), tableur avancé (C4.5).
- **5 briefs de mise en situation** : un par bloc + [projet final](../99-Brief/Data-Analyst-V2/BRIEF_PROJET_FINAL.md).

## Points de vigilance (périmètre)

- **ML (bloc 3)** : cibler « comprendre & utiliser » (chapitres 01, 02, 06, 07, 09, 12, 13, 21) —
  l'industrialisation (MLOps) relève du Data Scientist.
- **NLP (C3.5)** : un sous-ensemble **BoW / TF-IDF + classifieur simple** (Modules 2-3) suffit ;
  transformers/BERT sont hors périmètre DA.
- **Scraping (C1.5)** : toujours cadrer juridiquement (robots.txt, CGU, RGPD).
