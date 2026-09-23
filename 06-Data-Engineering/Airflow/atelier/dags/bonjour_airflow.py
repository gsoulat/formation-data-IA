"""
### Premier DAG — lundi

Trois tâches enchaînées, écrites avec l'API TaskFlow d'Airflow 3.
Déclenche-le à la main (bouton ▶), puis ouvre la vue Grid et les logs.
"""

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="bonjour_airflow",
    schedule=None,                                    # uniquement à la main
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["cours", "lundi"],
    doc_md=__doc__,
)
def bonjour_airflow():
    @task
    def extraire() -> list[int]:
        print("Extraction de quelques montants de courses")
        return [12, 7, 31, 18]

    @task
    def transformer(montants: list[int]) -> dict:
        return {"nb": len(montants), "total": sum(montants)}

    @task
    def charger(resume: dict) -> None:
        print(f"{resume['nb']} courses, {resume['total']} dollars au total")

    # Passer la sortie d'une tâche à la suivante crée la dépendance ET l'échange de données (XCom).
    charger(transformer(extraire()))


bonjour_airflow()
