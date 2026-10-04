# 01 — Introduction à Apache Airflow

## Qu'est-ce qu'Apache Airflow ?

Apache Airflow est une plateforme open-source d'**orchestration de workflows**. Créé par Airbnb en 2014 et donné à la fondation Apache en 2016, il est aujourd'hui l'un des outils les plus utilisés dans l'écosystème Data Engineering.

Airflow permet de :
- **Définir** des pipelines de données sous forme de code Python
- **Planifier** leur exécution (cron, intervalles, déclenchement manuel ou par événement)
- **Surveiller** l'état de chaque tâche via une interface web
- **Rejouer** des exécutions passées en cas d'échec
- **Visualiser** les dépendances entre tâches

> Airflow n'est **pas** un outil de traitement de données. Il ne déplace pas, ne transforme pas les données lui-même. Il **orchestre** des outils qui le font (Spark, dbt, pandas, SQL...).

---

## Le concept fondamental : le DAG

Un **DAG** (Directed Acyclic Graph — Graphe Orienté Acyclique) est la brique de base d'Airflow.

### Définition formelle

Un DAG est un graphe dans lequel :
- Les **nœuds** représentent des **tâches** (tasks)
- Les **arêtes** représentent des **dépendances** entre tâches
- Le graphe est **orienté** (les tâches s'exécutent dans un sens)
- Le graphe est **acyclique** (pas de boucle infinie)

### Représentation visuelle

```
extract_data  ──►  transform_data  ──►  load_to_db
                         │
                         ▼
                   send_notification
```

Dans cet exemple :
- `extract_data` doit terminer avant `transform_data`
- `transform_data` déclenche ensuite `load_to_db` ET `send_notification` en parallèle
- Pas de cycle : aucune tâche ne dépend d'elle-même

### Règle fondamentale des DAGs

```
Un DAG = un pipeline logique
Une Task = une unité de travail atomique
```

---

## Cas d'usage typiques

### 1. Pipeline ETL quotidien

```
Extraction API  →  Nettoyage  →  Chargement Data Warehouse  →  Notification Slack
```

### 2. Pipeline de Machine Learning

```
Extraction données  →  Préparation features  →  Entraînement modèle
                                                        │
                              Évaluation métriques  ←──┘
                                        │
                           Enregistrement MLflow
```

### 3. Pipeline de reporting

```
Agrégation SQL  →  Export CSV  →  Upload S3  →  Email rapport
```

### 4. Orchestration dbt

```
dbt seed  →  dbt run  →  dbt test  →  dbt docs generate
```

---

## Architecture d'Airflow

Airflow est composé de plusieurs composants qui interagissent ensemble.

### Vue d'ensemble

```
┌──────────────────────────────────────────────────────────────┐
│                       APACHE AIRFLOW 3                        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐       │
│  │  API Server  │  │  Scheduler   │  │ DAG Processor │       │
│  │ (UI + API    │  │              │  │ (analyse les  │       │
│  │  REST)       │  │              │  │  fichiers DAG)│       │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘       │
│         │                 │                  │                │
│         └─────────────────┼──────────────────┘                │
│                           │                                   │
│                  ┌────────▼────────┐                          │
│                  │   Metadata DB   │ (PostgreSQL / MySQL)     │
│                  └─────────────────┘                          │
│                                                               │
│  ┌──────────────────────────────────────────┐                │
│  │              Executor                     │  API           │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  d'exécution   │
│  │  │ Worker 1│  │ Worker 2│  │ Worker 3│  │ ─────────────► │
│  │  └─────────┘  └─────────┘  └─────────┘  │  (API Server)  │
│  └──────────────────────────────────────────┘                │
│                                                               │
│  ┌──────────────┐                                             │
│  │  DAGs Folder │ (répertoire Python partagé)                 │
│  └──────────────┘                                             │
└──────────────────────────────────────────────────────────────┘
```

> **Si vous venez d'Airflow 2 :** le *Web Server* (Flask + Gunicorn) a été remplacé par l'**API Server**, l'analyse des fichiers DAG est sortie du Scheduler pour devenir un composant à part (le **DAG Processor**), et les tâches n'accèdent plus directement à la Metadata DB : elles passent par l'**API d'exécution**.

### Le Scheduler

C'est le **cerveau** d'Airflow. Il :
- Lit les DAGs déjà analysés et leurs planifications dans la Metadata DB
- Crée des **DAG Runs** selon les schedules définis
- Soumet les tâches prêtes à l'**Executor**
- Gère les dépendances et les états des tâches

### Le DAG Processor

Composant séparé du Scheduler depuis Airflow 3 (commande `airflow dag-processor`). Il :
- Scanne le dossier `dags/` en permanence : les fichiers connus sont ré-analysés toutes les ~30 secondes, les nouveaux fichiers sont recherchés toutes les 5 minutes (valeurs par défaut)
- Exécute le code Python de chaque fichier pour en extraire les DAGs
- Enregistre le résultat (DAGs sérialisés, erreurs d'import) dans la Metadata DB

Le Scheduler et l'API Server ne lisent donc jamais vos fichiers `.py` directement.

### L'API Server

Il remplace le Web Server d'Airflow 2 (commande `airflow api-server`). Il sert à la fois :
- l'**interface web** (réécrite en React pour Airflow 3), qui permet de :
  - Visualiser tous les DAGs et leurs états
  - Déclencher manuellement des DAG Runs
  - Consulter les logs de chaque tâche
  - Gérer les Variables et Connexions
- l'**API REST** publique (`/api/v2`), pour piloter Airflow depuis un script ou un autre outil
- l'**API d'exécution**, utilisée par les workers pour lire et écrire l'état des tâches, les XComs, les Variables et les Connexions

Par défaut : `http://localhost:8080`

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** L'interface web Airflow 3 — page de la liste des DAGs avec plusieurs DAGs dans différents états (running, success, failed)
> **Expliquer :** Présenter les informations affichées pour chaque DAG : nom et tags, planification, prochain run, dernier run et son état. Montrer comment filtrer par tags et par état, et comment activer/mettre en pause un DAG.

---

### Le Worker

Un Worker est un processus qui **exécute** les tâches. Selon l'executor configuré :
- **LocalExecutor** : les tâches s'exécutent dans des sous-processus sur la machine du Scheduler (jusqu'à N en parallèle)
- **CeleryExecutor** : des workers Celery distincts récupèrent les tâches depuis une queue (Redis/RabbitMQ)
- **KubernetesExecutor** : chaque tâche est exécutée dans un Pod Kubernetes éphémère

En Airflow 3, le code d'une tâche ne se connecte plus à la Metadata DB : le worker dialogue avec l'**API d'exécution** de l'API Server. Conséquence pratique : on n'ouvre plus de session SQLAlchemy sur la base Airflow depuis une tâche, comme le montrent certains tutoriels Airflow 2.

### La Metadata Database

Base de données relationnelle (PostgreSQL recommandé en production) qui stocke :
- Les définitions de DAGs (métadonnées)
- L'historique des DAG Runs et Task Instances
- Les Variables et Connexions
- Les XComs (données échangées entre tâches)
- Les utilisateurs et leurs permissions (avec le gestionnaire d'authentification FAB)

> La metadata DB ne contient **pas** vos données métier — seulement les métadonnées Airflow.

### Le Triggerer

Composant optionnel pour les **Deferrable Operators**. Au lieu de bloquer un worker en attendant (ex: poll S3 toutes les 30s), le Triggerer gère les I/O asynchrones sans monopoliser un worker.

---

## Cycle de vie d'une tâche

```
                    ┌─────────┐
                    │   none   │  (task définie mais pas encore planifiée)
                    └────┬────┘
                         │ Scheduler crée le DAG Run
                    ┌────▼────┐
                    │scheduled│
                    └────┬────┘
                         │ Executor prend en charge
                    ┌────▼────┐
                    │ queued  │
                    └────┬────┘
                         │ Worker commence
                    ┌────▼────┐
                    │ running │
                    └────┬────┘
                    ┌────┴──────┐
                    │           │
               ┌────▼───┐  ┌───▼──────┐
               │success │  │  failed  │
               └────────┘  └───┬──────┘
                                │ (si retries configurés)
                           ┌───▼──────┐
                           │up_for_retry│
                           └───┬──────┘
                                │
                           (retente)
```

---

## DAG Run vs Task Instance

| Concept | Définition |
|---|---|
| **DAG** | La définition statique du pipeline (le code Python) |
| **DAG Run** | Une exécution concrète du DAG à une date donnée |
| **Task** | La définition statique d'une tâche dans un DAG |
| **Task Instance** | Une exécution concrète d'une Task dans un DAG Run donné |

Exemple :
- Vous avez un DAG `etl_quotidien` planifié à 06h00 chaque jour
- Chaque matin à 06h00, Airflow crée un **DAG Run** pour ce DAG
- Chaque tâche dans ce DAG Run est une **Task Instance**
- Vous pouvez avoir 365 DAG Runs d'un même DAG sur une année

---

## La notion de logical_date (ex-execution_date)

> C'est un concept **crucial** et souvent source de confusion.

Chaque DAG Run porte une **date logique** (`logical_date`) : la date *pour laquelle* le run est créé, qui ne dépend pas du moment où il tourne réellement (un run rejoué trois jours plus tard garde la même `logical_date`). Dans les tutoriels Airflow 2, elle s'appelle `execution_date` : ce nom a été supprimé en Airflow 3.

Un run porte aussi un **intervalle de données** (`data_interval_start`, `data_interval_end`) : la période qu'il est censé traiter. C'est ici qu'Airflow 3 change le comportement par défaut.

**Par défaut en Airflow 3** — un schedule cron ou un préréglage (`@daily`, `0 6 * * *`...) utilise `CronTriggerTimetable` : la date logique est **le moment du déclenchement**, et l'intervalle de données est vide.

```
DAG planifié avec schedule="@daily"
Run déclenché le 16 janvier à 00:00:00
→ logical_date = data_interval_start = data_interval_end = 2024-01-16 00:00:00
→ {{ ds }} vaut "2024-01-16"
→ Pour traiter les données du 15 janvier, la tâche calcule
  elle-même la période : logical_date - 1 jour
```

**Comportement historique d'Airflow 2** — la date logique est le **début de la période traitée**, et le run ne démarre qu'une fois la période terminée (comportement dit **"end of interval"**). On le retrouve en Airflow 3 en choisissant explicitement `CronDataIntervalTimetable` :

```python
from airflow.timetables.interval import CronDataIntervalTimetable

schedule = CronDataIntervalTimetable("0 0 * * *", timezone="UTC")
```

```
Run déclenché le 16 janvier à 00:00:00
→ logical_date = data_interval_start = 2024-01-15 00:00:00
→ data_interval_end = 2024-01-16 00:00:00
→ Ce run traite les données du 15 janvier
```

À retenir : avant d'écrire « je traite la période [`data_interval_start`, `data_interval_end`) », vérifiez quelle timetable votre DAG utilise. Avec le défaut d'Airflow 3, ces deux bornes sont identiques.

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** La vue "Graph" d'un DAG dans l'interface web (bascule Grid / Graph en haut de la page du DAG), montrant les nœuds (tâches) et les arêtes (dépendances) avec des couleurs par état
> **Expliquer :** Pointer chaque nœud en expliquant que chaque couleur correspond à un état (succès, échec, en cours, ignoré... : s'appuyer sur la légende de l'interface). Montrer comment cliquer sur un nœud pour voir les détails de la Task Instance.

---

## Comparaison avec d'autres outils

| Outil | Type | Points forts | Limites |
|---|---|---|---|
| **Airflow** | Orchestrateur de workflows | Flexibilité totale Python, UI riche, vaste écosystème | Complexité, courbe d'apprentissage |
| **Prefect** | Orchestrateur moderne | Plus simple, Cloud natif, meilleure UX | Moins mature, moins de providers |
| **Dagster** | Orchestrateur data-centric | Typage des assets, observabilité | Paradigme différent, plus récent |
| **dbt** | Transformation SQL | Excellent pour les transformations SQL | Uniquement SQL, pas d'orchestration générale |
| **Luigi** | Orchestrateur (Spotify) | Simple, léger | UI limitée, moins populaire |
| **Cron** | Planificateur basique | Natif Linux, zéro config | Pas de dépendances, pas de retry, pas de UI |

---

## Points clés à retenir

1. **Airflow orchestre, il n'exécute pas** — c'est un chef d'orchestre, pas un musicien
2. **Tout est du code Python** — les DAGs sont des fichiers `.py`, versionnables avec Git
3. **Idempotence** — chaque tâche doit pouvoir être rejouée sans effet de bord
4. **La `logical_date`** (ex-`execution_date`) est la date logique du run, pas le moment où il tourne réellement ; par défaut en Airflow 3, c'est la date de déclenchement planifiée
5. **Le Scheduler** est le composant central — s'il tombe, rien ne s'exécute ; le **DAG Processor** analyse les fichiers, l'**API Server** sert l'interface et les API
6. **La Metadata DB** est critique — la perdre = perdre tout l'historique

---

## Pour aller plus loin

- [Architecture Airflow (officiel)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- [DAGs concepts (officiel)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Airflow dans le monde réel — Astronomer Blog](https://www.astronomer.io/blog/)
