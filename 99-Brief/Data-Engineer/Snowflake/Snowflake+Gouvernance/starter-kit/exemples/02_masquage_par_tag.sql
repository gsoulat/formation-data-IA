-- =====================================================================
-- 02_masquage_par_tag.sql — masquer toutes les colonnes taguées, avec une exception
-- Après 01_role_gouvernance.sql. Partie A en entier (Cmd+Maj+Entrée), puis les tests un par un.
-- Rejouable : on peut relancer la partie A après avoir modifié une règle.
-- =====================================================================

-- ===================================================================== A. Écrire et attacher
USE SECONDARY ROLES NONE;
USE ROLE EX_GOUVERNANCE;
USE WAREHOUSE EXEMPLE_WH;

-- Une politique renvoie le type qu'elle reçoit : il en faut une par type de colonne taguée.
-- Ici, une pour le texte, une pour les nombres (score).

-- Rejouable, étape 1 : créer la politique si elle n'existe pas, avec un corps provisoire.
-- (CREATE OR REPLACE échouerait au second passage : on ne remplace pas une politique attachée.)
CREATE MASKING POLICY IF NOT EXISTS EXEMPLE_GOUV.GOUVERNANCE.MASK_TEXTE
  AS (val STRING) RETURNS STRING -> val;

-- Rejouable, étape 2 : écrire le vrai corps. ALTER ... SET BODY fonctionne même si elle est attachée.
ALTER MASKING POLICY EXEMPLE_GOUV.GOUVERNANCE.MASK_TEXTE SET BODY ->
  CASE
    -- L'exception : la politique lit la valeur du tag de la colonne en cours de lecture.
    -- Une colonne taguée 'identifiant' reste visible de tous (pour compter et joindre).
    WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('EXEMPLE_GOUV.GOUVERNANCE.PII') = 'identifiant'
      THEN val
    -- Le pipeline voit tout en clair : s'il lisait un masque, il recopierait le masque.
    WHEN CURRENT_ROLE() = 'EX_PIPELINE'
      THEN val
    -- Le vendeur appelle ses clients : nom et téléphone en clair.
    WHEN CURRENT_ROLE() = 'EX_VENDEUR'
         AND SYSTEM$GET_TAG_ON_CURRENT_COLUMN('EXEMPLE_GOUV.GOUVERNANCE.PII') IN ('nom', 'telephone')
      THEN val
    -- Un masque partiel : on garde le domaine de l'e-mail.
    WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('EXEMPLE_GOUV.GOUVERNANCE.PII') = 'email'
      THEN REGEXP_REPLACE(val, '.+@', '*****@')
    ELSE '*****'
  END;

CREATE MASKING POLICY IF NOT EXISTS EXEMPLE_GOUV.GOUVERNANCE.MASK_NOMBRE
  AS (val NUMBER) RETURNS NUMBER -> val;
ALTER MASKING POLICY EXEMPLE_GOUV.GOUVERNANCE.MASK_NOMBRE SET BODY ->
  CASE
    WHEN CURRENT_ROLE() = 'EX_PIPELINE' THEN val
    WHEN CURRENT_ROLE() = 'EX_ANALYSTE' THEN ROUND(val, -2)   -- l'ordre de grandeur seulement
    ELSE NULL
  END;

-- Attacher les deux politiques AU TAG (et non aux colonnes) : toute colonne qui porte le tag,
-- aujourd'hui ou demain, est protégée. Cette commande échoue si c'est déjà fait : le bloc
-- ci-dessous attrape l'erreur et affiche son message, pour que la partie A reste rejouable.
EXECUTE IMMEDIATE $$
BEGIN
  ALTER TAG EXEMPLE_GOUV.GOUVERNANCE.PII SET
    MASKING POLICY EXEMPLE_GOUV.GOUVERNANCE.MASK_TEXTE,
    MASKING POLICY EXEMPLE_GOUV.GOUVERNANCE.MASK_NOMBRE;
  RETURN 'Politiques attachées au tag.';
EXCEPTION
  WHEN STATEMENT_ERROR THEN
    RETURN 'Non attachées, lire le message (déjà attachées ?) : ' || SQLERRM;
END;
$$;

-- Vérifier : le tag porte bien les deux politiques
SELECT policy_name, policy_kind, ref_column_name, tag_name
FROM TABLE(EXEMPLE_GOUV.INFORMATION_SCHEMA.POLICY_REFERENCES(
  REF_ENTITY_NAME => 'EXEMPLE_GOUV.DONNEES.CLIENTS', REF_ENTITY_DOMAIN => 'TABLE'));

-- ===================================================================== B. Tester (un bloc à la fois)
-- Prévoyez le résultat AVANT de lancer chaque test.

-- Test 1 : EX_PIPELINE → tout en clair
USE SECONDARY ROLES NONE;
USE ROLE EX_PIPELINE;
USE WAREHOUSE EXEMPLE_WH;
SELECT * FROM EXEMPLE_GOUV.DONNEES.CLIENTS WHERE client_id = 'C1';

-- Test 2 : EX_VENDEUR → nom et téléphone en clair, *****@exemple.test, score NULL
USE SECONDARY ROLES NONE;
USE ROLE EX_VENDEUR;
USE WAREHOUSE EXEMPLE_WH;
SELECT * FROM EXEMPLE_GOUV.DONNEES.CLIENTS WHERE client_id = 'C1';

-- Test 3 : EX_ANALYSTE → C1 visible, nom et téléphone *****, *****@exemple.test, score 700
USE SECONDARY ROLES NONE;
USE ROLE EX_ANALYSTE;
USE WAREHOUSE EXEMPLE_WH;
SELECT * FROM EXEMPLE_GOUV.DONNEES.CLIENTS WHERE client_id = 'C1';

-- Question : l'analyste lance  SELECT COUNT(*) FROM ... WHERE email LIKE 'claire%'.
-- Que renvoie-t-elle, et pourquoi ?
