# Image Airflow officielle, étendue avec ce dont le cours a besoin.
#
# Pourquoi un Dockerfile plutôt que _PIP_ADDITIONAL_REQUIREMENTS ?
# _PIP_ADDITIONAL_REQUIREMENTS réinstalle les paquets à CHAQUE démarrage de
# CHAQUE conteneur : lent, fragile, et une version différente peut arriver du
# jour au lendemain. Ici, l'installation a lieu une fois, à la construction.
#
# Le provider Snowflake est déjà inclus dans l'image officielle : rien à ajouter.

FROM apache/airflow:3.3.2

USER airflow

RUN pip install --no-cache-dir "pytest==8.4.2"
