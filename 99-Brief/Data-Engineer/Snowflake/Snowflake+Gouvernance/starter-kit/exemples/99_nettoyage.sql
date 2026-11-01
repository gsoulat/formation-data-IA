-- =====================================================================
-- 99_nettoyage.sql — tout supprimer, avec ACCOUNTADMIN, en entier.
-- Une politique attachée ne se supprime pas seule (il faut la détacher d'abord) ; ici, on supprime
-- la base entière, ce qui emporte tout d'un coup.
-- =====================================================================
USE SECONDARY ROLES NONE;
USE ROLE ACCOUNTADMIN;
-- La base : ACCOUNTADMIN en est propriétaire. La supprimer supprime tout ce qu'elle contient
--    (tables, tag, politiques, et les tâches, qui s'arrêtent), même ce qui appartient à d'autres rôles.
DROP DATABASE IF EXISTS EXEMPLE_GOUV;
DROP WAREHOUSE IF EXISTS EXEMPLE_WH;
DROP ROLE IF EXISTS EX_PIPELINE;
DROP ROLE IF EXISTS EX_GOUVERNANCE;
DROP ROLE IF EXISTS EX_VENDEUR;
DROP ROLE IF EXISTS EX_ANALYSTE;
