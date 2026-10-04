-- STAGING : renommage et typage uniquement. Aucun filtre, aucune jointure :
-- la vue contient exactement autant de lignes que la table RAW.
CREATE OR REPLACE VIEW NYC_TAXI.STAGING.STG_TLC__YELLOW_TRIPS AS
SELECT
    -- identifiants et codes
    vendorid::integer                        AS vendor_key,
    COALESCE(ratecodeid, 99)::integer        AS rate_code_key,
    payment_type::integer                    AS payment_type_key,
    pulocationid::integer                    AS pickup_zone_key,
    dolocationid::integer                    AS dropoff_zone_key,

    -- horodatages
    tpep_pickup_datetime                     AS pickup_at,
    tpep_dropoff_datetime                    AS dropoff_at,

    -- attributs du trajet
    passenger_count::integer                 AS passenger_count,
    trip_distance::float                     AS trip_distance_miles,
    store_and_fwd_flag = 'Y'                 AS is_store_and_forward,

    -- montants (USD)
    fare_amount::float                       AS fare_amount,
    extra::float                             AS extra_amount,
    mta_tax::float                           AS mta_tax_amount,
    tip_amount::float                        AS tip_amount,
    tolls_amount::float                      AS tolls_amount,
    improvement_surcharge::float             AS improvement_surcharge_amount,
    COALESCE(congestion_surcharge, 0)::float AS congestion_surcharge_amount,
    COALESCE(airport_fee, 0)::float          AS airport_fee_amount,
    COALESCE(cbd_congestion_fee, 0)::float   AS cbd_congestion_fee_amount,
    total_amount::float                      AS total_amount,

    -- traçabilité : le mois est extrait du nom du fichier (yellow_tripdata_2025-01.parquet)
    _source_file                             AS source_file,
    TO_DATE(REGEXP_SUBSTR(_source_file, '[0-9]{4}-[0-9]{2}'), 'YYYY-MM') AS source_file_month,
    _loaded_at                               AS loaded_at
FROM NYC_TAXI.RAW.YELLOW_TRIPDATA;
