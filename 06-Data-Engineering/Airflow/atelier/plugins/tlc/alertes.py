"""Rappel d'échec — À COMPLÉTER vendredi.

Une alerte exploitable à 3 h du matin contient : le DAG, la tâche, la période de
données, le numéro de tentative, l'erreur, et le lien direct vers les logs.
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def construire_message(context) -> dict:
    """Renvoie {"dag", "tache", "periode", "tentative", "erreur", "logs"} à partir du contexte.

    Pistes : context["ti"] (dag_id, task_id, try_number, log_url),
    context.get("data_interval_start") (absent pour un déclenchement manuel),
    context.get("exception").
    """
    raise NotImplementedError("TODO vendredi")


def signaler_echec(context) -> None:
    """À brancher dans default_args={"on_failure_callback": signaler_echec}.

    Écrit le message dans les logs ; si la variable Airflow ALERTE_WEBHOOK existe,
    l'envoie aussi en POST. Un webhook injoignable ne doit jamais masquer l'erreur d'origine.
    """
    raise NotImplementedError("TODO vendredi")
