-- À exécuter avec le rôle des outils (vérifiez le rôle affiché en haut à droite de la feuille).
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Chauffeurs : typage et nettoyage léger du fichier RH.
CREATE OR REPLACE VIEW NYC_TAXI.STAGING.STG_RH__DRIVERS AS
SELECT
    driver_id,
    first_name,
    last_name,
    LOWER(TRIM(email))          AS email,
    NULLIF(TRIM(phone), '')     AS phone,
    birth_date::date            AS birth_date,
    tlc_license_number,
    INITCAP(TRIM(depot))        AS depot,
    hire_date::date             AS hire_date,
    end_date::date              AS end_date,
    _source_file                AS source_file,
    _loaded_at                  AS loaded_at
FROM NYC_TAXI.RAW.DRIVERS;
