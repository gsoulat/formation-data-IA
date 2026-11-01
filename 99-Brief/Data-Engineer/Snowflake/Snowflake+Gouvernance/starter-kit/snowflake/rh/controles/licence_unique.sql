-- MODÈLE de règle de qualité : une requête qui renvoie UNE ligne et UNE colonne,
-- le nombre de lignes en anomalie. Zéro = la règle est respectée.
-- Règle : un numéro de licence TLC n'appartient qu'à un seul chauffeur.
SELECT COUNT(*) - COUNT(DISTINCT tlc_license_number) AS nb_anomalies
FROM NYC_TAXI.RAW.DRIVERS;
