# 📊 Parcours : Data Analyst V2

[🏠 Retour à l'accueil](README.md)

Ce parcours prépare au métier de **Data Analyst** dans une acception **technique et polyvalente** :
un profil capable de **collecter** (SQL, API, scraping), **traiter en Python** (pandas, RegEx),
**modéliser** (statistiques et Machine Learning) et **restituer** (dataviz Python, cartographie,
tableaux de bord BI).

> **V1 ou V2 ?** Le parcours [Data Analyst (V1)](PATH_DATA_ANALYST.md) est centré **Business
> Intelligence** (Power BI, DAX, dashboards). Cette **V2** est plus large et plus technique :
> elle ajoute un fort socle **programmation Python, collecte automatisée et Machine Learning**.
> Les deux parcours coexistent ; choisissez selon le profil visé.

- **Conformité (compétences → cours)** : [`15-Business-Intelligence/CONFORMITE-DA-V2.md`](15-Business-Intelligence/CONFORMITE-DA-V2.md)
- **Briefs du parcours** : [`99-Brief/Data-Analyst-V2/`](99-Brief/Data-Analyst-V2/)

---

## 🧭 Les 4 blocs de compétences

| Bloc | Intitulé | Dominante |
|:---:|:---|:---|
| **1** | Collecte : exploration & requêtage des bases, récupération des données | SQL, scraping, API REST, RGPD |
| **2** | Automatisation du traitement : nettoyage, complétion, correction | Python, pandas, RegEx |
| **3** | Modélisation des données structurées : corrélations & Machine Learning | statistiques, ML, NLP |
| **4** | Visualisation : valorisation, interprétation & tableau de bord | dataviz Python, cartographie, BI |

> Format de référence : **~27 semaines** (1 bloc = plusieurs semaines de cours + 1 brief de mise
> en situation), avec un **socle maths & stats** avant la modélisation, puis un **projet final**
> intégrant les 4 blocs.

---

## 📅 Timeline de Formation (27 semaines · un brief par bloc + projet final)

### 🟦 Bloc 1 — Collecte des données (S1-S6)
*Modéliser, requêter, automatiser la récupération, garantir le RGPD.*

| Sem. | Cours associé | 🎯 Livrable |
|:---:|:---|:---|
| **S1** | [Métier de Data Analyst](15-Business-Intelligence/01-Metier-Data-Analyst/) · [Panorama outils BI](15-Business-Intelligence/02-Panorama-Outils-BI/) | Prise en main, installation |
| **S2** | [SQL — Select & agrégations](01-Fondamentaux/SQL/01-Introduction-Select/) · [Agrégations](01-Fondamentaux/SQL/02-Agregations-Groupby/) | Requêtes de base |
| **S3** | [SQL — Jointures](01-Fondamentaux/SQL/03-Jointures/) · [Conception DDL/DML](01-Fondamentaux/SQL/04-Conception-DDL-DML/) | Modéliser une base relationnelle |
| **S4** | [SQL — Fonctions avancées (CTE, fenêtres)](01-Fondamentaux/SQL/05-Fonctions-Avancees/) · [Extraction & analyse](01-Fondamentaux/SQL/09-Extraction-Analyse/) | Requêtes d'analyse avancées |
| **S5** | [API REST & Requests](01-Fondamentaux/Python/06-Data-Engineering/) · [Web scraping](15-Business-Intelligence/14-Collecte-Donnees/02-web-scraping.md) | Automatiser une collecte |
| **S6** | [Processus de collecte](15-Business-Intelligence/14-Collecte-Donnees/01-processus-collecte.md) · [RGPD & gouvernance](01-Fondamentaux/RGPD-Gouvernance/) | 🏁 [Brief Bloc 1 — Collecte](99-Brief/Data-Analyst-V2/BRIEF_BLOC_1_COLLECTE.md) |

### 🟩 Bloc 2 — Automatisation du traitement (S7-S11)
*Nettoyer, uniformiser et anonymiser via un programme réutilisable.*

| Sem. | Cours associé | 🎯 Livrable |
|:---:|:---|:---|
| **S7** | [Python — Syntaxe & algorithmie](01-Fondamentaux/Python/01-Syntaxe/) · [Algorithmie](01-Fondamentaux/Algorithmie/) | Scripter un traitement |
| **S8** | [Python — Qualité & tests](01-Fondamentaux/Python/05-Qualite-Tests/) · [Bonnes pratiques](01-Fondamentaux/Bonne%20pratique/) | Clean code (PEP8) |
| **S9** | [Pandas — bases & avancé](01-Fondamentaux/Python/06-Data-Engineering/) · [EDA avec pandas](15-Business-Intelligence/04-Analyse-Exploratoire-EDA/) | Manipuler des DataFrames |
| **S10** | [Nettoyage des données](15-Business-Intelligence/16-Nettoyage-Donnees/) | Outliers & valeurs manquantes |
| **S11** | [Expressions régulières](01-Fondamentaux/Python/04-Bibliotheque-Standard/) · [Anonymisation RGPD](01-Fondamentaux/RGPD-Gouvernance/05-anonymisation-pseudonymisation.md) | 🏁 [Brief Bloc 2 — Traitement](99-Brief/Data-Analyst-V2/BRIEF_BLOC_2_TRAITEMENT.md) |

### 🧮 Socle Maths & Stats (S12-S13)
*Sécuriser les statistiques mobilisées par la modélisation et la décision par la donnée.*

| Sem. | Cours associé | 🎯 Livrable |
|:---:|:---|:---|
| **S12** | [Statistiques descriptives & régression](01-Fondamentaux/Mathematiques/03-Statistiques-Descriptives/) · [Probabilités](01-Fondamentaux/Mathematiques/04-Probabilites/) · [Stats appliquées](15-Business-Intelligence/04-Analyse-Exploratoire-EDA/) | Corrélations, distributions |
| **S13** | [Statistique inférentielle (tests, p-value, IC)](01-Fondamentaux/Mathematiques/05-Statistique-Inferentielle/) · [A/B testing](01-Fondamentaux/Mathematiques/05-Statistique-Inferentielle/03-ab-testing.md) | Décider face au hasard |

### 🟨 Bloc 3 — Modélisation & Machine Learning (S14-S18)
*Prévisions (régression / classification), NLP, biais.*

| Sem. | Cours associé | 🎯 Livrable |
|:---:|:---|:---|
| **S14** | [ML — Comprendre les données & valider](08-Machine-Learning/cours/06-comprendre-donnees.md) · [Feature engineering](08-Machine-Learning/cours/07-feature-engineering.md) · [Validation](08-Machine-Learning/cours/13-validation-generalisation.md) | Process ML |
| **S15** | [ML — Régression (modèles linéaires)](08-Machine-Learning/cours/09-modeles-lineaires.md) | Prévoir une valeur numérique |
| **S16** | [ML — Classification](08-Machine-Learning/cours/10-arbres-forets.md) · [Métriques](08-Machine-Learning/cours/12-metriques-classification.md) | Catégoriser |
| **S17** | [NLP — nettoyage & vectorisation](09-Deep-Learning/NLP/) | Analyse de sentiments |
| **S18** | [Interprétabilité & éthique](08-Machine-Learning/cours/14-interpretabilite-ethique.md) · [Éthique, biais & RGPD](15-Business-Intelligence/12-Ethique-Biais-RGPD/) | 🏁 [Brief Bloc 3 — Modélisation](99-Brief/Data-Analyst-V2/BRIEF_BLOC_3_MODELISATION.md) |

### 🟥 Bloc 4 — Visualisation & tableau de bord (S19-S24)
*Dataviz descriptive & interactive, cartographie, BI, accessibilité, restitution.*

| Sem. | Cours associé | 🎯 Livrable |
|:---:|:---|:---|
| **S19** | [Dataviz descriptive (EDA)](15-Business-Intelligence/04-Analyse-Exploratoire-EDA/) · [Maths pour la dataviz](01-Fondamentaux/Mathematiques/06-Mathematiques-Dataviz/) | Graphiques descriptifs |
| **S20** | [Dataviz interactive (Plotly/Bokeh)](15-Business-Intelligence/11-Visualisations-Avancees/02-dataviz-interactive-python.md) | Graphiques interactifs |
| **S21** | [Cartographie (Folium)](15-Business-Intelligence/11-Visualisations-Avancees/03-cartographie-folium.md) | Cartes de données |
| **S22** | [Tableur avancé (TCD)](15-Business-Intelligence/19-Tableur-Avance/01-tableur-tcd.md) | Croisements & recherches |
| **S23** | [Dashboards](15-Business-Intelligence/07-Dashboards-Fondamentaux/) · [Modèle étoile & Power Query](15-Business-Intelligence/09-Modelisation-Etoile-PowerQuery/) · [DAX](15-Business-Intelligence/10-DAX/) · [Viz avancées & accessibilité](15-Business-Intelligence/11-Visualisations-Avancees/) | Tableau de bord BI |
| **S24** | [Restitution & storytelling](15-Business-Intelligence/08-Restitution-Storytelling/) · [Accompagnement métier](15-Business-Intelligence/13-Accompagnement-Metier/) | 🏁 [Brief Bloc 4 — Visualisation](99-Brief/Data-Analyst-V2/BRIEF_BLOC_4_VISUALISATION.md) |

### 🏁 Projet final (S25-S27)
*Chaîne complète, de la collecte au tableau de bord.*

| Sem. | Cours associé | 🎯 Livrable |
|:---:|:---|:---|
| **S25-27** | [Préparation à l'évaluation](15-Business-Intelligence/18-Preparation-Certification/) · *projet de bout en bout* | 🏁 [Brief Projet final](99-Brief/Data-Analyst-V2/BRIEF_PROJET_FINAL.md) |

> 🗓️ **5 briefs de mise en situation** (un par bloc + projet final), adossés à ~27 semaines de
> cours dont un **socle maths & stats** avant la modélisation. Index : [briefs Data Analyst V2](99-Brief/Data-Analyst-V2/README.md).

---

## 🗺️ Ce que couvre le parcours

| Domaine | Couvert par |
| :--- | :--- |
| **Collecte** (SQL, API, scraping, RGPD) | [SQL](01-Fondamentaux/SQL/) · [Python/06](01-Fondamentaux/Python/06-Data-Engineering/) · [15-BI/14](15-Business-Intelligence/14-Collecte-Donnees/) · [RGPD](01-Fondamentaux/RGPD-Gouvernance/) |
| **Traitement** (Python, pandas, RegEx) | [Python](01-Fondamentaux/Python/) · [15-BI/16](15-Business-Intelligence/16-Nettoyage-Donnees/) |
| **Modélisation** (stats, ML, NLP) | [Mathématiques](01-Fondamentaux/Mathematiques/) · [08-Machine-Learning](08-Machine-Learning/) · [09-DL/NLP](09-Deep-Learning/NLP/) |
| **Visualisation** (dataviz, cartographie, BI) | [15-Business-Intelligence](15-Business-Intelligence/) (modules 04, 07-11, 17, 19) |

### 🤖 Périmètre Machine Learning & NLP — à cibler

Les modules [08-Machine-Learning](08-Machine-Learning/) et [09-Deep-Learning/NLP](09-Deep-Learning/NLP/)
vont **au-delà** du niveau Data Analyst (jusqu'au MLOps et aux transformers). Pour ce parcours,
on cible « **comprendre & utiliser** » : chapitres ML **01, 02, 06, 07, 09, 12, 13, 21** et, en
NLP, les **modules 2-3** (nettoyage, BoW/TF-IDF, classifieur simple). L'industrialisation
(Docker, MLflow, BERT) relève du profil Data Scientist.

---

## 🎯 Ce que vous saurez faire

| Bloc | Compétence clé | Livrable attendu |
| :--- | :--- | :--- |
| **Collecte** | Modéliser, requêter et automatiser une collecte (API/scraping), RGPD | Base SQL + scripts de collecte + registre RGPD |
| **Traitement** | Nettoyer et uniformiser via un programme réutilisable | Outil de traitement Python + tests |
| **Modélisation** | Prévoir (régression/classification), analyser des sentiments, expliquer les biais | Notebooks ML + note biais |
| **Visualisation** | Concevoir un tableau de bord interactif et accessible | Dashboard BI + cartographie + restitution |

---

## 🛠️ Outils enseignés
**SQL** (PostgreSQL/SQLite) · **Python** (pandas, numpy, **requests + BeautifulSoup**,
matplotlib/seaborn, **Plotly/Bokeh**, **Folium**, scikit-learn) · **Power BI** (Power Query + DAX)
ou **Tableau** · **Tableur** (Excel / Google Sheets — TCD) · **Git/GitHub**.

---
[🏠 Retour à l'accueil](README.md)
