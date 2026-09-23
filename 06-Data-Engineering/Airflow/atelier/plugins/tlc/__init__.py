"""Outils partagés par les DAG du fil rouge NYC Taxi (fichiers publiés par la TLC).

Le dossier plugins/ est ajouté au sys.path de tous les composants d'Airflow
(scheduler, dag-processor, triggerer) : `from tlc import ...` fonctionne partout.
"""

URL_BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def nom_fichier(mois: str) -> str:
    """Nom du fichier TLC d'un mois, par exemple yellow_tripdata_2025-01.parquet."""
    return f"yellow_tripdata_{mois}.parquet"


def url_fichier(mois: str) -> str:
    return f"{URL_BASE}/{nom_fichier(mois)}"
