"""
### Vendredi — point de départ : les tests

1. Complétez plugins/tlc/alertes.py, puis branchez
   default_args={"on_failure_callback": signaler_echec} sur vos DAG taxi_*.
2. Copiez les tests ci-dessous À LA SUITE de tests/test_dags.py et complétez les TODO.
3. Lancez :  docker compose exec airflow-scheduler pytest /opt/airflow/tests -q

Cours : 05-vendredi-fiabilite-tests.md
"""

import pytest


def test_structure_ingestion(dagbag):
    dag = dagbag.get_dag("taxi_jaune_ingestion")
    # TODO : l'ensemble exact des task_id attendus
    # TODO : les tâches qui suivent verifier_nouveaute sont telecharger et deja_a_jour
    # TODO : charger est dans le pool "snowflake" ; attendre_publication n'a aucune reprise
    raise NotImplementedError


def test_indicateurs_declenche_par_la_donnee(dagbag):
    # TODO : taxi_jaune_indicateurs a un planning qui dépend de l'asset nyc_taxi.raw.yellow_trips
    raise NotImplementedError


class FauxHook:
    """Remplace SnowflakeHook : enregistre les requêtes au lieu de les exécuter."""

    def __init__(self, lignes_en_base):
        self.requetes, self.lignes_en_base = [], lignes_en_base

    def run(self, sql, autocommit=True, parameters=None):
        self.requetes.append((sql, autocommit))

    def get_first(self, sql, parameters=None):
        return (self.lignes_en_base,)


def test_chargement_idempotent_dans_une_transaction():
    from tlc.chargement import charger_mois

    hook = FauxHook(lignes_en_base=100)
    charger_mois(hook, {"mois": "2025-01", "chemin": "/tmp/f.parquet", "nb_lignes": 100})
    # TODO : un PUT, puis DELETE + COPY INTO envoyés ENSEMBLE avec autocommit=False
    raise NotImplementedError


def test_chargement_echoue_si_le_compte_ne_tombe_pas_juste():
    # TODO : avec un FauxHook qui annonce 99 lignes pour un fichier de 100, charger_mois lève une erreur
    raise NotImplementedError


def test_message_alerte_exploitable():
    # TODO : construire_message() sur un faux contexte contient la période, l'erreur et le lien des logs
    raise NotImplementedError
