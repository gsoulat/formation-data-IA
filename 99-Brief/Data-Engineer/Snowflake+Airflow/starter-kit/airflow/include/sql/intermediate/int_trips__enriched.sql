-- Trajets valides du mois, dédoublonnés et enrichis.
-- La TLC ne fournit pas d'identifiant de trajet : la clé est un MD5 de la clé métier composite.
DELETE FROM NYC_TAXI.INTERMEDIATE.INT_TRIPS__ENRICHED
WHERE source_file_month = '{{ ds }}'::date;

INSERT INTO NYC_TAXI.INTERMEDIATE.INT_TRIPS__ENRICHED
WITH valid_trips AS (
    SELECT *
    FROM NYC_TAXI.INTERMEDIATE.INT_TRIPS__FLAGGED
    WHERE source_file_month = '{{ ds }}'::date
      AND rejection_reason IS NULL
),

deduplicated AS (
    SELECT *
    FROM valid_trips
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY vendor_key, pickup_at, dropoff_at, pickup_zone_key, dropoff_zone_key,
                     trip_distance_miles, fare_amount, total_amount
        ORDER BY loaded_at
    ) = 1
)

SELECT
    MD5(CONCAT_WS('|',
        COALESCE(vendor_key::varchar, ''), COALESCE(pickup_at::varchar, ''), COALESCE(dropoff_at::varchar, ''),
        COALESCE(pickup_zone_key::varchar, ''), COALESCE(dropoff_zone_key::varchar, ''),
        COALESCE(trip_distance_miles::varchar, ''), COALESCE(fare_amount::varchar, ''),
        COALESCE(total_amount::varchar, '')
    ))                                                       AS trip_sk,

    vendor_key,
    rate_code_key,
    payment_type_key,
    pickup_zone_key,
    dropoff_zone_key,

    pickup_at,
    dropoff_at,
    pickup_at::date                                          AS pickup_date,
    TO_NUMBER(TO_CHAR(pickup_at, 'YYYYMMDD'))                AS pickup_date_key,
    HOUR(pickup_at)                                          AS pickup_hour,
    DAYOFWEEKISO(pickup_at)                                  AS pickup_day_of_week_iso,
    DAYOFWEEKISO(pickup_at) >= 6                             AS is_weekend,

    passenger_count,
    is_store_and_forward,
    trip_distance_miles,
    ROUND(trip_duration_min, 2)                              AS trip_duration_min,
    ROUND(trip_distance_miles / NULLIF(trip_duration_min, 0) * 60, 2) AS avg_speed_mph,

    fare_amount,
    extra_amount,
    mta_tax_amount,
    tip_amount,
    tolls_amount,
    improvement_surcharge_amount,
    congestion_surcharge_amount,
    airport_fee_amount,
    cbd_congestion_fee_amount,
    total_amount,
    -- le pourboire n'est enregistré que pour les paiements par carte (code 1)
    CASE WHEN payment_type_key = 1 AND fare_amount > 0
         THEN ROUND(tip_amount / fare_amount * 100, 2) END   AS tip_rate_pct,

    source_file,
    source_file_month,
    loaded_at
FROM deduplicated;
