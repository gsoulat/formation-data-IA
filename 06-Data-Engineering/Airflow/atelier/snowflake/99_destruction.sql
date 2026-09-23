-- ===========================================================================
-- Tout supprimer à la fin de la formation (ou pour repartir de zéro).
-- Rien de ce qui suit n'est récupérable après la période de Time Travel.
-- ===========================================================================

USE ROLE ACCOUNTADMIN;

DROP DATABASE IF EXISTS NYC_TAXI;
DROP WAREHOUSE IF EXISTS WH_AIRFLOW;
DROP USER IF EXISTS AIRFLOW_SVC;
DROP ROLE IF EXISTS ROLE_AIRFLOW;
DROP RESOURCE MONITOR IF EXISTS RM_FORMATION;

-- Vérifier qu'aucun entrepôt ne tourne encore :
SHOW WAREHOUSES;
