# Mémo des commandes

Toutes les commandes se lancent depuis `06-Data-Engineering/Airflow/atelier/`.

## La stack

| Action | Commande |
|---|---|
| Construire l'image (après modification du `Dockerfile`) | `docker compose build` |
| Initialiser (une seule fois) | `docker compose up airflow-init` |
| Démarrer | `docker compose up -d` |
| État et santé des services | `docker compose ps` |
| Suivre les logs d'un service | `docker compose logs -f airflow-scheduler` |
| Recharger après modification de `.env` | `docker compose up -d` |
| Arrêter (garde les données) | `docker compose down` |
| **Tout effacer** (base de métadonnées comprise) | `docker compose down -v` |
| Ouvrir un terminal dans un conteneur | `docker compose exec airflow-scheduler bash` |

## Airflow en ligne de commande

Préfixe : `docker compose exec airflow-scheduler`

| Action | Commande |
|---|---|
| Lister les DAG | `airflow dags list` |
| Voir les erreurs d'import | `airflow dags list-import-errors` |
| Activer / mettre en pause | `airflow dags unpause <dag_id>` · `airflow dags pause <dag_id>` |
| Déclencher | `airflow dags trigger <dag_id>` |
| Déclencher avec paramètres | `airflow dags trigger taxi_jaune_ingestion -c '{"mois": "2025-01"}'` |
| Exécuter un DAG entier dans le terminal | `airflow dags test <dag_id>` (ajouter `-c '{...}'` pour des paramètres) |
| Exécuter une seule tâche | `airflow tasks test <dag_id> <task_id> <date>` |
| Lister les exécutions | `airflow dags list-runs <dag_id>` |
| États des tâches d'une exécution | `airflow tasks states-for-dag-run <dag_id> <run_id>` |
| Rattraper un historique | `airflow backfill create --dag-id <dag_id> --from-date 2025-01-01 --to-date 2025-03-01` |
| … sans rien lancer | ajouter `--dry-run` |
| Créer un pool | `airflow pools set snowflake 2 "Chargements Snowflake"` |
| Lire une connexion | `airflow connections get snowflake_default` |
| Créer / lire une variable | `airflow variables set CLE valeur` · `airflow variables get CLE` |
| Lancer les tests | `pytest /opt/airflow/tests -q` |

## Appeler une fonction de `plugins/` à la main

```bash
docker compose exec -e PYTHONPATH=/opt/airflow/plugins airflow-scheduler python -c "
from tlc.chargement import telecharger_mois; print(telecharger_mois('2025-01'))"
```

(Airflow ajoute `plugins/` au chemin d'import de ses propres processus, pas d'un `python` lancé à
la main : d'où le `PYTHONPATH`.)

## Snowflake

| Action | Où / commande |
|---|---|
| Tester la connexion depuis Airflow | `python -c "from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook; print(SnowflakeHook().get_first('SELECT CURRENT_USER(), CURRENT_ROLE()'))"` |
| Lignes par mois chargé | `SELECT SOURCE_FILE, COUNT(*) FROM NYC_TAXI.RAW.YELLOW_TRIPS GROUP BY 1 ORDER BY 1;` |
| Colonnes de la table | `SELECT COLUMN_NAME, DATA_TYPE FROM NYC_TAXI.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'YELLOW_TRIPS';` |
| Fichiers dans le stage | `LIST @NYC_TAXI.RAW.TLC_STAGE;` |
| Historique des chargements | `SELECT * FROM NYC_TAXI.RAW.LOAD_LOG ORDER BY MOIS;` |
| L'entrepôt est-il suspendu ? | `SHOW WAREHOUSES;` (colonne `state`) |
| Crédits consommés | Snowsight › *Admin › Cost Management* |
| Tout supprimer | `snowflake/99_destruction.sql` |

## Gabarits Jinja utiles

| Gabarit | Valeur pour l'exécution qui traite janvier 2025 |
|---|---|
| `{{ data_interval_start }}` | `2025-01-01T00:00:00+00:00` |
| `{{ data_interval_end }}` | `2025-02-01T00:00:00+00:00` |
| `{{ ds }}` | `2025-01-01` |
| `{{ data_interval_start.strftime('%Y-%m') }}` | `2025-01` |
| `{{ params.mois }}` | la valeur passée au déclenchement |
| `{{ var.value.CLE }}` | la variable Airflow `CLE` |
