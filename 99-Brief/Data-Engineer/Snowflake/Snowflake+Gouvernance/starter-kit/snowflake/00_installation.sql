-- =====================================================================
-- 00_installation.sql — un compte Snowflake vide devient prêt pour le brief
-- Crée le warehouse, la base NYC_TAXI et ses schémas, et le rôle des outils (TRANSFORMER),
-- avec lequel vous chargerez les données et ferez tourner les tâches planifiées.
-- À exécuter en entier avec ACCOUNTADMIN (Cmd+Maj+Entrée). Rejouable.
-- =====================================================================
USE ROLE ACCOUNTADMIN;
SET moi = CURRENT_USER();

-- 1. Le warehouse : la puissance de calcul. La plus petite taille, éteinte après 60 s sans requête.
CREATE WAREHOUSE IF NOT EXISTS NYC_TAXI_WH
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;

-- 2. La base et ses couches
CREATE DATABASE IF NOT EXISTS NYC_TAXI;
CREATE SCHEMA IF NOT EXISTS NYC_TAXI.RAW     COMMENT = 'Copie fidèle des fichiers sources';
CREATE SCHEMA IF NOT EXISTS NYC_TAXI.STAGING COMMENT = 'Vues de typage et de nettoyage';
CREATE SCHEMA IF NOT EXISTS NYC_TAXI.MARTS   COMMENT = 'Tables prêtes pour les métiers';

-- 3. Le rôle des outils : il charge, transforme et fait tourner les tâches planifiées.
--    Il est propriétaire de tout ce qu'il crée. Rattaché à SYSADMIN.
CREATE ROLE IF NOT EXISTS TRANSFORMER COMMENT = 'Rôle des outils : chargement, transformations, tâches planifiées';
GRANT ROLE TRANSFORMER TO ROLE SYSADMIN;
GRANT ROLE TRANSFORMER TO USER IDENTIFIER($moi);
GRANT USAGE, OPERATE ON WAREHOUSE NYC_TAXI_WH TO ROLE TRANSFORMER;
GRANT USAGE ON DATABASE NYC_TAXI TO ROLE TRANSFORMER;
GRANT USAGE, CREATE TABLE, CREATE STAGE, CREATE FILE FORMAT ON SCHEMA NYC_TAXI.RAW TO ROLE TRANSFORMER;
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA NYC_TAXI.STAGING TO ROLE TRANSFORMER;
GRANT USAGE, CREATE TABLE, CREATE VIEW, CREATE TASK ON SCHEMA NYC_TAXI.MARTS TO ROLE TRANSFORMER;

-- 4. Le droit de faire tourner des tâches planifiées : il ne peut venir que d'ACCOUNTADMIN
GRANT EXECUTE TASK ON ACCOUNT TO ROLE TRANSFORMER;

-- Vérifier : RAW, STAGING et MARTS (plus INFORMATION_SCHEMA et PUBLIC)
SHOW SCHEMAS IN DATABASE NYC_TAXI;
