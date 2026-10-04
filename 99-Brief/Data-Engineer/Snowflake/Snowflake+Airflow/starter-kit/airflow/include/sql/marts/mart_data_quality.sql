-- Rapport qualité par fichier source : combien de lignes écartées et pourquoi.
CREATE OR REPLACE TABLE NYC_TAXI.MARTS.MART_DATA_QUALITY AS
WITH counts AS (
    SELECT
        source_file,
        source_file_month,
        COALESCE(rejection_reason, 'valid') AS status,
        COUNT(*) AS nb_rows
    FROM NYC_TAXI.INTERMEDIATE.INT_TRIPS__FLAGGED
    GROUP BY 1, 2, 3
),

totals AS (
    SELECT source_file, SUM(nb_rows) AS nb_rows_total
    FROM counts
    GROUP BY 1
)

SELECT
    c.source_file,
    c.source_file_month,
    c.status,
    c.nb_rows,
    t.nb_rows_total,
    ROUND(c.nb_rows / t.nb_rows_total * 100, 3) AS pct_of_file
FROM counts c
JOIN totals t ON t.source_file = c.source_file;
