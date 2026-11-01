-- =====================================================================
-- 01_role_gouvernance.sql — un rôle qui écrit les règles sans lire les données
-- Après 00_bac_a_sable.sql. Exécuter en entier (Cmd+Maj+Entrée). Rejouable.
-- Retenez la carte : qui POSSÈDE l'objet, et qui a reçu quel PRIVILÈGE pour agir dessus.
-- =====================================================================

-- 1. Les droits « sur tout le compte » ne peuvent venir que d'ACCOUNTADMIN.
--    Ils permettent d'attacher une politique à une table qu'on ne possède pas.
USE SECONDARY ROLES NONE;
USE ROLE ACCOUNTADMIN;
GRANT APPLY MASKING POLICY    ON ACCOUNT TO ROLE EX_GOUVERNANCE;
GRANT APPLY ROW ACCESS POLICY ON ACCOUNT TO ROLE EX_GOUVERNANCE;

-- 2. EX_GOUVERNANCE possède le schéma GOUVERNANCE : il y crée le tag sans autre droit.
USE ROLE EX_GOUVERNANCE;
USE WAREHOUSE EXEMPLE_WH;
CREATE TAG IF NOT EXISTS EXEMPLE_GOUV.GOUVERNANCE.PII
  ALLOWED_VALUES 'identifiant', 'nom', 'email', 'telephone', 'score'
  COMMENT = 'Nature de la donnée personnelle d''une colonne. Déclenche le masquage.';

-- 3. Qui pose le tag sur les colonnes ? Ici, le propriétaire de la table (EX_PIPELINE).
--    Il doit voir le schéma du tag, et recevoir APPLY sur CE tag (pas sur tous).
GRANT USAGE ON SCHEMA EXEMPLE_GOUV.GOUVERNANCE TO ROLE EX_PIPELINE;
GRANT APPLY ON TAG EXEMPLE_GOUV.GOUVERNANCE.PII TO ROLE EX_PIPELINE;

-- 4. EX_PIPELINE tague ses colonnes. region n'est pas taguée : elle servira à filtrer les lignes.
USE ROLE EX_PIPELINE;
USE WAREHOUSE EXEMPLE_WH;
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS MODIFY COLUMN client_id SET TAG EXEMPLE_GOUV.GOUVERNANCE.PII = 'identifiant';
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS MODIFY COLUMN nom       SET TAG EXEMPLE_GOUV.GOUVERNANCE.PII = 'nom';
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS MODIFY COLUMN email     SET TAG EXEMPLE_GOUV.GOUVERNANCE.PII = 'email';
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS MODIFY COLUMN telephone SET TAG EXEMPLE_GOUV.GOUVERNANCE.PII = 'telephone';
ALTER TABLE EXEMPLE_GOUV.DONNEES.CLIENTS MODIFY COLUMN score     SET TAG EXEMPLE_GOUV.GOUVERNANCE.PII = 'score';

-- 5. Vérifier, AVEC LE PROPRIÉTAIRE : 5 colonnes taguées.
--    Avec EX_GOUVERNANCE, la même requête renvoie une erreur ou un résultat vide : INFORMATION_SCHEMA ne montre
--    que ce que le rôle actif a le droit de voir, et il n'a aucun droit sur la table.
SELECT column_name, tag_value
FROM TABLE(EXEMPLE_GOUV.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('EXEMPLE_GOUV.DONNEES.CLIENTS', 'table'))
WHERE tag_name = 'PII'
ORDER BY column_name;

-- Pour voir la carte des droits d'un rôle :  SHOW GRANTS TO ROLE EX_GOUVERNANCE;
