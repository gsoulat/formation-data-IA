"""Télécharger un mois de courses et le charger dans Snowflake, de façon idempotente.

À COMPLÉTER : mardi (telecharger_mois), mercredi (charger_mois), jeudi (journaliser,
etag_deja_charge). Les signatures sont imposées : les DAG et les tests s'appuient dessus.
"""

from __future__ import annotations

import os
from pathlib import Path

from tlc import nom_fichier, url_fichier  # noqa: F401  (vous en aurez besoin)

DOSSIER = Path(os.environ.get("TAXI_DATA_DIR", "/opt/airflow/data")) / "yellow"
STAGE = "RAW.TLC_STAGE"
TABLE = "RAW.YELLOW_TRIPS"


def telecharger_mois(mois: str) -> dict:
    """Mardi. Télécharge le fichier du mois dans DOSSIER, sans jamais laisser de fichier tronqué.

    Renvoie {"mois": "2025-01", "chemin": "/opt/airflow/data/yellow/...", "nb_lignes": 3475226}.
    Pistes : requests.get(..., stream=True), un fichier .part renommé à la fin,
    pyarrow.parquet.ParquetFile(chemin).metadata.num_rows.
    """
    raise NotImplementedError("TODO mardi")


def charger_mois(hook, fichier: dict) -> dict:
    """Mercredi. PUT dans le stage, puis DELETE + COPY INTO dans une seule transaction,
    puis contrôle du nombre de lignes. `hook` est un SnowflakeHook (ou un faux, dans les tests).

    Renvoie {"mois": ..., "source": "2025-01/yellow_tripdata_2025-01.parquet", "nb_lignes": ...}.
    """
    raise NotImplementedError("TODO mercredi")


def journaliser(hook, chargement: dict, publication: dict) -> None:
    """Jeudi. Enregistre (MERGE) le mois, l'ETag, la taille et le nombre de lignes dans RAW.LOAD_LOG."""
    raise NotImplementedError("TODO jeudi")


def etag_deja_charge(hook, mois: str) -> str | None:
    """Jeudi. Renvoie l'ETag du dernier chargement de ce mois, ou None."""
    raise NotImplementedError("TODO jeudi")
