-- =====================================================================
-- 03_acces_par_ligne.sql — filtrer les lignes avec une table de correspondance
-- Après 02_masquage_par_tag.sql. Partie A en entier, puis les tests un par un. Rejouable.
-- =====================================================================

-- ===================================================================== A. Écrire et attacher
USE SECONDARY ROLES NONE;
USE ROLE EX_GOUVERNANCE;
USE WAREHOUSE EXEMPLE_WH;

-- 1. Qui voit quelle région : des lignes dans une table, pas des valeurs écrites dans la politique.
--    Ouvrir une région à un vendeur = ajouter une ligne, sans toucher à la politique.
CREATE TABLE IF NOT EXISTS EXEMPLE_GOUV.GOUVERNANCE.ACCES_REGION (
    role_name VARCHAR NOT NULL,
    region    VARCHAR NOT NULL     -- une région, ou * pour toutes
);
DELETE FROM EXEMPLE_GOUV.GOUVERNANCE.ACCES_REGION;
INSERT INTO EXEMPLE_GOUV.GOUVERNANCE.ACCES_REGION VALUES
    ('EX_PIPELINE', '*'),      -- sans cette ligne, le pipeline ne verrait plus rien, sans erreur
    ('EX_ANALYSTE', '*'),
    ('EX_VENDEUR',  'Nord');

-- 2. La politique : appelée pour CHAQUE ligne lue, avec la valeur de la colonne region.
--    Elle renvoie TRUE (la ligne s'affiche) ou FALSE (elle disparaît du résultat).
--    La sous-requête lit ACCES_REGION avec les droits du PROPRIÉTAIRE de la politique
--    (EX_GOUVERNANCE) : les rôles métier n'ont pas besoin de lire cette table.
CREATE ROW ACCESS POLICY IF NOT EXISTS EXEMPLE_GOUV.GOUVERNANCE.RAP_REGION
  AS (region_ligne VARCHAR) RETURNS BOOLEAN -> FALSE;     -- corps provisoire (rejouable)

ALTER ROW ACCESS POLICY EXEMPLE_GOUV.GOUVERNANCE.RAP_REGION SET BODY ->
  EXISTS (
    SELECT 1
    FROM EXEMPLE_GOUV.GOUVERNANCE.ACCES_REGION a
    WHERE a.role_name = CURRENT_ROLE()          -- le rôle actif, pas les rôles secondaires
      AND a.region IN (region_ligne, '*')
  );

-- 3. L'attacher à la table, sur la colonne region. On retire d'abord ce qui est déjà attaché :
--    DROP ALL ne fait rien s'il n'y a rien, ADD échouerait s'il y avait déjà une politique.
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS DROP ALL ROW ACCESS POLICIES;
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS ADD ROW ACCESS POLICY EXEMPLE_GOUV.GOUVERNANCE.RAP_REGION ON (region);

-- ===================================================================== B. Tester (un bloc à la fois)

-- Test 1 : EX_VENDEUR → une seule région, Nord, 2 clients (masqués comme au fichier 02)
USE SECONDARY ROLES NONE;
USE ROLE EX_VENDEUR;
USE WAREHOUSE EXEMPLE_WH;
SELECT region, COUNT(*) AS nb FROM EXEMPLE_GOUV.DONNEES.CLIENTS GROUP BY region;

-- Test 2 : EX_ANALYSTE → 3 régions, 2 clients chacune
USE SECONDARY ROLES NONE;
USE ROLE EX_ANALYSTE;
USE WAREHOUSE EXEMPLE_WH;
SELECT region, COUNT(*) AS nb FROM EXEMPLE_GOUV.DONNEES.CLIENTS GROUP BY region;

-- Test 3 : ouvrir le Sud au vendeur, SANS modifier la politique
USE SECONDARY ROLES NONE;
USE ROLE EX_GOUVERNANCE;
USE WAREHOUSE EXEMPLE_WH;
INSERT INTO EXEMPLE_GOUV.GOUVERNANCE.ACCES_REGION VALUES ('EX_VENDEUR', 'Sud');
USE ROLE EX_VENDEUR;
SELECT region, COUNT(*) AS nb FROM EXEMPLE_GOUV.DONNEES.CLIENTS GROUP BY region;   -- Nord et Sud

-- Test 4 : le pipeline reconstruit la table → les politiques restent en place, valeurs réelles
USE SECONDARY ROLES NONE;
USE ROLE EX_PIPELINE;
USE WAREHOUSE EXEMPLE_WH;
INSERT OVERWRITE INTO EXEMPLE_GOUV.DONNEES.CLIENTS
SELECT * FROM EXEMPLE_GOUV.DONNEES.CLIENTS;                 -- recopie la table sur elle-même
USE ROLE EX_ANALYSTE;
SELECT * FROM EXEMPLE_GOUV.DONNEES.CLIENTS WHERE client_id = 'C1';   -- toujours masqué
-- Question : que se passerait-il avec CREATE OR REPLACE TABLE ... AS SELECT à la place ?
