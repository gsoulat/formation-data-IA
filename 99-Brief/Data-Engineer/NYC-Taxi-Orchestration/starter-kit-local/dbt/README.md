# Votre projet dbt

Ce dossier est monté dans le conteneur sous `/opt/airflow/dbt`, et les variables
`DBT_PROFILES_DIR` et `DBT_PROJECT_DIR` y pointent déjà.

**Rien n'est fourni ici** : l'initialisation du projet, le profil DuckDB, les modèles, les tests
et la documentation sont votre travail.

Pour démarrer :

```bash
docker exec -it nyctaxi_airflow bash
cd /opt/airflow/dbt
dbt init            # ou créez dbt_project.yml et profiles.yml à la main
dbt debug
```

Le profil doit pointer vers la base DuckDB partagée, dont le chemin est disponible dans la
variable d'environnement `DUCKDB_PATH` (`/opt/airflow/data/nyc_taxi.duckdb`).

> **Attention à la concurrence.** DuckDB n'accepte qu'un seul processus en écriture à la fois.
> Si `dbt run` s'exécute pendant qu'une tâche d'ingestion écrit dans la même base, vous
> obtiendrez une erreur de verrou. C'est un vrai sujet de conception de votre DAG, pas un bug :
> comment garantissez-vous qu'une seule tâche écrit à la fois ?

- Adaptateur dbt-duckdb : https://github.com/duckdb/dbt-duckdb
- Documentation dbt : https://docs.getdbt.com
