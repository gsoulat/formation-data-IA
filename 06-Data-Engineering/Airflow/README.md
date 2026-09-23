# Apache Airflow 3 en local — orchestrer l'ingestion des taxis de New York dans Snowflake

> **Une semaine, un pipeline.** Chaque mois, la commission des taxis de New York (TLC) publie les
> courses du mois écoulé, avec un à trois mois de retard, à une date que personne ne connaît à
> l'avance. Vous allez construire le pipeline qui attend ce fichier, le charge dans Snowflake sans
> jamais créer de doublon, rattrape l'historique, calcule des indicateurs et vous prévient quand
> quelque chose casse.

| | |
|---|---|
| **Durée** | 5 jours · 35 h |
| **Version** | Apache Airflow **3.3** (image officielle `apache/airflow:3.3.2`) |
| **Entrepôt** | Snowflake, compte d'essai gratuit (30 jours) |
| **Données** | [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) — taxis jaunes, Parquet mensuel, ~3,5 millions de courses par mois |
| **Prérequis** | Python (fonctions, décorateurs), SQL, Docker et Docker Compose, ligne de commande |
| **Prépare** | le brief [NYC-Taxi-Orchestration — variante A (Snowflake + dbt + Airflow)](../../99-Brief/Data-Engineer/NYC-Taxi-Orchestration/VARIANTE_A_SNOWFLAKE_DBT_AIRFLOW.md) |

## Pourquoi un orchestrateur ?

Un script lancé par `cron` chaque nuit fonctionne… jusqu'au jour où il échoue. Ce jour-là :

- **personne ne le sait** : `cron` n'a pas d'interface, pas d'alerte, pas d'historique ;
- **on ne sait plus quoi relancer** : quels mois ont été chargés ? lesquels manquent ?
- **les étapes s'enchaînent quand même** : la transformation tourne sur des données incomplètes.

Airflow répond à ces trois problèmes : il **montre** chaque exécution, il **rejoue** précisément
ce qui manque, et il **enchaîne** les étapes selon leurs dépendances.

## La semaine

| Jour | Cours | Ce que vous construisez |
|---|---|---|
| **Lundi** | [01 — Architecture et premier DAG](01-lundi-architecture-premier-dag.md) | la stack Docker, ses cinq services, votre premier DAG |
| **Mardi** | [02 — Le temps : planification et ingestion](02-mardi-planification-ingestion.md) | un DAG mensuel qui télécharge le bon mois, rejouable, rattrapable |
| **Mercredi** | [03 — Snowflake : connexion, chargement, parallélisme](03-mercredi-snowflake-connexions-parallelisme.md) | le chargement idempotent dans Snowflake, le rattrapage en parallèle |
| **Jeudi** | [04 — Capteurs différés, assets et branchement](04-jeudi-capteurs-assets-branchement.md) | un pipeline qui attend la donnée au lieu de l'horloge |
| **Vendredi** | [05 — Fiabilité, tests et mini-brief](05-vendredi-fiabilite-tests.md) | rappels d'échec, tests automatisés, puis un mini-brief en autonomie |

À garder ouverts toute la semaine :

- [Mémo des commandes](memo-commandes.md)
- [Dépannage : « mon DAG n'apparaît pas », « ma tâche ne démarre pas »…](depannage.md)
- [Vidéos récentes sur Airflow 3 et Snowflake](videos.md)

## L'atelier

Tout le code de la semaine vit dans [`atelier/`](atelier/) :

```
atelier/
├── docker-compose.yaml     la stack (dérivée du fichier officiel, commentée service par service)
├── Dockerfile              l'image Airflow étendue
├── .env.example            à copier en .env
├── dags/                   vos DAG (un DAG d'exemple fourni : bonjour_airflow.py)
├── exercices/              le point de départ de chaque journée
├── plugins/tlc/            code partagé : capteur différé fourni, le reste à écrire
├── tests/                  vos tests de DAG
├── snowflake/              scripts d'installation et de destruction côté Snowflake
├── secrets/                votre clé privée Snowflake (jamais commitée)
└── data/                   fichiers téléchargés (jamais commités)
```

## Airflow 2 → Airflow 3 : ce qui a changé

Beaucoup de tutoriels en ligne enseignent encore Airflow 2. Voici ce qui vous piégera si vous les
suivez :

| Airflow 2 | Airflow 3 |
|---|---|
| `airflow webserver` | `airflow api-server` (l'interface et l'API REST v2) |
| le scheduler lit les fichiers de DAG | un service séparé, le **dag-processor**, les lit |
| `from airflow.decorators import dag, task` | `from airflow.sdk import dag, task` |
| `Dataset` | `Asset` |
| `schedule="@monthly"` crée un intervalle de données | `schedule="@monthly"` **ne crée plus d'intervalle** : utiliser `CronDataIntervalTimetable` si vous en avez besoin (mardi) |
| un déclenchement manuel a une date logique | un déclenchement manuel n'a **pas** de date logique |
| les tâches peuvent lire la base de métadonnées | interdit : elles passent par l'API d'exécution |
| `from airflow.models import DagBag` | `from airflow.dag_processing.dagbag import DagBag` |

## Compétences travaillées

| Compétence | Où |
|---|---|
| Automatiser l'extraction de données depuis une source externe | lundi, mardi |
| Intégrer des données dans un entrepôt de données (Snowflake) | mercredi |
| Orchestrer un pipeline : dépendances, planification, reprise | toute la semaine |
| Sécuriser les accès (secrets hors du code, moindre privilège) | mercredi |
| Surveiller et fiabiliser un pipeline (alertes, tests) | vendredi |

## Pour aller plus loin

- Documentation officielle Airflow 3 : https://airflow.apache.org/docs/apache-airflow/stable/
- Airflow 3 — notes de migration : https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html
- Provider Snowflake : https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/
- Snowflake — `COPY INTO` : https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
