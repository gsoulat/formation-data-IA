-- =====================================================================
-- 04_vue_catalogue.sql — une vue de catalogue pour UNE table, à étendre à plusieurs
-- Après 03_acces_par_ligne.sql. Exécuter en entier, puis le test avec l'analyste.
-- =====================================================================
USE SECONDARY ROLES NONE;
USE ROLE EX_PIPELINE;
USE WAREHOUSE EXEMPLE_WH;

COMMENT ON TABLE  EXEMPLE_GOUV.DONNEES.CLIENTS           IS 'Clients fictifs du bac à sable : 1 ligne = 1 client.';
COMMENT ON COLUMN EXEMPLE_GOUV.DONNEES.CLIENTS.client_id IS 'Identifiant interne du client.';
COMMENT ON COLUMN EXEMPLE_GOUV.DONNEES.CLIENTS.region    IS 'Région commerciale. Sert à filtrer les lignes.';

-- Une ligne par colonne : sa description (INFORMATION_SCHEMA.COLUMNS) et son tag
-- (TAG_REFERENCES_ALL_COLUMNS, une fonction qu'on appelle pour UNE table à la fois).
-- Pour plusieurs tables : un bloc SELECT ... FROM TABLE(...) par table, réunis par UNION ALL
-- dans le WITH, puis la même jointure.
CREATE OR REPLACE VIEW EXEMPLE_GOUV.DONNEES.V_CATALOGUE AS
WITH tags AS (
    SELECT object_schema, object_name, column_name, tag_name, tag_value
    FROM TABLE(EXEMPLE_GOUV.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('EXEMPLE_GOUV.DONNEES.CLIENTS', 'table'))
)
SELECT
    c.table_name,
    c.column_name,
    c.data_type,
    c.comment                                               AS description,
    MAX(IFF(g.tag_name = 'PII', g.tag_value, NULL))         AS donnee_personnelle
FROM EXEMPLE_GOUV.INFORMATION_SCHEMA.COLUMNS c
LEFT JOIN tags g
  ON g.object_schema = c.table_schema AND g.object_name = c.table_name AND g.column_name = c.column_name
WHERE c.table_schema = 'DONNEES' AND c.table_name = 'CLIENTS'
GROUP BY 1, 2, 3, 4;

GRANT SELECT ON VIEW EXEMPLE_GOUV.DONNEES.V_CATALOGUE TO ROLE EX_ANALYSTE;

-- Avec le propriétaire : 6 lignes, descriptions et tags
SELECT * FROM EXEMPLE_GOUV.DONNEES.V_CATALOGUE ORDER BY column_name;

-- Test : la même vue lue par l'analyste. Combien de lignes, et les tags sont-ils là ?
-- INFORMATION_SCHEMA dépend du rôle qui interroge : comparez, et notez ce que vous observez.
USE ROLE EX_ANALYSTE;
SELECT * FROM EXEMPLE_GOUV.DONNEES.V_CATALOGUE ORDER BY column_name;
