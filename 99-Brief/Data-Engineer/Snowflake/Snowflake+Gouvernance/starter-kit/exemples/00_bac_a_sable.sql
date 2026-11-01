-- =====================================================================
-- 00_bac_a_sable.sql — un petit cas indépendant pour apprendre les gestes, pas votre brief
-- Une base EXEMPLE_GOUV, une table de 6 clients fictifs, quatre rôles. Tout se supprime à la fin
-- (99_nettoyage.sql). À exécuter en entier avec ACCOUNTADMIN (Cmd+Maj+Entrée). Rejouable.
-- =====================================================================
USE ROLE ACCOUNTADMIN;
SET moi = CURRENT_USER();

-- Les rôles : ni rattachés à SYSADMIN, ni entre eux. Chacun ne fait que son métier.
CREATE ROLE IF NOT EXISTS EX_PIPELINE    COMMENT = 'Charge et transforme : propriétaire des données';
CREATE ROLE IF NOT EXISTS EX_GOUVERNANCE COMMENT = 'Écrit les règles : tags et politiques. Ne lit pas les données';
CREATE ROLE IF NOT EXISTS EX_VENDEUR     COMMENT = 'Vendeur de la région Nord';
CREATE ROLE IF NOT EXISTS EX_ANALYSTE    COMMENT = 'Analyse toutes les régions, sans identifier personne';
GRANT ROLE EX_PIPELINE    TO USER IDENTIFIER($moi);
GRANT ROLE EX_GOUVERNANCE TO USER IDENTIFIER($moi);
GRANT ROLE EX_VENDEUR     TO USER IDENTIFIER($moi);
GRANT ROLE EX_ANALYSTE    TO USER IDENTIFIER($moi);

-- Un warehouse à part, que tous les rôles ont le droit d'utiliser
CREATE WAREHOUSE IF NOT EXISTS EXEMPLE_WH
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
GRANT USAGE ON WAREHOUSE EXEMPLE_WH TO ROLE EX_PIPELINE;
GRANT USAGE ON WAREHOUSE EXEMPLE_WH TO ROLE EX_GOUVERNANCE;
GRANT USAGE ON WAREHOUSE EXEMPLE_WH TO ROLE EX_VENDEUR;
GRANT USAGE ON WAREHOUSE EXEMPLE_WH TO ROLE EX_ANALYSTE;

-- La base et ses deux schémas. ACCOUNTADMIN les crée, puis DONNE la propriété :
-- le propriétaire d'un schéma peut y créer ce qu'il veut, sans autre droit.
CREATE DATABASE IF NOT EXISTS EXEMPLE_GOUV;
CREATE SCHEMA IF NOT EXISTS EXEMPLE_GOUV.DONNEES;
CREATE SCHEMA IF NOT EXISTS EXEMPLE_GOUV.GOUVERNANCE;
GRANT OWNERSHIP ON SCHEMA EXEMPLE_GOUV.DONNEES     TO ROLE EX_PIPELINE    COPY CURRENT GRANTS;
GRANT OWNERSHIP ON SCHEMA EXEMPLE_GOUV.GOUVERNANCE TO ROLE EX_GOUVERNANCE COPY CURRENT GRANTS;

-- Entrer dans la base : USAGE sur la base, puis sur le schéma (le propriétaire l'a déjà)
GRANT USAGE ON DATABASE EXEMPLE_GOUV TO ROLE EX_PIPELINE;
GRANT USAGE ON DATABASE EXEMPLE_GOUV TO ROLE EX_GOUVERNANCE;
GRANT USAGE ON DATABASE EXEMPLE_GOUV TO ROLE EX_VENDEUR;
GRANT USAGE ON DATABASE EXEMPLE_GOUV TO ROLE EX_ANALYSTE;

-- Les données : créées par EX_PIPELINE, qui en devient propriétaire
USE ROLE EX_PIPELINE;
USE WAREHOUSE EXEMPLE_WH;
CREATE TABLE IF NOT EXISTS EXEMPLE_GOUV.DONNEES.CLIENTS (
    client_id      VARCHAR,
    nom            VARCHAR,
    email          VARCHAR,
    telephone      VARCHAR,
    region         VARCHAR,
    score          NUMBER
);
INSERT OVERWRITE INTO EXEMPLE_GOUV.DONNEES.CLIENTS VALUES
    ('C1', 'Martin',  'claire.martin@exemple.test',  '06 00 00 00 01', 'Nord', 720),
    ('C2', 'Bernard', 'paul.bernard@exemple.test',   '06 00 00 00 02', 'Nord', 640),
    ('C3', 'Petit',   'lea.petit@exemple.test',      '06 00 00 00 03', 'Sud',  810),
    ('C4', 'Durand',  'hugo.durand@exemple.test',    '06 00 00 00 04', 'Sud',  590),
    ('C5', 'Leroy',   'ines.leroy@exemple.test',     '06 00 00 00 05', 'Est',  700),
    ('C6', 'Moreau',  'nils.moreau@exemple.test',    '06 00 00 00 06', 'Est',  660);

-- Le propriétaire accorde la lecture : au vendeur et à l'analyste, pas au rôle de gouvernance.
-- Celui-ci reçoit seulement l'usage du schéma : voir les tables (pour y attacher ses politiques), pas leur contenu.
GRANT USAGE ON SCHEMA EXEMPLE_GOUV.DONNEES TO ROLE EX_GOUVERNANCE;
GRANT USAGE ON SCHEMA EXEMPLE_GOUV.DONNEES TO ROLE EX_VENDEUR;
GRANT USAGE ON SCHEMA EXEMPLE_GOUV.DONNEES TO ROLE EX_ANALYSTE;
GRANT SELECT ON TABLE EXEMPLE_GOUV.DONNEES.CLIENTS TO ROLE EX_VENDEUR;
GRANT SELECT ON TABLE EXEMPLE_GOUV.DONNEES.CLIENTS TO ROLE EX_ANALYSTE;

-- Vérifier : 6 clients
SELECT COUNT(*) AS nb_clients FROM EXEMPLE_GOUV.DONNEES.CLIENTS;
