-- À exécuter avec le rôle des outils (vérifiez le rôle affiché en haut à droite de la feuille).
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Services : typage, et une seule ligne par service (la première chargée).
CREATE OR REPLACE VIEW NYC_TAXI.STAGING.STG_RH__DRIVER_SHIFTS AS
SELECT
    shift_id,
    driver_id,
    shift_date::date            AS shift_date,
    INITCAP(TRIM(depot))        AS depot,
    start_hour::integer         AS start_hour,
    hours_worked::float         AS hours_worked,
    trips_count::integer        AS trips_count,
    revenue_usd::float          AS revenue_usd,
    _source_file                AS source_file,
    _loaded_at                  AS loaded_at
FROM NYC_TAXI.RAW.DRIVER_SHIFTS
QUALIFY ROW_NUMBER() OVER (PARTITION BY shift_id ORDER BY _loaded_at) = 1;
