CREATE OR REPLACE TABLE NYC_TAXI.MARTS.DIM_ZONE AS
SELECT
    zone_key,
    zone_name,
    borough,
    service_zone,
    zone_name ILIKE '%airport%' OR borough = 'EWR' AS is_airport,
    zone_key IN (264, 265)                         AS is_unknown_zone
FROM NYC_TAXI.STAGING.STG_TLC__TAXI_ZONES;
