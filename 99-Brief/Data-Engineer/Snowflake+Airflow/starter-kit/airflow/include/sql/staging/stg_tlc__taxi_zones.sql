CREATE OR REPLACE VIEW NYC_TAXI.STAGING.STG_TLC__TAXI_ZONES AS
SELECT
    locationid::integer AS zone_key,
    zone                AS zone_name,
    borough             AS borough,
    service_zone        AS service_zone,
    _source_file        AS source_file,
    _loaded_at          AS loaded_at
FROM NYC_TAXI.RAW.TAXI_ZONE_LOOKUP;
