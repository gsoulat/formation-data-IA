-- Répond à la question centrale : OÙ et QUAND la demande est la plus forte,
-- et combien rapporte un trajet. Grain : zone de prise en charge × heure × type de jour.
CREATE OR REPLACE TABLE NYC_TAXI.MARTS.MART_ZONE_HOURLY_DEMAND AS
SELECT
    f.pickup_zone_key,
    z.zone_name                                 AS pickup_zone_name,
    z.borough                                   AS pickup_borough,
    z.is_airport                                AS pickup_is_airport,
    f.pickup_hour,
    f.is_weekend,

    COUNT(*)                                    AS nb_trips,
    COUNT(DISTINCT f.pickup_date)               AS nb_days,
    ROUND(COUNT(*) / NULLIF(COUNT(DISTINCT f.pickup_date), 0), 1) AS avg_trips_per_day,
    ROUND(SUM(f.total_amount), 2)               AS total_revenue,
    ROUND(AVG(f.total_amount), 2)               AS avg_revenue_per_trip,
    ROUND(AVG(f.fare_amount), 2)                AS avg_fare,
    ROUND(AVG(f.trip_distance_miles), 2)        AS avg_distance_miles,
    ROUND(AVG(f.trip_duration_min), 1)          AS avg_duration_min,
    ROUND(AVG(f.avg_speed_mph), 1)              AS avg_speed_mph,
    ROUND(AVG(f.tip_rate_pct), 1)               AS avg_tip_rate_pct_card,
    ROUND(SUM(f.total_amount) / NULLIF(SUM(f.trip_duration_min), 0) * 60, 2) AS revenue_per_hour_driven
FROM NYC_TAXI.MARTS.FCT_TRIPS f
LEFT JOIN NYC_TAXI.MARTS.DIM_ZONE z ON z.zone_key = f.pickup_zone_key
GROUP BY 1, 2, 3, 4, 5, 6;
