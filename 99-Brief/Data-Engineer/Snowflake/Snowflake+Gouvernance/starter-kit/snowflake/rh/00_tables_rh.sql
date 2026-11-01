-- À exécuter avec le rôle des outils (vérifiez le rôle affiché en haut à droite de la feuille).
USE ROLE TRANSFORMER;
USE WAREHOUSE NYC_TAXI_WH;

-- Tables du domaine RH. CREATE TABLE IF NOT EXISTS : la tâche peut être rejouée sans rien casser,
-- et les tables ne sont jamais recréées (ce qui est posé dessus reste en place).

CREATE TABLE IF NOT EXISTS NYC_TAXI.MARTS.DIM_DRIVER (
    driver_id            VARCHAR,
    first_name           VARCHAR,
    last_name            VARCHAR,
    email                VARCHAR,
    phone                VARCHAR,
    birth_date           DATE,
    tlc_license_number   VARCHAR,
    depot                VARCHAR,
    hire_date            DATE,
    end_date             DATE,
    is_active            BOOLEAN,
    tenure_years         FLOAT
);

CREATE TABLE IF NOT EXISTS NYC_TAXI.MARTS.MART_DRIVER_MONTHLY (
    activity_month       DATE,
    driver_id            VARCHAR,
    driver_name          VARCHAR,
    depot                VARCHAR,
    nb_shifts            INTEGER,
    hours_worked         FLOAT,
    trips_count          INTEGER,
    revenue_usd          FLOAT
);

-- Référentiel des dépôts : une ligne par dépôt, aucune donnée personnelle
CREATE TABLE IF NOT EXISTS NYC_TAXI.MARTS.DIM_DEPOT (
    depot                VARCHAR,
    quartier             VARCHAR,
    ouvert_en            INTEGER,
    nb_places            INTEGER
);
