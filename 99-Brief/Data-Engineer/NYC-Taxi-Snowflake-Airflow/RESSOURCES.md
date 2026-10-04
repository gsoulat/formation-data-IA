# Ressources — parcours d'apprentissage par jour

À coller dans le champ « Ressources » de Simplonline. Liens de documentation vérifiés le 2 octobre 2026 sauf mention contraire ; existence des vidéos vérifiée le 4 octobre 2026.

Méthode : pour chaque jour, 1) suivre le guide pas à pas indiqué en premier (les guides Snowflake se reproduisent sur votre compte, le guide Airflow se lit : son exemple n'est pas exécutable tel quel), 2) transposer aux données NYC Taxi, 3) aller chercher le détail dans la documentation officielle, 4) regarder une vidéo si un geste reste flou. Les vidéos en anglais ont des sous-titres automatiques français sur YouTube (Paramètres → Sous-titres → Traduire automatiquement).

## Kit de démarrage

- Fichiers SQL fournis, contrat de la couche RAW, schéma du pipeline, détail des étapes, configuration Airflow : à parcourir https://github.com/gsoulat/formation-data-IA/tree/main/99-Brief/Data-Engineer/NYC-Taxi-Snowflake-Airflow/starter-kit ou à télécharger en une archive https://raw.githubusercontent.com/gsoulat/formation-data-IA/main/99-Brief/Data-Engineer/NYC-Taxi-Snowflake-Airflow/starter-kit.zip

## Avant le premier jour

Installer :
- Sous Windows uniquement, WSL avec Ubuntu (les commandes du brief sont celles d'un terminal Linux) : https://learn.microsoft.com/fr-fr/windows/wsl/install
- Python 3.12 et savoir créer un environnement virtuel : https://docs.python.org/fr/3/tutorial/venv.html
- Docker Desktop ou équivalent : https://www.docker.com/products/docker-desktop/
- Astro CLI : https://www.astronomer.io/docs/astro/cli/install-cli
- Compte d'essai Snowflake, édition Enterprise, région européenne : https://www.snowflake.com/en/snowflake-trial/
- Vidéo (EN, 5 min) — Snowflake Trial without a credit card, Pragmatic Works : https://www.youtube.com/watch?v=BraR6fToqiI

Regarder :
- Vidéo (EN, 2 min) — Medallion Architecture Explained in 2 minutes : https://www.youtube.com/watch?v=RjC8LnvZsIc
- Vidéo (EN) — Introduction to Snowflake, NIC IT Academy : https://www.youtube.com/watch?v=H40Y6nDoD8g
- Vidéo (FR) — Apache Airflow #1 Introduction, NetSecDev : https://www.youtube.com/watch?v=lZhnUkIjksY

## Jour 1 — Comprendre les données et créer l'entrepôt Snowflake

Guide à suivre en premier (FR) :
- Sécurité : rôles, droits et utilisateurs de service en SQL (modèle de droits, script d'infrastructure, paire de clés, identifiant de compte, test de connexion, diagnostic des erreurs, exercice) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md

Sources de données :
- Page officielle TLC Trip Record Data : https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Fichiers Parquet : https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet (puis 2025-02, 2025-03)
- Liste des zones : https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
- Dictionnaire de données yellow (PDF) : https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
- Lire un fichier Parquet avec DuckDB : https://duckdb.org/docs/stable/data/parquet/overview

Documentation officielle Snowflake :
- Vue d'ensemble du contrôle d'accès (rôles, privilèges, propriété des objets) : https://docs.snowflake.com/en/user-guide/security-access-control-overview
- Identifiant de compte (format organisation-compte) : https://docs.snowflake.com/en/user-guide/admin-account-identifier
- CREATE WAREHOUSE (suspension automatique) : https://docs.snowflake.com/en/sql-reference/sql/create-warehouse
- Authentification par paire de clés : https://docs.snowflake.com/en/user-guide/key-pair-auth
- CREATE USER avec TYPE = SERVICE : https://docs.snowflake.com/en/sql-reference/sql/create-user

Vidéos Snowflake :
- Vidéo (EN, cours complet à parcourir par chapitre) — Snowflake Full course, NIC IT Academy : https://www.youtube.com/watch?v=SU9YM8Fm4Cg
- Vidéo (EN) — Roles in Snowflake : https://www.youtube.com/watch?v=-1aHd1WYus4
- Vidéo (FR) — Stocker et visualiser des données dans Snowflake, Mind7 Consulting : https://www.youtube.com/watch?v=9vZr6NcSVls

## Jour 2 — Charger les fichiers dans la couche RAW

Guide à suivre en premier (FR) :
- Charger des fichiers en SQL : format de fichier, stage, PUT et COPY INTO (options expliquées une par une, choix des types, script Python rejouable, diagnostic des erreurs, exercice) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md

Documentation officielle :
- PUT (ne fonctionne pas dans Snowsight) : https://docs.snowflake.com/en/sql-reference/sql/put
- COPY INTO table : https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
- Historique de chargement COPY_HISTORY : https://docs.snowflake.com/en/sql-reference/functions/copy_history
- Connecteur Python Snowflake : https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-example
- Bibliothèque requests, téléchargement en flux : https://requests.readthedocs.io/en/latest/user/quickstart/#raw-response-content

Vidéos Snowflake :
- Vidéo (EN) — Snowflake Data Loading: Using COPY Command & Stages, KnowHow Academy : https://www.youtube.com/watch?v=ZKiA6P_jU8k
- Vidéo (EN) — How to Load CSV File into Snowflake Table from Internal Named Stage, VCKLY Tech : https://www.youtube.com/watch?v=--wXAEV2MBo
- Vidéo (EN) — Snowflake Stages, Data Loading and Unloading, SleekData : https://www.youtube.com/watch?v=reWO0qqnpN0
- Vidéo (EN) — Snowflake : Copy Into et Snowpipe, Daniel Wilczak : https://www.youtube.com/watch?v=K9i_PWE_HHw

## Jour 3 — Premier pipeline Airflow : automatiser le chargement

Guide à suivre en premier (FR) :
- Airflow 3 avec Astro CLI, sections 1 à 5 (différences Airflow 2 / 3, projet Astro, connexion Snowflake par clé, date logique et reprise d'historique, DAG de chargement complet) : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md

Cours Airflow (FR, Airflow 3) :
- Introduction, architecture et vocabulaire : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/01-Fondamentaux/01-introduction.md
- Écrire un premier DAG : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/01-Fondamentaux/03-premier-dag.md
- Tâches Python (`@task`) : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/02-Operateurs/01-operateurs-python.md
- Passer une valeur d'une tâche à l'autre (XCom) : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/03-Concepts-Avances/01-xcom.md
- Variables et connexions : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/03-Concepts-Avances/02-variables-connections.md
- Rejouer sans doublon, catchup, backfill : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/04-Bonnes-Pratiques/01-idempotence.md

Documentation officielle :
- Astro CLI : https://www.astronomer.io/docs/astro/cli/install-cli
- Écrire un DAG avec TaskFlow (Airflow 3) : https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html
- Planification et catchup : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/cron.html
- Connexion Snowflake du provider : https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html
- Cours gratuit Airflow 101 (Airflow 3), Astronomer Academy : https://academy.astronomer.io/path/airflow-101

Vidéos Airflow :
- Vidéo (EN, cours complet à parcourir par chapitre) — Airflow 3.0 Masterclass, Data-2-Dollars : https://www.youtube.com/watch?v=RFVqzMyOicc
- Vidéo (EN, cours complet) — Airflow Tutorial For Beginners (2026), Ansh Lamba : https://www.youtube.com/watch?v=IiczxlbQb8s
- Vidéo (EN) — Intro to Airflow for ETL With Snowflake, Astronomer : https://www.youtube.com/watch?v=3-XGY0bGJ6g
- Vidéo (FR) — Apache Airflow #07 comprendre et créer un DAG pas à pas, NetSecDev : https://www.youtube.com/watch?v=XywtT8eNOIY

Attention : les vidéos antérieures à 2025 utilisent Airflow 2 (`from airflow.decorators import dag, task`, `schedule_interval`). En Airflow 3, on écrit `from airflow.sdk import dag, task` et `schedule`. Le tableau de la section 1 du guide donne toutes les correspondances.

## Jour 4 — Transformer et contrôler les données avec Airflow

Guide à suivre en premier (FR) :
- Airflow 3 avec Astro CLI, section 6 (fichiers SQL, paramètres par mois, contrôles, groupes de tâches) et section 8 (lire l'interface, diagnostiquer) : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md

Cours Airflow (FR, Airflow 3) :
- Exécuter du SQL et contrôler les données : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/02-Operateurs/02-operateurs-sql.md

Documentation officielle :
- Opérateurs SQL communs (SQLExecuteQueryOperator, SQLCheckOperator), lien non vérifié : https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/operators.html
- Variables disponibles dans les modèles (`ds`, `logical_date`, `params`), lien non vérifié : https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
- QUALIFY (dédoublonnage dans les fichiers fournis) : https://docs.snowflake.com/en/sql-reference/constructs/qualify
- DATEDIFF : https://docs.snowflake.com/en/sql-reference/functions/datediff

Vidéos Airflow et Snowflake :
- Vidéo (EN) — End to End Parallel Data Quality Check Pipeline Project with Airflow and Snowflake, The Data and AI Guy : https://www.youtube.com/watch?v=6nVcqSCeNPY
- Vidéo (EN) — End-to-End Parallel ETL Pipeline with Airflow, Snowflake, and S3 Buckets, The Data and AI Guy : https://www.youtube.com/watch?v=Zn-EAUCwLys

## Jour 5 — Contrôler, documenter et présenter

- Mesurer les crédits consommés par jour (à lancer avec ACCOUNTADMIN ; les chiffres peuvent avoir jusqu'à 3 h de retard ; requête non testée sur le compte de validation) :
  ```sql
  USE ROLE ACCOUNTADMIN;
  SELECT warehouse_name, DATE(start_time) AS jour, ROUND(SUM(credits_used), 3) AS credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
  WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
  GROUP BY 1, 2 ORDER BY 2;
  ```
- Suivi des coûts dans l'interface et autres requêtes : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/09-monitoring.md
- Documentation WAREHOUSE_METERING_HISTORY : https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history
- Vérifier les droits d'un rôle : section 4 du guide Sécurité (jour 1).

## Bonus

- Bonus 1, notification Discord (liens non vérifiés) : créer un webhook https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks ; fonctions de rappel d'Airflow, section 9 du guide Airflow 3 et https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html
- Bonus 2, déployer sur Astro : essai gratuit https://www.astronomer.io/try-astro/ et documentation du déploiement (lien non vérifié) https://www.astronomer.io/docs/astro/deploy-code

## Pour aller plus loin
- Modélisation dimensionnelle, Kimball Group : https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
- Dynamic Data Masking Snowflake : https://docs.snowflake.com/en/user-guide/security-column-ddm-intro
- Snowflake Hands-On Essentials (badges gratuits) : https://learn.snowflake.com/
