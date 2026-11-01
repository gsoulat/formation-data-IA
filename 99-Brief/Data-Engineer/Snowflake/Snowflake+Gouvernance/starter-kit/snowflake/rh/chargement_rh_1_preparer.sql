-- =====================================================================
-- chargement_rh_1_preparer.sql — FOURNI : charger les deux fichiers RH dans RAW, étape 1 sur 2 : préparer.
-- Le chargement se fait en trois temps (guide, jour 1, étape 8) :
--   1. chargement_rh_1_preparer.sql : format de fichier, stage, tables ;
--   2. déposer les deux CSV sur le stage depuis Snowsight (pas de SQL, voir la fin du fichier 1) ;
--   3. chargement_rh_2_copier.sql : copie dans les tables, stage vidé, vérifications.
-- Exécuter chaque fichier en entier (Cmd+Maj+Entrée). Rejouable.
-- =====================================================================
USE SECONDARY ROLES NONE;
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- ===================================================================== A. Préparer
-- Le format de fichier : comment lire un CSV (séparateur, ligne d'en-tête, guillemets)
CREATE FILE FORMAT IF NOT EXISTS NYC_TAXI.RAW.CSV_RH
  TYPE = CSV
  SKIP_HEADER = 1                       -- la première ligne contient les noms de colonnes
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  TRIM_SPACE = FALSE;                   -- RAW est une copie fidèle, espaces compris

-- Le stage : un espace de dépôt dans Snowflake, où l'on pose les fichiers avant de les copier.
-- Chiffrement côté serveur et table de répertoire : nécessaires pour déposer et voir les fichiers dans Snowsight.
CREATE STAGE IF NOT EXISTS NYC_TAXI.RAW.RH_STAGE
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  DIRECTORY = (ENABLE = TRUE)
  COMMENT = 'Dépôt temporaire du fichier RH, vidé après chaque chargement (règle R3)';

-- Les deux tables RAW : les colonnes du contrat (section 2), plus deux colonnes techniques
CREATE TABLE IF NOT EXISTS NYC_TAXI.RAW.DRIVERS (
    driver_id VARCHAR, first_name VARCHAR, last_name VARCHAR, email VARCHAR, phone VARCHAR,
    birth_date DATE, tlc_license_number VARCHAR, depot VARCHAR, hire_date DATE, end_date DATE,
    _source_file VARCHAR, _loaded_at TIMESTAMP_NTZ);
CREATE TABLE IF NOT EXISTS NYC_TAXI.RAW.DRIVER_SHIFTS (
    shift_id VARCHAR, driver_id VARCHAR, shift_date DATE, depot VARCHAR, start_hour INTEGER,
    hours_worked FLOAT, trips_count INTEGER, revenue_usd FLOAT,
    _source_file VARCHAR, _loaded_at TIMESTAMP_NTZ);

-- ===================================================================== Ensuite : déposer les fichiers (Snowsight)
-- Onglet Databases (à côté de Workspaces) ou menu Catalog → Database Explorer → NYC_TAXI → RAW → Stages → RH_STAGE,
-- bouton « + Files », puis choisir data/drivers.csv et data/driver_shifts.csv.
-- Puis vérifiez qu'ils sont bien là, avant de lancer chargement_rh_2_copier.sql :
--   LIST @NYC_TAXI.RAW.RH_STAGE;     -- 2 fichiers : rh_stage/drivers.csv et rh_stage/driver_shifts.csv


-- Vérifier : le stage RH_STAGE existe
SHOW STAGES IN SCHEMA NYC_TAXI.RAW;
