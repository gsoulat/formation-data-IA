-- Calendrier généré sur le périmètre du projet (paramètres du DAG).
CREATE OR REPLACE TABLE NYC_TAXI.MARTS.DIM_DATE AS
WITH spine AS (
    SELECT DATEADD('day', ROW_NUMBER() OVER (ORDER BY SEQ4()) - 1, '{{ params.start_month }}'::date) AS full_date
    FROM TABLE(GENERATOR(ROWCOUNT => 400))
)
SELECT
    TO_NUMBER(TO_CHAR(full_date, 'YYYYMMDD')) AS date_key,
    full_date,
    YEAR(full_date)                           AS year,
    QUARTER(full_date)                        AS quarter,
    MONTH(full_date)                          AS month,
    MONTHNAME(full_date)                      AS month_name,
    DAY(full_date)                            AS day_of_month,
    DAYOFWEEKISO(full_date)                   AS day_of_week_iso,
    DAYNAME(full_date)                        AS day_name,
    DAYOFWEEKISO(full_date) >= 6              AS is_weekend
FROM spine
WHERE full_date < '{{ params.end_month }}'::date;
