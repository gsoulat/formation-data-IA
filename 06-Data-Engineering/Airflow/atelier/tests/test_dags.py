"""Tests des DAG : à lancer avant chaque commit.

    docker compose exec airflow-scheduler pytest /opt/airflow/tests -q

Vous compléterez ce fichier vendredi (voir exercices/vendredi_fiabilite.py).
"""

import pytest
from airflow.dag_processing.dagbag import DagBag


@pytest.fixture(scope="session")
def dagbag():
    return DagBag(dag_folder="/opt/airflow/dags")


def test_aucune_erreur_import(dagbag):
    assert dagbag.import_errors == {}, dagbag.import_errors


def test_chaque_dag_a_des_tags(dagbag):
    for dag_id, dag in dagbag.dags.items():
        assert dag.tags, f"{dag_id} n\'a pas de tag"
