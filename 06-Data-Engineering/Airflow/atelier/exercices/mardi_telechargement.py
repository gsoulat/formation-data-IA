"""
### Mardi — point de départ : télécharger le bon mois, et seulement lui

Copiez ce fichier dans dags/, puis complétez les TODO.
Cours : 02-mardi-planification-ingestion.md
"""

from datetime import timedelta

import pendulum
from airflow.sdk import dag, task

from tlc.chargement import telecharger_mois  # TODO mardi : écrire cette fonction dans plugins/tlc/chargement.py


@dag(
    dag_id="taxi_jaune_telechargement",
    # TODO : un planning MENSUEL AVEC intervalle de données (attention au piège d'Airflow 3).
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=2,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)},
    tags=["cours", "mardi", "nyc-taxi"],
)
def taxi_jaune_telechargement():
    @task
    def telecharger(data_interval_start=None) -> dict:
        # TODO : déduire le mois (AAAA-MM) de data_interval_start, puis appeler telecharger_mois.
        raise NotImplementedError

    @task
    def controler(fichier: dict, data_interval_start=None, data_interval_end=None) -> dict:
        # TODO : compter les courses dont tpep_pickup_datetime sort de l'intervalle
        # (pyarrow.parquet.read_table(..., columns=[...]) et pyarrow.compute),
        # l'afficher, et échouer au-delà de 1 %.
        raise NotImplementedError

    controler(telecharger())


taxi_jaune_telechargement()
