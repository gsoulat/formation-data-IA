-- À exécuter avec le rôle des outils (vérifiez le rôle affiché en haut à droite de la feuille).
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Référentiel des dépôts : les trois garages d'où partent les taxis.
-- INSERT OVERWRITE vide la table et la remplit, sans la recréer.
INSERT OVERWRITE INTO NYC_TAXI.MARTS.DIM_DEPOT (depot, quartier, ouvert_en, nb_places) VALUES
    ('Bronx',    'Hunts Point',       2009, 140),
    ('Brooklyn', 'East New York',     2011, 120),
    ('Queens',   'Long Island City',  2008, 180);
