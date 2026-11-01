-- =====================================================================
-- 05_taches_planifiees.sql — enchaîner des traitements chaque jour, et s'arrêter sur une règle bloquante
-- Après 04_vue_catalogue.sql. Exécuter bloc par bloc, en lisant les commentaires.
-- Une tâche (TASK) = une instruction SQL que Snowflake lance seul, à heure fixe ou après une autre tâche.
-- Plusieurs tâches liées par AFTER forment un graphe : la première (la racine) porte l'horaire.
-- =====================================================================

-- ===================================================================== 1. Le droit de faire tourner des tâches
USE SECONDARY ROLES NONE;
USE ROLE ACCOUNTADMIN;
GRANT EXECUTE TASK ON ACCOUNT TO ROLE EX_PIPELINE;

-- ===================================================================== 2. La table des résultats de qualité
USE ROLE EX_PIPELINE;
USE WAREHOUSE EXEMPLE_WH;
CREATE TABLE IF NOT EXISTS EXEMPLE_GOUV.DONNEES.QUALITE (
    regle VARCHAR, mesure_le TIMESTAMP_NTZ, nb_anomalies NUMBER, seuil NUMBER, statut VARCHAR);

-- ===================================================================== 3. Les tâches
-- L'ordre qui protège : on CONTRÔLE d'abord, et on ne RECONSTRUIT que si le contrôle est passé.

-- La racine : chaque jour à 7 h (heure de Paris), elle mesure la règle.
-- Un bloc de script (EXECUTE IMMEDIATE $$ … $$) permet plusieurs instructions et une condition :
-- on ENREGISTRE toujours la mesure, PUIS on lève une erreur si la règle bloquante est dépassée.
-- La tâche échoue alors, et les tâches qui viennent après elle ne partent pas.
-- Une tâche se crée suspendue : elle ne tourne pas tant qu'on ne l'a pas activée.
CREATE OR REPLACE TASK EXEMPLE_GOUV.DONNEES.T_QUALITE
  WAREHOUSE = EXEMPLE_WH
  SCHEDULE = 'USING CRON 0 7 * * * Europe/Paris'
AS
EXECUTE IMMEDIATE $$
DECLARE
  nb      INTEGER;
  seuil   INTEGER DEFAULT 0;
  bloquee EXCEPTION (-20001, 'Règle bloquante email_present en dépassement');
BEGIN
  SELECT COUNT(*) INTO :nb FROM EXEMPLE_GOUV.DONNEES.CLIENTS WHERE email IS NULL;
  INSERT INTO EXEMPLE_GOUV.DONNEES.QUALITE (regle, mesure_le, nb_anomalies, seuil, statut)
    SELECT 'email_present', CURRENT_TIMESTAMP()::timestamp_ntz, :nb, :seuil,
           IFF(:nb <= :seuil, 'OK', 'ALERTE');
  IF (nb > seuil) THEN
    RAISE bloquee;
  END IF;
  RETURN 'OK';
END;
$$;

-- La suivante : elle ne part que si la racine a réussi (AFTER).
CREATE OR REPLACE TASK EXEMPLE_GOUV.DONNEES.T_RECONSTRUIRE
  WAREHOUSE = EXEMPLE_WH
  AFTER EXEMPLE_GOUV.DONNEES.T_QUALITE
AS
  INSERT OVERWRITE INTO EXEMPLE_GOUV.DONNEES.CLIENTS SELECT * FROM EXEMPLE_GOUV.DONNEES.CLIENTS;

-- ===================================================================== 4. Activer, lancer, regarder
-- Activer la racine ET toutes les tâches qui en dépendent (sinon les suivantes ne partent pas)
SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('EXEMPLE_GOUV.DONNEES.T_QUALITE');

-- Lancer tout de suite, sans attendre 7 h
EXECUTE TASK EXEMPLE_GOUV.DONNEES.T_QUALITE;

-- Attendre une minute, puis regarder : les deux tâches en SUCCEEDED, une ligne OK dans QUALITE.
-- (Dans Snowsight : onglet Databases → EXEMPLE_GOUV → DONNEES → Tasks → T_QUALITE → onglets Graph et Run History.)
SELECT name, state, error_message, completed_time
FROM TABLE(EXEMPLE_GOUV.INFORMATION_SCHEMA.TASK_HISTORY())
WHERE name IN ('T_QUALITE', 'T_RECONSTRUIRE') AND state <> 'SCHEDULED'
ORDER BY completed_time DESC LIMIT 10;
SELECT * FROM EXEMPLE_GOUV.DONNEES.QUALITE ORDER BY mesure_le DESC;

-- ===================================================================== 5. Prouver que la règle bloque
-- Créez une anomalie, relancez : T_QUALITE passe en FAILED avec le message, une ligne ALERTE est
-- enregistrée, et T_RECONSTRUIRE ne part pas.
UPDATE EXEMPLE_GOUV.DONNEES.CLIENTS SET email = NULL WHERE client_id = 'C6';
EXECUTE TASK EXEMPLE_GOUV.DONNEES.T_QUALITE;
-- … attendre une minute, puis relancer les deux SELECT du bloc 4.
-- Questions : pourquoi enregistrer la mesure AVANT de lever l'erreur ? Pourquoi contrôler AVANT de reconstruire ?

-- ===================================================================== 6. Modifier ou arrêter les tâches
-- Pour modifier une tâche du graphe, suspendez d'abord la racine, modifiez, puis réactivez :
--   ALTER TASK EXEMPLE_GOUV.DONNEES.T_QUALITE SUSPEND;   … CREATE OR REPLACE TASK …   SELECT SYSTEM$TASK_DEPENDENTS_ENABLE(…);
-- Une tâche activée tourne chaque jour et consomme des crédits : à la fin, suspendez la racine.
ALTER TASK EXEMPLE_GOUV.DONNEES.T_QUALITE SUSPEND;
