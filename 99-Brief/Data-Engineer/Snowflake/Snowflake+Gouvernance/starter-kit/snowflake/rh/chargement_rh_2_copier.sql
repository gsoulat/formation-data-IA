-- =====================================================================
-- chargement_rh_2_copier.sql — FOURNI : charger les deux fichiers RH dans RAW, étape 2 sur 2 : copier.
-- Le chargement se fait en trois temps (guide, jour 1, étape 8) :
--   1. chargement_rh_1_preparer.sql : format de fichier, stage, tables ;
--   2. déposer les deux CSV sur le stage depuis Snowsight (pas de SQL, voir la fin du fichier 1) ;
--   3. chargement_rh_2_copier.sql : copie dans les tables, stage vidé, vérifications.
-- Exécuter chaque fichier en entier (Cmd+Maj+Entrée). Rejouable.
-- =====================================================================
USE SECONDARY ROLES NONE;
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Avant : les deux fichiers doivent être sur le stage (LIST @NYC_TAXI.RAW.RH_STAGE; → 2 lignes).
-- ===================================================================== C. Copier, puis vider le stage
-- $1, $2… : les colonnes du fichier, dans l'ordre. METADATA$… : le nom du fichier et l'heure du chargement.
-- PURGE = TRUE retire le fichier du stage une fois copié : c'est la règle R3 du contrat.
COPY INTO NYC_TAXI.RAW.DRIVERS
FROM (SELECT $1, $2, $3, $4, $5, $6::date, $7, $8, $9::date, $10::date,
             METADATA$FILENAME, METADATA$START_SCAN_TIME::timestamp_ntz
      FROM @NYC_TAXI.RAW.RH_STAGE)
FILES = ('drivers.csv')
FILE_FORMAT = (FORMAT_NAME = NYC_TAXI.RAW.CSV_RH)
ON_ERROR = ABORT_STATEMENT
PURGE = TRUE;

COPY INTO NYC_TAXI.RAW.DRIVER_SHIFTS
FROM (SELECT $1, $2, $3::date, $4, $5::integer, $6::float, $7::integer, $8::float,
             METADATA$FILENAME, METADATA$START_SCAN_TIME::timestamp_ntz
      FROM @NYC_TAXI.RAW.RH_STAGE)
FILES = ('driver_shifts.csv')
FILE_FORMAT = (FORMAT_NAME = NYC_TAXI.RAW.CSV_RH)
ON_ERROR = ABORT_STATEMENT
PURGE = TRUE;

-- Vérifier : 400 chauffeurs, 25 951 services, 0 fichier resté sur le stage
SELECT
    (SELECT COUNT(*) FROM NYC_TAXI.RAW.DRIVERS)       AS chauffeurs,
    (SELECT COUNT(*) FROM NYC_TAXI.RAW.DRIVER_SHIFTS) AS services;
LIST @NYC_TAXI.RAW.RH_STAGE;            -- aucun fichier
-- Relancé, ce fichier ne charge rien de plus : COPY INTO se souvient des fichiers déjà chargés.
