-- Le mois traité est bien présent dans RAW.
SELECT COUNT(*) > 0
FROM NYC_TAXI.RAW.YELLOW_TRIPDATA
WHERE _source_file = 'yellow_tripdata_{{ logical_date.strftime("%Y-%m") }}.parquet';
