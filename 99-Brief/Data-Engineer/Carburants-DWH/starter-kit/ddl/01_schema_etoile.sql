-- ============================================================
-- KIT DE DEMARRAGE — Schéma en étoile "entrepôt prix carburants" (Rouleo)
--
-- Etat HERITE du prédécesseur. Défauts volontaires, au coeur du brief :
--   * dim_station n'a AUCUNE historisation : sa clé primaire est la clé
--     naturelle de la station, donc toute évolution de ses caractéristiques
--     ne peut qu'ECRASER la version précédente. C'est ce qui fait bouger
--     rétroactivement l'analyse "autoroute vs réseau ordinaire".
--   * fait_prix n'a aucune contrainte d'unicité métier : rejouer un
--     chargement crée des doublons silencieux.
--   * latitude / longitude sont stockées TELLES QUE PUBLIEES dans l'archive
--     XML, c'est-à-dire en centièmes de millième de degré (entiers), sans
--     conversion. Le prédécesseur ne s'en est jamais aperçu.
--
-- Usage : psql -d carburants -f ddl/01_schema_etoile.sql
-- ============================================================

CREATE SCHEMA IF NOT EXISTS entrepot;
SET search_path TO entrepot;

-- ---------- Dimension temps (grain : le jour) ----------
CREATE TABLE IF NOT EXISTS dim_temps (
    temps_id     INTEGER      PRIMARY KEY,          -- format AAAAMMJJ
    date_jour    DATE         NOT NULL UNIQUE,
    annee        INTEGER      NOT NULL,
    trimestre    INTEGER      NOT NULL,
    mois         INTEGER      NOT NULL,
    nom_mois     VARCHAR(20)  NOT NULL,
    jour         INTEGER      NOT NULL,
    jour_semaine VARCHAR(10)  NOT NULL,
    est_weekend  BOOLEAN      NOT NULL
);

-- ---------- Dimension carburant ----------
-- Les identifiants sont ceux de la source officielle (1 = Gazole, etc.).
CREATE TABLE IF NOT EXISTS dim_carburant (
    carburant_id SMALLINT     PRIMARY KEY,
    nom          VARCHAR(20)  NOT NULL UNIQUE
);

-- ---------- Dimension station ----------
-- NOTE (héritage) : aucune historisation. La clé primaire est la clé
-- naturelle publiée par la source, si bien que toute mise à jour écrase
-- l'état précédent : type de voirie, services, horaires, adresse.
-- C'est le bug métier central du brief.
CREATE TABLE IF NOT EXISTS dim_station (
    station_id       VARCHAR(12)  PRIMARY KEY,   -- identifiant du point de vente
    adresse          VARCHAR(200),
    ville            VARCHAR(120),
    code_postal      VARCHAR(10),
    code_departement VARCHAR(3),
    type_voirie      VARCHAR(2),                 -- 'R' route, 'A' autoroute... et parfois autre chose
    latitude_brute   NUMERIC(14,5),              -- TEL QUEL depuis la source : pas des degrés
    longitude_brute  NUMERIC(14,5),              -- TEL QUEL depuis la source : pas des degrés
    services         TEXT,                        -- liste concaténée, séparateur '|'
    automate_24_24   BOOLEAN,
    date_chargement  TIMESTAMP    NOT NULL DEFAULT now()
);

-- ---------- Table de faits : un relevé de prix ----------
-- Grain : une station x un carburant x un horodatage de relevé.
-- NOTE (héritage) : aucune contrainte d'unicité sur le grain métier,
-- donc aucun garde-fou contre le rejeu d'un chargement.
CREATE TABLE IF NOT EXISTS fait_prix (
    prix_id      BIGSERIAL    PRIMARY KEY,
    station_id   VARCHAR(12)  NOT NULL REFERENCES dim_station (station_id),
    carburant_id SMALLINT     NOT NULL REFERENCES dim_carburant (carburant_id),
    temps_id     INTEGER      NOT NULL REFERENCES dim_temps (temps_id),
    horodatage   TIMESTAMP    NOT NULL,
    prix         NUMERIC(6,3) NOT NULL,
    source       VARCHAR(20)  NOT NULL DEFAULT 'archive_annuelle'
);

CREATE INDEX IF NOT EXISTS idx_fait_prix_station   ON fait_prix (station_id);
CREATE INDEX IF NOT EXISTS idx_fait_prix_temps     ON fait_prix (temps_id);
CREATE INDEX IF NOT EXISTS idx_fait_prix_carburant ON fait_prix (carburant_id);
CREATE INDEX IF NOT EXISTS idx_dim_station_dept    ON dim_station (code_departement);
