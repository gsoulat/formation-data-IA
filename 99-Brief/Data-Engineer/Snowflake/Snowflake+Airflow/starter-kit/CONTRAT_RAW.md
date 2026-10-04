# Contrat de la couche RAW

Les fichiers SQL fournis lisent deux tables et écrivent dans trois schémas. Ils ne fonctionnent que si votre entrepôt respecte exactement les noms ci-dessous. Les fichiers SQL ne se modifient pas : c'est l'entrepôt qui s'adapte.

## Ce qui est imposé, ce qui est libre

| Objet | Nom | Imposé ? |
|---|---|---|
| Base | `NYC_TAXI` | oui |
| Schémas | `RAW`, `STAGING`, `INTERMEDIATE`, `MARTS` | oui |
| Tables RAW | `YELLOW_TRIPDATA`, `TAXI_ZONE_LOOKUP` | oui, colonnes comprises |
| Warehouse | par exemple `NYC_TAXI_WH` | libre |
| Rôle des outils | par exemple `TRANSFORMER` | libre |
| Utilisateur de service | par exemple `AIRFLOW_SVC` | libre |
| Stage, formats de fichier | à votre choix | libre |

Le rôle des outils doit pouvoir créer des tables, un stage et des formats de fichier dans `RAW`, et créer des tables et des vues dans `STAGING`, `INTERMEDIATE` et `MARTS`.

## Table `NYC_TAXI.RAW.YELLOW_TRIPDATA`

Une ligne par trajet, copie fidèle des fichiers Parquet mensuels. Les noms de colonnes sont ceux des fichiers TLC, sans distinction de majuscules.

| Colonne | Nature |
|---|---|
| `vendorid` | nombre entier |
| `tpep_pickup_datetime` | date et heure, sans fuseau |
| `tpep_dropoff_datetime` | date et heure, sans fuseau |
| `passenger_count` | nombre entier |
| `trip_distance` | nombre à décimales |
| `ratecodeid` | nombre entier |
| `store_and_fwd_flag` | texte (`Y` ou `N`) |
| `pulocationid` | nombre entier |
| `dolocationid` | nombre entier |
| `payment_type` | nombre entier |
| `fare_amount` | nombre à décimales |
| `extra` | nombre à décimales |
| `mta_tax` | nombre à décimales |
| `tip_amount` | nombre à décimales |
| `tolls_amount` | nombre à décimales |
| `improvement_surcharge` | nombre à décimales |
| `total_amount` | nombre à décimales |
| `congestion_surcharge` | nombre à décimales |
| `airport_fee` | nombre à décimales |
| `cbd_congestion_fee` | nombre à décimales |
| `_source_file` | texte, colonne technique |
| `_loaded_at` | date et heure sans fuseau, colonne technique |

Attention au choix des types Snowflake : dans les fichiers, une même colonne peut être entière un mois et décimale le suivant, et un type de nombre sans décimales arrondit les montants. Le guide de chargement (section 4) explique quel type choisir.

## Table `NYC_TAXI.RAW.TAXI_ZONE_LOOKUP`

| Colonne | Nature |
|---|---|
| `locationid` | nombre entier, unique |
| `borough` | texte |
| `zone` | texte |
| `service_zone` | texte |
| `_source_file` | texte, colonne technique |
| `_loaded_at` | date et heure sans fuseau, colonne technique |

## Colonnes techniques

Elles n'existent pas dans les fichiers : c'est le chargement qui les remplit.

- `_source_file` contient le nom du fichier chargé, par exemple `yellow_tripdata_2025-01.parquet`. Les fichiers SQL en extraient le mois (`2025-01`) pour savoir à quel mois appartient chaque ligne : le nom doit conserver le motif `AAAA-MM`.
- `_loaded_at` contient la date et l'heure du chargement. Elle sert à garder la première version d'un trajet présent deux fois.

## Vérifier le contrat

```sql
-- Les deux tables existent et appartiennent au rôle des outils (colonne owner)
SHOW TABLES IN SCHEMA NYC_TAXI.RAW;

-- Un mois chargé : environ 3,47 millions de lignes pour janvier 2025, colonnes techniques remplies
SELECT _source_file, COUNT(*), MIN(_loaded_at) FROM NYC_TAXI.RAW.YELLOW_TRIPDATA GROUP BY 1;

-- Les montants ont gardé leurs décimales
SELECT fare_amount, total_amount FROM NYC_TAXI.RAW.YELLOW_TRIPDATA LIMIT 5;

SELECT COUNT(*) FROM NYC_TAXI.RAW.TAXI_ZONE_LOOKUP;   -- 265
```

Si une colonne manque ou porte un autre nom, la première tâche de transformation échoue avec `invalid identifier`.
