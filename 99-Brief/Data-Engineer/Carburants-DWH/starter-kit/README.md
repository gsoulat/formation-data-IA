# Kit de démarrage — entrepôt des prix des carburants (Rouleo)

Ce kit contient **l'existant dont vous héritez**, pas la solution. Les données ne sont
pas fournies : elles sont réelles et publiques, les scripts vont les chercher.

## Contenu

- `docker-compose.yml` — PostgreSQL 16 + MailHog (serveur SMTP de test)
- `.env.example` — variables d'environnement d'exemple
- `ddl/01_schema_etoile.sql` — le schéma en étoile existant
- `bootstrap.py` — chargement initial depuis l'archive annuelle officielle (~386 Mo de XML)
- `etl_nocturne.py` — **l'ETL nocturne hérité, volontairement défaillant**

## Mise en route

```bash
# 1. Variables d'environnement
cp .env.example .env          # puis adaptez les valeurs

# 2. Services
docker compose up -d
docker compose ps             # postgres doit être "healthy"

# 3. Dépendances Python
python3 -m venv .venv && source .venv/bin/activate
pip install psycopg2-binary

# 4. Schéma de l'entrepôt
set -a && source .env && set +a
psql "postgresql://$PGUSER:$PGPASSWORD@$PGHOST:$PGPORT/$PGDATABASE" -f ddl/01_schema_etoile.sql

# 5. Chargement initial (l'historique dont vous héritez)
#    Commencez petit : deux départements suffisent pour travailler.
python3 bootstrap.py --annee 2025 --departements 59,62

# 6. L'ETL nocturne hérité, sur le flux temps réel
python3 etl_nocturne.py
```

Le premier lancement de `bootstrap.py` télécharge une archive d'environ 32 Mo
(386 Mo décompressés) et la met en cache dans `data/`. Le parcours du fichier prend
une à deux minutes, même quand vous ne chargez que deux départements : le script doit
traverser tout le XML pour les trouver.

## Vérifier que l'existant tourne

```sql
SELECT count(*) FROM entrepot.dim_station;
SELECT count(*) FROM entrepot.fait_prix;
SELECT source, count(*) FROM entrepot.fait_prix GROUP BY source;
```

## Avant de commencer la Phase 2

`etl_nocturne.py` est **l'existant à auditer, pas à rafistoler**. Lisez son en-tête :
ses six défauts y sont listés. Votre travail commence par les démontrer, requête à
l'appui, puis par les corriger dans votre propre chaîne — pas dans ce fichier.

Deux pistes pour l'audit, à vérifier vous-même :

- relancez `etl_nocturne.py` deux fois de suite et comparez `count(*)` sur `fait_prix` ;
- comparez `latitude_brute` pour une station chargée par `bootstrap.py` puis par
  `etl_nocturne.py`, et demandez-vous ce que vaut réellement ce nombre.

## Sources officielles

- Archive annuelle : https://donnees.roulez-eco.fr/opendata/annee/2025
- Flux instantané : https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/
