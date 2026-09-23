"""
### Mercredi — point de départ : charger dans Snowflake, puis rattraper en parallèle

Deux DAG dans ce fichier. Copiez-le dans dags/ À LA PLACE de votre fichier du mardi
(même dag_id pour le premier), puis complétez les TODO.
Cours : 03-mercredi-snowflake-connexions-parallelisme.md

Avant : le pool doit exister ->  airflow pools set snowflake 2 "Chargements Snowflake"
"""

from datetime import timedelta
from pathlib import Path  # noqa: F401

import pendulum
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook  # noqa: F401
from airflow.sdk import CronDataIntervalTimetable, Param, dag, task  # noqa: F401

from tlc.chargement import charger_mois, telecharger_mois  # noqa: F401


@dag(
    dag_id="taxi_jaune_telechargement",
    schedule=CronDataIntervalTimetable("@monthly", timezone="UTC"),
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=2,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)},
    tags=["cours", "mercredi", "nyc-taxi"],
)
def taxi_jaune_telechargement():
    @task
    def telecharger(data_interval_start=None) -> dict:
        ...  # reprenez votre version du mardi

    # TODO : une tâche `charger` limitée par le pool "snowflake", qui appelle
    # charger_mois(SnowflakeHook(), fichier). Où placer le contrôle du mardi ?
    telecharger()


taxi_jaune_telechargement()


@dag(
    dag_id="taxi_jaune_rattrapage",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    params={
        # TODO : deux paramètres "debut" et "fin", format AAAA-MM, validés par un motif.
    },
    default_args={"retries": 2},
    tags=["cours", "mercredi", "nyc-taxi"],
)
def taxi_jaune_rattrapage():
    @task
    def lister_mois(params=None) -> list[str]:
        # TODO : la liste des mois entre params["debut"] et params["fin"], bornes incluses.
        raise NotImplementedError

    # TODO : une tâche `rattraper(mois)` (télécharger + charger + supprimer le fichier local),
    # dans le pool "snowflake", appliquée à chaque mois avec .expand().


taxi_jaune_rattrapage()
