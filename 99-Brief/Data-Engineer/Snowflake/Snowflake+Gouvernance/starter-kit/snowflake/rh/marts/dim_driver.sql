-- À exécuter avec le rôle des outils (vérifiez le rôle affiché en haut à droite de la feuille).
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Dimension chauffeur : une ligne par chauffeur.
-- INSERT OVERWRITE vide la table et la remplit, sans la recréer.
INSERT OVERWRITE INTO NYC_TAXI.MARTS.DIM_DRIVER
SELECT
    driver_id,
    first_name,
    last_name,
    email,
    phone,
    birth_date,
    tlc_license_number,
    depot,
    hire_date,
    end_date,
    end_date IS NULL                                                          AS is_active,
    ROUND(DATEDIFF(day, hire_date, COALESCE(end_date, CURRENT_DATE())) / 365.25, 1) AS tenure_years
FROM NYC_TAXI.STAGING.STG_RH__DRIVERS;
