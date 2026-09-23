# Brief Bloc 1 — Mettre en place une collecte de données pour NordRetail

## Informations

| Critère | Valeur |
|---------|--------|
| **Bloc** | Bloc 1 — Collecte : exploration & requêtage des bases, récupération des données |
| **Durée** | ~2 semaines (10 jours) |
| **Niveau** | Intermédiaire |
| **Modalité** | Binôme |
| **Technologies** | SQL (SQLite ou PostgreSQL), Python (requests, BeautifulSoup, pandas), Git/GitHub |
| **Prérequis** | [SQL](../../01-Fondamentaux/SQL/) · [API REST & Requests](../../01-Fondamentaux/Python/06-Data-Engineering/) · [Web scraping](../../15-Business-Intelligence/14-Collecte-Donnees/02-web-scraping.md) · [RGPD](../../01-Fondamentaux/RGPD-Gouvernance/) |

## Description rapide

En binôme, vous incarnez la cellule data de **NordRetail**. La direction veut disposer d'une
base de ventes fiable et enrichie de sources externes (prix concurrents, météo). Vous **modélisez
une base relationnelle**, écrivez des **requêtes d'analyse avancées**, **automatisez** la
récupération de données depuis une API et par web scraping, et vous **documentez la conformité
RGPD** de l'ensemble. Livrable : un processus de collecte reproductible et légal.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Modéliser une base de données relationnelle** répondant à un besoin métier (tables, clés, intégrité).
- **Écrire des requêtes SQL avancées** : agrégations, jointures, sous-requêtes, vues.
- **Automatiser une collecte** depuis une API REST (`requests`) et par web scraping (`BeautifulSoup`).
- **Contrôler la légalité** d'une collecte (`robots.txt`, CGU) et **documenter le RGPD** (registre des traitements).
- Évaluer la **qualité** et les **possibilités d'exploitation** des données collectées.

## Contexte

**L'entreprise et son problème**

NordRetail, enseigne des Hauts-de-France (12 magasins + e-commerce), pilote ses ventes « au
feeling ». Les données de caisse existent (exports plats), mais rien n'est structuré ni enrichi :
impossible de comparer les prix aux concurrents, ni de relier les ventes à des facteurs externes
(météo, saisonnalité). La direction vous mandate pour **construire la brique de collecte** d'un
futur système décisionnel.

**La question centrale**

> « De quelles données NordRetail a-t-elle besoin, où les trouver, et comment les rassembler de
> façon fiable, automatisée et légale ? »

**Les sources fournies**

Vous partez du jeu **NordRetail** dans [`../Data-Analyst/data/`](../Data-Analyst/data/) :
`ventes_magasins.csv` (~12 000 ventes), `referentiel_produits.csv`, `setup.sql`. Vous les
chargez dans une base SQL. Les sources externes (prix concurrents, météo) sont récupérées par
scraping / API pendant le brief.

## Modalités pédagogiques

Projet en BINÔME sur ~10 jours, dépôt GitHub public partagé.

### Phase 1 — Modélisation de la base relationnelle (J1-J2)

À partir des fichiers fournis, concevez un **modèle relationnel** : quelles tables (ventes,
produits, magasins), quelles clés primaires et étrangères, quelles contraintes d'intégrité ?
Écrivez le DDL (`CREATE TABLE`), justifiez la granularité et documentez le schéma (diagramme).
Chargez les données. Comment garantissez-vous l'intégrité référentielle (une vente pointe vers
un produit et un magasin existants) ?

### Phase 2 — Requêtes d'analyse avancées (J3-J4)

Écrivez une **bibliothèque de requêtes SQL** répondant à des questions métier : CA par magasin
et par mois (agrégation + `GROUP BY`), top produits (sous-requête ou fenêtre), comparaison
magasin/e-commerce (jointures), création d'une **vue** réutilisable pour le reporting. Chaque
requête est commentée et rattachée à une question métier.

### Phase 3 — Automatiser la collecte externe : API + scraping (J5-J7)

Enrichissez la base. Récupérez des données **via une API REST** (par exemple météo Open-Meteo,
gratuite et sans clé) avec `requests`, en documentant le format d'échange (JSON). Récupérez des
**prix concurrents par web scraping** (`BeautifulSoup`) sur un site autorisé — **après** avoir
vérifié `robots.txt` et les CGU. Temporisez vos requêtes, identifiez votre `User-Agent`.
Consolidez le tout dans la base ou dans des CSV propres.

### Phase 4 — Conformité RGPD & documentation (J8-J9)

Pour chaque source, identifiez les **données personnelles** éventuelles (ex. `client_id`) et
remplissez un **registre des traitements** simplifié : finalité, base légale, durée de
conservation, risques. Justifiez la légalité du scraping réalisé. Documentez tout le processus
de collecte (schéma des flux : source → collecte → base).

### Phase 5 — Restitution (J10)

Présentez votre processus de collecte à un « comité data » : d'où viennent les données, comment
elles sont rassemblées, et sous quelles garanties de qualité et de conformité.

## Modalités d'évaluation

- **Revue technique (60 %)** : qualité du modèle relationnel, justesse des requêtes SQL, robustesse
  des scripts de collecte (API + scraping), reproductibilité.
- **Restitution orale (40 %)** : 12 min de présentation du processus + 8 min de questions,
  incluant la justification RGPD et légale.

**Validation partielle** : un binôme dont la collecte externe n'est pas totalement aboutie mais
dont le modèle SQL et les requêtes avancées sont justes et documentés valide les acquis SQL.

## Livrables attendus

- Un **dépôt GitHub public** contenant :
  - le **script SQL** de création et chargement de la base (`schema.sql`) + un **diagramme** du modèle ;
  - la **bibliothèque de requêtes** (`.sql`) commentées, dont au moins une vue ;
  - les **scripts Python** de collecte (API + scraping), exécutables et temporisés ;
  - les **données collectées** (CSV) ;
  - un **`README.md`** : description, technologies, lancement, auteurs.
- Un **registre des traitements RGPD** (Markdown) + une note de légalité du scraping.
- Un **schéma des flux de collecte**.

## Critères de performance

**Modéliser une base relationnelle**
- Le modèle (tables, clés, contraintes) répond au besoin métier et l'intégrité est garantie.
- Le DDL est correct et la granularité est justifiée.

**Requêter avec rigueur**
- Agrégations, jointures et sous-requêtes fonctionnent et répondent aux questions posées.
- Au moins une vue réutilisable est créée ; les requêtes sont optimisées et commentées.

**Automatiser la collecte**
- Les données sont récupérées automatiquement via une API REST (format d'échange documenté).
- Le web scraping fonctionne, est temporisé et identifié (`User-Agent`).

**Garantir la conformité**
- Le `robots.txt` / les CGU sont vérifiés et la légalité est argumentée.
- Chaque donnée personnelle est inscrite au registre (finalité, base légale, risques).

## Ressources

- Cours — [Web scraping](../../15-Business-Intelligence/14-Collecte-Donnees/02-web-scraping.md) · [Processus de collecte](../../15-Business-Intelligence/14-Collecte-Donnees/01-processus-collecte.md)
- Cours — [SQL](../../01-Fondamentaux/SQL/) · [API REST & Requests](../../01-Fondamentaux/Python/06-Data-Engineering/)
- Cours — [RGPD & gouvernance](../../01-Fondamentaux/RGPD-Gouvernance/)
- API météo libre (sans clé) : https://open-meteo.com/
- Données NordRetail : [`../Data-Analyst/data/`](../Data-Analyst/data/)
- Étape suivante du parcours : [Bloc 2 — Automatisation du traitement](BRIEF_BLOC_2_TRAITEMENT.md)
