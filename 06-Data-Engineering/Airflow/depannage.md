# Dépannage

Chaque cas ci-dessous a été rencontré en préparant ce cours. Commencez toujours par
`docker compose ps` : un service qui n'est pas `healthy` explique la moitié des pannes.

## La stack ne démarre pas

| Symptôme | Cause probable | Solution |
|---|---|---|
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | une autre application utilise le port 8080 | `AIRFLOW_PORT=8088` dans `.env`, puis `docker compose up -d` et http://localhost:8088 |
| les conteneurs redémarrent en boucle | pas assez de mémoire pour Docker | Docker Desktop › Settings › Resources : 4 Go minimum, 8 Go conseillés |
| `airflow-init` affiche `Exited (0)` | rien : il s'exécute une fois puis s'arrête | c'est normal |
| `airflow-init` échoue | base de métadonnées dans un état incohérent | `docker compose down -v` puis `docker compose up airflow-init` (**efface** l'historique Airflow, pas vos fichiers) |
| Linux : `Permission denied` sur `logs/` ou `dags/` | `AIRFLOW_UID` ne correspond pas à votre utilisateur | `AIRFLOW_UID=$(id -u)` dans `.env` |
| Windows : tout est très lent, DAG pas détectés | l'atelier est sous `/mnt/c/…` | déplacez-le dans le système de fichiers de WSL (`~/…`) |

## Mon DAG n'apparaît pas

```
Le fichier est-il dans atelier/dags/ ?  ── non ──▶ le déplacer
        │ oui
Bandeau rouge « DAG Import Errors » ?   ── oui ──▶ lire l'erreur (voir tableau ci-dessous)
        │ non
Moins de 30 s depuis la sauvegarde ?    ── oui ──▶ attendre (le dag-processor relit toutes les 30 s)
        │ non
airflow-dag-processor healthy ?         ── non ──▶ docker compose logs airflow-dag-processor
        │ oui
La dernière ligne appelle-t-elle la fonction du DAG ? (ex. bonjour_airflow())
```

| Erreur d'import | Cause |
|---|---|
| `ModuleNotFoundError: No module named 'tlc'` | le dossier `plugins/tlc/` manque, ou il n'a pas de `__init__.py` |
| `ModuleNotFoundError: No module named '<paquet>'` | le paquet n'est pas dans l'image : l'ajouter au `Dockerfile`, puis `docker compose build && docker compose up -d` |
| `AirflowDagDuplicatedIdException` | deux fichiers déclarent le même `dag_id` (souvent : l'ancien exercice est resté dans `dags/`) |
| `ValueError: URI format snowflake:// must contain database, schema, and table names` | un `Asset("snowflake://…")` incomplet : utilisez un nom simple, par exemple `Asset("nyc_taxi.raw.yellow_trips")` |
| `ImportError: cannot import name 'DagBag' from 'airflow.models'` (dans les tests) | Airflow 3 : `from airflow.dag_processing.dagbag import DagBag` |
| `ModuleNotFoundError: No module named 'airflow.decorators'` | tutoriel Airflow 2 : `from airflow.sdk import dag, task` |

## Mon DAG apparaît mais ne fait rien

| Symptôme | Cause probable | Solution |
|---|---|---|
| exécutions en `queued` indéfiniment | **le DAG est en pause** (c'est le cas de tout nouveau DAG) | l'activer : interrupteur dans l'interface, ou `airflow dags unpause <dag_id>` |
| exécutions en `queued`, DAG actif | le scheduler est arrêté | `docker compose ps`, puis `docker compose start airflow-scheduler` |
| tâche en `deferred` depuis longtemps | normal si la donnée n'est pas publiée. Anormal si le triggerer est arrêté | `docker compose ps` ; logs de la tâche (fichier `*.trigger.*.log`) |
| tâche en attente, jamais lancée, avec un pool | le pool n'existe pas, ou toutes ses places sont prises | `airflow pools list` ; `airflow pools set snowflake 2 "…"` |
| l'exécution du 1er du mois traite le **mois en cours** au lieu du mois écoulé | `schedule="@monthly"` n'a plus d'intervalle en Airflow 3 | `schedule=CronDataIntervalTimetable("@monthly", timezone="UTC")` |
| un déclenchement manuel ne traite pas le mois attendu | en Airflow 3, un déclenchement manuel n'a pas de date logique | passer le mois en paramètre, ou lancer un backfill |
| `airflow dags test` semble figé | une tâche attend sa reprise : `dags test` patiente pendant tout le `retry_delay` | lire les logs affichés au-dessus ; réduire `retry_delay` pendant la mise au point |

## Mes tâches échouent

| Message | Cause probable | Solution |
|---|---|---|
| `403 Client Error: Forbidden` sur une URL TLC | le mois n'est **pas encore publié** (le CDN répond 403, pas 404) | ce n'est pas une panne : attendre avec un capteur différé |
| `The conn_id snowflake_default isn't defined` | la connexion n'est pas déclarée, ou `.env` n'a pas été rechargé | vérifier `.env`, puis `docker compose up -d` |
| `The private_key_file path points to an empty or invalid file` | la clé n'est pas dans `atelier/secrets/`, ou le chemin est faux | `ls secrets/` ; le chemin dans la connexion est celui **du conteneur** : `/opt/airflow/secrets/rsa_key.p8` |
| `JWT token is invalid` (Snowflake) | la clé publique enregistrée dans Snowflake ne correspond pas à la clé privée | `DESC USER AIRFLOW_SVC;` puis `ALTER USER AIRFLOW_SVC SET RSA_PUBLIC_KEY='…';` |
| `Insufficient privileges` / `Object does not exist or not authorized` | le rôle d'Airflow n'a pas le droit, ou n'est pas le bon rôle | vérifier `role` dans la connexion ; relire le bloc 4 du script d'installation |
| `Warehouse 'WH_AIRFLOW' cannot be resumed because resource monitor … has exceeded its quota` | le plafond de crédits est atteint | normal : c'est le garde-fou. Voir avec le formateur avant de le relever |
| le nombre de lignes d'un mois **double** après une relance | le chargement n'est pas idempotent | `DELETE` et `COPY INTO` dans la même transaction (`autocommit=False`) |
| `No module named 'tlc'` dans un `python -c` lancé à la main | `plugins/` n'est sur le chemin que pour les processus Airflow | `docker compose exec -e PYTHONPATH=/opt/airflow/plugins …` |

## Tout remettre à zéro

```bash
docker compose down -v            # efface la base de métadonnées d'Airflow (DAG, exécutions, XCom)
rm -rf logs/* data/yellow         # efface les logs et les fichiers téléchargés
docker compose up airflow-init
docker compose up -d
```

Côté Snowflake : `snowflake/99_destruction.sql`, puis `snowflake/01_installation.sql`.
