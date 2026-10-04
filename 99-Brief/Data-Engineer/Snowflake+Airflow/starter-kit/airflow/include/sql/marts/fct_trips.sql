-- Table de faits au grain « 1 ligne = 1 trajet ». Alimentée mois par mois :
-- relancer le run d'un mois efface puis réinsère ce mois, sans toucher aux autres.
DELETE FROM NYC_TAXI.MARTS.FCT_TRIPS
WHERE source_file_month = '{{ ds }}'::date;

INSERT INTO NYC_TAXI.MARTS.FCT_TRIPS
SELECT
    trip_sk,
    pickup_date_key,
    pickup_zone_key,
    dropoff_zone_key,
    payment_type_key,
    rate_code_key,
    vendor_key,

    pickup_at,
    dropoff_at,
    pickup_date,
    pickup_hour,
    is_weekend,
    passenger_count,

    trip_distance_miles,
    trip_duration_min,
    avg_speed_mph,
    fare_amount,
    tip_amount,
    tolls_amount,
    -- Le fournisseur 1 inclut déjà la surtaxe de congestion, les frais d'aéroport et le péage
    -- du quartier central dans extra : les ajouter une seconde fois dépasserait total_amount.
    extra_amount + mta_tax_amount + improvement_surcharge_amount
      + CASE WHEN vendor_key = 1 THEN 0
             ELSE congestion_surcharge_amount + airport_fee_amount + cbd_congestion_fee_amount
        END                                                  AS surcharges_amount,
    total_amount,
    tip_rate_pct,

    source_file,
    source_file_month,
    loaded_at
FROM NYC_TAXI.INTERMEDIATE.INT_TRIPS__ENRICHED
WHERE source_file_month = '{{ ds }}'::date;
