# Tests de vos DAG

Ce dossier est **vide volontairement** : écrire les tests fait partie du socle du brief.

Il est monté dans le conteneur sous `/opt/airflow/tests`, et `pytest` y est déjà disponible.

```bash
docker exec nyctaxi_airflow pytest /opt/airflow/tests -q
```

Au minimum, le socle attend deux choses :

1. **Aucun DAG n'a d'erreur d'import.** Un DAG qui ne s'importe pas n'apparaît pas dans
   l'interface, et vous ne le voyez que le lendemain. Un test doit le détecter en une seconde.
2. **La structure attendue est là** : les tâches que vous croyez avoir déclarées existent, et les
   dépendances entre elles sont celles que vous pensez.

Pistes de départ, à creuser dans la documentation officielle : `DagBag` pour charger les DAG et
inspecter `import_errors`, et `dag.test()` pour exécuter un DAG de bout en bout en local.

- Tester ses DAG : https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag
