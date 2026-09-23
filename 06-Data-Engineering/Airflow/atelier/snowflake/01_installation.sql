-- ===========================================================================
-- Installation Snowflake pour le cours Airflow — à exécuter UNE fois
-- dans une feuille de calcul Snowsight (Projects > Worksheets), en entier.
--
-- Avant de lancer : remplacer <CLE_PUBLIQUE> (fin de fichier, section 5) par le
-- contenu de secrets/rsa_key.pub SANS les lignes -----BEGIN/END----- ni retours
-- à la ligne. Voir le cours du mercredi pour générer la paire de clés.
-- ===========================================================================

USE ROLE ACCOUNTADMIN;

-- 1. Garde-fou financier ----------------------------------------------------
-- L'essai gratuit donne un crédit limité et dure 30 jours. Ce moniteur coupe
-- l'entrepôt du cours s'il consomme plus de 10 crédits dans le mois.
-- (Un entrepôt X-SMALL consomme 1 crédit par heure d'activité.)
CREATE RESOURCE MONITOR IF NOT EXISTS RM_FORMATION
  WITH CREDIT_QUOTA = 10
       FREQUENCY = MONTHLY
       START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 75 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;

-- 2. Entrepôt de calcul -----------------------------------------------------
-- AUTO_SUSPEND = 60 : l'entrepôt s'éteint après 60 s sans requête.
-- C'est LE réglage qui protège les crédits. Ne jamais le monter « pour aller plus vite ».
CREATE WAREHOUSE IF NOT EXISTS WH_AIRFLOW
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;
ALTER WAREHOUSE WH_AIRFLOW SET RESOURCE_MONITOR = RM_FORMATION;

-- 3. Base et schémas --------------------------------------------------------
-- RAW   : les données telles que publiées par la source, jamais modifiées à la main
-- MARTS : les tables calculées pour l'analyse
CREATE DATABASE IF NOT EXISTS NYC_TAXI;
CREATE SCHEMA IF NOT EXISTS NYC_TAXI.RAW;
CREATE SCHEMA IF NOT EXISTS NYC_TAXI.MARTS;

-- 4. Rôle d'Airflow : le strict nécessaire ----------------------------------
CREATE ROLE IF NOT EXISTS ROLE_AIRFLOW;
GRANT USAGE ON WAREHOUSE WH_AIRFLOW TO ROLE ROLE_AIRFLOW;
GRANT USAGE ON DATABASE NYC_TAXI TO ROLE ROLE_AIRFLOW;
GRANT USAGE, CREATE TABLE, CREATE STAGE ON SCHEMA NYC_TAXI.RAW TO ROLE ROLE_AIRFLOW;
GRANT USAGE, CREATE TABLE ON SCHEMA NYC_TAXI.MARTS TO ROLE ROLE_AIRFLOW;
-- Pour pouvoir consulter les tables d'Airflow depuis Snowsight avec ton compte :
GRANT ROLE ROLE_AIRFLOW TO ROLE SYSADMIN;

-- 5. Utilisateur de service, authentifié par clé ----------------------------
-- TYPE = SERVICE : pas de mot de passe, pas d'interface web, pas de MFA.
-- C'est le type prévu pour un programme comme Airflow. Snowflake refuse de
-- plus en plus les connexions par simple mot de passe : la clé est la norme.
CREATE USER IF NOT EXISTS AIRFLOW_SVC
  TYPE = SERVICE
  DEFAULT_ROLE = ROLE_AIRFLOW
  DEFAULT_WAREHOUSE = WH_AIRFLOW
  DEFAULT_NAMESPACE = NYC_TAXI.RAW
  RSA_PUBLIC_KEY = '<CLE_PUBLIQUE>';
GRANT ROLE ROLE_AIRFLOW TO USER AIRFLOW_SVC;

-- 6. Objets créés PAR le rôle d'Airflow (il en est donc propriétaire) -------
USE ROLE ROLE_AIRFLOW;
USE WAREHOUSE WH_AIRFLOW;
USE SCHEMA NYC_TAXI.RAW;

-- Zone de dépôt interne : Airflow y envoie les fichiers avec PUT.
CREATE STAGE IF NOT EXISTS TLC_STAGE
  COMMENT = 'Fichiers Parquet de la TLC, un dossier par mois';

-- Table brute. ENABLE_SCHEMA_EVOLUTION : quand la TLC ajoute une colonne
-- (cbd_congestion_fee en 2025, request_source en 2026), COPY INTO l'ajoute
-- à la table au lieu d'échouer ou de l'ignorer.
CREATE TABLE IF NOT EXISTS YELLOW_TRIPS (
  VENDORID               NUMBER,
  TPEP_PICKUP_DATETIME   TIMESTAMP_NTZ,
  TPEP_DROPOFF_DATETIME  TIMESTAMP_NTZ,
  PASSENGER_COUNT        NUMBER,
  TRIP_DISTANCE          FLOAT,
  RATECODEID             NUMBER,
  STORE_AND_FWD_FLAG     VARCHAR,
  PULOCATIONID           NUMBER,
  DOLOCATIONID           NUMBER,
  PAYMENT_TYPE           NUMBER,
  FARE_AMOUNT            FLOAT,
  EXTRA                  FLOAT,
  MTA_TAX                FLOAT,
  TIP_AMOUNT             FLOAT,
  TOLLS_AMOUNT           FLOAT,
  IMPROVEMENT_SURCHARGE  FLOAT,
  TOTAL_AMOUNT           FLOAT,
  CONGESTION_SURCHARGE   FLOAT,
  AIRPORT_FEE            FLOAT,
  SOURCE_FILE            VARCHAR       COMMENT 'Fichier d''origine dans le stage, ex. 2025-01/yellow_tripdata_2025-01.parquet',
  LOADED_AT              TIMESTAMP_LTZ COMMENT 'Heure du chargement'
)
ENABLE_SCHEMA_EVOLUTION = TRUE
COMMENT = 'Courses de taxis jaunes NYC, telles que publiées par la TLC';

-- Journal des chargements : sert à savoir si un fichier a été republié (ETag).
CREATE TABLE IF NOT EXISTS LOAD_LOG (
  MOIS       VARCHAR(7) NOT NULL,
  ETAG       VARCHAR,
  TAILLE     NUMBER,
  NB_LIGNES  NUMBER,
  CHARGE_LE  TIMESTAMP_LTZ
);

-- Vérification : doit afficher RSA_PUBLIC_KEY_FP renseigné.
USE ROLE ACCOUNTADMIN;
DESC USER AIRFLOW_SVC;
