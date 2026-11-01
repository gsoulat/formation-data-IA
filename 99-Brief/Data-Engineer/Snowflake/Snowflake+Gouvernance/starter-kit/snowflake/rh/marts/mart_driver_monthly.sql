-- À exécuter avec le rôle des outils (vérifiez le rôle affiché en haut à droite de la feuille).
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Activité mensuelle de chaque chauffeur : services, heures, courses, recette.
INSERT OVERWRITE INTO NYC_TAXI.MARTS.MART_DRIVER_MONTHLY
SELECT
    DATE_TRUNC('month', s.shift_date)::date     AS activity_month,
    s.driver_id,
    d.first_name || ' ' || d.last_name          AS driver_name,
    s.depot,
    COUNT(*)                                    AS nb_shifts,
    ROUND(SUM(s.hours_worked), 1)               AS hours_worked,
    SUM(s.trips_count)                          AS trips_count,
    ROUND(SUM(s.revenue_usd), 2)                AS revenue_usd
FROM NYC_TAXI.STAGING.STG_RH__DRIVER_SHIFTS s
LEFT JOIN NYC_TAXI.MARTS.DIM_DRIVER d ON d.driver_id = s.driver_id
GROUP BY 1, 2, 3, 4;
