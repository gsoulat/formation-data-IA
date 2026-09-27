# Image Airflow augmentee de DuckDB et dbt-duckdb.
#
# On passe par un Dockerfile plutot que par _PIP_ADDITIONAL_REQUIREMENTS : les
# dependances sont installees UNE FOIS a la construction, pas a chaque
# demarrage du conteneur. Vos redemarrages seront quasi instantanes.
#
# Seuls duckdb et dbt-duckdb sont epingles ; pip resout dbt-core lui-meme, ce
# qui evite les conflits de version entre l'adaptateur et le coeur de dbt.

FROM apache/airflow:3.3.0-python3.12

USER airflow

RUN pip install --no-cache-dir \
      "duckdb==1.5.5" \
      "dbt-duckdb==1.10.1" \
      "requests"
