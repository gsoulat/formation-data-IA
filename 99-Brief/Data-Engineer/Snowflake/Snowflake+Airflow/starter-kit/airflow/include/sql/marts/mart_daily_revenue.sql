-- Chiffre d'affaires quotidien par mode de paiement. Grain : jour × mode de paiement.
CREATE OR REPLACE TABLE NYC_TAXI.MARTS.MART_DAILY_REVENUE AS
SELECT
    d.full_date,
    d.day_name,
    d.is_weekend,
    p.payment_type_label,

    COUNT(*)                              AS nb_trips,
    ROUND(SUM(f.total_amount), 2)         AS total_revenue,
    ROUND(SUM(f.fare_amount), 2)          AS total_fare,
    ROUND(SUM(f.tip_amount), 2)           AS total_tips,
    ROUND(SUM(f.surcharges_amount), 2)    AS total_surcharges,
    ROUND(AVG(f.total_amount), 2)         AS avg_revenue_per_trip,
    ROUND(SUM(f.trip_distance_miles), 1)  AS total_distance_miles
FROM NYC_TAXI.MARTS.FCT_TRIPS f
JOIN NYC_TAXI.MARTS.DIM_DATE d              ON d.date_key = f.pickup_date_key
LEFT JOIN NYC_TAXI.MARTS.DIM_PAYMENT_TYPE p ON p.payment_type_key = f.payment_type_key
GROUP BY 1, 2, 3, 4;
