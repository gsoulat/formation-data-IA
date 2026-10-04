-- Chaque trajet du mois reçoit AU PLUS une raison de rejet : la première règle qui échoue.
-- On ne supprime rien ici : c'est int_trips__enriched qui filtre.
-- Rejouable : on efface le mois traité avant de le réinsérer.
DELETE FROM NYC_TAXI.INTERMEDIATE.INT_TRIPS__FLAGGED
WHERE source_file_month = '{{ ds }}'::date;

INSERT INTO NYC_TAXI.INTERMEDIATE.INT_TRIPS__FLAGGED
SELECT
    s.*,
    DATEDIFF('second', pickup_at, dropoff_at) / 60.0 AS trip_duration_min,
    CASE
        WHEN pickup_at IS NULL OR dropoff_at IS NULL
            THEN 'timestamp_null'
        WHEN dropoff_at <= pickup_at
            THEN 'duration_non_positive'
        -- en secondes : DATEDIFF('minute') compte les changements de minute, pas la durée réelle
        WHEN DATEDIFF('second', pickup_at, dropoff_at) > {{ params.max_trip_duration_min }} * 60
            THEN 'duration_too_long'
        WHEN DATE_TRUNC('month', pickup_at) <> source_file_month
            THEN 'pickup_outside_file_month'
        WHEN trip_distance_miles <= 0 OR trip_distance_miles > {{ params.max_trip_distance_miles }}
            THEN 'distance_out_of_range'
        WHEN fare_amount < 0 OR total_amount <= 0
            THEN 'amount_non_positive'
        WHEN pickup_zone_key IS NULL OR dropoff_zone_key IS NULL
            THEN 'zone_null'
        ELSE NULL
    END AS rejection_reason
FROM NYC_TAXI.STAGING.STG_TLC__YELLOW_TRIPS s
WHERE source_file_month = '{{ ds }}'::date;
