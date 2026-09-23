"""
### Jeudi — point de départ : attendre la donnée, ne rien faire pour rien, enchaîner par la donnée

Copiez ce fichier dans dags/, puis complétez les TODO. Il remplace le DAG mensuel du mercredi
(supprimez taxi_jaune_telechargement de dags/ ; gardez taxi_jaune_rattrapage).
Cours : 04-jeudi-capteurs-assets-branchement.md
"""

from datetime import timedelta
from pathlib import Path  # noqa: F401

import pendulum
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator  # noqa: F401
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook  # noqa: F401
from airflow.providers.standard.operators.empty import EmptyOperator  # noqa: F401
from airflow.sdk import Asset, CronDataIntervalTimetable, Param, dag, get_current_context, task  # noqa: F401

from tlc import url_fichier  # noqa: F401
from tlc.capteurs import FichierPublieSensor  # noqa: F401  (fourni : lisez-le)
from tlc.chargement import charger_mois, etag_deja_charge, journaliser, telecharger_mois  # noqa: F401

TRAJETS_BRUTS = Asset("nyc_taxi.raw.yellow_trips")

# TODO : le gabarit Jinja du mois traité : le paramètre "mois" s'il est fourni,
# sinon le début de l'intervalle de données.
MOIS = "TODO"


def mois_courant() -> str:
    # TODO : même logique que MOIS, mais en Python, à partir de get_current_context().
    raise NotImplementedError


@dag(
    dag_id="taxi_jaune_ingestion",
    schedule=CronDataIntervalTimetable("@monthly", timezone="UTC"),
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=3,
    # TODO : un paramètre "mois" (vide par défaut, motif AAAA-MM).
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["cours", "jeudi", "nyc-taxi"],
)
def taxi_jaune_ingestion():
    # TODO 1 : le capteur différé "attendre_publication" (vérification toutes les 6 h,
    #          abandon après 90 jours, aucune reprise).
    # TODO 2 : @task.branch "verifier_nouveaute" -> "telecharger" ou "deja_a_jour".
    # TODO 3 : "telecharger", "charger" (pool + asset en sortie + journaliser l'ETag).
    # TODO 4 : "nettoyer" : supprime le fichier local même si le chargement a échoué.
    pass


taxi_jaune_ingestion()


@dag(
    dag_id="taxi_jaune_indicateurs",
    schedule=None,  # TODO : déclenché par l'asset TRAJETS_BRUTS
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    default_args={"retries": 1},
    tags=["cours", "jeudi", "nyc-taxi"],
)
def taxi_jaune_indicateurs():
    # TODO : deux SQLExecuteQueryOperator (conn_id="snowflake_default") :
    #   MARTS.QUALITE_MENSUELLE    : par mois du fichier source, lignes, lignes hors du mois,
    #                                montants <= 0, distances nulles
    #   MARTS.INDICATEURS_MENSUELS : par mois du fichier source, sur les lignes valides :
    #                                nb de courses, distance médiane, montant médian, taux de pourboire
    pass


taxi_jaune_indicateurs()
