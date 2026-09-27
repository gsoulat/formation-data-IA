# NYC Taxi — trois variantes d'un même brief

Trois déclinaisons du **même projet**, avec le même jeu de données réel, la même question
centrale, les mêmes phases et les mêmes critères d'évaluation. **Seule la stack change.**

Choisissez-en **une** selon l'infrastructure dont vous disposez et ce que vous voulez faire
travailler. Les trois valident les mêmes compétences.

| | [Variante A](VARIANTE_A_SNOWFLAKE_DBT_AIRFLOW.md) | [Variante B](VARIANTE_B_BIGQUERY_DBT_COMPOSER.md) | [Variante C](VARIANTE_C_DUCKDB_DBT_AIRFLOW.md) |
|---|---|---|---|
| **Entrepôt** | Snowflake | BigQuery | DuckDB (local) |
| **Transformation** | dbt Core | dbt Core | dbt Core |
| **Orchestration** | Airflow auto-hébergé | Cloud Composer (Airflow managé) | Airflow auto-hébergé |
| **Compte requis** | essai Snowflake 30 j | compte GCP + carte bancaire | **aucun** |
| **Coût réel** | 0 € (crédits d'essai) | quelques dizaines d'€ de crédits sur 5 j — **à vérifier sur la [grille tarifaire](https://cloud.google.com/composer/pricing) avant de lancer** | **0 €** |
| **Risque principal** | expiration de l'essai | **facture Composer si non détruit** | volumétrie sur portable |
| **Ce que ça fait travailler en plus** | gestion des crédits, warehouses | IaC, IAM, coûts cloud réels | performance locale, formats colonne |
| **Durée** | 5 jours | 5 jours | 5 jours |

## Laquelle choisir ?

- **Variante C (DuckDB)** — le défaut recommandé. Aucun compte, aucune carte bancaire, aucun
  risque de facture, et l'apprenant garde un projet qui tourne sur son portable après la
  formation. C'est aussi la seule qui fonctionne si le wifi de la salle est capricieux.
- **Variante A (Snowflake)** — si vous voulez qu'ils touchent un vrai entrepôt cloud sans
  exposer de moyen de paiement. L'essai de 30 jours suffit largement.
- **Variante B (BigQuery + Composer)** — si le parcours vise explicitement le cloud managé et
  que vous acceptez d'encadrer la facturation. **Attention** : Cloud Composer n'a pas d'offre
  gratuite et un environnement oublié allumé continue de facturer, nuits et week-ends compris.
  La destruction de l'environnement est un livrable, pas une consigne. Vérifiez la grille
  tarifaire en vigueur avant de programmer ce brief.

## Rapport avec le brief existant

Le brief historique [`../Snowflake+Dbt/nyc_taxi_dbt_pipeline.md`](../Snowflake+Dbt/nyc_taxi_dbt_pipeline.md)
reste valable : il fait 3 jours et place dbt et l'orchestration en **options**. Ces trois
variantes font 5 jours et mettent **dbt et l'orchestration dans le socle** — c'est la
différence de fond, et la raison des deux jours supplémentaires.

## Airflow avancé

Les trois variantes partagent un **socle Airflow avancé** exigé (API TaskFlow, mapping dynamique,
capteur différé, déclenchement piloté par la donnée, branchement, reprises et pools, rappels de
défaillance, connexions et variables, tests de DAG). C'est la différence majeure avec le brief
historique, où l'orchestration était optionnelle.

## Kit de démarrage

[`starter-kit-local/`](starter-kit-local/) — Airflow 3.3 + DuckDB + dbt, testé, en une commande.
Sert la variante C, et sert à la variante B pour développer les DAG en local avant de les
déployer sur Composer.
